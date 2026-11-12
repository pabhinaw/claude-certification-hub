// Shows a greeting based on the visitor's local time of day.
// Runs entirely in the browser: nothing is stored or sent anywhere.
(function () {
  function greet() {
    var el = document.getElementById("hub-greeting");
    if (!el) return;
    var h = new Date().getHours();
    var text;
    if (h >= 5 && h < 12)       text = "Good morning";
    else if (h >= 12 && h < 17) text = "Good afternoon";
    else if (h >= 17 && h < 22) text = "Good evening";
    else                        text = "Studying late? Good luck";
    el.textContent = text;
  }
  if (typeof document$ !== "undefined") {
    document$.subscribe(greet);            // works with Material's page loading
  } else {
    document.addEventListener("DOMContentLoaded", greet);
  }
})();
