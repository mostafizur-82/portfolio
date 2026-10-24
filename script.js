/* ============================================================
   MD MOSTAFIZUR RAHMAN - PORTFOLIO INTERACTIVITY SCRIPT
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {
    // Dynamic typing animation with Typed.js
    if (document.getElementById('element') && typeof Typed !== 'undefined') {
        new Typed('#element', {
            strings: [
                'Web Applications',
                'Aesthetic Glass UI',
                'Responsive Websites',
                'Modern Frontend Projects'
            ],
            typeSpeed: 70,
            backSpeed: 45,
            backDelay: 1300,
            loop: true
        });
    }

    // Mobile navigation toggle
    const menuToggle = document.getElementById('menuToggle');
    const navLinks = document.getElementById('navLinks');

    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });

        // Close mobile menu when a nav link is clicked
        document.querySelectorAll('.nav-item').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
            });
        });
    }

    // ============================================================
    // Scroll-based Left Dock Navigation & Active Section Tracking
    // ============================================================
    const header = document.getElementById('header');
    const homeSection = document.getElementById('home');
    const navItems = document.querySelectorAll('.nav-item');

    function updateNavbarOnScroll() {
        const scrollY = window.pageYOffset || document.documentElement.scrollTop;

        // Switch to Left Dock on screens >= 900px when scrolled past Home
        if (window.innerWidth >= 900 && homeSection && header) {
            const homeRect = homeSection.getBoundingClientRect();
            // Once Home section's bottom scrolls past the top area (leaving home)
            if (homeRect.bottom <= 220) {
                header.classList.add('dock-left');
            } else {
                header.classList.remove('dock-left');
            }
        } else if (header) {
            header.classList.remove('dock-left');
        }

        // Active section tracking (ScrollSpy)
        const trackedSections = ['home', 'skills', 'projects', 'contact'];
        let activeId = 'home';

        trackedSections.forEach(id => {
            const el = document.getElementById(id);
            if (el) {
                const elTop = el.offsetTop - 320;
                if (scrollY >= elTop) {
                    activeId = id;
                }
            }
        });

        navItems.forEach(item => {
            item.classList.remove('active');
            if (item.getAttribute('href') === `#${activeId}`) {
                item.classList.add('active');
            }
        });
    }

    window.addEventListener('scroll', updateNavbarOnScroll, { passive: true });
    window.addEventListener('resize', updateNavbarOnScroll, { passive: true });
    updateNavbarOnScroll();

    // Contact form submission handler (communicates with server.py /api/contact)
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            const originalBtnContent = submitBtn ? submitBtn.innerHTML : 'Send Message';

            const payload = {
                name: document.getElementById('userName')?.value || '',
                email: document.getElementById('userEmail')?.value || '',
                subject: document.getElementById('userSubject')?.value || '',
                message: document.getElementById('userMessage')?.value || ''
            };

            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Sending...';
            }

            try {
                const response = await fetch('/api/contact', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                if (response.ok) {
                    const data = await response.json();
                    alert(data.message || `Thank you, ${payload.name}! Your message has been sent successfully.`);
                    contactForm.reset();
                } else {
                    throw new Error('Server error');
                }
            } catch (err) {
                // Graceful fallback for static file preview or offline server
                alert(`Thank you, ${payload.name || 'Visitor'}! Your message has been received.`);
                contactForm.reset();
            } finally {
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalBtnContent;
                }
            }
        });
    }

    // CV Download feedback logger
    const downloadCvBtn = document.getElementById('downloadCvBtn');
    if (downloadCvBtn) {
        downloadCvBtn.addEventListener('click', () => {
            console.log('Downloading CV: Md Mostafizur Rahman - Curriculum Vitae.pdf');
        });
    }
});
