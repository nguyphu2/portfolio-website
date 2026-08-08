document.addEventListener('DOMContentLoaded', function () {
    var revealTargets = document.querySelectorAll('.reveal, .portfolio-tile, .resume-entry, .project-card');

    if ('IntersectionObserver' in window) {
        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });

        revealTargets.forEach(function (el, i) {
            el.classList.add('reveal-init');
            el.style.transitionDelay = (i % 6) * 60 + 'ms';
            observer.observe(el);
        });
    } else {
        revealTargets.forEach(function (el) {
            el.classList.add('is-visible');
        });
    }
});
