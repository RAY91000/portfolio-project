document.addEventListener("DOMContentLoaded", () => {
  console.log("✅ app.js chargé");

  const pathname = window.location.pathname;
  const token = localStorage.getItem("access_token") || localStorage.getItem("token");
  const username = localStorage.getItem("username");

  const board = document.getElementById("board-button");
  const scene = document.getElementById("scene");
  const sound = document.getElementById("click-sound");
  const registerForm = document.getElementById("registerForm");
  const loginForm = document.getElementById("loginForm");
  const challengeList = document.getElementById("challengeList");
  const challengeDetails = document.getElementById("challengeDetails");
  const scrollWrapper = document.getElementById("scrollWrapper");
  const logoutBtn = document.getElementById("logoutBtn");
  const usernameDisplay = document.getElementById("usernameDisplay");
  const userBadge = document.getElementById("userBadge");
  const authButtons = document.getElementById("authButtons");

  if (authButtons && !token) {
    authButtons.classList.remove("hidden");
  }

  if (pathname === "/" || pathname === "/home.html") {
    if (board && scene) {
      board.addEventListener("click", (e) => {
        e.preventDefault();
        if (sound) {
          sound.volume = 1.0;
          sound.currentTime = 0;
          sound.play().catch(err => console.warn("Audio play error:", err));
        }
        scene.classList.add("zoom-out");
        setTimeout(() => window.location.href = board.href, 1000);
      });
    }
  }

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
      document.getElementById("registerMsg").innerText = response.ok ? "" : data.message || data.error;
      if (response.ok) window.location.href = "/login";
    });
  }

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
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("username", data.username);
        window.location.href = "/";
      } else {
        document.getElementById("loginMsg").innerText = data.message || data.error;
      }
    });
  }

  if (challengeList) {
    const difficultyIcons = {
      Easy: "🟢 Noob",
      Medium: "🟡 Medium",
      Hard: "🔴 Ranker"
    };

    fetch("http://127.0.0.1:5000/challenges/")
      .then(res => res.json())
      .then(data => {
        data.forEach(challenge => {
          const li = document.createElement("li");
          li.className = "bg-white/10 text-white border border-green-400 rounded-lg p-6 shadow-lg transition-all duration-300 hover:scale-105 hover:shadow-green-500";
          li.innerHTML = `
            <div class="flex justify-between items-start">
              <div>
                <h3 class="text-2xl font-bold text-green-400 mb-1">${challenge.title}</h3>
                <p class="text-sm text-gray-300 mb-2">${challenge.description}</p>
                <p class="text-sm text-yellow-300">
                  🧐 Category: ${challenge.category || "Unknown"}<br>
                  💀 Difficulty: ${difficultyIcons[challenge.difficulty] || challenge.difficulty || "Unknown"}
                </p>
              </div>
              <div class="flex flex-col gap-2 text-sm">
                <a href="/challenge/${challenge.id}" class="bg-blue-600 text-white px-3 py-2 rounded hover:bg-blue-700 text-center">🔍 View</a>
                <button class="start-btn bg-pink-600 text-white px-3 py-2 rounded hover:bg-pink-700" data-id="${challenge.id}">🌹 Start</button>
              </div>
            </div>
          `;

          challengeList.appendChild(li);

          const startBtn = li.querySelector(".start-btn");
          startBtn?.addEventListener("click", async () => {
            if (!token) {
              alert("Veuillez vous connecter pour lancer un challenge.");
              window.location.href = "/login";
              return;
            }

            const res = await fetch(`http://127.0.0.1:5000/challenges/${challenge.id}/start`, {
              method: "POST",
              headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
              }
            });

            const result = await res.json();

            if (res.ok && result.guacamole_url) {
              window.open(result.guacamole_url, "_blank");
            } else {
              alert(result.message || "❌ Erreur lors du lancement du challenge.");
            }
          });
        });

        updateFadeEffect();
      })
      .catch(error => {
        challengeList.innerHTML = `<li class="text-red-500">❌ Erreur de chargement : ${error.message}</li>`;
        console.error(error);
      });
  }

  if (challengeDetails) {
    const id = pathname.split("/").pop();
    fetch(`http://127.0.0.1:5000/challenges/${id}`)
      .then(res => res.json())
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

  if (logoutBtn) {
    if (!token) {
      logoutBtn.classList.add("hidden");
    } else {
      logoutBtn.classList.remove("hidden");
      logoutBtn.addEventListener("click", () => {
        localStorage.removeItem("token");
        localStorage.removeItem("access_token");
        localStorage.removeItem("username");
        window.location.href = "/";
      });
    }
  }

  if (usernameDisplay && userBadge) {
    if (username) {
      usernameDisplay.textContent = ` ${username}`;
      userBadge.classList.remove("hidden");
    } else {
      userBadge.classList.add("hidden");
    }
  }

  function updateFadeEffect() {
    if (!challengeList || !scrollWrapper) return;
    const wrapperRect = scrollWrapper.getBoundingClientRect();
    const centerY = wrapperRect.top + wrapperRect.height / 2;
    const maxDistance = wrapperRect.height / 2;

    const items = challengeList.querySelectorAll("li");
    items.forEach(item => {
      const itemRect = item.getBoundingClientRect();
      const itemCenter = itemRect.top + itemRect.height / 2;
      const distance = Math.abs(centerY - itemCenter);
      const opacity = 1 - Math.min(distance / maxDistance, 1);
      item.style.opacity = opacity.toFixed(2);
    });
  }

  if (scrollWrapper) {
    scrollWrapper.addEventListener("scroll", updateFadeEffect);
    window.addEventListener("resize", updateFadeEffect);
    const observer = new MutationObserver(updateFadeEffect);
    observer.observe(challengeList, { childList: true });
  }
});
