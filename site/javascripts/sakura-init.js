// docs/javascripts/sakura-init.js
// 3D 层次花瓣飘落效果 — 逼真樱花瓣
(function () {
  var STARTED = false;
  var PETAL_COUNT = 20;

  // 仿真樱花渐变：白芯 → 粉 → 深粉边缘
  var PETAL_COLORS = [
    "radial-gradient(circle at 30% 25%, #fff 5%, #fce4ec 30%, #f8bbd0 70%, #f48fb1)",
    "radial-gradient(circle at 35% 30%, #fff5f5 5%, #fecdd3 35%, #fda4af 75%, #fb7185)",
    "radial-gradient(circle at 25% 20%, #fff 8%, #ffe4e6 40%, #fecaca 70%, #fca5a5)",
    "radial-gradient(circle at 30% 30%, #fff1f2 5%, #fce7f3 35%, #f9a8d4 70%, #f472b6)",
    "radial-gradient(circle at 40% 25%, #fff 10%, #fdf2f8 35%, #fbcfe8 65%, #f9a8d4)"
  ];

  var SHAPES = ["petal--shape-a", "petal--shape-b"];

  // 三层深度：近景、中景、远景
  var LAYERS = [
    { cls: "petal--near", weight: 0.2, dur: [12, 16], drift: 90, swing: 40 },
    { cls: "petal--mid",  weight: 0.5, dur: [18, 25], drift: 60, swing: 30 },
    { cls: "petal--far",  weight: 0.3, dur: [25, 35], drift: 35, swing: 16 }
  ];

  function isLowPerformance() {
    return window.matchMedia("(prefers-reduced-motion: reduce)").matches ||
           window.matchMedia("(pointer: coarse)").matches ||
           (navigator.hardwareConcurrency && navigator.hardwareConcurrency <= 4);
  }

  function pickLayer() {
    var r = Math.random();
    if (r < LAYERS[0].weight) return LAYERS[0];
    if (r < LAYERS[0].weight + LAYERS[1].weight) return LAYERS[1];
    return LAYERS[2];
  }

  function start() {
    if (STARTED) return;
    STARTED = true;

    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    var count = isLowPerformance() ? 10 : PETAL_COUNT;
    var container = document.createElement("div");
    container.className = "petals-layer";
    var frag = document.createDocumentFragment();

    for (var i = 0; i < count; i++) {
      var L = pickLayer();
      var shape = SHAPES[Math.random() * SHAPES.length | 0];
      var p = document.createElement("span");
      p.className = "petal " + L.cls + " " + shape;
      p.style.left = Math.random() * 100 + "vw";
      p.style.backgroundImage = PETAL_COLORS[Math.random() * PETAL_COLORS.length | 0];

      // 随机选择两种 3D 翻转动画之一
      p.style.animationName = Math.random() > 0.5 ? "petal-3d-a" : "petal-3d-b";

      var dur = L.dur[0] + Math.random() * (L.dur[1] - L.dur[0]);
      p.style.animationDuration = dur.toFixed(1) + "s";
      p.style.animationDelay = (-Math.random() * dur).toFixed(1) + "s";

      // 随机漂移与摇摆幅度
      p.style.setProperty("--drift", (Math.random() * L.drift * 2 - L.drift).toFixed(1) + "px");
      p.style.setProperty("--swing", (Math.random() * L.swing).toFixed(1) + "px");

      frag.appendChild(p);
    }

    container.appendChild(frag);
    document.body.appendChild(container);
  }

  // 适配 MkDocs/Zensical 的 SPA 导航
  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(start);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
