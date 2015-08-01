var pirateLearnerGlobal = pirateLearnerGlobal || {};

$(document).ready(function(){
	pirateLearnerGlobal.voting = {};
	pirateLearnerGlobal.voting.vote_id = 0;
	
	var getCookie = getCookie || function(name){
	    var cookieValue = null;
	    if (document.cookie && document.cookie != '') {
	        var cookies = document.cookie.split(';');
	        for (var i = 0; i < cookies.length; i++) {
	            var cookie = jQuery.trim(cookies[i]);
	            // Does this cookie string begin with the name we want?
	            if (cookie.substring(0, name.length + 1) == (name + '=')) {
	                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                break;
	            }
	        }
	    }
	    return cookieValue;
	};
	
	var csrfSafeMethod = csrfSafeMethod || function(method) {
	    // these HTTP methods do not require CSRF protection
	    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	};
	

	pirateLearnerGlobal.voting.csrftoken = getCookie('csrftoken');
	
	/**
	 * Update vote stats in the appropriate fields
	 */
	var updateScore = function(data){	
		/* Upvote and Downvote updates */
		$('#upvote_count').html(data['vote']['upvotes']);
		$('#downvote_count').html(data['vote']['downvotes']);
		
		/* Update user score symbols on it if he has voted */
		pirateLearnerGlobal.voting.userVote = 
				(data['uservote']['vote'] != null)? parseInt(data['uservote']['vote']): 0;

		console.log('User Vote: '+ pirateLearnerGlobal.voting.userVote);
		pirateLearnerGlobal.voting.vote_id = 
					(data['uservote']['id'] != null)? parseInt(data['uservote']['id']): 0;	
		console.log('User Vote ID: '+ pirateLearnerGlobal.voting.vote_id);
					
		if(pirateLearnerGlobal.voting.userVote===1){
			$('#upvote').children('.glyphicon-chevron-up').addClass('voted');	
		}
		else if(pirateLearnerGlobal.voting.userVote===-1){
			$('#downvote').children('.glyphicon-chevron-down').addClass('voted');	
		}
		else{
			$('#upvote').children('.glyphicon-chevron-up').removeClass('voted');
			$('#downvote').children('.glyphicon-chevron-down').removeClass('voted');
		}
	};
	
	/**
	 * Receive aggregate voting statistics
	 */
	var receiveVoteStats = function(){
		
		$.ajaxSetup({
	        beforeSend: function(xhr, settings) {
	            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	                xhr.setRequestHeader("X-CSRFToken", pirateLearnerGlobal.voting.csrftoken);
	            }
	        }
	    });
		
		$.ajax({
		    // the URL for the request
		    url: '/rest/blogcontent/'+pirateLearnerGlobal.voting.id+'/',
		 
		    // the data to send (will be converted to a query string)
		    data: {
		        format:'json'
		    },
		 
		    // whether this is a POST or GET request
		    type: "GET",
		 
		    // the type of data we expect back
		    dataType : "json",
		 
		    // code to run if the request succeeds;
		    // the response is passed to the function
		    success: updateScore,
		 
		    // code to run if the request fails; the raw request and
		    // status codes are passed to the function
		    error: function( xhr, status, errorThrown ) {
		        //alert( "Sorry, there was a problem!" );
		        console.log( "Error: " + errorThrown );
		        console.log( "Status: " + status );
		        console.dir( xhr );
		    },
		 
		    // code to run regardless of success or failure
		    complete: function( xhr, status ) {
		        //alert( "The request is complete!" );
		    }
		});
	};
	
	var confirmVote = function(data, ErrorText, thrownError){
				
		pirateLearnerGlobal.voting.vote_id = (data['id']!=undefined)?data['id']:0;
		/* It is upvote confirmation */
		if(parseInt(data['vote'])== 1){
			$('#upvote').children('.glyphicon-chevron-up').addClass('voted');
			/* Update score */
			$('#upvote_count').html(parseInt($('#upvote_count').text()) + 1);
			pirateLearnerGlobal.voting.userVote = 1;
		}
		/* or downvote confirmation */
		else if(parseInt(data['vote'])== -1){
			$('#downvote').children('.glyphicon-chevron-down').addClass('voted');
			/* Update score */
			$('#downvote_count').html(parseInt($('#downvote_count').text()) + 1);
			pirateLearnerGlobal.voting.userVote = -1;
		}
		/* or he has just undone the previous vote*/
		else{
			if(pirateLearnerGlobal.voting.userVote == 1){
				$('#upvote').children('.glyphicon-chevron-up').removeClass('voted');
				/* Update score */
				$('#upvote_count').html(parseInt($('#upvote_count').text()) - 1);
			}
			else{
				$('#downvote').children('.glyphicon-chevron-down').removeClass('voted');
				/* Update score */
				$('#downvote_count').html(parseInt($('#downvote_count').text()) - 1);				
			}
			pirateLearnerGlobal.voting.userVote = 0;
		}
	};
	
	/**
	 * Validate and send vote to server
	 */
	var validateAndSend = function(e){
		
		
		/* Check login */
		if(pirateLearnerGlobal.user['id'] == 0)
		{
			$('#loginPrompt').modal({
				backdrop: true
			})
			return;
		}
		
		//e.preventDefault();
		vote = 0;
		method = "POST";
		postUrl = window.location.origin+"/en/rest/votes/";
		
		if($(this).attr('id') == 'upvote'){
			vote = 1;
		}
		else{
			vote = -1;
		}
		/* Now, determine if we are actually voting, or undoing a vote */
		if (pirateLearnerGlobal.voting.userVote == vote){
			/* We're undoing */
			vote = -vote;
		}
		if(pirateLearnerGlobal.voting.vote_id != 0){
			postUrl = postUrl+pirateLearnerGlobal.voting.vote_id+'/';
			method="PUT";
		}
		
		//console.log('Clicked: '+ vote+'\nMethod: '+method);
		data = {
				'content_type': pirateLearnerGlobal.voting.content_type,
                'object_id':pirateLearnerGlobal.voting.id,
                'vote':vote,
				};
		
		 $.ajaxSetup({
		        beforeSend: function(xhr, settings) {
		            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
		                xhr.setRequestHeader("X-CSRFToken", pirateLearnerGlobal.voting.csrftoken);
		            }
		        }
		    });
		    //Save Form Data........
		    $.ajax({
		        cache: false,
		        url : postUrl,
		        type: method,
		        dataType : "json",
		        contentType: "application/json;",
		        data : JSON.stringify(data),
		        context : this,
		        success : confirmVote,
		        error : function (xhRequest, ErrorText, thrownError) {
		            //alert("Failed to process annotation correctly, please try again");
		        	/* Show error to user */
		        	$('#article-actions_error').removeClass('hidden');
		        	$('#article-actions_text').html(xhRequest.responseJSON['detail']);
		        }
		    });
		e.stopPropagation(); 
		return false;
	};
	
	/*
	 * Fetch the content type and ID of the post
	 */	
	pirateLearnerGlobal.voting.id = parseInt($('.rest').attr('data-id'));
	pirateLearnerGlobal.voting.content_type = parseInt($('.rest').attr('data-content-type'));
	/*
	 * Request for the vote statistics on the post via REST interface 
	 */
	receiveVoteStats();
	
	/*
	 * Bind methods to click on upvote and downvote buttons and enable the buttons
	 */
	
	$('#upvote').removeClass('text-muted').on('click', validateAndSend);
	$('#downvote').removeClass('text-muted').on('click', validateAndSend);
	
	$('#article-actions-close').on('click', function(){
		/* Hide the error class*/
		$('#article-actions_error').addClass('hidden');
	});
});