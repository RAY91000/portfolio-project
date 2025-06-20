document.addEventListener("DOMContentLoaded", () => {
  // ✅ Home page zoom + sound
  if (window.location.pathname === "/" || window.location.pathname === "/home.html") {
    const board = document.getElementById("board-button");
    const scene = document.getElementById("scene");
    const sound = document.getElementById("click-sound");

    if (board && scene) {
      board.addEventListener("click", function (e) {
        e.preventDefault();
        if (sound) {
          sound.volume = 1.0;
          sound.currentTime = 0;
          sound.play().catch(err => console.warn("Audio play error:", err));
        }
        scene.classList.add("zoom-out");
        setTimeout(() => {
          window.location.href = board.href;
        }, 1000);
      });
    }
  }

  const registerForm = document.getElementById("registerForm");
  const loginForm = document.getElementById("loginForm");
  const challengeList = document.getElementById("challengeList");
  const challengeDetails = document.getElementById("challengeDetails");
  const scrollWrapper = document.getElementById("scrollWrapper");

  // ✅ Register
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

  // ✅ Login
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

  // ✅ Load Challenges
  if (challengeList) {
    const difficultyIcons = {
      "Easy": "🟢 Noob",
      "Medium": "🟡 Medium",
      "Hard": "🔴 Ranker"
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
                <a href="/challenge/${challenge.id}" class="bg-blue-600 text-white px-3 py-2 rounded hover:bg-blue-700 text-center">
                  🔍 View
                </a>
                <button class="start-btn bg-pink-600 text-white px-3 py-2 rounded hover:bg-pink-700" data-id="${challenge.id}">
                  🌹 Start
                </button>
              </div>
            </div>
          `;
          challengeList.appendChild(li);

          const startBtn = li.querySelector(".start-btn");
          if (startBtn) {
            startBtn.addEventListener("click", async () => {
              const token = localStorage.getItem("token");
              if (!token) {
                alert("Please log in to start the challenge.");
                window.location.href = "/login";
                return;
              }

              const response = await fetch(`http://127.0.0.1:5000/challenges/${challenge.id}/start`, {
                method: "POST",
                headers: {
                  "Authorization": `Bearer ${token}`,
                  "Content-Type": "application/json"
                }
              });

              const result = await response.json();
              alert(result.message || "Challenge started successfully!");
            });
          }
        });

        updateFadeEffect();
      })
      .catch(error => {
        challengeList.innerHTML = `<li class="text-red-500">❌ Failed to load challenges: ${error.message}</li>`;
        console.error(error);
      });
  }

  // ✅ Challenge Detail View
  if (challengeDetails) {
    const id = window.location.pathname.split("/").pop();
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

  // ✅ Logout button
  const logoutBtn = document.getElementById("logoutBtn");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", () => {
      localStorage.removeItem("token");
      localStorage.removeItem("username");
      window.location.href = "/login";
    });
  }

  // ✅ Show username if logged in
  const usernameDisplay = document.getElementById("usernameDisplay");
  const userBadge = document.getElementById("userBadge");
  if (usernameDisplay && userBadge) {
    const username = localStorage.getItem("username");
    if (username) {
      usernameDisplay.textContent = ` ${username}`;
      userBadge.classList.remove("hidden");
    } else {
      userBadge.classList.add("hidden");
    }
  }

  // ✅ Fade effect
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
