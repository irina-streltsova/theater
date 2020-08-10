(function($) {
    "use strict"; // Start of use strict

    // Smooth scrolling using jQuery easing
    $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function() {
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
            if (target.length) {
                $('html, body').animate({
                    scrollTop: (target.offset().top - 56)
                }, 1000, "easeInOutExpo");
                return false;
            }
        }
    });

    $('body').scrollspy({
        target: '#main-nav',
        offset: 57
    });

    var navbarCollapse = function() {
        if ($("#main-nav").offset().top > 100) {
            $("#main-nav").addClass("navbar-scrolled");
        } else {
            $("#main-nav").removeClass("navbar-scrolled");
        }
    };
    navbarCollapse();
    $(window).scroll(navbarCollapse);

})(jQuery); // End of use strict