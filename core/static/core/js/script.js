        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
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