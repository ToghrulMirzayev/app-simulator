document.addEventListener("DOMContentLoaded", async function () {
  const statusValue = document.getElementById("status-value");
  const statusInput = document.getElementById("status-input");
  const updateButton = document.querySelector("button");
  const phraseText = document.getElementById("phrase-text");

  async function fetchStatus() {
    try {
      const response = await fetch("/api/status");
      const data = await response.json();
      const status = data.status.toUpperCase();

      statusValue.textContent = status;

      statusValue.classList.remove("healthy", "warning", "bad");

      if (status === "HEALTHY") {
        statusValue.classList.add("healthy");
      } else if (status === "WARNING") {
        statusValue.classList.add("warning");
      } else if (status === "BAD") {
        statusValue.classList.add("bad");
      }
    } catch (error) {
      statusValue.textContent = "ERROR";
      statusValue.classList.add("bad");
      console.error("Failed to fetch status:", error);
    }
  }

  async function fetchUpdateEnabled() {
    try {
      const response = await fetch("/api/update-enabled");
      const data = await response.json();
      const isUpdateEnabled = data.is_update_enabled;
      statusInput.disabled = !isUpdateEnabled;
      updateButton.disabled = !isUpdateEnabled;
    } catch (error) {
      console.error("Failed to fetch update enabled status:", error);
    }
  }

  async function fetchNewPhrase() {
    try {
      const response = await fetch("/api/phrase-of-the-day");
      const data = await response.json();
      phraseText.innerText = data.phrase_of_the_day;
    } catch (error) {
      console.error("Failed to fetch phrase of the day:", error);
    }
  }

  await fetchStatus();
  await fetchUpdateEnabled();
  await fetchNewPhrase();

  window.updateStatus = async function () {
    const statusInputValue = statusInput.value;
    const status = parseInt(statusInputValue, 10);

    if (isNaN(status)) {
      console.error("Invalid input");
      return;
    }

    try {
      const response = await fetch("/api/status", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: status })
      });

      if (response.ok) {
        await fetchStatus();
      } else {
        console.error("Status update error");
      }
    } catch (error) {
      console.error("Status update error:", error);
    }
  };

  const themeToggle = document.getElementById("theme-toggle");

  if (localStorage.getItem("theme") === "dark") {
    document.body.classList.add("dark-theme");
    themeToggle.checked = true;
  }

  themeToggle.addEventListener("change", function () {
    if (themeToggle.checked) {
      document.body.classList.add("dark-theme");
      localStorage.setItem("theme", "dark");
    } else {
      document.body.classList.remove("dark-theme");
      localStorage.setItem("theme", "light");
    }
  });
});
