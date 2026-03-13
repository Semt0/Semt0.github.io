// docs/javascripts/sakura-init.js
// 简易花瓣飘落效果，不依赖外部插件
(function () {
  var STARTED = false;
  var PETAL_COUNT = 32; // 稍微多一点
  var PETAL_COLORS = [
    "radial-gradient(circle at 30% 30%, #fecaca, #fb7185)", // 标准粉
    "radial-gradient(circle at 20% 25%, #ffe4e6, #fb7195)", // 偏淡粉
    "radial-gradient(circle at 35% 30%, #fee2e2, #f97373)", // 带一点红
    "radial-gradient(circle at 25% 35%, #fdf2f8, #f472b6)"  // 偏樱花粉
  ];

  function start() {
    if (STARTED) return;
    STARTED = true;

    var layer = document.createElement("div");
    layer.className = "petals-layer";

    for (var i = 0; i < PETAL_COUNT; i++) {
      var p = document.createElement("span");
      p.className = "petal";
      p.style.left = Math.random() * 100 + "vw";
      // 随机尺寸：基础 0.7 ~ 1.25 倍
      var sizeScale = 0.7 + Math.random() * 0.55;
      p.style.width = 8 * sizeScale + "px";
      p.style.height = 12 * sizeScale + "px";

      // 随机挑选一种渐变色，制造颜色细微变化
      var colorIndex = Math.floor(Math.random() * PETAL_COLORS.length);
      p.style.backgroundImage = PETAL_COLORS[colorIndex];
      var duration = 12 + Math.random() * 8;   // 12–20s，慢一点
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