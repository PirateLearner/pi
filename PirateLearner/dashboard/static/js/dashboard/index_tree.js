 function setup_index(data){

	console.log("Success from server");
	$("#indextree").html(data);
	$('#indextree').treed({openedClass:'glyphicon-folder-open', closedClass:'glyphicon-folder-close'});
	$('#active-index').expand_active({openedClass:'glyphicon-folder-open', closedClass:'glyphicon-folder-close'});
}

	 /**
	  * Make an ajax request to server for index
	  * It first checks for data-parent value in 'index-tree' id if found send it with the 
	  * url in the form of get request.
	  */
	function getIndexForUrl(){

		var parent = $("#indextree").attr("data-parent");
		console.log(parent);
		console.log("Ajax request for index is sent to server");
		$.ajax({
		    // the URL for the request
		    url: window.location.origin+'/en/C/get-index/',
		 
		    // the data to send (will be converted to a query string)
		    data: {
		        format:'json',
		        section:parent
		    },
		 
		    // whether this is a POST or GET request
		    type: "GET",
		 
		    // the type of data we expect back
		    dataType : "html",
		 
		    // code to run if the request succeeds;
		    // the response is passed to the function
		    success: setup_index,
		 
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
	 }



$.fn.extend({
    treed: function (o) {
      
      var openedClass = 'glyphicon-minus-sign';
      var closedClass = 'glyphicon-plus-sign';
      
      if (typeof o != 'undefined'){
        if (typeof o.openedClass != 'undefined'){
        openedClass = o.openedClass;
        }
        if (typeof o.closedClass != 'undefined'){
        closedClass = o.closedClass;
        }
      };
      
	 console.log( "inside function" );
        //initialize each of the top levels
        var tree = $(this);
        tree.addClass("tree");
        tree.find('li').has("ul").each(function () {
            var branch = $(this); //li with children ul
            branch.prepend("<i class='indicator glyphicon " + closedClass + "'></i>");
            branch.addClass('branch');
            branch.on('click', function (e) {
                if (this == e.target) {
                    var icon = $(this).children('i:first');
                    icon.toggleClass(openedClass + " " + closedClass);
                    $(this).children().children().toggle();
                }
            })
            branch.children().children().toggle();
        });
        //fire event from the dynamically added icon
      tree.find('.branch .indicator').each(function(){
        $(this).on('click', function () {
            $(this).closest('li').click();
        });
      });
        //fire event to open branch if the li contains an anchor instead of text
/*        tree.find('.branch>a').each(function () {
            $(this).on('click', function (e) {
                $(this).closest('li').click();
                e.preventDefault();
            });
        });
        //fire event to open branch if the li contains a button instead of text
        tree.find('.branch>button').each(function () {
            $(this).on('click', function (e) {
                $(this).closest('li').click();
                e.preventDefault();
            });
        });
*/
    }

});

$.fn.extend({
expand_active: function (o) {

      var openedClass = 'glyphicon-minus-sign';
      var closedClass = 'glyphicon-plus-sign';
      
      if (typeof o != 'undefined'){
        if (typeof o.openedClass != 'undefined'){
        openedClass = o.openedClass;
        }
        if (typeof o.closedClass != 'undefined'){
        closedClass = o.closedClass;
        }
      };

	/* change the color to red */
	$(this).addClass("branch-active");

	/* open the chidlren if this is brach */
	if ($(this).parent("li").hasClass("branch"))
	{
		$(this).parent("li").children().children().toggle();
	}


	/* change the display of parent and it's sibling iteratively until last */
	$(this).parents("li:not(:last)").toggle();
	$(this).parents("li").siblings().toggle();

	/* Change the glyphicon to open */
	var icon = $(this).parents("li").children("i");
	icon.toggleClass(openedClass + " " + closedClass);

}

});


//Initialization of treeviews
// A $( document ).ready() block.

$( document ).ready(function() {
    console.log( "ready!" );
/*
	$('#indextree').treed({openedClass:'glyphicon-folder-open', closedClass:'glyphicon-folder-close'});
	$('#active-index').expand_active({openedClass:'glyphicon-folder-open', closedClass:'glyphicon-folder-close'});
*/
	getIndexForUrl();
});



