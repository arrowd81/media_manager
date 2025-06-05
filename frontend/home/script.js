function goToLogin() {
    window.location.href = "/login";
}

function goToSearch() {
    const query = document.getElementById("searchInput").value;
    window.location.href = "/search.html?q=" + encodeURIComponent(query);
}

async function fetchAnime() {
    try {
        const response = await fetch("/default_recommend");
        const data = await response.json();

        const animeList = document.getElementById("animeList");

        data.forEach(anime => {
            const card = document.createElement("div");
            card.className = "anime-card";

            card.innerHTML = `
        <img src="/pictures/${anime.image_path}" alt="${anime.main_name}" class="anime-img" />
        <div class="anime-title">${anime.main_name}</div>
      `;

            animeList.appendChild(card);
        });
    } catch (error) {
        console.error("Failed to fetch anime:", error);
    }
}

fetchAnime();
