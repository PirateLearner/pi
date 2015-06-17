/* Makes a Jquery Ajax call to get the current user attributes */

var pirateLearnerGlobal = pirateLearnerGlobal || {};
pirateLearnerGlobal.user = null;
	
var setupUser = function(user){
		pirateLearnerGlobal.user = user;
		//console.log(pirateLearnerGlobal.user);
	};

(function($)
{

	 function getCurrentUser(){

		 //console.log('In getCurrentUser');
		/* On load, make an ajax request to fetch comments */
		//Using the core $.ajax() method
		$.ajax({
		    // the URL for the request
		    url: '/voting/users/current/',
		 
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
		    success: setupUser,
		 
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
		 getCurrentUser();
	 });

})(window.jQuery);


//console.log('getuser.js => pirateLearnerGlobal');
//console.log(pirateLearnerGlobal);
