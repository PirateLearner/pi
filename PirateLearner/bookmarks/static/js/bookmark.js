

var is_request = false;
var lastMessage = 'success';
/* Initialize global pirateLearner Object to house our everything */
var pirateLearnerGlobal = pirateLearnerGlobal || {};
pirateLearnerGlobal.bookMarks = {};
pirateLearnerGlobal.bookMarks.prevURL = '';

pirateLearnerGlobal.ckeditor = {};
pirateLearnerGlobal.ckeditor.toolbar = {
										'titles':[],
										'admin':[],
										'user':[],
									};
pirateLearnerGlobal.ckeditor.toolbar.titles = [
	                                             ["Bold", "Italic", "Underline","Subscript", "Superscript"],	                                             
	                                             ['Undo', 'Redo'],
	                                            ];
pirateLearnerGlobal.ckeditor.toolbar.admin = [
	                                             ["Bold", "Italic", "Underline", "Strike"],
	                                             ['NumberedList', 'BulletedList', "Indent", "Outdent", 'JustifyLeft', 'JustifyCenter',
	                                        'JustifyRight', 'JustifyBlock'],
	                                             ["Image", "Table", "Link", "Unlink", "Anchor", "SectionLink", "Subscript", "Superscript"], 
	                                             ['Undo', 'Redo'], ["Source"],["Maximize"],
	                                            ];
pirateLearnerGlobal.ckeditor.toolbar.user = [
	                                             ["Bold", "Italic", "Underline", "Strike"],
	                                             ['NumberedList', 'BulletedList', "Indent", "Outdent", 'JustifyLeft', 'JustifyCenter',
	                                        'JustifyRight', 'JustifyBlock'],
	                                             ["Image", "Table", "Link", "Unlink", "Anchor", "SectionLink", "Subscript", "Superscript"], 
	                                             ['Undo', 'Redo'], ["Source"],["Maximize"],
	                                            ];

var hideAllMessages = function (){

	var myMessages = ['info','warning','error','success'];
	
	$('#flash_message').addClass('hidden')
	
	 for (i=0; i<myMessages.length; i++){
		 $('#flash_' + myMessages[i]).addClass('hidden')
	 }
};

var showMessage = function (data){

	$('#flash_message').removeClass('hidden')
	$('#flash_' + data.message_type).text(data.message)
	$('#flash_' + data.message_type).removeClass('hidden')
};

var hideMessage = function (Message){

	$('#flash_message').addClass('hidden')
	$('#flash_' + Message).addClass('hidden')
};

/**
 * Select image to the left as active image and also display it.
 * If it is the first image, then roll over to the rightmost image
 */
var rollLeft = function(){
	/* Get currently active image */
	activeImage = $('img.active');
	parentElement = $('.bookmark-form');
	activeImage.removeClass('active');
	activeImage.addClass('hidden');
	console.log(activeImage);
	/* Subtract 2 for arrows */
	numImages = activeImage.parent().children('img').length;
	if(activeImage.index()==0){
		/* Select last sibling */
		activeImage = $('div.bookmark-form img:last-of-type');
	}
	else{
		activeImage = $('div.bookmark-form img:eq('+(activeImage.index()-1)+')');
	}
	activeImage.removeClass('hidden');
	activeImage.addClass('active');
	/* Update the value of image field also */
	$("#id_image_url").val(activeImage.attr('src'));
}

/**
 * Select image to the right as active image and also display it.
 * If it is the last image, then roll over to the leftmost image
 */
var rollRight = function(){
	/* Get currently active image */
	activeImage = $('img.active');
	parentElement = $('.bookmark-form');
	activeImage.removeClass('active');
	activeImage.addClass('hidden');
	console.log(activeImage);
	/* Subtract 2 for arrows */
	numImages = activeImage.parent().children('img').length;
	if(activeImage.index()==(numImages-1)){
		/* Select first sibling */
		activeImage = $('div.bookmark-form img:first-of-type');
	}
	else{
		activeImage = $('div.bookmark-form img:eq('+(activeImage.index()+1)+')');
	}
	activeImage.removeClass('hidden');
	activeImage.addClass('active');
	/* Update the value of image field also */
	$("#id_image_url").val(activeImage.attr('src'));
}

/**
 * Creates a snippet with containers for numImages images to be cycled.
 */
var createSnippet = function(numImages){
	/* Create a snippet body only if it hasn't been created yet */
	if(typeof(pirateLearnerGlobal.snippetElement) === 'undefined'){
		pirateLearnerGlobal.snippetElement = $('<div class="bookmark-form clearfix hidden" id="snippet_header"></div>');
		imageContainer= $('<div class="bookmark-form__image"></div>');
		for(i=0 ; i<numImages; i++){
			/* Create containers for each image*/
			if(i==0){
				imageContainer.append('<img class="active" id="slide_'+i+'"/>');
			}
			else{
				imageContainer.append('<img class="hidden" id="slide_'+i+'"/>');
			}
		}
		if(numImages>0){
			imageContainer.append('<div class="bookmark-form-image__slide close-cross"><span class="glyphicon glyphicon-remove"></span></div>');
		}
		if(numImages>1){
			/* Allow arrows to cycle through images and select one*/
			imageContainer.append('<div class="bookmark-form-image__slide left-arrow"><span class="glyphicon glyphicon-chevron-left"></span></div>');
			imageContainer.append('<div class="bookmark-form-image__slide right-arrow"><span class="glyphicon glyphicon-chevron-right"></span></div>');
		}
		else{
			/* We'll still have arrows, but hidden. This is to prevent unbind errors */
			imageContainer.append('<div class="bookmark-form-image__slide left-arrow hidden"><span class="glyphicon glyphicon-chevron-left"></span></div>');
			imageContainer.append('<div class="bookmark-form-image__slide right-arrow hidden"><span class="glyphicon glyphicon-chevron-right"></span></div>');			
		}
		pirateLearnerGlobal.snippetElement.append(imageContainer);
		/* Also add the title and description field */
		textContainer = $('<div class="bookmark-form__text"></div>');
		textContainer.append($('<div class="bookmark-form__title" id="snippet_title" contenteditable="true"></div>'));
		textContainer.append($('<div class="bookmark-form__description" id="snippet_description" contenteditable="true"></div>'));
		
		pirateLearnerGlobal.snippetElement.append(textContainer);
		pirateLearnerGlobal.snippetElement.insertAfter($('#div_id_folder'));
		
		/* Bind events to form elements */
		$('#snippet_title').keyup(function(event){$("#id_title").val($('#snippet_title').text());});
		$('#snippet_description').keyup(function(event){$("#id_description").val($('#snippet_description').text());});
		
		$('.left-arrow').click(rollLeft);
		$('.right-arrow').click(rollRight);
		$('.close-cross').click(function(){
			console.log('Removing Images');
			$("#id_image_url").val('');
			console.log($("#id_image_url").val());
			$(".bookmark-form__image").addClass('hidden');
		});
	}/* endof if typeof(pirateLearnerGlobal.snippetElement) */
	
	else{
		/* Just remove the previous images element and construct only them while blanking out the rest of the fields */
		$('.left-arrow').unbind("click", rollLeft);
		$('.right-arrow').unbind("click", rollRight);
		$('.close-cross').unbind("click");
		$('.bookmark-form__image').remove();
		imageContainer= $('<div class="bookmark-form__image"></div>');
		for(i=0 ; i<numImages; i++){
			/* Create containers for each image*/
			if(i==0){
				imageContainer.append('<img class="active" id="slide_'+i+'"/>');
			}
			else{
				imageContainer.append('<img class="hidden" id="slide_'+i+'"/>');
			}
		}
		if(numImages>0){
			imageContainer.append('<div class="bookmark-form-image__slide close-cross"><span class="glyphicon glyphicon-remove"></span></div>');
		}
		if(numImages>1){
			/* Allow arrows to cycle through images and select one*/
			imageContainer.append('<div class="bookmark-form-image__slide left-arrow"><span class="glyphicon glyphicon-chevron-left"></span></div>');
			imageContainer.append('<div class="bookmark-form-image__slide right-arrow"><span class="glyphicon glyphicon-chevron-right"></span></div>');
		}
		else{
			/* We'll still have arrows, but hidden. This is to prevent unbind errors */
			imageContainer.append('<div class="bookmark-form-image__slide left-arrow hidden"><span class="glyphicon glyphicon-chevron-left"></span></div>');
			imageContainer.append('<div class="bookmark-form-image__slide right-arrow hidden"><span class="glyphicon glyphicon-chevron-right"></span></div>');			
		}

		pirateLearnerGlobal.snippetElement.prepend(imageContainer);
		/* Blank other fields */
		$('.bookmark-form__title').val('');
		$('.bookmark-form__description').val('');
		$('.left-arrow').click(rollLeft);
		$('.right-arrow').click(rollRight);
		$('.close-cross').click(function(){
			console.log('Removing Images');
			$("#id_image_url").val('');
			console.log($("#id_image_url").val());
			$(".bookmark-form__image").addClass('hidden');
		});
	}	
}

/**
 * Got a successful response from the server. Now, setup this snippet into a container.
 */
var setup_snippet = function(data){
				
		if (data.message_type == 'success'){
			if(is_request)
			{
				hideMessage(lastMessage);
				hideAllMessages();
			}				
			/*
			 * Create a snippet element with number of retrieved images as input parameter
			 */
			createSnippet(data.image_list.length);
			
			var snippet_head = $("#snippet_header");
			var snippet_title = $("#snippet_title");
			var snippet_description = $("#snippet_description");
			
			snippet_title.text(data.title);
			snippet_description.text(data.description);
			
			
			for(i=0;i<data.image_list.length;i++){
				snippet_image = $('#slide_'+i);
				snippet_image.attr('src',data.image_list[i]);
			}
			
			/* Unleash the cracken. Just kidding, unhide the element now that it has been setup*/
			$("#div_id_title").addClass('hidden');
			$("#div_id_description").addClass('hidden');
			
			snippet_head.removeClass( 'hidden' );
			
			/* update the values of hidden form once */
			$("#id_title").val(data.title);
			$("#id_description").val(data.description);
			$("#id_image_url").val(data.image_list[0]);
			
			showMessage(data);
			is_request = true;
			lastMessage = data.message_type;
			
			/* Enable Inline editing */
			CKEDITOR.inline('snippet_title', {'toolbar':pirateLearnerGlobal.ckeditor.toolbar.titles});
			CKEDITOR.inline('snippet_description', {'toolbar':pirateLearnerGlobal.ckeditor.toolbar.user});
		}
		else if(data.message_type == 'danger'){
			if(is_request)
			{
				hideMessage(lastMessage);
			}
			showMessage(data);
			is_request = true;
			lastMessage = data.message_type;
			/* Also hide the snippet view and unhide the form view for manual entry */
			$("#div_id_title").removeClass('hidden');
			$("#div_id_description").removeClass('hidden');
			$("#snippet_header").addClass('hidden');
		}
		
};


 
 (function($)
{
	 
	 /**
	  * Makes an Ajax request to fetch the contents of the bookmarked page. 
	  * It first checks if there has been previous requests to the same URL field to prevent 
	  * repeated calls on focusout, and also validates URL field as a valid http(s) field.
	  */
	 function getBookmarkFromUrl(){
		 
		 
		 pirateLearnerGlobal.domElement = $("#id_url") 
		 if((pirateLearnerGlobal.domElement.val() === '') || 
				 (pirateLearnerGlobal.bookMarks.prevURL === pirateLearnerGlobal.domElement.val())){
			 /* Previous URL and this URL are the same. Or, the field is empty Nothing to do */
			 return;
		 }
		 else{
			 /* Validate the sanity of this URL once */
			 var myRegExp =/^(?:(?:https?|ftp):\/\/)(?:\S+(?::\S*)?@)?(?:(?!10(?:\.\d{1,3}){3})(?!127(?:\.\d{1,3}){3})(?!169\.254(?:\.\d{1,3}){2})(?!192\.168(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:\/[^\s]*)?$/i;
			 if (!myRegExp.test(pirateLearnerGlobal.domElement.val())){
				 console.log("Not a valid URL.");
				 return;
			 }
		 }
		 
		$.ajax({
		    // the URL for the request
		    url: window.location.origin+'/en/bookmarks/add/',
		 
		    // the data to send (will be converted to a query string)
		    data: {
		        format:'json',
		        url:pirateLearnerGlobal.domElement.val()
		    },
		 
		    // whether this is a POST or GET request
		    type: "GET",
		 
		    // the type of data we expect back
		    dataType : "json",
		 
		    // code to run if the request succeeds;
		    // the response is passed to the function
		    success: setup_snippet,
		 
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

	 
	 
	 
	 $.fn.ready(function(){	
		 $("#id_url").focusout(function(){
				 getBookmarkFromUrl();
	 });
	 });

	 $.fn.ready(function(){	
	$("#Checkall_id").change(function () {
    		$("input:checkbox").prop('checked', $(this).prop("checked"));
	  });
	 });
	 
})(window.jQuery);
