document.addEventListener("DOMContentLoaded", () => {
        const ctx = document.getElementById('newsChart').getContext('2d');
        const chartData = {
            labels: ['Фейковые новости', 'Достоверные новости'],
            datasets: [{
                label: 'Процентное соотношение',
                data: [{{ fake_percentage }}, {{ real_percentage }}],
                backgroundColor: ['#ff6384', '#36a2eb'],
                hoverBackgroundColor: ['#ff6384', '#36a2eb'],
                borderWidth: 1
            }]
        };

        const chartOptions = {
            responsive: false, // Отключаем автоматическое масштабирование
            maintainAspectRatio: true, // Сохраняем пропорции
        };

        new Chart(ctx, {
            type: 'pie',
            data: chartData,
            options: chartOptions,
        });
    });