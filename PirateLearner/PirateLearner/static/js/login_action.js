var pirateLearnerGlobal = pirateLearnerGlobal || {};
pirateLearnerGlobal.user = pirateLearnerGlobal.user || null;

$(document).ready(function(){
	/**
	 * Binds the Login Class to Modal Event to pop up the Login Overlay if the user is not logged in.
	 * Stops the default action from happening.
	 */
	showLogin = function(){
		$('#loginPrompt').modal({
			backdrop: true
		})
	};
	/* Bind to all places */
	$('.login-button').on('click', showLogin);
});