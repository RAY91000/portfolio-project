document.addEventListener("DOMContentLoaded", () => {
    const registerForm = document.getElementById("registerForm");
    const loginForm = document.getElementById("loginForm");
    const challengeList = document.getElementById("challengeList");
    const challengeDetails = document.getElementById("challengeDetails");


    // Handle Register Form
    if (registerForm) {
        registerForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const formData = new FormData(registerForm);
            const response = await fetch("http://127.0.0.1:5000/register", {
                method: "POST",
                body: formData,
                cache: "no-store"
            });
            const data = await response.json();

            if (response.ok) {
                window.location.href = "/login";
            } else {
                document.getElementById("registerMsg").innerText = data.message || data.error;
            }     
        });
    }

    // Handle Login Form
    if (loginForm) {
        loginForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const formData = new FormData(loginForm);
            const response = await fetch("http://127.0.0.1:5000/login", {
                method: "POST",
                body: formData,
                cache: "no-store"
            });
            const data = await response.json();
            if (data.access_token) {
                localStorage.setItem("token", data.access_token);
                localStorage.setItem("username", data.username);
                window.location.href = "/challenges";
            } else {
                document.getElementById("loginMsg").innerText = data.message || data.error;
            }
        });
    }

    // Load Challenge List
    if (challengeList) {
        
        const difficultyIcons = {
            "Easy": "🟢 Noob",
            "Medium": "🟡 Medium",
            "Hard": "🔴 Ranker"
        };

        fetch("http://127.0.0.1:5000/challenges/", {
            method: "GET"
        })
            .then(res => res.json())
            .then(data => {
                data.forEach(challenge => {
                    const li = document.createElement("li");

                    li.className = `
                        bg-[#1e1e2f] text-white border border-green-400
                        rounded-lg p-6 mb-4 shadow-lg
                        transition-all duration-300 hover:scale-105 hover:shadow-green-500
                    `;

                    li.innerHTML = `
                        <div class="flex justify-between items-start">
                            <div>
                                <h3 class="text-2xl font-bold text-green-400 mb-1">${challenge.title}</h3>
                                <p class="text-sm text-gray-300 mb-2">${challenge.description}</p>
                                <p class="text-sm text-yellow-300">
                                    🧠 Category: ${challenge.category || "Unknown"}<br>
                                    💀 Difficulty: ${difficultyIcons[challenge.difficulty] || challenge.difficulty || "Unknown"}
                                </p>
                            </div>
                            <div class="flex flex-col gap-2 text-sm">
                                <a href="/challenge/${challenge.id}" class="bg-blue-600 text-white px-3 py-2 rounded hover:bg-blue-700 text-center">
                                    🔍 View
                                </a>
                                <button class="bg-pink-600 text-white px-3 py-2 rounded hover:bg-pink-700">
                                    🕹️ Start
                                </button>
                            </div>
                        </div>
                    `;

                    challengeList.appendChild(li);
                });
            })
            .catch(error => {
                challengeList.innerHTML = `<li class="text-red-500">❌ Failed to load challenges: ${error.message}</li>`;
                console.error(error);
            });
    }

    // Attach event listener to start button
    const startBtn = li.querySelector("start-btn");
    startBtn.addEventListener("click", async () => {
        const token = localStorage.getItem("token");
        const challengeId = startBtn.dataset.id;

        const response = await fetch(`http://127.0.0.1:5000/challenges/${challengeId}/start`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            }
        });
        const result = await response.json();
        alert(result.message ||" Challenge started successfully!");
    })

    // Load Challenge Details
    if (challengeDetails) {
        const challengeId = window.location.pathname.split("/").pop();

        fetch(`http://127.0.0.1:5000/challenges/${challengeId}`, {
            method: "GET",
        })
        .then(res => {
            if (!res.ok) throw new Error("Erreur HTTP: " + res.status);
            return res.json();
        })
        .then(ch => {
            challengeDetails.innerHTML = `
                <h1 class="text-3xl font-bold text-green-400">${ch.title}</h1>
                <p class="text-gray-300 text-sm whitespace-pre-line">${ch.instructions}</p>
                `;
            })
            .catch(error => {
                challengeDetails.innerHTML = `<p class="text-red-500">Erreur de chargement du challenge.</p>`;
                console.error(error);
            });
    }
});
