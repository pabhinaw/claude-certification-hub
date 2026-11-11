// Shows a greeting based on the visitor's local time of day.
// Runs entirely in the browser: nothing is stored or sent anywhere.
(function () {
  function greet() {
    var el = document.getElementById("hub-greeting");
    if (!el) return;
    var h = new Date().getHours();
    var text;
    if (h >= 5 && h < 12)       text = "☀️  Good morning, learner. Fresh mind, perfect time to study.";
    else if (h >= 12 && h < 17) text = "🌤️  Good afternoon, learner. Ready for your next topic?";
    else if (h >= 17 && h < 21) text = "🌆  Good evening, learner. Let's make today's study count.";
    else                        text = "🌙  Burning the midnight oil? Welcome, learner.";
    el.textContent = text;
  }
  if (typeof document$ !== "undefined") {
    document$.subscribe(greet);            // works with Material's page loading
  } else {
    document.addEventListener("DOMContentLoaded", greet);
  }
})();
