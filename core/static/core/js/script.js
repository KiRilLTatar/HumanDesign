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
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: formData,
            credentials: "same-origin"
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('registerModal').style.display = 'none';

                window.location.reload();
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
                    document.getElementById('loginModal').style.display = 'none';

                    window.location.reload();

                } else {
                    
                    document.getElementById("login-error").textContent = data.error;
                }
            })
        };
    }
});


document.addEventListener('DOMContentLoaded', function() {
    // Создаем водные частицы для фона
    const particlesContainer = document.getElementById('particles');
    const particleCount = 30;
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.classList.add('particle');
        
        // Случайные параметры
        const size = Math.random() * 20 + 5;
        const posX = Math.random() * 100;
        const delay = Math.random() * 15;
        const duration = 15 + Math.random() * 20;
        
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        particle.style.left = `${posX}%`;
        particle.style.bottom = `-${size}px`;
        particle.style.animationDelay = `${delay}s`;
        particle.style.animationDuration = `${duration}s`;
        
        particlesContainer.appendChild(particle);
    }
    
    // Установка текущей даты как значения по умолчанию (25 лет назад)
    const today = new Date();
    const birthDateInput = document.getElementById('birthDate');
    const defaultBirthDate = new Date(today.getFullYear() - 25, today.getMonth(), today.getDate());
    birthDateInput.valueAsDate = defaultBirthDate;
    
    // Установка времени по умолчанию
    document.getElementById('birthTime').value = '12:00';
    
    // Обработка отправки формы
    const baziForm = document.getElementById('baziForm');
    
    baziForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const submitBtn = baziForm.querySelector('.submit-btn');
        const originalText = submitBtn.innerHTML;

        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Идёт расчёт...';
        submitBtn.disabled = true;

        const formData = new FormData();
        formData.append('name', document.getElementById('fullName').value);
        formData.append('birthDate', document.getElementById('birthDate').value);
        formData.append('birthTime', document.getElementById('birthTime').value);
        formData.append('birthPlace', document.getElementById('birthPlace').value);
        formData.append('gender', document.querySelector('input[name="gender"]:checked')?.value || '');
        formData.append('question', document.getElementById('question').value);

        console.log('Отправлены данные формы:', Object.fromEntries(formData));

        try {
            const url = baziForm.dataset.url;
            const response = await fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCsrfToken()
                }
            });

            const result = await response.json();

            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;

            if (response.ok && result.status === 'success') {
                displayBaziResult(result.data);
                baziForm.reset();
                document.getElementById('birthDate').valueAsDate = defaultBirthDate;
                document.getElementById('birthTime').value = '12:00';
            } else {
                const errors = result.errors || { general: 'Произошла ошибка при расчете карты Ба Цзы' };
                displayErrors(errors);
            }
        } catch (error) {
            console.error('Ошибка запроса:', error);
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
            displayErrors({ general: 'Ошибка связи с сервером. Пожалуйста, попробуйте снова.' });
        }
    });

    function getCsrfToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        return cookieValue || '';
    }

    function displayBaziResult(data) {
        const resultContainer = document.getElementById('baziResult');
        if (!resultContainer) {
            console.error('Контейнер для результатов (#baziResult) не найден');
            alert('Ошибка: контейнер для результатов не найден');
            return;
        }
        
        const baziCard = data.bazi_card;
        const activePillar = baziCard.luck_pillars.active_pillar;
        
        // Форматирование возраста для столпов удачи
        function formatAge(age) {
            return Math.floor(age) + '-' + Math.floor(age + 10);
        }
        
        // Создаем HTML для результатов
        let html = `
            <div class="result-header">
                <h2>Карта Бацзы для ${data.name}</h2>
                <p>Дата рождения: ${data.birthDate} ${data.birthTime} | Место: ${data.birthPlace} | Пол: ${data.gender === 'male' ? 'Мужской' : 'Женский'}</p>
                ${data.question ? `<p>Вопрос: ${data.question}</p>` : ''}
            </div>
            
            <div class="result-section">
                <div class="result-section-title">
                    <i class="fas fa-chart-line"></i>
                    <h3>Основные элементы</h3>
                </div>
                
                <div class="pillars-grid">
                    <div class="pillar-card">
                        <div class="pillar-label">Год</div>
                        <div class="pillar-value">${baziCard.year_pillar.stem} ${baziCard.year_pillar.branch}</div>
                        <div class="hidden-stems">${baziCard.hidden_stems.year.join(', ')}</div>
                    </div>
                    
                    <div class="pillar-card">
                        <div class="pillar-label">Месяц</div>
                        <div class="pillar-value">${baziCard.month_pillar.stem} ${baziCard.month_pillar.branch}</div>
                        <div class="hidden-stems">${baziCard.hidden_stems.month.join(', ')}</div>
                    </div>
                    
                    <div class="pillar-card">
                        <div class="pillar-label">День</div>
                        <div class="pillar-value">${baziCard.day_pillar.stem} ${baziCard.day_pillar.branch}</div>
                        <div class="hidden-stems">${baziCard.hidden_stems.day.join(', ')}</div>
                    </div>
                    
                    <div class="pillar-card">
                        <div class="pillar-label">Час</div>
                        <div class="pillar-value">${baziCard.hour_pillar.stem} ${baziCard.hour_pillar.branch}</div>
                        <div class="hidden-stems">${baziCard.hidden_stems.hour.join(', ')}</div>
                    </div>
                </div>
                
                <div style="display: flex; justify-content: center; gap: 30px; flex-wrap: wrap;">
                    <div>
                        <div class="pillar-label">Элемент личности</div>
                        <div class="element-badge">${baziCard.personality_element}</div>
                    </div>
                    
                    <div>
                        <div class="pillar-label">Сила карты</div>
                        <div class="strength-badge">${baziCard.strength}</div>
                    </div>
                </div>
            </div>
            
            <div class="result-section">
                <div class="result-section-title">
                    <i class="fas fa-ankh"></i>
                    <h3>Божества</h3>
                </div>
                
                <div class="deities-grid">
                    <div class="deity-card">
                        <div class="deity-type">Год (${baziCard.year_pillar.stem}):</div>
                        <div>${baziCard.deities.year_stem}</div>
                    </div>
                    
                    <div class="deity-card">
                        <div class="deity-type">Месяц (${baziCard.month_pillar.stem}):</div>
                        <div>${baziCard.deities.month_stem}</div>
                    </div>
                    
                    <div class="deity-card">
                        <div class="deity-type">День (${baziCard.day_pillar.stem}):</div>
                        <div>${baziCard.deities.day_stem}</div>
                    </div>
                    
                    <div class="deity-card">
                        <div class="deity-type">Час (${baziCard.hour_pillar.stem}):</div>
                        <div>${baziCard.deities.hour_stem}</div>
                    </div>
                </div>
            </div>`;
            
        // Добавляем раздел со звездами, если они есть
        if (baziCard.stars && baziCard.stars.length > 0) {
            html += `
            <div class="result-section">
                <div class="result-section-title">
                    <i class="fas fa-star"></i>
                    <h3>Символические звезды</h3>
                </div>
                <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                    ${baziCard.stars.map(star => 
                        `<div class="element-badge">${star}</div>`
                    ).join('')}
                </div>
            </div>`;
        }
        
        // Добавляем раздел со столпами удачи
        html += `
            <div class="result-section">
                <div class="result-section-title">
                    <i class="fas fa-history"></i>
                    <h3>Столпы Удачи</h3>
                </div>
                
                <table class="luck-pillars-table">
                    <thead>
                        <tr>
                            <th>Возраст</th>
                            <th>Столп</th>
                        </tr>
                    </thead>
                    <tbody>`;
        
        baziCard.luck_pillars.luck_pillars.forEach(pillar => {
            const isActive = activePillar && 
                             pillar.start_age === activePillar.start_age && 
                             pillar.pillar === activePillar.pillar;
            
            html += `
                <tr ${isActive ? 'class="current-pillar"' : ''}>
                    <td>${formatAge(pillar.start_age)}</td>
                    <td>${pillar.pillar}</td>
                </tr>`;
        });
        
        html += `
                    </tbody>
                </table>
                
                ${activePillar ? `
                <div style="margin-top: 25px; padding: 15px; background: rgba(26, 74, 107, 0.4); border-radius: 12px;">
                    <div style="font-weight: bold; margin-bottom: 10px; color: #4aa8d8;">Текущий Столп Удачи:</div>
                    <div>${activePillar.pillar} (${formatAge(activePillar.start_age)} лет)</div>
                </div>` : ''}
            </div>`;
        
        // Добавляем ошибки, если они есть
        if (baziCard.luck_pillars.errors && baziCard.luck_pillars.errors.length > 0) {
            html += `
            <div class="result-section">
                <div class="result-section-title">
                    <i class="fas fa-exclamation-triangle"></i>
                    <h3>Ошибки расчета</h3>
                </div>
                <ul style="color: #ff6b6b;">
                    ${baziCard.luck_pillars.errors.map(err => `<li>${err}</li>`).join('')}
                </ul>
            </div>`;
        }
        
        // Вставляем HTML в контейнер и отображаем его
        resultContainer.innerHTML = html;
        resultContainer.style.display = 'block';
        
        // Прокручиваем страницу к результатам
        resultContainer.scrollIntoView({ behavior: 'smooth' });
    }
    
    function displayErrors(errors) {
        const resultContainer = document.getElementById('baziResult');
        if (!resultContainer) {
            console.error('Контейнер для результатов (#baziResult) не найден');
            alert('Ошибка: контейнер для результатов не найден');
            return;
        }

        let errorHtml = '<div class="result-header"><h2>Ошибки</h2></div><ul style="color: #ff6b6b;">';
        for (const [key, value] of Object.entries(errors)) {
            errorHtml += `<li>${key}: ${value}</li>`;
        }
        errorHtml += '</ul>';
        resultContainer.innerHTML = errorHtml;
        resultContainer.style.display = 'block';
        resultContainer.scrollIntoView({ behavior: 'smooth' });
        
        alert('Произошла ошибка при расчете карты Ба Цзы. Проверьте введенные данные.');
    }
});