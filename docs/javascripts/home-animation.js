/* 首页性能优化：头像预加载 + 栏目动画 */
(function () {
  // ===== 头像预加载优化 =====
  (function preloadAvatar() {
    // 提前建立连接，减少 DNS 和 TCP 握手时间
    var linkPreconnect = document.createElement('link');
    linkPreconnect.rel = 'preconnect';
    linkPreconnect.href = 'https://github.com';
    linkPreconnect.crossOrigin = 'anonymous';
    document.head.appendChild(linkPreconnect);

    // 预加载头像图片
    var linkPreload = document.createElement('link');
    linkPreload.rel = 'preload';
    linkPreload.as = 'image';
    linkPreload.href = 'https://github.com/Semt0.png';
    linkPreload.type = 'image/png';
    document.head.appendChild(linkPreload);

    // 确保头像完全加载后再显示，防止露出背景色
    var avatarImg = document.querySelector('.home-avatar-img');
    if (avatarImg) {
      // 如果图片已经缓存完成，直接显示
      if (avatarImg.complete && avatarImg.naturalWidth > 0) {
        avatarImg.style.opacity = '1';
      } else {
        // 等待图片加载完成
        avatarImg.addEventListener('load', function() {
          avatarImg.style.opacity = '1';
        });
        // 加载失败时也显示（显示备用背景）
        avatarImg.addEventListener('error', function() {
          avatarImg.style.opacity = '1';
        });
      }
    }
  })();

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
