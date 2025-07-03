document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("login-form");
  const error = document.getElementById("login-error");

  form.onsubmit = (e) => {
    e.preventDefault();

    const formData = new FormData(form);

    fetch("/login", {
      method: "POST",
      body: formData
    })
    .then(res => res.json())
    .then(data => {
      if (data.access_token) {
        localStorage.setItem("access_token", data.access_token);
        alert("Connexion réussie !");
        window.location.href = "/challenges/page";
      } else {
        error.textContent = data.error || "Erreur de connexion";
      }
    });
  };
});
