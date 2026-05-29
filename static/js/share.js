// Global share button handler
// Works for any element with class="share-button" and optional data-url attribute

document.addEventListener("click", function (e) {
  const btn = e.target.closest(".share-button");
  if (!btn) return;

  e.preventDefault();

  const url = btn.dataset.url
    ? window.location.origin + btn.dataset.url
    : window.location.href;

  navigator.clipboard
    .writeText(url)
    .then(() => {
      if (window.toast) {
        window.toast("Ссылка скопирована: " + url, { type: 'info' });
      } else {
        alert("Ссылка скопирована: " + url);
      }
    })
    .catch((err) => {
      console.error("Ошибка копирования: ", err);
      fallbackCopyTextToClipboard(url);
    });
});

function fallbackCopyTextToClipboard(text) {
  try {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.setAttribute("readonly", "");
    textArea.style.position = "fixed";
    textArea.style.top = "-1000px";
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    const successful = document.execCommand("copy");
    document.body.removeChild(textArea);
    if (!successful) throw new Error("document.execCommand copy failed");
    if (window.toast) {
      window.toast("Ссылка скопирована: " + text, { type: 'info' });
    } else {
      alert("Ссылка скопирована: " + text);
    }
  } catch (err) {
    console.error("Ошибка копирования (fallback): ", err);
    window.prompt("Скопируйте ссылку:", text);
  }
}
