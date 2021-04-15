$(window).resize(function () {
   console.log("window width: "+ $(window).width());
   console.log("window.innerWidth: "+ window.innerWidth);
   if (window.innerWidth < 750) {
      $('.ih-item').removeClass('effect10 bottom_to_top').addClass('effect4 left_to_right');
   } else {
      $('.ih-item').removeClass('effect4 left_to_right').addClass('effect10 bottom_to_top');
   }
   if (window.innerWidth <= 1068) {
      $('.comments-info').css({"display": "block", "width": "100%"});
      $('#commentsSection').css({"padding-top": "10px","margin-left": "0px"});
   } else {
      $('.comments-info').css({"display": "table-cell", "width": "30%"});
      $('#commentsSection').css({"padding-top": "0px","margin-left": "1%"});
   }
}).resize();

$('#location_list').click(function (e) {
   bgReact($(this));
});

$('#internshipType_select').click(function () {
   bgReact($(this));
});

function bgReact(by) {
   $('header.masthead .overlay').css('opacity',0.3);
   $('#bannerTitle').css({
      'font-size':'3em',
      'text-shadow':''
   });

   if (by.attr("aria-expanded") == "false") {
      $('header.masthead .overlay').css('opacity',0.7);
      $('#bannerTitle').css({
         'font-size':'3.5em',
         'text-shadow':'#17a2b8 0 0 25px',
         'color':"#17a2b8;"
      });
   }
}

$(document).click(function() {
   $('header.masthead .overlay').css('opacity',0.3);
   $('#bannerTitle').css({
      'font-size':'3em',
      'text-shadow':''
   });

   let isShowLocation = $('location_list').hasClass('show');
   let isShowInternshipType = $('internshipType_list').hasClass('show');
   let anyIsShow = isShowLocation || isShowInternshipType;
   
   if (anyIsShow || ($("#bannerSearch").is(":focus"))){
      $('header.masthead .overlay').css('opacity',0.7);
      $('#bannerTitle').css({
         'font-size':'3.5em',
         'text-shadow':'#17a2b8 0 0 25px',
         'color':"#17a2b8;"
      });
   }
});

 /* auto completed js start */
function autocomplete(inp, arr) {
   /*the autocomplete function takes two arguments,
   the text field element and an array of possible autocompleted values:*/
   var currentFocus;
   /*execute a function when someone writes in the text field:*/
   inp.addEventListener("input", function(e) {
       var a, b, i, val = this.value;
       /*close any already open lists of autocompleted values*/
       closeAllLists();
       if (!val) { return false;}
       currentFocus = -1;
       /*create a DIV element that will contain the items (values):*/
       a = document.createElement("DIV");
       a.setAttribute("id", this.id + "autocomplete-list");
       a.setAttribute("class", "autocomplete-items col-md-10 col-lg-10 col-xl-10 mb-5 mb-md-0");
       /*append the DIV element as a child of the autocomplete container:*/
       this.parentNode.appendChild(a);
       /*for each item in the array...*/
       for (i = 0; i < arr.length; i++) {
         /*check if the item starts with the same letters as the text field value:*/
         //let condition = arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase();
         let condition = arr[i].toUpperCase().indexOf(val.toUpperCase());
         if (condition != -1) {
           const regex =  new RegExp(val.toUpperCase(),'g'); // correct way
           var newstr = arr[i].replace(regex,"<strong class='searchHighlight'>" + val.toUpperCase() + "</strong>");
           /*create a DIV element for each matching element:*/
           b = document.createElement("DIV");
           /*make the matching letters bold:*/
           //b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
           //b.innerHTML += arr[i].substr(val.length);
           b.innerHTML = newstr
           /*insert a input field that will hold the current array item's value:*/
           b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
           /*execute a function when someone clicks on the item value (DIV element):*/
               b.addEventListener("click", function(e) {
               /*insert the value for the autocomplete text field:*/
               inp.value = this.getElementsByTagName("input")[0].value;
               /*close the list of autocompleted values,
               (or any other open lists of autocompleted values:*/
               closeAllLists();
           });
           a.appendChild(b);
         }
       }
   });
   /*execute a function presses a key on the keyboard:*/
   inp.addEventListener("keydown", function(e) {
       var x = document.getElementById(this.id + "autocomplete-list");
       if (x) x = x.getElementsByTagName("div");
       if (e.keyCode == 40) {
         /*If the arrow DOWN key is pressed,
         increase the currentFocus variable:*/
         currentFocus++;
         /*and and make the current item more visible:*/
         addActive(x);
       } else if (e.keyCode == 38) { //up
         /*If the arrow UP key is pressed,
         decrease the currentFocus variable:*/
         currentFocus--;
         /*and and make the current item more visible:*/
         addActive(x);
       } else if (e.keyCode == 13) {
         /*If the ENTER key is pressed, prevent the form from being submitted,*/
         e.preventDefault();
         if (currentFocus > -1) {
           /*and simulate a click on the "active" item:*/
           if (x) x[currentFocus].click();
         }
       }
   });
   function addActive(x) {
     /*a function to classify an item as "active":*/
     if (!x) return false;
     /*start by removing the "active" class on all items:*/
     removeActive(x);
     if (currentFocus >= x.length) currentFocus = 0;
     if (currentFocus < 0) currentFocus = (x.length - 1);
     /*add class "autocomplete-active":*/
     x[currentFocus].classList.add("autocomplete-active");
   }
   function removeActive(x) {
     /*a function to remove the "active" class from all autocomplete items:*/
     for (var i = 0; i < x.length; i++) {
       x[i].classList.remove("autocomplete-active");
     }
   }
   function closeAllLists(elmnt) {
     /*close all autocomplete lists in the document,
     except the one passed as an argument:*/
     var x = document.getElementsByClassName("autocomplete-items");
     for (var i = 0; i < x.length; i++) {
       if (elmnt != x[i] && elmnt != inp) {
       x[i].parentNode.removeChild(x[i]);
     }
   }
 }
 /*execute a function when someone clicks in the document:*/
 document.addEventListener("click", function (e) {
     closeAllLists(e.target);
 });
 } 
 /* auto completed js end */

 /* window resize action */
 