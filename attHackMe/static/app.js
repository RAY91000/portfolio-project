document.addEventListener("DOMContentLoaded", () => {
    const registerForm = document.getElementById("registerForm");
    const loginForm = document.getElementById("loginForm");

    if (registerForm) {
        registerForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const formData = new FormData(registerForm);
            const response = await fetch("http://127.0.0.1:5000/register", {
                method: "POST",
                body: formData
            });
            const data = await response.json();
            document.getElementById("registerMsg").innerText = data.message || data.error;
        });
    }

    if (loginForm) {
        loginForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const formData = new FormData(loginForm);
            const response = await fetch("http://127.0.0.1:5000/login", {
                method: "POST",
                body: formData
            });
            const data = await response.json();
            document.getElementById("loginMsg").innerText = data.message || data.error;
        });
    }

    const challengeList = document.getElementById("challengeList");
    if (challengeList) {
        fetch("http://127.0.0.1:5000/challenges/")
            .then(res => res.json())
            .then(data => {
                data.forEach(challenge => {
                    const li = document.createElement("li");
                    li.textContent = `${challenge.title} - ${challenge.difficulty}`;
                    challengeList.appendChild(li);
                });
            });
    }
});
