// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// FAQ Accordion
document.querySelectorAll('.faq-item').forEach(item => {
    const question = item.querySelector('.faq-question');
    
    question.addEventListener('click', () => {
        const isActive = item.classList.contains('active');
        
        // Close all FAQ items
        document.querySelectorAll('.faq-item').forEach(faq => {
            faq.classList.remove('active');
        });
        
        // Open clicked item if it wasn't active
        if (!isActive) {
            item.classList.add('active');
        }
    });
});

// Navbar scroll effect
let lastScroll = 0;
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > 100) {
        navbar.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.5)';
    } else {
        navbar.style.boxShadow = 'none';
    }
    
    lastScroll = currentScroll;
});

// Add animation on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe feature cards and other elements
document.querySelectorAll('.feature-card, .step, .download-card, .faq-item').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});

// Mobile menu toggle
const initMobileMenu = () => {
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            menuToggle.innerHTML = navLinks.classList.contains('active') ? '✕' : '☰';
        });
        
        // Close menu when clicking a link
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
                menuToggle.innerHTML = '☰';
            });
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.navbar')) {
                navLinks.classList.remove('active');
                menuToggle.innerHTML = '☰';
            }
        });
    }
};

// Initialize mobile menu
initMobileMenu();

// Track download clicks (for analytics if needed)
document.querySelectorAll('.btn-download').forEach(btn => {
    btn.addEventListener('click', (e) => {
        console.log('Download clicked:', e.target.textContent);
        // Add Google Analytics or other tracking here if needed
    });
});

// Add sparkle effect to hero section
const createSparkle = () => {
    const hero = document.querySelector('.hero');
    if (!hero) return;
    
    const sparkle = document.createElement('div');
    sparkle.style.cssText = `
        position: absolute;
        width: 3px;
        height: 3px;
        background: white;
        border-radius: 50%;
        pointer-events: none;
        animation: sparkle-fade 2s ease-out forwards;
    `;
    
    sparkle.style.left = Math.random() * 100 + '%';
    sparkle.style.top = Math.random() * 100 + '%';
    
    hero.appendChild(sparkle);
    
    setTimeout(() => sparkle.remove(), 2000);
};

// Add sparkle animation CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes sparkle-fade {
        0% {
            opacity: 1;
            transform: scale(0);
        }
        50% {
            opacity: 1;
            transform: scale(1);
        }
        100% {
            opacity: 0;
            transform: scale(0);
        }
    }
`;
document.head.appendChild(style);

// Create sparkles periodically
setInterval(createSparkle, 500);

// Copy code to clipboard
document.querySelectorAll('.code-block code').forEach(code => {
    code.style.cursor = 'pointer';
    code.title = 'Click to copy';
    
    code.addEventListener('click', () => {
        navigator.clipboard.writeText(code.textContent).then(() => {
            const originalText = code.textContent;
            code.textContent = '✓ Copied!';
            code.style.color = 'var(--success)';
            
            setTimeout(() => {
                code.textContent = originalText;
                code.style.color = 'var(--secondary-color)';
            }, 2000);
        });
    });
});

console.log('7K Vault website loaded! 🔒');
