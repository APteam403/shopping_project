document.addEventListener('DOMContentLoaded', function() {
    // اسلایدر اصلی
    var swiper = new Swiper(".mySwiper", {
        spaceBetween: 30,
        centeredSlides: true,
        autoplay: {
            delay: 5000,
            disableOnInteraction: false,
        },
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
        },
        loop: true,
        effect: 'fade',
        fadeEffect: {
            crossFade: true
        },
    });
    
    // فعال کردن منوی همبرگری در نسخه موبایل
    var navbarToggler = document.querySelector('.navbar-toggler');
    if (navbarToggler) {
        navbarToggler.addEventListener('click', function() {
            this.querySelector('i').classList.toggle('fa-times');
        });
    }
    
    // انیمیشن اسکرول
    const animateElements = document.querySelectorAll('.animate-slide-up, .animate-fade-in');
    
    const animateOnScroll = () => {
        animateElements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (elementTop < windowHeight - 100) {
                element.style.opacity = 1;
                element.style.transform = 'translateY(0)';
            }
        });
    };
    
    // اجرای اولیه
    animateOnScroll();
    
    // اجرا هنگام اسکرول
    window.addEventListener('scroll', animateOnScroll);
});