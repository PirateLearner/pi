// By Simon Sarris
// www.simonsarris.com
// sarris@acm.org
//
// Last update December 2011
//
// Free to use and distribute at will
// So long as you are nice to people, etc

// Constructor for Shape objects to hold data for all drawn objects.
// For now they will just be defined as rectangles.
$(document).ready(function(){
function Shape(id,x, y, w, h, fill) {
	// This is a very simple and unsafe constructor. All we're doing is checking
	// if the values exist.
	// "x || 0" just means "if there is a value for x, use that. Otherwise use
	// 0."
	// But we aren't checking anything else! We could put "Lalala" for the value
	// of x
	this.id = id || "custom";
	this.x = x || 0;
	this.y = y || 0;
	this.w = w || 1;
	this.h = h || 1;
	this.fill = fill || '#AAAAAA';
};

// Draws this shape to a given context
Shape.prototype.draw = function(ctx) {
	ctx.fillStyle = this.fill;
	ctx.fillRect(this.x, this.y, this.w, this.h);
};

// Determine if a point is inside the shape's bounds
Shape.prototype.contains = function(mx, my) {
	// All we have to do is make sure the Mouse X,Y fall in the area between
	// the shape's X and (X + Width) and its Y and (Y + Height)
	return (this.x <= mx) && (this.x + this.w >= mx) && (this.y <= my)
			&& (this.y + this.h >= my);
};


Shape.prototype.print = function(){
	console.log(this.id + "--> " + this.x + " - " + this.y + ", " + this.w + "x" + this.h );
};

function CanvasState(canvas) {
	// **** First some setup! ****

	this.canvas = canvas;
	this.width = canvas.width;
	this.height = canvas.height;
	this.ctx = canvas.getContext('2d');
	// This complicates things a little but but fixes mouse co-ordinate problems
	// when there's a border or padding. See getMouse for more detail
	var stylePaddingLeft, stylePaddingTop, styleBorderLeft, styleBorderTop;
	if (document.defaultView && document.defaultView.getComputedStyle) {
		this.stylePaddingLeft = parseInt(document.defaultView.getComputedStyle(
				canvas, null)['paddingLeft'], 10) || 0;
		this.stylePaddingTop = parseInt(document.defaultView.getComputedStyle(
				canvas, null)['paddingTop'], 10) || 0;
		this.styleBorderLeft = parseInt(document.defaultView.getComputedStyle(
				canvas, null)['borderLeftWidth'], 10) || 0;
		this.styleBorderTop = parseInt(document.defaultView.getComputedStyle(
				canvas, null)['borderTopWidth'], 10) || 0;
	}
	// Some pages have fixed-position bars (like the stumbleupon bar) at the top
	// or left of the page
	// They will mess up mouse coordinates and this fixes that
	var html = document.body.parentNode;
	this.htmlTop = html.offsetTop;
	this.htmlLeft = html.offsetLeft;

	// **** Keep track of state! ****

	this.valid = false; // when set to false, the canvas will redraw everything
	this.shapes = []; // the collection of things to be drawn
	this.dragging = false; // Keep track of when we are dragging
	// the current selected object. In the future we could turn this into an
	// array for multiple selection
	this.selection = null;
	this.dragoffx = 0; // See mousedown and mousemove events for explanation
	this.dragoffy = 0;

	// save the old position of the selected shape so that we may cancle the move if objects overlaps
	this.selection_old = null;
	
	// **** Then events! ****

	// This is an example of a closure!
	// Right here "this" means the CanvasState. But we are making events on the
	// Canvas itself,
	// and when the events are fired on the canvas the variable "this" is going
	// to mean the canvas!
	// Since we still want to use this particular CanvasState in the events we
	// have to save a reference to it.
	// This is our reference!
	var myState = this;

	// fixes a problem where double clicking causes text to get selected on the
	// canvas
	canvas.addEventListener('selectstart', function(e) {
		e.preventDefault();
		return false;
	}, false);
	// Up, down, and move are for dragging
	canvas.addEventListener('mousedown', function(e) {
		var mouse = myState.getMouse(e);
		var mx = mouse.x;
		var my = mouse.y;
		var shapes = myState.shapes;
		var l = shapes.length;
		for (var i = l - 1; i >= 0; i--) {
			if (shapes[i].contains(mx, my)) {
				var mySel = shapes[i];
				// Keep track of where in the object we clicked
				// so we can move it smoothly (see mousemove)
				myState.dragoffx = mx - mySel.x;
				myState.dragoffy = my - mySel.y;
				myState.dragging = true;
				myState.selection = mySel;
				myState.selection_old = new Shape("canvas_old",mySel.x, mySel.y, mySel.w, mySel.h,mySel.fill);
				myState.valid = false;
				return;
			}
		}
		// havent returned means we have failed to select anything.
		// If there was an object selected, we deselect it
		if (myState.selection) {
			myState.selection = null;
			myState.selection_old = null;
			myState.valid = false; // Need to clear the old selection border
		}
	}, true);
	canvas.addEventListener('mousemove', function(e) {
		if (myState.dragging) {
			var mouse = myState.getMouse(e);
			// We don't want to drag the object by its top-left corner, we want
			// to drag it
			// from where we clicked. Thats why we saved the offset and use it
			// here
			myState.selection.x = mouse.x - myState.dragoffx;
			myState.selection.y = mouse.y - myState.dragoffy;
			myState.valid = false; // Something's dragging so we must redraw
		}
	}, true);
	canvas.addEventListener('mouseup', function(e) {
		
		myState.printShapes();
		if (myState.dragging) {
			if(myState.overlaps()) {
				console.log("Warnings: Items overlaps in the Canvas !!!");
				myState.selection.x = myState.selection_old.x;
				myState.selection.y = myState.selection_old.y;
				myState.valid = false; // Something's dragging so we must redraw
			}
			else {
				
				console.log("Warnings: Items don't overlaps in the Canvas !!!");
				myState.fillData();
			}
		}
		myState.dragging = false;

	}, true);
	// double click for making new shapes
	canvas.addEventListener('dblclick', function(e) {
		var mouse = myState.getMouse(e);
		myState.addShape(new Shape("canvas_added",mouse.x - 10, mouse.y - 10, 20, 20,
				'rgba(0,255,0,.6)'));
	}, true);

	// **** Options! ****

	this.selectionColor = '#CC0000';
	this.selectionWidth = 2;
	this.interval = 30;
	setInterval(function() {
		myState.draw();
	}, myState.interval);
};

CanvasState.prototype.addShape = function(shape) {
	this.shapes.push(shape);
	this.valid = false;
};

CanvasState.prototype.clear = function() {
	this.ctx.clearRect(0, 0, this.width, this.height);
};

// While draw is called as often as the INTERVAL variable demands,
// It only ever does something if the canvas gets invalidated by our code
CanvasState.prototype.draw = function() {
	// if our state is invalid, redraw and validate!
	if (!this.valid) {
		var ctx = this.ctx;
		var shapes = this.shapes;
		this.clear();

		// ** Add stuff you want drawn in the background all the time here **

		// draw all shapes
		var l = shapes.length;
		for (var i = 0; i < l; i++) {
			var shape = shapes[i];
			// We can skip the drawing of elements that have moved off the
			// screen:
			if (shape.x > this.width || shape.y > this.height
					|| shape.x + shape.w < 0 || shape.y + shape.h < 0)
				continue;
			shapes[i].draw(ctx);
		}

		// draw selection
		// right now this is just a stroke along the edge of the selected Shape
		if (this.selection != null) {
			ctx.strokeStyle = this.selectionColor;
			ctx.lineWidth = this.selectionWidth;
			var mySel = this.selection;
			ctx.strokeRect(mySel.x, mySel.y, mySel.w, mySel.h);
		}

		// ** Add stuff you want drawn on top all the time here **

		this.valid = true;
	}
};

// Creates an object with x and y defined, set to the mouse position relative to
// the state's canvas
// If you wanna be super-correct this can be tricky, we have to worry about
// padding and borders
CanvasState.prototype.getMouse = function(e) {
	var element = this.canvas, offsetX = 0, offsetY = 0, mx, my;

	// Compute the total offset
	if (element.offsetParent !== undefined) {
		do {
			offsetX += element.offsetLeft;
			offsetY += element.offsetTop;
		} while ((element = element.offsetParent));
	}

	// Add padding and border style widths to offset
	// Also add the <html> offsets in case there's a position:fixed bar
	offsetX += this.stylePaddingLeft + this.styleBorderLeft + this.htmlLeft;
	offsetY += this.stylePaddingTop + this.styleBorderTop + this.htmlTop;

	mx = e.pageX - offsetX;
	my = e.pageY - offsetY;

	// We return a simple javascript object (a hash) with x and y defined
	return {
		x : mx,
		y : my
	};
};

// print the shapes and there coordinates
CanvasState.prototype.printShapes = function() {
	var shapes = this.shapes;
	var l = shapes.length;
	for (var i = 0; i < l; i++) {
		var shape = shapes[i];
		// We can skip the drawing of elements that have moved off the
		// screen:
		shapes[i].print();
	}

};

// check if the shapes overlaps
CanvasState.prototype.overlaps = function() {
	var shapes = this.shapes;
	var l = shapes.length;
	for(var i=0; i< l;i++) {
		for(var j=i+1;j<l;j++) {
			
			
			if((shapes[i].y >= shapes[j].y && shapes[i].y <= shapes[j].y + shapes[j].h) && 
					((shapes[i].x >= shapes[j].x && shapes[i].x <= shapes[j].x + shapes[j].w) 
							|| (shapes[j].x >= shapes[i].x && shapes[j].x <= shapes[i].x + shapes[i].w)))
			{
				return true;
			}
			else if ((shapes[j].y >= shapes[i].y && shapes[j].y <= shapes[i].y + shapes[i].h) && 
					((shapes[j].x >= shapes[i].x && shapes[j].x <= shapes[i].x + shapes[i].w) ||
							(shapes[i].x >= shapes[j].x && shapes[i].x <= shapes[j].x + shapes[j].w))) {
				return true;
			}
		}
	}
	return false;
};

CanvasState.prototype.fillData = function() {
	console.log("Filling data in the HTML")
	var tmp = this.shapes;
	var data = {'name':'Home','obj_list':tmp};

	$("#id_object_list").val(JSON.stringify(data));
	console.log($("#id_object_list").val());
};


// If you dont want to use <body onLoad='init()'>
// You could uncomment this init() reference and place the script reference
// inside the body tag
// init();

function init() {
	var s = new CanvasState(document.getElementById('canvas1'));
	console.log(s);
	s.addShape(new Shape("1",10, 10, 50, 50)); // The default is gray
	s.addShape(new Shape("2",60, 70, 40, 60, 'lightskyblue'));
	// Lets make some partially transparent
	s.addShape(new Shape("3",80, 150, 60, 30, 'rgba(127, 255, 212, .5)'));
	s.addShape(new Shape("4",150, 80, 30, 80, 'rgba(245, 222, 179, .7)'));
	s.printShapes();
	if(s.overlaps()) {
		console.log("Warnings: Items overlaps in the Canvas !!!");
	}
	else {
		console.log("Warnings: Items don't overlaps in the Canvas !!!");
//		s.sendData();
	}
		
};


// Now go make something amazing!

//This function gets cookie with a given name
function getCookie(name) {
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
var csrftoken = getCookie('csrftoken');
 
/*
The functions below will create a header with csrftoken
*/
 
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
};

function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
};


//AJAX for posting
  function create_post() {
      console.log("create post is working!") // sanity check
      console.log($('#id_object_list').val())
      	$.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

      
      $.ajax({
          url : "page_create/", // the endpoint
          type : "POST", // http method
          data : { object_list : $('#id_object_list').val() }, // data sent with the post request

          // handle a successful response
          success : function(json) {
              console.log(json); // log the returned json to the console
              console.log("success"); // another sanity check
          },

          // handle a non-successful response
          error : function(xhr,errmsg,err) {
              $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                  " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
              console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
          }
      });
  };

  $('#id-previewForm').on('submit', function(event){
	  event.preventDefault();
	  console.log("form submitted!")  // sanity check
	  create_post();
});

// add plugin function 
 $(".addPlugin button").on('click', function (event) {   
	    console.log("You clicked foo! good work");
});
/* Actually make a call to init */
 init();
});