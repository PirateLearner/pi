/* Toggle between adding and removing the "is-collapsed" class when the user clicks on one of the "Section" buttons.
 The "is-collapsed" class is used to open the specific accordion panel */

 $( document ).ready(function() {
     console.log( "ready!" );
     var acc = document.getElementsByClassName("faq-section__list");
     var i;

     for (i = 0; i < acc.length; i++) {
         acc[i].onclick = function(){
           /*  this.classList.toggle("active"); */

           console.log("Clicked ", $(this));
           $(this).toggleClass("is-expanded");
           $(this).next().toggleClass("is-collapsed");

/*
             if ($(this).find('i').text() == 'keyboard_arrow_down'){
               $(this).find('i').text('keyboard_arrow_up');
             } else {
               $(this).find('i').text('keyboard_arrow_down');
             }
*/
         }
     }
 });
