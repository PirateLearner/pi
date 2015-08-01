/*
 * Global Variables for this script:
 */

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
}

function toggleBoolean(boolVal){
	return (!boolVal);
}

function hasClass(element, cls) {
	
    return(element.classList.contains(cls));
}

/* Use Getter and Setters to have a pointer like functionality here */
var pirateLearnerGlobal = pirateLearnerGlobal || {};

pirateLearnerGlobal.csrftoken = getCookie('csrftoken');

var commentDiv = [];
var wrapperDiv = [];

/* Currently selected section element whose annotations will be visible and form displayed */
pirateLearnerGlobal.activeAnnotation = null;
pirateLearnerGlobal.annotationOpen = false;
pirateLearnerGlobal.deletedAnnotation = null;

(function (window){
pirateLearnerGlobal.form_element = {}; //comment form that will be tossed around in annotations

pirateLearnerGlobal.form_element = document.createElement('form');

//pirateLearnerGlobal.form_element.setAttribute('action','/annotation/annotations/');
//pirateLearnerGlobal.form_element.setAttribute('enctype','multipart/form-data');
pirateLearnerGlobal.form_element.setAttribute('class','form-annotation');
pirateLearnerGlobal.form_element.setAttribute('id','form-annotation');
pirateLearnerGlobal.form_element.innerHTML = '<fieldset>'+
    	'<input type="hidden" name="csrfmiddlewaretoken" value="'+ 
    	getCookie('csrftoken') +
    	'">'+
		'<div class="control-group "><label for="paragraph_id" class="control-label  sr-only">paragraph id:</label>'+
        '<div class="controls"><input id="paragraph_id" name="paragraph_id" type="hidden" value="0">'+       
        '</div></div>'+
    	'<div class="control-group "><label for="body" class="control-label sr-only">body:</label>'+
        '<div class="controls"><textarea class ="user-input" cols="30" id="body" name="body" rows="2" placeholder="Make a note" required></textarea>'+
        '</div></div>'+
    	'<div class="control-group sr-only"><label for="privacy" class="control-label sr-only">privacy:</label>'+
        '<div class="controls"><select id="privacy" name="privacy"><option value="0" selected>Private</option> <option value="1">Share with Author</option>'+
        '<option value="2">Share with friends</option><option value="3">Public</option>'+
		'</select></div></div>'+
    	'<div class="control-group sr-only"><label for="privacy_override_flag" class="control-label">privacy override flag:</label>'+
        '<div class="controls"><input id="privacy_override_flag" name="privacy_override_flag" type="hidden">'+
        '</div></div>'+
    	'<div class="control-group sr-only"><label for="content_object" class="control-label">Content object:</label>'+
        '<div class="controls"><input id="content_object" name="content_object" type="hidden">'+
        '</div></div>'+
    	'<div class="control-group sr-only"><label for="site" class="control-label">site:</label>'+
        '<div class="controls sr-only"><select id="site" name="site" ><option value="1">example.com - 1</option>'+
		'</select></div></div>'+
    	'<div class="form-actions"><button id="post_annotation" class="btn btn-primary" title="Make a POST request on the Annotation resource">POST</button>'+
        '</div></fieldset>';

//$("form#form-annotation").submit(postNewAnnotation);
//console.log('self.js => formAnnotation');
//console.log('Event Registered on Click');


function cleanFormData(form){
	//console.log('cleanFormData');
	getObjectById(form, 'body').value = '';	
}



/**
 * removeElementFromFlow
 * @param id : String #Identifier of the element that must be removed from the flow
 * 
 * @detail Removes the Element with ID passed in as <id> from its parent and returns it as a reusable object for future
 */
function removeElementFromFlow(id , type){
	/* Setup default values in this function */
	id = typeof(id) !== undefined ? id : 'comment-form';
	type = typeof(type) !== undefined ? type : 'id';
	/* TODO: The above assignment doesn't work in case nothing is supplied*/
	
	/* Find element with id as <id> in the DOM */
	if(type=='id'){
		var element = document.getElementById(String(id));
	}
	else if(type=='class'){
		var element_array = document.getElementsByClassName(String(id));
		var element = element_array[0];		
	}
	
	/* If found, remove it from flow */
	if(element!= null){
		/* element found. remove it */
		var parent = element.parentNode;
		parent.removeChild(element);
	}//if element!=null
	return (element);
};

/**
 * attachElementTo
 * @param element : the object to re-attach
 * @param parent : class name of the parent where it must be reattached.
 * 
 * @detail Attaches an element back into the flow as a child to the container by className passed in parent
 */
function attachElementTo(element, parent){
	/* Setup default values if applicable */
	//element = typeof(element) !== undefined ? element : null;
	parent = typeof(parent) !==undefined ? parent : 'commentable-area';
	
	/* Find parent candidate */
	var parentObject = document.getElementsByClassName(String(parent));
	/* Append element to parent if parent is found and child object is valid */
	//console.log('Outside');
	for(var i=0; i < parentObject.length; i++){
		if(parentObject[i] != null){
			parentObject[i].appendChild(element);
			//console.log('Iniside');
		}//if parentObject != null
		else{
			console.log("parent not found");
		}	
	}
	
};


/**
 * attachElementToObject
 * @param element : the object to re-attach
 * @param parent : class name of the parent where it must be reattached.
 * 
 * @detail Attaches an element back into the flow as a child to the container by className passed in parent
 */
function attachElementToObject(element, parentObject){
	/* Setup default values if applicable */
	//element = typeof(element) !== undefined ? element : null;
	//parent = typeof(parent) !==undefined ? parent : 'commentable-area';

	/* Append element to parent if parent is found and child object is valid */
	parentObject.appendChild(element);	
};

/**
 * moveCommentsToParagraph
 * 
 * @detail Moves all the comments as the next elements to their dependent paragraph
 */
function moveCommentsToParagraph(){
	/* 
	 * create a div element for each paragraph and collect all the comments for that paragraph in that div
	 * Then insert this div below the respective paragraph
	 * default its visibility to none and add a '+' sign which enables the visibility of the respective div  
	 */
	
	/* First fetch all comments and remove them from flow */
	elementBlock = removeElementFromFlow('comments', 'id');
	
	/* initialize an empty array that will hold all the divs with paragraph IDs as keys */
	/*
	 * Example: arr[[comment1, comment2],[],[comment3]]
	 */
	var arr = {};
	var para_id = 0;
	/* recurse each child in it and surround that with a div */
	if(elementBlock.hasChildNodes()){
		var children = elementBlock.childNodes;
		
		for(var i=0; i< children.length; i++){
			/* access the comments object-id to find the paragraph ID */
			/* TODO: All of this must be done inside a document fragment createDocumentFragment to minimize number of reflows */
			if(children[i].nodeName != "DT" && children[i].nodeName != "DD"){
				continue;
			}
			if(children[i].nodeName== "DT"){
				para_id = parseInt(children[i].getAttribute('data-object-id'));
				/* also find its corresponding DD and set i to that value */
				for(var j= i; j<children.length; j++){
					if(children[j].nodeName !="DD"){
						continue;
					}
					i=j;
					break;
				}
			}
			/* para_id row has a comment div */
			if(arr[para_id] == null){
				/* create a div */
				var div= document.createElement('div');
				arr[para_id] = div;
			}
			/* insert the comment's content into the div and div at para_id value in array */
			var innerDiv = document.createElement('div');
			innerDiv.innerHTML = children[i].innerHTML;
			arr[para_id].appendChild(innerDiv);				
		}
	}
	/* Test: Try attach to sample element */
	/* 
	for (var div in arr){
		attachElementTo(arr[div],'commentable-area');
	}
	//Works!*/
	//console.log(arr);
	/* Now, remove the commentable area and insert the divs below their respective <p> */
	contentBlock= removeElementFromFlow('commentable-area', 'id');
	
	para_list = contentBlock.getElementsByTagName('p');
	for(var i=0; i<para_list.length;i++){
		var para = para_list[i].getAttribute('id');
		if( para != null && arr[parseInt(para)] != null){
			para_list[i].innerHTML += '<a href="#" onclick="showForm(this);" id="'+para+'" class="">+</a>';
			para_list[i].appendChild(arr[parseInt(para)]);			
		}
	}
	
	var container = document.getElementsByClassName('content');
	var firstChild = container[0].getElementsByTagName('h1'); 
	//console.log(firstChild);
	
	firstChild[0].parentNode.insertBefore(contentBlock, firstChild.nextSibling);
	attachElementTo(contentBlock, 'content');
	/*
	 * Later, this function should dynamically attach the form inside each div when it is displayed and 
	 * automatically set the value of its paragraph in the field.
	 * P.S.: Use attachElementTo function
	 */
};

/**
 * wrapElement must wrap the taget element object with the desired element, but must not remove 
 * it from flow and reattach or else its positioning will be lost.
 * 
 * @param targetElement : The object that must be wrapped
 * @param wrapperElement : The string 'name' of the tag with which it must be surrounded
 */
function wrapElement(targetElement, wrapperElement){
	/* Parent Node from where the node was taken */
	parentNode = targetElement.parentNode;
	/* Sibling just before it, so that we know where to insert */
	prevSibling = targetElement.previousSibling;
	parentNode.removeChild(targetElement);
	
	/* Create the div */
	newElement = document.createElement(String(wrapperElement));
	/* Put the element into the newly created wrapper*/
	newElement.appendChild(targetElement);
	/* Insert the new element back in the original place*/
	parentNode.insertBefore(newElement, prevSibling.nextSibling);
};


/**
 * transformIntoCommentable
 * 
 * @brief Transforms the elements of tag name <tagName> eg. <p> inside the element
 * 		with ID parentID into commentable area. It essentially adds a few classes to all children  
 * @param tagName
 * @param parentID
 */
function transfromIntoCommentable(tagName, parentID){
	/* Sanity Checks */
	parentID = typeof(parentID)!== undefined ? parentID : 'commentable-area';
	tagName = typeof(tagName)!== undefined ? tagName: 'p';
	//console.log('In transformer');
	/* First, get the parent element */
	//console.log(parentID);
	parent = document.getElementById(String(parentID));
	//console.log(parent);
	/* Get all children by this tagname in the parent */
	children = parent.getElementsByTagName(String(tagName));
	/* Now, assign a section-id to each para with an ID and a class name too */
	for(var i=0; i< children.length; i++){
		
		/* All elements should default to clear from floats*/
		//children[i].setAttribute('style','clear: both; ');
		
		if(children[i].hasAttribute('id')){
			var id = children[i].getAttribute('id');
			//console.log(id);
			children[i].setAttribute('data-section-id', id);
			//Directly setting the class would delete previous classes. It must be non-invasive.
			//children[i].className += 'commentable-section';
			
			/* Wrap it into a div */
			/* Let us not wrap it around */
			/*/*wrapElement(children[i], 'div');*/
			/* Now, the parent must have changed, so can we directly add class or ID? */
			/*children[i].parentNode.className = 'commentable-section';*/
			children[i].className += ' commentable-section';
			/*children[i].parentNode.setAttribute('comment-section-id',id);*/
			children[i].setAttribute('comment-section-id',id);
			//children[i].setAttribute('style',"float:left;width:80%;");
			/* We're done! */
			
			/* Okay, new revision: Add a div to the end of <p> element using appendchild */
			commentWrapper = document.createElement('div');
			commentWrapper.className = "side-comment";
			commentWrapper.innerHTML = '<a href="#" class="marker"><span class="comment-count">0</span></a>'+
						'<div class="comments-wrapper"><div class="comments"> </div>'+
						'<a href="#" class="add-comment">Leave a comment</a>'+
						/*
						'<div class="comment-form"><div class="author-avatar"><img src="public/images/user.png"></div>'+
						'<p class="author-name">You</p>'+
						'<input type="text" class="comment-box right-of-avatar" placeholder="Leave a comment...">'+
						'<div class="actions right-of-avatar"><a href="#" class="action-link post">Post</a>'+
			            '<a href="#" class="action-link cancel">Cancel</a></div></div>'+
			            */
			            '</div>';
			children[i].appendChild(commentWrapper);
		}
	}
	//console.log('After transform');
	//console.log(parent);
};

/*
 * ORIGINAL function, for tutorial basis
 * 
 * function transfromIntoCommentable(tagName, parentID){
	// Sanity Checks
	parentID = typeof(parentID)!== undefined ? parentID : 'commentable-area';
	tagName = typeof(tagName)!== undefined ? tagName: 'p';
	
	// First, get the parent element 
	console.log(parentID);
	parent = document.getElementById(String(parentID));
	console.log(parent);
	// Get all children by this tagname in the parent 
	children = parent.getElementsByTagName(String(tagName));
	// Now, assign a section-id to each para with an ID and a class name too 
	for(var i=0; i< children.length; i++){
		if(children[i].hasAttribute('id')){
			var id = children[i].getAttribute('id');
			console.log(id);
			children[i].setAttribute('data-section-id', id);
			//Directly setting the class would delete previous classes. It must be non-invasive.
			children[i].className += 'commentable-section';
		}
	}
};
 */

function getObjectById(parentObject, idName){
	//console.log('getObjectById');
	for(var i=0;i<parentObject.childNodes.length; i++){
		if(typeof parentObject.childNodes[i].getAttribute != 'function' ){
			
			return(null);
		}
		//console.log(parentObject.childNodes[i]);
		
		//console.log(parentObject.childNodes[i].getAttribute('id'));
		
		if(parentObject.childNodes[i].childNodes.length != 0){
			element = getObjectById(parentObject.childNodes[i], idName);
			if(element != null){
				//console.log(element);
				return(element);
			}			
		}		
		
		if(parentObject.childNodes[i].getAttribute('id') == idName){
			return(parentObject.childNodes[i]);
		}
	}
};

function displayForm(){
	showForm(this);
};

function hideForm(){	
	cleanFormData(pirateLearnerGlobal.form_element);
	pirateLearnerGlobal.form_element.classList.add('hidden');
};

function showForm(object){
	
	//console.log('showForm');
	var para_id= object.parentNode.parentNode.parentNode.getAttribute('data-section-id');
	var parent = object.parentNode.parentNode;
	//console.log(typeof(pirateLearnerGlobal.form_element));
	
	
	var el = getObjectById(pirateLearnerGlobal.form_element, 'paragraph_id');
	
	el.value=String(para_id);
	//console.log(el);
	
	var cObj = getObjectById(pirateLearnerGlobal.form_element, 'content_object');
	cObj.value='http://piratelocal.com/en/rest/blogcontent/'+ pirateLearnerGlobal.pk +'/';
	/* Revision 1: Now we want to attach the form to the element itself, not the parent */
	/* attachElementToObject(pirateLearnerGlobal.form_element, parent); */
	//attachElementToObject(pirateLearnerGlobal.form_element, parent);
	attachElementToObject(pirateLearnerGlobal.form_element, parent.getElementsByClassName('comments-wrapper')[0]);
	pirateLearnerGlobal.form_element.classList.remove('hidden');
	/*Bind to post submit event */
	var postBtn = getObjectById(pirateLearnerGlobal.form_element, 'post_annotation');
	
	$("form#form-annotation").unbind();
	if(pirateLearnerGlobal.user == null || pirateLearnerGlobal.user.username === ''){
		/* Needs to login */
		postBtn.innerHTML="Login";
		postBtn.setAttribute('onClick',"document.location.href = ('http://piratelocal.com/');");
	}
	//console.log('postBtn');
	//console.log(postBtn);
	//postBtn.addEventListener('click', postNewAnnotation);
	else{
		/* Is logged in */
		pirateLearnerGlobal.form_element.getElementsByClassName('user-input')[0].classList.remove('has-error');
	
		$("form#form-annotation").submit(postNewAnnotation);
	}
};

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
};

function postNewAnnotation(e){
//	console.log('PostAnnotation');
//	console.log($("form.form-annotation").serialize());
//	alert("Post submitted"+$("form.form-annotation").serialize());
	
	e.preventDefault();
	
	var data = {}
    var Form = $("form.form-annotation");
		
	

    //Gathering the Data
    //and removing undefined keys(buttons)
    $.each(this.elements, function(i, v){
            var input = $(v);
        data[input.attr("name")] = input.val();
        delete data["undefined"];
    });
    
    delete data["csrfmiddlewaretoken"];
    
    if(data["body"]===''){
    	this.getElementsByClassName('user-input')[0].classList.add('has-error');
    	return;
    }
    //console.log(JSON.stringify(data));

    //Form Validation goes here....

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", pirateLearnerGlobal.csrftoken);
            }
        }
    });
    //Save Form Data........
    $.ajax({
        cache: false,
        url : "http://piratelocal.com/en/rest/annotations/",
        type: "POST",
        dataType : "json",
        contentType: "application/json;",
        data : JSON.stringify(data),
        context : Form,
        success : renderResponse,
        error : function (xhRequest, ErrorText, thrownError) {
            //alert("Failed to process annotation correctly, please try again");
            console.log('xhRequest: ' + xhRequest + "\n");
            console.log('ErrorText: ' + ErrorText + "\n");
            console.log('thrownError: ' + thrownError + "\n");
        }
    });	
};

function renderResponse(callback){
	//console.log(callback);
   // console.log(JSON.parse(callback));
    //alert("Annotation Response received!");
    //console.log(callback.childNodes.length);
    /* A direct call to renderComments is not working. Apparently because all these entries need to be put in a dictionary */
    comment = [];
    comment[0] = callback;
    renderComments(comment);
    bindUnbindForm(pirateLearnerGlobal.activeAnnotation,false);
    hideForm();
    
    /* Rebind the form */
    bindUnbindForm(pirateLearnerGlobal.activeAnnotation,true);
}


function deleteComment(){
	id = this.getAttribute('id');
	
	/* Set the class of its master parent which needs to be deleted */
	this.parentNode.classList.add("deleted-comment");
	this.parentNode.classList.add("hidden");
	
	pirateLearnerGlobal.deletedAnnotation = this.parentNode ; 
	
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", pirateLearnerGlobal.csrftoken);
            }
        }
    });
    //Save Form Data........
    $.ajax({
        cache: false,
        url : "http://piratelocal.com/en/rest/annotations/"+id+"/",
        type: 'delete',        
        //data : {"_method":"DELETE"},
        success : removeComment,
        error : function (xhRequest, ErrorText, thrownError) {
            //alert("Failed to process annotation correctly, please try again");
            console.log('xhRequest: ' + xhRequest + "\n");
            console.log('ErrorText: ' + ErrorText + "\n");
            console.log('thrownError: ' + thrownError + "\n");
        }
    });
    this.removeEventListener('click', deleteComment);
	
};

function createComment(jsonComment, body){
	body.className = 'annotation';
	body.setAttribute('data-section-id',jsonComment.paragraph_id);
	body.innerHTML = '<div class="author-avatar">'+
					'<img src="/static/static/images/anonymous-user-gravatar.png">'+
					'</div>';
	body.innerHTML += '<a class="author-name right-of-avatar" href="#">'+
					 jsonComment.user + 
					 '</a>';
	body.innerHTML += '<p class="comment right-of-avatar">'+ jsonComment.body+"</p>";
	/* <form class="button-form" action="/en/annotation/annotations/11/" method="POST">
                <input type="hidden" name="csrfmiddlewaretoken" value="G7CSpyg1YnFw4795pYnOHdmRjCZMNWNu">
                <input type="hidden" name="_method" value="DELETE">
                <button class="btn btn-danger js-tooltip" data-original-title="Make a DELETE request on the Annotation resource">DELETE</button>
            </form>*/
	if(pirateLearnerGlobal.user != null || pirateLearnerGlobal.user.username !== ''){
		/* If the user is the author of this comment, then allow deletion. Else, fuck off! */
		if(pirateLearnerGlobal.user.username === jsonComment.user){
			body.innerHTML += '<a href="#" class="action-link delete" id="'+jsonComment.id+'">Delete</a>';
			body.getElementsByClassName('delete')[0].addEventListener('click',deleteComment);
			/* Bind the showform method to this particular instance */
			$('.delete').click(function(e) {
				e.preventDefault();
			});
		}
	}
};


function removeComment(data){
	/* Fuck! */
	parent = pirateLearnerGlobal.deletedAnnotation.parentNode;
	
	/* Find the deleted comment and remove it: from ul */
	parent.removeChild(parent.getElementsByClassName('deleted-comment')[0]);
	/* Update the comment count on its overall parent */
	absoluteParent = parent.parentNode.parentNode.parentNode;
	//console.log(absoluteParent);
	commentCount = parseInt(absoluteParent.getElementsByClassName('comment-count')[0].innerHTML) - 1;
	//console.log("New comment count \n"+ commentCount);
	if(commentCount == 0){
		absoluteParent.classList.remove('has-comments');
	}
	absoluteParent.getElementsByClassName('comment-count')[0].innerHTML = commentCount;	
}

function renderComments(comments){
	//console.log(comments);

	/* Parse the comments into HTML Elements */
	if(comments.length > 0){
		/* There are more than one comments */				
		/* First create the body of each comment as another div */
		for(var i=0; i< comments.length; i++){
			/* Update: Each child element should be a li and parent a ul */
			//commentDiv[i] = document.createElement('div');
			commentDiv[i] = document.createElement('li');
			createComment(comments[i], commentDiv[i]);
			
			/* Find a previous top-level div, sorted by the paragraph ID */
			var paraID = comments[i].paragraph_id;
			if(wrapperDiv[paraID] == null){
				/* Existing parent div not found, create one */
				//wrapperDiv[paraID] = document.createElement('div');
				//wrapperDiv[paraID].className = 'section-comment-wrapper comments-wrapper';
				wrapperDiv[paraID] = document.createElement('ul');
				wrapperDiv[paraID].className = 'comments';
			}
			/* If found, insert into the div */
			/* Append the comment div into this div */
			wrapperDiv[paraID].appendChild(commentDiv[i]);

		}
			
		/* Get the commentable-area from the document */
		parent = document.getElementById('commentable-area');
		
		
		//NOTE: TEST Code only. Surround All wrappers by a master wrapper and append it once to document
		/*
		testDiv = document.createElement('div');
		
		for(var i=0;i <wrapperDiv.length; i++){

			if(wrapperDiv[i] != null){
				testDiv.appendChild(wrapperDiv[i]);
			}
		}
		console.log(testDiv);
		parent.appendChild(testDiv);
		*/
		
		/* For each commentable-section, if there is a comment div with the same ID, 
		 * insert it as child to that div floating to right */
		for(var i=0; i< wrapperDiv.length; i++){
			if(wrapperDiv[i] != null){
				
				/* There must be a corresponding div created to append comments */
				searchStr = "[comment-section-id='"+ i +"']";
				//console.log(searchStr);
				elementList = document.querySelectorAll(searchStr);
				
				//console.log(elementList);
				/* Prepare the div for insertion */
				//wrapperDiv[i].setAttribute('style','float:right;width:15%');
				/* There is guaranteed to be only one kind of this kind */
				//elementList[0].appendChild(wrapperDiv[i]);
				
				/* Okay, now we need to look inside and insert inside */
				(elementList[0].getElementsByClassName('comments'))[0].appendChild(wrapperDiv[i]);
				
				/* New. Also update the comment count on the span if it is non-zero */
				if(wrapperDiv[i].childNodes.length !== 0){
					//console.log('Adding count to wrapper div');
					//console.log(wrapperDiv[i].childNodes.length);
					//console.log(wrapperDiv[i].childNodes);
					
					spanElement = elementList[0].getElementsByClassName('comment-count')[0];
					spanElement.innerHTML = wrapperDiv[i].childNodes.length; 
					
					/* Also add has-comments class to the parent */
					elementList[0].getElementsByClassName('side-comment')[0].classList.add('has-comments');
				}
			}
		}
	}
};



var el = document.getElementById('paragraph_id');
//console.log('form elements');
//console.log(el);
//console.log(pirateLearnerGlobal.form_element.getElementById('paragraph_id'));
/*
pirateLearnerGlobal.form_element = removeElementFromFlow("comment-form", 'id');
*/
//console.log('self.js => pirateLearnerGlobal');
//console.log(pirateLearnerGlobal);

function bindUnbindForm(formObject, bind){
	//console.log('in bindUnbindForm');
	if(bind){
		if(hasClass(formObject.getElementsByClassName('side-comment')[0], 'has-comments')){
			//console.log('Has comments');
			formObject.getElementsByClassName('add-comment')[0].addEventListener('click', displayForm);
		}
		else{
			/* Display form immediately rather than binding*/
			showForm(formObject.getElementsByClassName('add-comment')[0]);			
		}
	}
	else{
		formObject.getElementsByClassName('add-comment')[0].removeEventListener('click', displayForm);
	}
}
var commentsVisible = function(){
	toggleComments(this);
}

var toggleComments = function(object){
	
	/* Find and save the element we are going to work on */
	/* If it the first time that user has clicked to show the comments and form then 
	 * we have no work to do.
	 * 
	 * Else we need to switch off the previously active annotation block
	 */
	//console.log('In toggleComments');
	
	//console.log(object);
	parent = document.getElementById('commentable-container');
	container = object.parentNode.parentNode;
	
		
	/* If we are clicking for the first time, then globalActiveElement would be null, so we must assign this element to the global */
	/* And we must make its comment window roll out and previous comments visible */
	if(pirateLearnerGlobal.activeAnnotation == null){
		//console.log('1 => NULL');
		/* Roll out the comments window */
		parent.classList.add('side-comments-open');
		/* Save state */
		pirateLearnerGlobal.annotationOpen = true;
		/* Toggle the class of this element	*/
		container.getElementsByClassName('side-comment')[0].classList.add('active');
		
		/* Clear out the form Data */
		cleanFormData(pirateLearnerGlobal.form_element);
		
		/* Bind Show Form event */
		//container.getElementsByClassName('add-comment')[0].addEventListener('click', showForm);
		bindUnbindForm(container, true);
		
		/* update GlobalElement */
		pirateLearnerGlobal.activeAnnotation = container;
	}
	
	/* If globalElement and current element are the same, then it means that we're trying to close the comments window or reopening it */
	/* Thus, toggle our active status */
	/* close the window - side-comments-open */
	/* We don't update the global element because it is possible that the user put something in the comment form but did not post it. Maybe he changes his mind later */
	else if(pirateLearnerGlobal.activeAnnotation.getAttribute('id') === container.getAttribute('id')){
		//console.log('2 => SAME TOGGLE');
		/* Toggle the visibility of this container's comments */
		container.getElementsByClassName('side-comment')[0].classList.toggle('active');
		/* Roll down the comments window */
		parent.classList.toggle('side-comments-open');
		/* Save the state in global */
		pirateLearnerGlobal.annotationOpen = toggleBoolean(pirateLearnerGlobal.annotationOpen);

		/* Update the global Element too */
		pirateLearnerGlobal.activeAnnotation = container;
		
		/* The new state if closed, then the Submit event should be unbound */
		if(!pirateLearnerGlobal.annotationOpen){
			/* Unbind from the previous instance */
			bindUnbindForm(pirateLearnerGlobal.activeAnnotation,false);
			//pirateLearnerGlobal.activeAnnotation.getElementsByClassName('add-comment')[0].removeEventListener('click', showForm);
			/* Also hide the form */
			hideForm();
		}
		else{
			/* Bind Show Form event */
			//container.getElementsByClassName('add-comment')[0].addEventListener('click', showForm);
			bindUnbindForm(container, true);
		}
	}
	
	/* If globaElement and current element are different, then it means that we're trying to comment on, or view comments on a different para */
	/* Check state of window - open or close */
	/* if already open - don't toggle the window */
	/* toggle the active of the older element */
	/* else toggle the window. Old was already not active */
	/* Make the new element Globally active*/
	else{
		//console.log('3 => Different');
		/* If window was rolled out, then previous comments should be hidden and new ones displayed */
		//console.log('GlobalAnnotation');
		//console.log(pirateLearnerGlobal.activeAnnotation.getElementsByClassName('side-comment')[0]);
		if(pirateLearnerGlobal.annotationOpen == true){
			/* Toggle the visibility of old active element's comments */
			//console.log('Toggling Annotation');
			pirateLearnerGlobal.activeAnnotation.getElementsByClassName('side-comment')[0].classList.remove('active');
			
			/* Unbind from the previous instance */
			//pirateLearnerGlobal.activeAnnotation.getElementsByClassName('add-comment')[0].removeEventListener('click', showForm);
			bindUnbindForm(pirateLearnerGlobal.activeAnnotation, false);
			/* Also hide the form */
			hideForm();
		}
		/* Else, roll out the window now and then display the comments of newly active window*/
		else{
			parent.classList.add('side-comments-open');
			pirateLearnerGlobal.annotationOpen = true;
		}
		/* Make the elements of the new Global Active */
		container.getElementsByClassName('side-comment')[0].classList.add('active');
		
		/* Clear out form data */
		cleanFormData(pirateLearnerGlobal.form_element);
		
		/* Bind Show Form event */
		//container.getElementsByClassName('add-comment')[0].addEventListener('click', showForm);
		bindUnbindForm(container,true);
		
		/* Update the Global Element */
		pirateLearnerGlobal.activeAnnotation = container;
	}
	/* Bind the showform method to this particular instance */
	$('.add-comment').click(function(e) {
	    e.preventDefault();
	});
	
	//container.getElementsByClassName('add-comment')[0].addEventListener('click', showForm);
	//showForm(this);
	/* Also bind html to allow closing the comments by clicking anywhere */
	if(pirateLearnerGlobal.annotationOpen == true){
		//console.log('binding to html');
		$(document).on('click', function(event) {
			//console.log('Trigger');
			//console.log($(event.target));
			//console.log($(event.target).closest('.side-comment').length);
			if (!($(event.target).closest('.side-comment').length)){
				toggleComments($('.side-comment.active').find('a.marker')[0]);
			}
		});
	}
	else{
		//console.log('unbinding from html');
		$(document).unbind();
	}
};

(function($)
{

	 function getAnnotations(){

		//console.log('In getAnnotation');
		/* On load, make an ajax request to fetch comments */
		//Using the core $.ajax() method
		$.ajax({
		    // the URL for the request
		    url: pirateLearnerGlobal.contentResource +'/comments/',
		 
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
		    success: renderComments,
		 
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
		//moveCommentsToParagraph();
		 transfromIntoCommentable('p', 'commentable-container');
		 
		 /*Lets see if we can bind a listener to the first side-comment instance */
		 var sectionComments = document.getElementsByClassName('marker');
		// console.log('sectionComments');
		// console.log(sectionComments);
		 for(var i=0; i< sectionComments.length;i++){
			 sectionComments[i].addEventListener('click', commentsVisible);
		 }
		 $('.marker').click(function(e) {
			    e.preventDefault();
			});
		 
		 getAnnotations();
	 });
	
})(window.jQuery);



})(window);
