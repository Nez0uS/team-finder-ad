<script>
  document.addEventListener("DOMContentLoaded", () => {
    const isFavoritesPage = document.body.dataset.page === "favorites";

    document.querySelectorAll(".project-fav-icon").forEach(button => {
      button.addEventListener("click", async (e) => {
        e.preventDefault();

        const projectId = button.dataset.projectId;
        const isFav = button.dataset.fav === "true";
        const response = await fetch(`/projects/${projectId}/toggle-favorite/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
          },
          body: JSON.stringify({})
        });

        if (response.ok) {
          if (isFavoritesPage && isFav) {
            const card = button.closest(".project-card");
            card.remove();

            if (document.querySelectorAll(".project-card").length === 0) {
              const emptyBlock = document.querySelector("#empty-favorite-template");
              if (emptyBlock) {
                emptyBlock.style.display = "block";
              }
            }
          } else {
            if (isFav) {
              button.classList.remove("favorite");
              button.classList.add("not-favorite");
              button.dataset.fav = "false";
            } else {
              button.classList.remove("not-favorite");
              button.classList.add("favorite");
              button.dataset.fav = "true";
            }
          }
        } else {
          alert("Ошибка при обновлении избранного");
        }
      });
    });
  });

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
</script>
