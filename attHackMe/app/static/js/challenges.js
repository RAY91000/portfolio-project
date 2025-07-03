document.addEventListener('DOMContentLoaded', () => {
  const token = localStorage.getItem('access_token');

  const challengeList = document.getElementById('challenge-list');
  const detailsDiv = document.getElementById('challenge-details');
  const title = document.getElementById('challenge-title');
  const description = document.getElementById('challenge-description');
  const ip = document.getElementById('challenge-ip');
  const flagInput = document.getElementById('flag-input');
  const result = document.getElementById('submission-result');
  const submitBtn = document.getElementById('submit-flag');
  const startKaliBtn = document.getElementById('start-kali');

  let currentChallengeId = null;

  fetch('/challenges/')
    .then(res => res.json())
    .then(challenges => {
      challenges.forEach(challenge => {
        const li = document.createElement('li');
        li.textContent = `${challenge.title} (${challenge.difficulty})`;
        li.style.cursor = 'pointer';
        li.onclick = () => startChallenge(challenge.id);
        challengeList.appendChild(li);
      });
    });

  function startChallenge(id) {
    if (!token) {
      alert("Connecte-toi d'abord !");
      return;
    }

    fetch(`/challenges/start/${id}`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    .then(res => res.json())
    .then(data => {
      if (data.error) return alert("❌ " + data.error);

      currentChallengeId = id;
      detailsDiv.style.display = 'block';
      title.textContent = data.title;
      description.textContent = data.description;
      ip.textContent = data.ip;
      result.textContent = '';
    });
  }

  submitBtn.onclick = () => {
    if (!currentChallengeId || !flagInput.value) return;

    fetch('/submissions/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        challenge_id: currentChallengeId,
        flag_submitted: flagInput.value
      })
    })
    .then(res => res.json())
    .then(data => {
      result.textContent = data.message;
    });
  };

  startKaliBtn.onclick = () => {
    console.log("🟢 Bouton Kali cliqué");
    if (!token) {
      alert("Connecte-toi ou cré d'abord !");
      return;
    }

    // Redirection directe vers le reverse proxy
    window.open("http://localhost:8090/", "_blank");
  };
});
