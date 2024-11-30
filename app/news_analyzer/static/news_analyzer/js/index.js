document.addEventListener("DOMContentLoaded", () => {
    const navLinks = document.querySelectorAll(".nav-link");
    navLinks.forEach(link => {
        const linkHref = link.querySelector("a").getAttribute("href");
        if (window.location.pathname === linkHref) {
            link.classList.add("active");
        }
    });

    navLinks.forEach(link => {
        link.addEventListener("click", () => {
            navLinks.forEach(nav => nav.classList.remove("active"));
            link.classList.add("active");
        });
    });

    const textInput = document.querySelector(".text-input");
    const submitButton = document.querySelector(".submit-button");
    const loaderModal = document.getElementById("loaderModal");
    const resultModal = document.getElementById("resultModal");
    const resultTitle = document.getElementById("resultTitle");
    const probabilityText = document.getElementById("probabilityText");

    submitButton.addEventListener("click", async () => {
        const inputValue = textInput.value.trim();
        if (inputValue === "") return;

        loaderModal.style.display = "flex";

        try {
            const response = await fetch('/api/analyze-news/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ content: inputValue }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                console.error('Ошибка:', errorData.error);
                alert(`Ошибка: ${errorData.error}`);
                loaderModal.style.display = "none";
                return;
            }

            const result = await response.json();
            const isFake = result.is_fake;
            const probability = result.probability;

            resultTitle.textContent = isFake ? "Fake" : "Not Fake";
            probabilityText.textContent = `Вероятность: ${probability}%`;

            const add_to_db_response = await fetch('/api/add-news/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ content: inputValue, is_fake: isFake, probability: probability }),
            });
            console.log(add_to_db_response);

        } catch (error) {
            console.error('Ошибка сети или сервера:', error);
            alert('Произошла ошибка при обработке запроса. Попробуйте позже.');
        } finally {
            loaderModal.style.display = "none";
            resultModal.style.display = "flex";
            textInput.value = "";
        }
    });

    resultModal.addEventListener("click", (e) => {
        if (e.target === resultModal) {
            resultModal.style.display = "none";
        }
    });
});
