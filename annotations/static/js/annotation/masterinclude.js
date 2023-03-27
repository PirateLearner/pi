//Define Regex Ruleset Strings
/**
 * Okay. Lets try to make it more useful.
 * The problems that we're trying to solve here are:
 * 1. To present a single master include JS file that can intelligently load other JS as required per page.
 *  	This means, that there is a RuleSet maintained which compares the URL Patterns are accordingly, serves Scripts. 
 *  	For example, http://piratelocal.com/en/C/section-1/somebodys-poem/1/ has three parts we are interested in right now:
 *  		a. Language: en
 *  		b. App URL Name: Now that's tricky, since URLs don't necessarily correspond to URLs, so we'll keep a mapping for that
 *  				Appname: C -> blogcontent
 *  		c. Primary Key of content: 1
 *  The The App Name is required because for Generic Content Types to work, we'll need it. Also, if the REST API Resource is different than the appname
 *  for example, Appname is blogcontent, but API URL is blog, then we'll need a mapping to that too, since we need to automate calls to the API
 *  
 *  [[URL Patterns][Lookup Table Name]]
 *  [Lookup Table Name]-->
 *  	[Appname] [Scripts] [Content Type] [REST API Resource URL Suffix]
 *  
 *  Let's take the example of the current problem we're tackling. 
 *  App Name: blogcontent
 *  App URL Name: C
 *  Content Type: BlogContent
 *  REST API suffix: /annotation/blogcontent/
 *  To get Annotations per instance: /annotation/blogcontent/<pk>/comments/
 *  But, to post them: /annotation/annotations/
 *  
 *    This could be changed though, to let each app define its own saving mechanism but 
 *    there isn't much gain, since in any case, both will be filling the content_type URL field values
 *    which have to be present on the client.
 *  
 *  Thus, at the time of page loading, we will need the following values handy if annotations are to be used:
 *  content_type: URL to the main resource i.e.  /annotation/blogcontent/<pk>
 *  
 */
/* 
	Revision: POST creation of basic annotations, overlay and stuff. 
	Let us put every variable in a global object for PirateLearner to avoid any conflicts
*/
var pirateLearnerGlobal = {};
(function(window){

pirateLearnerGlobal.annotationIncludes = [/* JavaScripts */[/*'js/annotation/self.js', 'js/getuser.js'*/],
                          						/* CSS */['css/annotation/styles.css'],
						 							];
//Field Value Lookup Ruleset
pirateLearnerGlobal.scriptRuleSet = [['C', pirateLearnerGlobal.annotationIncludes,'BlogContent','/rest/blogcontent/'],
                   						 ['D', '', 'Testing', '']
                   						];//The last one is just for testing

//URL Top Pattern Ruleset
pirateLearnerGlobal.ruleSet = [
										[/^.+\.com\/(\w+)\/(\w*)\/.+\/([0-9]+)\/?/, pirateLearnerGlobal.scriptRuleSet]
               					];
//Convert them into Regex Expressions one time
pirateLearnerGlobal.regRules = [];
for(var i=0; i < pirateLearnerGlobal.ruleSet.length; i++){
	pirateLearnerGlobal.regRules[i] = new RegExp(pirateLearnerGlobal.ruleSet[i][0]);
	//console.log('Compiled RuleSet');
	//console.log(pirateLearnerGlobal.regRules[i]);
}
/* Healthy defaults */
pirateLearnerGlobal.language = 'en';
pirateLearnerGlobal.app = 'C';
pirateLearnerGlobal.pk = 0;
pirateLearnerGlobal.contentType = 'BlogContent';
pirateLearnerGlobal.contentResource = 'rest/blogcontent/'


pirateLearnerGlobal.user = null;
	
function createElements(sources){
	var elements = [];
	var numElements = 0;
	/* First Scripts */
	for(var i=0; i< sources[0].length; i++){
		elements[numElements] = document.createElement("script");
		elements[numElements].type = "text/javascript";			
		elements[numElements].src = '/static/static/'+ sources[0][i];
		numElements++;
	}
	/* Then CSS */
	for(var i=0; i< sources[1].length; i++){
	    elements[numElements] = document.createElement("link");
		elements[numElements].rel = "stylesheet";			
		elements[numElements].href = '/static/static/'+ sources[1][i];
		numElements++;
	}
	//console.log(elements);
	return elements;
};
	
/**
 * urlRouter 
 * @param url
 * @brief Checks on a Regex match and deciphers the Javascript that must be 
 * 			included.
 * @returns {String}
 */
function urlRouter(url){
	
	var elements = [];

	var src = '';
	for(var i=0; i< pirateLearnerGlobal.regRules.length; i++){
		/* Iteratively match up the overall URL Pattern with the top level ruleset */
		var match = url.match(pirateLearnerGlobal.regRules[i]);
		if(match !== null){
			/* Match was found. Now, find a more granular ruleSet to find what script to include for the captured values */
			
			pirateLearnerGlobal.language = match[1];
			pirateLearnerGlobal.app = match[2];
			pirateLearnerGlobal.pk = parseInt(match[3]);
			
			var diag_str = pirateLearnerGlobal.language + pirateLearnerGlobal.app + pirateLearnerGlobal.pk;
			//console.log(diag_str);
			
			for(var j=0; j< pirateLearnerGlobal.scriptRuleSet.length; j++){
				if(pirateLearnerGlobal.scriptRuleSet[j][0] === pirateLearnerGlobal.app){
					/* We've found an app URL Match */
					//console.log(pirateLearnerGlobal.scriptRuleSet[j]);
					/* Create html elements for each of the rule scripts and CSS */
					contentType = pirateLearnerGlobal.scriptRuleSet[j][2];
					elements = createElements(pirateLearnerGlobal.scriptRuleSet[j][1]);
					
					pirateLearnerGlobal.contentResource = pirateLearnerGlobal.scriptRuleSet[j][3] + pirateLearnerGlobal.pk;
					//console.log(pirateLearnerGlobal.contentResource);
					break;
				}
			}			
			break;
		}
		else{
			//var stri = 'Tried matching ' + url + 'against ' regRules[i];
			var stri = url + ' ' + pirateLearnerGlobal.regRules[i];
			//console.log(stri);
			//console.log('No match found');
		}
	}
	return elements;
};

pirateLearnerGlobal.head = document.getElementsByTagName('head')[0];

pirateLearnerGlobal.elements = urlRouter(document.URL);

//Finally, include the JS
for(var i=0; i< pirateLearnerGlobal.elements.length; i++){
	pirateLearnerGlobal.head.appendChild(pirateLearnerGlobal.elements[i]);
}

//console.log('masterinclude.js => pirateLearnerGlobal');
//console.log(pirateLearnerGlobal);
})(window);
