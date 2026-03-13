/* 首页四个栏目：滚动进入视口时淡入 + 上移，离开视口时淡出 */
(function () {
  function run() {
    var body = document.body;
    var sections = body.querySelectorAll(".home-section");
    if (!sections.length) return;

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("home-section-visible");
          } else {
            entry.target.classList.remove("home-section-visible");
          }
        });
      },
      {
        // 提前一点淡入 / 淡出
        rootMargin: "0px 0px -20px 0px",
        threshold: 0.1,
      }
    );

    sections.forEach(function (el) {
      observer.observe(el);
    });
  }

  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(run);
  } else {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", run);
    } else {
      run();
    }
  }
})();
