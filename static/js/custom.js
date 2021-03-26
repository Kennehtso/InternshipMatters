$(window).resize(function () {
   if (window.innerWidth < 750) {
      $('.ih-item').removeClass('effect10 bottom_to_top').addClass('effect4 left_to_right');
   } else {
      $('.ih-item').removeClass('effect4 left_to_right').addClass('effect10 bottom_to_top');
   }
}).resize();


$('#internshipType_select').click(function () {
   bgReact($(this));
});

$('#location_select').click(function (e) {
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