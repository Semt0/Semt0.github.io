// docs/javascripts/sakura-init.js
// 简易花瓣飘落效果，不依赖外部插件
(function () {
  var STARTED = false;
  var PETAL_COUNT = 18;

  function start() {
    if (STARTED) return;
    STARTED = true;

    var layer = document.createElement("div");
    layer.className = "petals-layer";

    for (var i = 0; i < PETAL_COUNT; i++) {
      var p = document.createElement("span");
      p.className = "petal";
      p.style.left = Math.random() * 100 + "vw";
      var duration = 10 + Math.random() * 6;   // 10–16s
      var delay = -Math.random() * duration;   // 负延迟打散初始位置
      p.style.animationDuration = duration + "s";
      p.style.animationDelay = delay + "s";
      layer.appendChild(p);
    }

    document.body.appendChild(layer);
  }

  // 适配 MkDocs/Zensical 的 SPA 导航
  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(function () {
      start();
    });
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();