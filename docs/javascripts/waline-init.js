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

    // 清空残留内容，确保干净初始化
    el.innerHTML = "";

    function doInit(mod) {
      walineModule = mod;
      walineInstance = mod.init({
        el: "#waline",
        serverURL: "https://my-waline-eta-beige.vercel.app",
        path: window.location.pathname,
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
