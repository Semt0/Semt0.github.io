/* 首页四个栏目：滚动进入视口时淡入 + 上移 - 性能优化版 */
(function () {
  // 存储已观察的元素，避免重复处理
  var observedElements = new WeakSet();

  function run() {
    var sections = document.querySelectorAll(".home-section");
    if (!sections.length) return;

    // 如果浏览器支持 prefers-reduced-motion，尊重用户设置
    var prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReducedMotion) {
      // 直接显示所有栏目，不使用动画
      sections.forEach(function (el) {
        el.classList.add("home-section-visible");
      });
      return;
    }

    var observerOptions = {
      // 提前一点淡入
      rootMargin: "0px 0px -10% 0px",
      threshold: 0.05, // 降低阈值减少触发次数
    };

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting && !observedElements.has(entry.target)) {
            entry.target.classList.add("home-section-visible");
            observedElements.add(entry.target);
            // 动画完成后取消观察，减少性能开销
            observer.unobserve(entry.target);
          }
        });
      },
      observerOptions
    );

    // 分批处理，避免阻塞主线程
    var i = 0;
    function processBatch() {
      var batchSize = 4; // 每批处理 4 个元素
      var end = Math.min(i + batchSize, sections.length);

      for (; i < end; i++) {
        var el = sections[i];
        // 初始状态添加硬件加速
        el.style.transform = "translateZ(0)";
        observer.observe(el);
      }

      if (i < sections.length) {
        requestAnimationFrame(processBatch);
      }
    }

    requestAnimationFrame(processBatch);
  }

  // 延迟执行，避免与首屏渲染冲突
  function scheduleRun() {
    if (typeof requestIdleCallback !== 'undefined') {
      requestIdleCallback(run, { timeout: 200 });
    } else {
      setTimeout(run, 100);
    }
  }

  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(scheduleRun);
  } else {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", scheduleRun);
    } else {
      scheduleRun();
    }
  }
})();
