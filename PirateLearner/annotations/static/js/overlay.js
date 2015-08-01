/* Achieving closure, so that no variables from this script meddle with other javascript's variables, or globals */
	var pirateLearnerGlobal = pirateLearnerGlobal || {};
	pirateLearnerGlobal.overlayOpen = false;
	
(function (window) {
	
	var closeBttn;
   var triggerBttn;
/* we would want to have the overlay object persistent */
//	var overlayVar = {};
//	overlayVar.overlayObj = null;
	pirateLearnerGlobal.overlayObj = null;	
/* Ideally, it should be the same button, with toggle function  but let it be for learning */

var showLoginModal = function(){
  $("#myModal").modal('show');
};


/* This function must be separate because we would want to unbind the event listener from the escape key when we 
	roll out of overlay mode. This is because pressing the escape key would again call the close overlay, which
	merely toggles the class, and hence, it would put overlay on and off, once triggered. 
*/
var bindToEscape = function(event){
    	// Bind to both command (for Mac) and control (for Win/Linux)
    	
    	if (event.keyCode == 27) {          
    		toggleOverlay();
    	}	
    };	

/* Now, define the open overlay function */
    
var toggleOverlay = function () {
	 	
 	if(pirateLearnerGlobal.user == null || pirateLearnerGlobal.user.username === ''){
		showLoginModal();
		return; 	
 	}
 	
 	targetNode = document.getElementById('overlay-target');
 	bodyObj = document.getElementsByTagName('body');
 	
 	if(pirateLearnerGlobal.overlayOpen == false){
 		targetNode.classList.add('fullscreen-mode');
 		pirateLearnerGlobal.overlayOpen = true;
 		window.addEventListener('keydown', bindToEscape);
 		bodyObj[0].classList.add('stop-overflow');
 		this.classList.remove('pl-expand');
 		this.classList.add('pl-contract'); 		
 	}
 	
 	else{
 		targetNode.classList.remove('fullscreen-mode');
 		pirateLearnerGlobal.overlayOpen = false;
 		window.removeEventListener('keydown', bindToEscape);
 		bodyObj[0].classList.remove('stop-overflow');
 		this.classList.remove('pl-contract');
 		this.classList.add('pl-expand');
 	}
	
};


var bindEvents = function(){
		/* Bind a listener to #open-overlay button */
		triggerBttn = document.getElementById('trigger-overlay');
		//Bypassing failure checks during proof of concepts	
		triggerBttn.addEventListener( 'click', toggleOverlay );

		console.log('Open Event Registered');
	};

document.addEventListener( "DOMContentLoaded", bindEvents, false );
})(window);