(function () {
  var walineInstance = null;
  var walineModule = null;

  function run() {
    var el = document.getElementById("waline");

    // 销毁旧实例
    if (walineInstance) {
      try { walineInstance.destroy(); } catch (e) {}
      walineInstance = null;
    }

    if (!el) return;

    // 避免站点的全局 KaTeX 自动扫描误处理评论区内容。
    el.classList.add("katex-ignore");

    // 清空残留内容，确保干净初始化
    el.innerHTML = "";

    function doInit(mod) {
      walineModule = mod;
      var walineOptions = {
        el: "#waline",
        serverURL: "https://my-waline-eta-beige.vercel.app",
        path: window.location.pathname,
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

      walineInstance = mod.init({
        ...walineOptions,
      });
    }

    if (walineModule) {
      doInit(walineModule);
    } else {
      import("https://unpkg.com/@waline/client@v3/dist/waline.js").then(doInit);
    }
  }

  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(run);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }
})();
