(function () {
  function bindToggle(input) {
    if (!input || input.dataset.eyeBound === "1") return;

    input.dataset.eyeBound = "1";
    input.type = "password";

    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "button";
    btn.style.marginLeft = "8px";
    btn.setAttribute("aria-label", "Toggle API key visibility");
    btn.textContent = "\u{1F441}";

    btn.addEventListener("click", function () {
      var hidden = input.type === "password";
      input.type = hidden ? "text" : "password";
      btn.textContent = hidden ? "\u{1F576}" : "\u{1F441}";
    });

    input.parentNode.appendChild(btn);
  }

  function init() {
    var input = document.getElementById("id_openrouter_api_key");
    bindToggle(input);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
