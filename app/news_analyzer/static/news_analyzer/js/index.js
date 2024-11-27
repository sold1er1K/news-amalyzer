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
});

document.addEventListener("DOMContentLoaded", () => {
    const textInput = document.querySelector(".text-input");
    const submitButton = document.querySelector(".submit-button");

    submitButton.addEventListener("click", () => {
        const inputValue = textInput.value;
        console.log(inputValue);
        textInput.value = "";
    });
});