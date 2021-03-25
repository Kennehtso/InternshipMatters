$(window).resize(function() {
    if (window.innerWidth < 750) {
        $('.ih-item').removeClass('effect10 bottom_to_top').addClass('effect4 left_to_right');
     } else{
        $('.ih-item').removeClass('effect4 left_to_right').addClass('effect10 bottom_to_top');  
     }
        }).resize();