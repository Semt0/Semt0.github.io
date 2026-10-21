(function () {
  var walineInstance = null;
  var walineModulePromise = null;
  var navigationId = 0;

  function loadWaline(url) {
    if (!walineModulePromise) {
      walineModulePromise = import(url)
        .catch(function (err) {
          walineModulePromise = null;
          throw err;
        });
    }
    return walineModulePromise;
  }

  function logError(message, err) {
    if (typeof console !== 'undefined' && console.error) {
      console.error('[Waline] ' + message, err);
    }
  }

  function run() {
    var currentNavigation = ++navigationId;
    var el = document.getElementById("waline");

    // 销毁旧实例
    if (walineInstance) {
      if (typeof walineInstance.destroy === 'function') {
        try {
          walineInstance.destroy();
        } catch (e) {
          logError('Failed to destroy previous Waline instance', e);
        }
      }
      walineInstance = null;
    }

    if (!el) return;
    var path = el.dataset.commentPath || window.location.pathname;

    // 避免站点的全局 KaTeX 自动扫描误处理评论区内容。
    el.classList.add("katex-ignore");

    // 清空残留内容，确保干净初始化
    el.innerHTML = "";

    function doInit(mod) {
      // A module download may finish after instant navigation has replaced
      // the page (including a page with comments disabled).
      if (currentNavigation !== navigationId ||
          el !== document.getElementById("waline")) return;
      var walineOptions = {
        el: el,
        serverURL: "https://my-waline-eta-beige.vercel.app",
        path: path,
        lang: "zh-CN",
        dark: '[data-md-color-scheme="slate"]',
      };

      // 显式复用页面已加载的 KaTeX，确保评论区公式渲染稳定一致。
      if (window.katex && typeof window.katex.renderToString === "function") {
        walineOptions.texRenderer = function (blockMode, tex) {
          return window.katex.renderToString(tex, {
            displayMode: blockMode,
            throwOnError: false,
            strict: "ignore",
          });
        };
      }

      try {
        walineInstance = mod.init(walineOptions);
      } catch (e) {
        logError('Failed to initialize Waline', e);
      }
    }

    loadWaline(new URL(el.dataset.clientUrl, window.location.href).href)
      .then(doInit)
      .catch(function (e) {
        if (currentNavigation !== navigationId) return;
        logError('Failed to load Waline client module', e);
        el.textContent = "评论区加载失败，请刷新页面重试。";
      });
  }

  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(run);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }
})();
