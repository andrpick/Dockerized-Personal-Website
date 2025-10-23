// UI interactions: sticky header shadow, scroll-to-top, and reduced-motion friendly animations
(function () {
    const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // Sticky header shadow on scroll
    const header = document.querySelector('header');
    const shadowClass = 'header--elevated';
    function onScroll() {
        if (!header) return;
        if (window.scrollY > 8) {
            header.classList.add(shadowClass);
        } else {
            header.classList.remove(shadowClass);
        }
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    // Scroll to top button
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'to-top-btn';
    btn.setAttribute('aria-label', 'Scroll to top');
    btn.innerHTML = '▲';
    document.body.appendChild(btn);

    function updateToTopVisibility() {
        const threshold = 400;
        if (window.scrollY > threshold) {
            btn.classList.add('to-top-btn--visible');
        } else {
            btn.classList.remove('to-top-btn--visible');
        }
    }

    btn.addEventListener('click', function () {
        if (prefersReduced) {
            window.scrollTo(0, 0);
        } else {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    });

    window.addEventListener('scroll', updateToTopVisibility, { passive: true });
    updateToTopVisibility();
})();

// Image modal functionality
function openModal(img) {
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImage');
    const caption = document.getElementById('caption');
    
    modal.style.display = 'block';
    modalImg.src = img.src;
    caption.innerHTML = img.alt;
}

function closeModal() {
    document.getElementById('imageModal').style.display = 'none';
}

// Close modal with Escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeModal();
    }
});

// Dropdown menu functionality
function toggleDropdown(button) {
    const dropdown = button.parentElement;
    const menu = dropdown.querySelector('.dropdown-menu');
    const isOpen = menu.classList.contains('show');
    
    // Close all other dropdowns
    document.querySelectorAll('.dropdown-menu.show').forEach(openMenu => {
        if (openMenu !== menu) {
            openMenu.classList.remove('show');
        }
    });
    
    // Toggle current dropdown
    if (isOpen) {
        menu.classList.remove('show');
    } else {
        // Simple approach: always position upward if button is in bottom half of screen
        const buttonRect = button.getBoundingClientRect();
        const screenHeight = window.innerHeight;
        const buttonCenter = buttonRect.top + (buttonRect.height / 2);
        
        // Reset positioning classes
        menu.classList.remove('dropdown-menu-up');
        
        // If button is in bottom half of screen, position upward
        if (buttonCenter > screenHeight / 2) {
            menu.classList.add('dropdown-menu-up');
        }
        
        menu.classList.add('show');
    }
}

// Close dropdowns when clicking outside
document.addEventListener('click', function(event) {
    if (!event.target.closest('.dropdown')) {
        document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
            menu.classList.remove('show');
        });
    }
});

// Close dropdowns when pressing Escape
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
            menu.classList.remove('show');
        });
    }
});

// Close dropdowns on window resize to prevent positioning issues
window.addEventListener('resize', function() {
    document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
        menu.classList.remove('show');
    });
});



