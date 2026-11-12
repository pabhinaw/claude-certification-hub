/* Learner comments (giscus). Nothing is requested from giscus.app or GitHub
 * until the visitor clicks "Load comments". The only thing remembered is that
 * choice, in this browser, so the comments load automatically next time. */
(function () {
  "use strict";
  var KEY = "hub-comments-ok";
  function theme() {
    return document.body.getAttribute("data-md-color-scheme") === "slate" ? "dark" : "light";
  }
  function remembered() { try { return localStorage.getItem(KEY) === "1"; } catch (e) { return false; } }
  function remember() { try { localStorage.setItem(KEY, "1"); } catch (e) { /* ignore */ } }

  function load(gate, mount) {
    if (mount.dataset.loaded) return;
    mount.dataset.loaded = "1";
    var s = document.createElement("script");
    s.src = "https://giscus.app/client.js";
    s.async = true;
    s.crossOrigin = "anonymous";
    var a = {
      "data-repo": gate.dataset.repo, "data-repo-id": gate.dataset.repoId,
      "data-category": gate.dataset.category, "data-category-id": gate.dataset.categoryId,
      "data-mapping": "specific", "data-term": gate.dataset.term, "data-strict": "1",
      "data-reactions-enabled": "1", "data-emit-metadata": "0", "data-input-position": "top",
      "data-theme": theme(), "data-lang": "en", "data-loading": "lazy"
    };
    Object.keys(a).forEach(function (k) { s.setAttribute(k, a[k]); });
    mount.appendChild(s);
    gate.hidden = true;
  }

  function syncTheme() {
    var frame = document.querySelector("iframe.giscus-frame");
    if (!frame || !frame.contentWindow) return;
    frame.contentWindow.postMessage({ giscus: { setConfig: { theme: theme() } } }, "https://giscus.app");
  }

  function boot() {
    var gate = document.getElementById("hub-comments-gate");
    var mount = document.getElementById("hub-comments-mount");
    var btn = document.getElementById("hub-comments-load");
    if (!gate || !mount || !btn || gate.dataset.ready) return;
    gate.dataset.ready = "1";
    btn.addEventListener("click", function () { remember(); load(gate, mount); });
    if (remembered()) load(gate, mount);
    new MutationObserver(syncTheme).observe(document.body, { attributes: true, attributeFilter: ["data-md-color-scheme"] });
  }
  if (typeof document$ !== "undefined") document$.subscribe(boot);
  else document.addEventListener("DOMContentLoaded", boot);
})();
