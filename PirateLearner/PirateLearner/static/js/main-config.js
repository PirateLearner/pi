$(document).ready(function(){

$(".js-click").click(function(e){
//extract data-url and then go to url
var ele = $(e.target);
var final_element;
if (ele.data("url") === undefined)
{	
	console.log("Did not found the url serach for parent");
	final_element = ele.closest(".js-click")
	console.log(final_element);
}
else {
	final_element = ele;
}
console.log("Hey "+ final_element.data("url"));
window.location.href = final_element.data("url");
return false;
});  

$('.carousel').slick({
    dots: true,
    infinite: true,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 5000,
    fade: true,
    speed: 500,
    cssEase: 'linear',
  });

$(function() {
  $('a[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
      if (target.length) {
		console.log(target.offset().top);
        $('html, body').animate({
          scrollTop: target.offset().top
        }, 1000);
        return false;
      }
    }
  });
});

});
