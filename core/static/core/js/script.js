// Плавная прокрутка
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                const targetId = this.getAttribute('href');
                if (targetId === '#') {
                    e.preventDefault();
                    return;
                }

                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    e.preventDefault();
                    targetElement.scrollIntoView({
                        behavior: 'smooth'
                    });
                }
            });
        });
        
        // Анимация элементов при скролле
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    setTimeout(() => {
                        entry.target.style.opacity = 1;
                        entry.target.style.transform = 'translateY(0)';
                    }, 200);
                }
            });
        }, { threshold: 0.1 });
        
        document.querySelectorAll('.element, .step, .pillar').forEach(el => {
            el.style.opacity = 0;
            el.style.transform = 'translateY(30px)';
            el.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
            observer.observe(el);
        });
        
        // Динамическое изменение шапки
        window.addEventListener('scroll', () => {
            const header = document.querySelector('header');
            if (window.scrollY > 100) {
                header.style.boxShadow = '0 5px 20px rgba(0, 0, 0, 0.3)';
                header.style.background = 'rgba(10, 42, 67, 0.95)';
            } else {
                header.style.boxShadow = '0 2px 15px rgba(0, 0, 0, 0.2)';
                header.style.background = 'rgba(10, 42, 67, 0.85)';
            }
        });
        
        // Анимация волн
        const waves = document.querySelectorAll('.waves');
        waves.forEach((wave, index) => {
            wave.style.animationDelay = `${index * 2}s`;
        });
        
        // Modal functionality
        const loginModal = document.getElementById('loginModal');
        const registerModal = document.getElementById('registerModal');
        const loginLink = document.getElementById('loginLink');
        const registerLink = document.getElementById('registerLink');
        const showLogin = document.getElementById('showLogin');
        const showRegister = document.getElementById('showRegister');
        const closeButtons = document.querySelectorAll('.close-modal');
        
        // Open login modal
        loginLink.addEventListener('click', (e) => {
            e.preventDefault();
            closeAllModals();
            loginModal.classList.add('active');
        });
        
        // Open register modal
        registerLink.addEventListener('click', (e) => {
            e.preventDefault();
            closeAllModals();
            registerModal.classList.add('active');
        });
        
        // Switch to register from login
        showRegister.addEventListener('click', (e) => {
            e.preventDefault();
            closeAllModals();
            registerModal.classList.add('active');
        });
        
        // Switch to login from register
        showLogin.addEventListener('click', (e) => {
            e.preventDefault();
            closeAllModals();
            loginModal.classList.add('active');
        });
        
        // Close modals
        closeButtons.forEach(button => {
            button.addEventListener('click', () => {
                closeAllModals();
            });
        });
        
        // Close modals when clicking outside
        window.addEventListener('click', (e) => {
            if (e.target === loginModal) {
                closeAllModals();
            }
            if (e.target === registerModal) {
                closeAllModals();
            }
        });
        
        function closeAllModals() {
            loginModal.classList.remove('active');
            registerModal.classList.remove('active');
        }

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById('registerForm');
    if (!form) return;

    const url = form.dataset.url;

    form.onsubmit = function (e) {
        e.preventDefault();

        const formData = new FormData(form);

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: formData,
            credentials: "same-origin"
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const modal = bootstrap.Modal.getInstance(document.getElementById('registerModal'));
                closeAllModals();

                form.reset();
                window.location.href = data.redirect_url;
            } else {
                const errors = data.errors || ["Ошибка регистрации"];
                alert(errors.join("\n"));
            }
        })
    };
});


document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("loginForm");

    if (loginForm) {
        loginForm.onsubmit = function (e) {
            e.preventDefault(); 

            const url = loginForm.dataset.url; 
            const formData = new FormData(loginForm); 

            fetch(url, {
                method: "POST",
                body: formData,
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                credentials: "include"
            })
            .then((res) => res.json()) 
            .then((data) => {
                if (data.success) {
                    const modal = bootstrap.Modal.getInstance(document.getElementById("loginModal"));
                    closeAllModals();

                    loginForm.reset();

                    window.location.reload();  

                } else {
                    
                    document.getElementById("login-error").textContent = data.error;
                }
            })
        };
    }
});
