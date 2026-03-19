// docs/javascripts/sakura-init.js
// 优化版花瓣飘落效果 - 提升性能
(function () {
  var STARTED = false;
  // 减少花瓣数量以提升性能
  var PETAL_COUNT = 18;
  var PETAL_COLORS = [
    "radial-gradient(circle at 30% 30%, #fecaca, #fb7185)",
    "radial-gradient(circle at 20% 25%, #ffe4e6, #fb7195)",
    "radial-gradient(circle at 35% 30%, #fee2e2, #f97373)",
    "radial-gradient(circle at 25% 35%, #fdf2f8, #f472b6)"
  ];

  // 检测是否为低性能设备
  function isLowPerformanceDevice() {
    // 检测移动设备或电池节能模式
    return window.matchMedia('(pointer: coarse)').matches ||
           (navigator.hardwareConcurrency && navigator.hardwareConcurrency <= 4);
  }

  function start() {
    if (STARTED) return;
    STARTED = true;

    // 低性能设备减少花瓣数量
    var count = isLowPerformanceDevice() ? 10 : PETAL_COUNT;

    var layer = document.createElement("div");
    layer.className = "petals-layer";
    // 使用 DocumentFragment 批量插入 DOM
    var fragment = document.createDocumentFragment();

    for (var i = 0; i < count; i++) {
      var p = document.createElement("span");
      p.className = "petal";
      p.style.left = Math.random() * 100 + "vw";
      var sizeScale = 0.7 + Math.random() * 0.55;
      p.style.width = (8 * sizeScale | 0) + "px";
      p.style.height = (12 * sizeScale | 0) + "px";

      var colorIndex = Math.floor(Math.random() * PETAL_COLORS.length);
      p.style.backgroundImage = PETAL_COLORS[colorIndex];
      // 错开动画时间，避免同时计算
      var duration = 15 + Math.random() * 10;
      var delay = -Math.random() * duration;
      p.style.animationDuration = duration + "s";
      p.style.animationDelay = delay + "s";
      // 随机水平漂移距离
      p.style.setProperty('--drift', (Math.random() * 60 - 30).toFixed(1) + 'px');
      fragment.appendChild(p);
    }

    layer.appendChild(fragment);
    document.body.appendChild(layer);
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