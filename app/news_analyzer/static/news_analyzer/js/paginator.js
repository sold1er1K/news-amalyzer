document.addEventListener('DOMContentLoaded', function () {
    const prevButton = document.querySelector('.page-prev');
    const nextButton = document.querySelector('.page-next');
    const pageNumberSpan = document.querySelector('.page-number');
    const totalPagesSpan = document.querySelector('.total-pages');
    const currentPage = parseInt(pageNumberSpan.dataset.page);
    const totalPages = parseInt(totalPagesSpan.textContent);

    // Логика для кнопки "Предыдущая страница"
    prevButton.addEventListener('click', function () {
        if (currentPage > 1) {
            const newPage = currentPage - 1;
            window.location.href = `?page=${newPage}`;
        }
    });

    // Логика для кнопки "Следующая страница"
    nextButton.addEventListener('click', function () {
        if (currentPage < totalPages) {
            const newPage = currentPage + 1;
            window.location.href = `?page=${newPage}`;
        }
    });
});