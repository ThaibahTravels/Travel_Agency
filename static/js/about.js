document.addEventListener("DOMContentLoaded", function () {
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
});