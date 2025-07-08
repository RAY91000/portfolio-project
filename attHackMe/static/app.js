document.addEventListener("DOMContentLoaded", () => {
  console.log("✅ app.js chargé");

  const pathname = window.location.pathname;
  const token = localStorage.getItem("access_token") || localStorage.getItem("token");
  const username = localStorage.getItem("username");

  const board = document.getElementById("board-button");
  const scene = document.getElementById("scene");
  const sound = document.getElementById("click-sound");
  const registerForm = document.getElementById("registerForm");
  const challengeList = document.getElementById("challengeList");
  const challengeDetails = document.getElementById("challengeDetails");
  const scrollWrapper = document.getElementById("scrollWrapper");
  const logoutBtn = document.getElementById("logoutBtn");
  const usernameDisplay = document.getElementById("usernameDisplay");
  const userBadge = document.getElementById("userBadge");
  const authButtons = document.getElementById("authButtons");

  // 👋 Affiche Register/Login uniquement si l’utilisateur n’est PAS connecté
  if (authButtons && !token) {
    authButtons.classList.remove("hidden");
  }

    
  // 🎮 Page d'accueil : zoom et son
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

  // 📝 Formulaire d'inscription avec vérification UX du mot de passe
  const registerFormEl = document.getElementById("registerForm");

  if (registerFormEl) {
    registerFormEl.addEventListener("submit", async (e) => {
      e.preventDefault();

      const formData = new FormData(e.target);
      const password = formData.get("password");

      // 🔐 Vérifie la complexité du mot de passe
      const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$/;

      if (!passwordPattern.test(password)) {
        alert(
          "Le mot de passe doit contenir au moins 8 caractères, avec une majuscule, une minuscule, un chiffre et un caractère spécial."
        );
        return;
      }

      // ✅ Mot de passe valide, envoie la requête
      const response = await fetch("http://127.0.0.1:5000/register", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();

      if (response.ok) {
        alert(result.message);
        window.location.href = "/verify_email";
      } else {
        alert(result.error || "Erreur lors de l'inscription.");
      }
    });
  }




  // 🔐 Formulaire de connexion
    const loginForm = document.getElementById("loginForm");
    console.log("Form trouvé ?", loginForm);

    if (loginForm) {
      loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const formData = new FormData(loginForm);

        try {
          const response = await fetch("http://127.0.0.1:5000/login", {
            method: "POST",
            body: formData,
            cache: "no-store"
          });

          const data = await response.json();
          console.log("Login response:", data);

          if (data.access_token) {
            localStorage.setItem("token", data.access_token);
            localStorage.setItem("username", data.username);
            window.location.href = "/";
          } else {
            document.getElementById("loginMsg").innerText = data.message || data.error;
          }
        } catch (err) {
          console.error("Erreur lors de la requête :", err);
          document.getElementById("loginMsg").innerText = "Erreur réseau lors de la connexion.";
        }
      });
    }



  // 🧠 Affichage des challenges
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
              ${token ? `<button class="kali-btn bg-green-600 text-white px-3 py-2 rounded hover:bg-green-700" data-id="${challenge.id}">🔓 VM Kali</button>` : ""}
            </div>
          </div>
        `;

        challengeList.appendChild(li);

        // 🎯 Start challenge
        const startBtn = li.querySelector(".start-btn");
        startBtn?.addEventListener("click", async () => {
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

          if (response.ok) {
            window.open(`/start.html/${challenge.id}`, "_blank");
          } else {
            alert(result.message || "An error occurred.");
          }
        });


        // 🔓 Lancer VM Kali
        const kaliBtn = li.querySelector(".kali-btn");
        kaliBtn?.addEventListener("click", async () => {
          const response = await fetch("http://127.0.0.1:5000/start", {
            method: "POST",
            headers: {
              Authorization: `Bearer ${token}`
            }
          });

          const data = await response.json();
          if (data.guacamole_url) {
            window.open(data.guacamole_url, "_blank");
          } else {
            alert("Erreur de lancement de la VM Kali.");
          }
        });
      });

      updateFadeEffect();
    })
    .catch(error => {
      challengeList.innerHTML = `<li class="text-red-500">❌ Failed to load challenges: ${error.message}</li>`;
      console.error(error);
    });
}


  // 📄 Détail d’un challenge
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

  // 🔚 Déconnexion
  if (logoutBtn) {
    const token = localStorage.getItem("token") || localStorageStorage.getItem("access_token");
    if (!token) {
      logoutBtn.classList.add("hidden"); // Masquer le bouton si non connecté
    } else {
      logoutBtn.classList.remove("hidden"); // Afficher le bouton si connecté
      logoutBtn.addEventListener("click", () => {
        localStorage.removeItem("token");
        localStorage.removeItem("access_token");
        localStorage.removeItem("username");
        window.location.href = "/";
      });
    }
  }

  // 👤 Affichage de l’utilisateur connecté
  if (usernameDisplay && userBadge) {
    if (username) {
      usernameDisplay.textContent = ` ${username}`;
      userBadge.classList.remove("hidden");
    } else {
      userBadge.classList.add("hidden");
    }
  }

  // Sélection de soldat
    const soldierList = [
    "soldat1.png",
    "soldat2.png",
    "soldat3.png"
  ];

  let currentIndex = parseInt(localStorage.getItem("selectedSoldierIndex")) || 0;

  const soldierImage = document.getElementById("soldierImage");
  const nextBtn = document.getElementById("nextSoldierBtn");

  if (soldierImage) {
    soldierImage.src = `/static/images/soldiers/${soldierList[currentIndex]}`;
  }

  if (nextBtn && soldierImage) {
    nextBtn.addEventListener("click", () => {
      currentIndex = (currentIndex + 1) % soldierList.length;
      localStorage.setItem("selectedSoldierIndex", currentIndex);
      soldierImage.src = `/static/images/soldiers/${soldierList[currentIndex]}`;
    });
  }


  // 🎨 Effet de fondu des challenges
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

  // 🛠️ Paramètres utilisateur (settings.html)
  if (document.getElementById("page-settings")) {
    loadProfileData();
  }

  // 👤 Chargement des infos du profil (profile.html uniquement)
  if (window.location.pathname === "/profile.html") {
    const token = localStorage.getItem("access_token") || localStorage.getItem("token");
    if (!token) {
      window.location.href = "/login";
      return;
    }

    fetch("/profileview", {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
      .then(res => res.json())
      .then(user => {
        console.log("✅ Données profil chargées :", user);

        document.getElementById("usernameDisplay").textContent = user.username;

        if (user.email) {
          document.getElementById("userEmail").textContent = user.email;
        }

        if (user.avatar) {
          document.getElementById("current-avatar").src = `/static/images/avatars/${user.avatar}`;
        }

        if (user.banner) {
          document.getElementById("current-banner").src = `/static/images/banners/${user.banner}`;
        }

        document.getElementById("userBadge")?.classList.remove("hidden");
      })
      .catch(err => {
        console.error("❌ Erreur de chargement profil :", err);
      });
  }

});


function loadProfileData() {
  console.log("✅ Fonction loadProfileData appelée");

  const avatarList = ["avatar1.png", "avatar2.png", "avatar3.png", "avatar4.png"];
  const bannerList = ["banner1.jpg", "banner2.jpg", "banner3.jpg", "banner4.jpg"];

  const baseAvatarPath = "/static/images/avatars/";
  const baseBannerPath = "/static/images/banners/";

  let selectedAvatar = null;
  let selectedBanner = null;

  const avatarContainer = document.getElementById("avatar-list");
  const bannerContainer = document.getElementById("banner-list");

  const currentAvatar = document.getElementById("current-avatar");
  const currentBanner = document.getElementById("current-banner");
  const emailPublicCheckbox = document.getElementById("email_public");
  const messageBox = document.getElementById("settings-message");

  function populateSelection(container, list, type, selectedValue) {
    console.log(`🧩 populateSelection pour ${type}, valeur sélectionnée: ${selectedValue}`);
    container.innerHTML = "";

    list.forEach(imgName => {
      const img = document.createElement("img");
      img.src = (type === "avatar" ? baseAvatarPath : baseBannerPath) + imgName;
      img.classList.add(type === "avatar" ? "avatar-option" : "banner-option");
      img.width = type === "avatar" ? 80 : 160;
      img.height = type === "avatar" ? 80 : 90;

      if (imgName === selectedValue) img.classList.add("selected");

      img.onclick = () => {
        document.querySelectorAll("." + (type === "avatar" ? "avatar-option" : "banner-option"))
          .forEach(el => el.classList.remove("selected"));
        img.classList.add("selected");

        if (type === "avatar") {
          selectedAvatar = imgName;
          currentAvatar.src = baseAvatarPath + imgName;
          avatarContainer.classList.add("hidden");
        } else {
          selectedBanner = imgName;
          currentBanner.src = baseBannerPath + imgName;
          bannerContainer.classList.add("hidden");
        }
      };

      container.appendChild(img);
    });
  }

  currentAvatar?.addEventListener("click", () => {
    console.log("clic sur avatar");
    avatarContainer?.classList.toggle("hidden");
  });

  currentBanner?.addEventListener("click", () => {
    bannerContainer?.classList.toggle("hidden");
  });

  const token = localStorage.getItem("access_token") || localStorage.getItem("token");
  if (!token) return;

  fetch("/profileview", {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
    .then(res => res.json())
    .then(user => {
      console.log("donnée user :", user);
      selectedAvatar = user.avatar || avatarList[0];
      selectedBanner = user.banner || bannerList[0];

      currentAvatar.src = baseAvatarPath + selectedAvatar;
      currentBanner.src = baseBannerPath + selectedBanner;

      emailPublicCheckbox.checked = user.show_email || false;

      populateSelection(avatarContainer, avatarList, "avatar", selectedAvatar);
      populateSelection(bannerContainer, bannerList, "banner", selectedBanner);
    })
    .catch(err => console.error("Erreur lors du chargement du profil:", err));

  const settingsForm = document.getElementById("settings-form");
  settingsForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email_public = emailPublicCheckbox.checked;

    const res = await fetch("/settings", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({
        avatar: selectedAvatar,
        banner: selectedBanner,
        email_public
      })
    });

    const data = await res.json();

    if (res.ok) {
      messageBox.textContent = "✅ Paramètres mis à jour.";
      messageBox.className = "text-green-400 text-sm mt-2 text-center";
    } else {
      messageBox.textContent = data.error || "❌ Erreur inconnue.";
      messageBox.className = "text-red-400 text-sm mt-2 text-center";
    }
  });
}