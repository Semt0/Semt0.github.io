(function () {
  function render() {
    var content = document.querySelector('.md-content__inner');
    if (!content || typeof renderMathInElement !== 'function') return;
    renderMathInElement(content, {
      delimiters: [
        { left: '$$', right: '$$', display: true },
        { left: '$', right: '$', display: false },
        { left: '\\(', right: '\\)', display: false },
        { left: '\\[', right: '\\]', display: true }
      ],
      ignoredClasses: ['katex-ignore', 'katex']
    });
  }
  if (typeof document$ !== 'undefined' && document$.subscribe) {
    document$.subscribe(render);
  } else if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', render, { once: true });
  } else {
    render();
  }
})();
