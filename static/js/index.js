document.addEventListener("DOMContentLoaded", function () {
  // Counter Animation Logic
  const counterElement = document.getElementById("traveler-counter");

  if (counterElement) {
    const observer = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          let count = 0;
          const target = 2000;
          const increment = Math.ceil(target / 100);

          const counterInterval = setInterval(() => {
            count += increment;
            if (count >= target) {
              count = target;
              clearInterval(counterInterval);
            }
            entry.target.textContent = count;
          }, 50);

          // Stop observing after the counter starts
          observer.unobserve(entry.target);
        }
      });
    });

    observer.observe(counterElement);
  }

  // Slick Carousel Initialization
  $(document).ready(function () {
    // Function to initialize Slick Carousel with dynamic dot adjustment
    function initializeSlickCarousel(selector, slidesToShow, slidesToScroll) {
      const carousel = $(selector);

      carousel.slick({
        infinite: true, // Continuous loop
        slidesToShow: slidesToShow, // Number of slides to show at a time
        slidesToScroll: slidesToScroll, // Number of slides to scroll at a time
        autoplay: true, // Enable auto-scroll
        autoplaySpeed: 2000, // Auto-scroll speed (2 seconds)
        dots: true, // Show dots
        arrows: false, // Disable arrows (prev/next buttons)
        centerMode: false, // Disable centering
        responsive: [
          {
            breakpoint: 1024,
            settings: {
              slidesToShow: 2, // Show 2 slides on medium screens
              slidesToScroll: 2
            }
          },
          {
            breakpoint: 600,
            settings: {
              slidesToShow: 1, // Show 1 slide on small screens
              slidesToScroll: 1
            }
          }
        ]
      });
    }

    // Initialize carousels
    initializeSlickCarousel('.slick-carousel', 3, 3); // Packages and Services sections
  });
});