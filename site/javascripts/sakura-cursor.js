(function () {
  var STORAGE_KEY = "__sakura_cursor_enabled";
  var state = {
    initialized: false,
    layer: null,
    lastTrailAt: 0,
    lastX: 0,
    lastY: 0,
    listenersBound: false,
    enabled: true,
    toggleButton: null
  };

  var TRAIL_INTERVAL = 52;
  var MIN_MOVE_DISTANCE = 12;
  var MAX_NODES = 36;

  function prefersReducedMotion() {
    return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  }

  function readStoredEnabled() {
    try {
      var raw = window.localStorage.getItem(STORAGE_KEY);
      return raw == null ? true : raw !== "0";
    } catch (e) {
      return true;
    }
  }

  function persistEnabled(enabled) {
    try {
      window.localStorage.setItem(STORAGE_KEY, enabled ? "1" : "0");
    } catch (e) {}
  }

  function isLowPerformance() {
    return window.matchMedia("(pointer: coarse)").matches ||
      (navigator.hardwareConcurrency && navigator.hardwareConcurrency <= 4);
  }

  function ensureLayer() {
    if (state.layer && document.body.contains(state.layer)) return state.layer;

    var layer = document.querySelector(".sakura-cursor-layer");
    if (!layer) {
      layer = document.createElement("div");
      layer.className = "sakura-cursor-layer";
      document.body.appendChild(layer);
    }

    state.layer = layer;
    return layer;
  }

  function clearEffects() {
    var layer = ensureLayer();
    layer.innerHTML = "";
  }

  function syncToggleButton() {
    if (!state.toggleButton) return;
    var enabled = state.enabled;
    var label = enabled ? "关闭鼠标特效" : "开启鼠标特效";
    state.toggleButton.classList.toggle("is-active", enabled);
    state.toggleButton.setAttribute("aria-pressed", enabled ? "true" : "false");
    state.toggleButton.setAttribute("title", label);
    state.toggleButton.setAttribute("aria-label", label);
  }

  function setEnabled(enabled) {
    state.enabled = !!enabled;
    persistEnabled(state.enabled);
    if (!state.enabled) clearEffects();
    syncToggleButton();
  }

  function createToggleButton() {
    var button = document.createElement("label");
    button.className = "md-header__button md-icon sakura-cursor-toggle";
    button.setAttribute("role", "button");
    button.setAttribute("tabindex", "0");
    button.innerHTML =
      '<svg viewBox="0 0 24 24" aria-hidden="true">' +
        '<path d="M9.5 2.8 10.7 6a2 2 0 0 0 1.2 1.2l3.2 1.2-3.2 1.2a2 2 0 0 0-1.2 1.2l-1.2 3.2-1.2-3.2a2 2 0 0 0-1.2-1.2L3.9 8.4l3.2-1.2A2 2 0 0 0 8.3 6z"></path>' +
        '<path d="M17.2 13.8 18 16a1.4 1.4 0 0 0 .8.8l2.2.8-2.2.8a1.4 1.4 0 0 0-.8.8l-.8 2.2-.8-2.2a1.4 1.4 0 0 0-.8-.8l-2.2-.8 2.2-.8a1.4 1.4 0 0 0 .8-.8z"></path>' +
      '</svg>';
    button.addEventListener("click", function (event) {
      event.preventDefault();
      setEnabled(!state.enabled);
    });
    button.addEventListener("keydown", function (event) {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        setEnabled(!state.enabled);
      }
    });
    return button;
  }

  function ensureToggleButton() {
    var palette = document.querySelector('form.md-header__option[data-md-component="palette"]');
    if (!palette || !palette.parentNode) return;

    var existing = document.querySelector(".sakura-cursor-toggle");
    if (existing) {
      state.toggleButton = existing;
      syncToggleButton();
      return;
    }

    var button = createToggleButton();
    palette.parentNode.insertBefore(button, palette);
    state.toggleButton = button;
    syncToggleButton();
  }

  function trimNodes() {
    var layer = ensureLayer();
    while (layer.childNodes.length > MAX_NODES) {
      layer.removeChild(layer.firstChild);
    }
  }

  function spawnPetal(x, y, mode) {
    var layer = ensureLayer();
    var petal = document.createElement("span");
    var angle = Math.random() * Math.PI * 2;
    var distance = mode === "burst"
      ? 18 + Math.random() * 34
      : 8 + Math.random() * 12;
    var driftX = Math.cos(angle) * distance;
    var driftY = Math.sin(angle) * distance + (mode === "burst" ? 10 : -8);
    var rotation = (Math.random() * 120 - 60).toFixed(1) + "deg";
    var scale = (0.72 + Math.random() * 0.5).toFixed(2);

    petal.className = "sakura-cursor-petal " + (mode === "burst" ? "is-burst" : "is-trail");
    petal.style.left = x.toFixed(1) + "px";
    petal.style.top = y.toFixed(1) + "px";
    petal.style.setProperty("--tx", driftX.toFixed(1) + "px");
    petal.style.setProperty("--ty", driftY.toFixed(1) + "px");
    petal.style.setProperty("--rotate", rotation);
    petal.style.setProperty("--scale", scale);
    petal.style.opacity = mode === "burst" ? "0.78" : "0.56";

    layer.appendChild(petal);
    petal.addEventListener("animationend", function () {
      petal.remove();
    }, { once: true });
  }

  function spawnBloom(x, y) {
    var layer = ensureLayer();
    var bloom = document.createElement("span");
    bloom.className = "sakura-cursor-bloom";
    bloom.style.left = x.toFixed(1) + "px";
    bloom.style.top = y.toFixed(1) + "px";
    layer.appendChild(bloom);
    bloom.addEventListener("animationend", function () {
      bloom.remove();
    }, { once: true });
  }

  function onPointerMove(event) {
    if (!state.enabled || prefersReducedMotion()) return;

    var now = performance.now();
    var dx = event.clientX - state.lastX;
    var dy = event.clientY - state.lastY;
    var distance = Math.sqrt(dx * dx + dy * dy);

    if (now - state.lastTrailAt < TRAIL_INTERVAL || distance < MIN_MOVE_DISTANCE) {
      return;
    }

    state.lastTrailAt = now;
    state.lastX = event.clientX;
    state.lastY = event.clientY;

    spawnPetal(event.clientX, event.clientY, "trail");
    trimNodes();
  }

  function onPointerDown(event) {
    if (!state.enabled || prefersReducedMotion()) return;

    var burstCount = isLowPerformance() ? 4 : 7;
    spawnBloom(event.clientX, event.clientY);

    for (var i = 0; i < burstCount; i++) {
      spawnPetal(event.clientX, event.clientY, "burst");
    }

    trimNodes();
  }

  function bindEvents() {
    if (state.listenersBound) return;
    state.listenersBound = true;
    window.addEventListener("pointermove", onPointerMove, { passive: true });
    window.addEventListener("pointerdown", onPointerDown, { passive: true });
  }

  function start() {
    state.enabled = readStoredEnabled();
    ensureLayer();
    ensureToggleButton();
    bindEvents();
    state.initialized = true;
  }

  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(start);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
