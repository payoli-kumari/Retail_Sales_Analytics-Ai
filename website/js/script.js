/* ============================================= */
/*         MAIN SCRIPT                            */
/*         Retail Sales Analytics                 */
/*         KPI Counters, Smooth Scroll,           */
/*         Fade-in, Mobile Menu, Active Nav       */
/* ============================================= */

document.addEventListener('DOMContentLoaded', function () {

    // =========================================
    // 1. NAVBAR — Scroll Effect & Active Link
    // =========================================
    const navbar = document.getElementById('navbar');
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('section[id]');

    function updateNavbar() {
        if (window.scrollY > 60) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }

    function updateActiveNav() {
        const scrollPos = window.scrollY + 150;
        sections.forEach(section => {
            const top = section.offsetTop;
            const height = section.offsetHeight;
            const id = section.getAttribute('id');
            if (scrollPos >= top && scrollPos < top + height) {
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${id}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }

    window.addEventListener('scroll', function () {
        updateNavbar();
        updateActiveNav();
    }, { passive: true });

    updateNavbar();

    // =========================================
    // 2. MOBILE MENU TOGGLE
    // =========================================
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function () {
            navToggle.classList.toggle('active');
            navMenu.classList.toggle('active');
        });

        // Close menu on link click
        navLinks.forEach(link => {
            link.addEventListener('click', function () {
                navToggle.classList.remove('active');
                navMenu.classList.remove('active');
            });
        });

        // Close on outside click
        document.addEventListener('click', function (e) {
            if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
                navToggle.classList.remove('active');
                navMenu.classList.remove('active');
            }
        });
    }

    // =========================================
    // 3. SMOOTH SCROLL FOR ANCHOR LINKS
    // =========================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            const target = document.querySelector(targetId);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // =========================================
    // 4. FADE-IN ON SCROLL (Intersection Observer)
    // =========================================
    const fadeElements = document.querySelectorAll('.fade-in');

    const fadeObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                // Stagger the animation slightly for elements in the same group
                setTimeout(() => {
                    entry.target.classList.add('visible');
                }, index * 80);
                fadeObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -40px 0px'
    });

    fadeElements.forEach(el => fadeObserver.observe(el));

    // =========================================
    // 5. KPI COUNTER ANIMATION
    // =========================================
    const kpiValues = document.querySelectorAll('.kpi-value[data-target]');
    let kpiAnimated = false;

    function formatNumber(num, separator) {
        if (separator) {
            return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
        }
        return num.toString();
    }

    function animateCounter(element) {
        const target = parseFloat(element.dataset.target);
        const prefix = element.dataset.prefix || '';
        const suffix = element.dataset.suffix || '';
        const decimals = parseInt(element.dataset.decimals) || 0;
        const useSeparator = element.dataset.separator === 'true';
        const duration = 2000;
        const startTime = performance.now();

        function easeOutQuart(t) {
            return 1 - Math.pow(1 - t, 4);
        }

        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const easedProgress = easeOutQuart(progress);
            let currentValue = easedProgress * target;

            if (decimals > 0) {
                element.textContent = prefix + currentValue.toFixed(decimals) + suffix;
            } else {
                const intValue = Math.floor(currentValue);
                element.textContent = prefix + formatNumber(intValue, useSeparator) + suffix;
            }

            if (progress < 1) {
                requestAnimationFrame(update);
            } else {
                // Ensure final value is exact
                if (decimals > 0) {
                    element.textContent = prefix + target.toFixed(decimals) + suffix;
                } else {
                    element.textContent = prefix + formatNumber(Math.round(target), useSeparator) + suffix;
                }
            }
        }

        requestAnimationFrame(update);
    }

    const kpiObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !kpiAnimated) {
                kpiAnimated = true;
                kpiValues.forEach((kpi, index) => {
                    setTimeout(() => animateCounter(kpi), index * 150);
                });
                kpiObserver.disconnect();
            }
        });
    }, {
        threshold: 0.3
    });

    // Observe the KPI section
    const kpiSection = document.getElementById('kpis');
    if (kpiSection) {
        kpiObserver.observe(kpiSection);
    }

    // =========================================
    // 6. CATEGORY BAR FILL ANIMATION
    // =========================================
    const categoryBars = document.querySelectorAll('.category-bar-fill');
    const categoryObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const fills = entry.target.querySelectorAll('.category-bar-fill');
                fills.forEach(fill => {
                    const width = fill.style.width;
                    fill.style.width = '0%';
                    setTimeout(() => {
                        fill.style.width = width;
                    }, 300);
                });
                categoryObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.3 });

    const categorySection = document.querySelector('.category-cards');
    if (categorySection) {
        categoryObserver.observe(categorySection);
    }

    // =========================================
    // 7. RECOMMENDATION IMPACT BAR ANIMATION
    // =========================================
    const recImpactFills = document.querySelectorAll('.rec-impact-fill');
    const recObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const fills = entry.target.querySelectorAll('.rec-impact-fill');
                fills.forEach(fill => {
                    const targetWidth = fill.style.width;
                    fill.style.width = '0%';
                    setTimeout(() => {
                        fill.style.width = targetWidth;
                        fill.style.transition = 'width 1.5s ease';
                    }, 300);
                });
                recObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.3 });

    const recSection = document.querySelector('.recommendations-grid');
    if (recSection) {
        recObserver.observe(recSection);
    }

});
