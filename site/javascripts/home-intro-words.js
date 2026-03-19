/* 个人介绍：先显示头像，再每个单词依次淡入 - 性能优化版 */
(function () {
  var WORD_DELAY = 0.055; // 稍微缩短间隔
  var AVATAR_DURATION = 0.4;
  var AVATAR_DELAY = 0.08;
  var TEXT_START_DELAY = AVATAR_DELAY + AVATAR_DURATION + 0.12;

  // 使用 requestIdleCallback 或 setTimeout 延迟执行，避免阻塞首屏
  function scheduleWork(fn) {
    if (typeof requestIdleCallback !== 'undefined') {
      requestIdleCallback(fn, { timeout: 100 });
    } else {
      setTimeout(fn, 50);
    }
  }

  function run() {
    var hero = document.querySelector(".home-hero");
    if (!hero) return;

    // 使用 requestAnimationFrame 确保在下一帧执行 DOM 操作
    requestAnimationFrame(function () {
      processHero(hero);
    });
  }

  function processHero(hero) {
    var title = hero.querySelector(".home-title");
    var wordIndex = 0;

    if (title && !title.querySelector(".home-intro-word")) {
      var parts = title.textContent.trim().split(/(\s+)/);
      var fragment = document.createDocumentFragment();

      parts.forEach(function (p) {
        if (/\S/.test(p)) {
          var span = document.createElement("span");
          span.className = "home-intro-word";
          span.style.animationDelay = (TEXT_START_DELAY + wordIndex * WORD_DELAY).toFixed(3) + "s";
          span.textContent = p;
          // 使用 GPU 加速
          span.style.transform = "translateZ(0)";
          fragment.appendChild(span);
          wordIndex++;
        } else {
          fragment.appendChild(document.createTextNode(p));
        }
      });

      title.textContent = "";
      title.appendChild(fragment);
    }

    var subtitle = hero.querySelector(".home-subtitle");
    var badgeEndTime = 0;

    if (subtitle && !subtitle.querySelector(".home-intro-word")) {
      var titleWordCount = wordIndex || ((title && title.textContent.trim().split(/\s+/).length) || 4);
      var subtitleStart = TEXT_START_DELAY + titleWordCount * WORD_DELAY;
      var result = wrapWordsRecursive(subtitle, subtitleStart, subtitle);
      subtitle.textContent = "";
      subtitle.appendChild(result.fragment);
      badgeEndTime = result.nextDelaySeconds - WORD_DELAY + 0.35;
    } else if (title) {
      var titleWordCount = wordIndex || (title.textContent.trim().split(/\s+/).length || 4);
      badgeEndTime = TEXT_START_DELAY + titleWordCount * WORD_DELAY + 0.35;
    }

    // 社交图标行：等待所有文字淡入完成后再整体淡入
    var socialRow = hero.querySelector(".home-social-row");
    if (socialRow && badgeEndTime > 0) {
      // 使用 setTimeout 在文字动画完成后触发动画
      var delayMs = Math.round(badgeEndTime * 1000);
      setTimeout(function() {
        socialRow.classList.add("social-row-animate");
      }, delayMs);
    }
  }

  function wrapWordsRecursive(container, startDelaySeconds, root) {
    var delaySeconds = startDelaySeconds;
    var fragment = document.createDocumentFragment();

    for (var i = 0; i < container.childNodes.length; i++) {
      var node = container.childNodes[i];
      if (node.nodeType === Node.TEXT_NODE) {
        var parts = node.textContent.split(/(\s+)/);
        parts.forEach(function (p) {
          if (/\S/.test(p)) {
            var span = document.createElement("span");
            span.className = "home-intro-word";
            span.style.animationDelay = delaySeconds.toFixed(3) + "s";
            span.style.transform = "translateZ(0)";
            span.textContent = p;
            fragment.appendChild(span);
            delaySeconds += WORD_DELAY;
          } else {
            fragment.appendChild(document.createTextNode(p));
          }
        });
      } else if (node.nodeType === Node.ELEMENT_NODE) {
        var sub = wrapWordsRecursive(node, delaySeconds, root);
        fragment.appendChild(sub.fragment);
        delaySeconds = sub.nextDelaySeconds;
      }
    }

    if (container !== root) {
      var wrap = document.createElement(container.nodeName.toLowerCase());
      for (var a = 0; a < container.attributes.length; a++) {
        wrap.setAttribute(container.attributes[a].name, container.attributes[a].value);
      }
      wrap.appendChild(fragment);
      return { fragment: wrap, nextDelaySeconds: delaySeconds };
    }
    return { fragment: fragment, nextDelaySeconds: delaySeconds };
  }

  // 延迟执行动画初始化
  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(function () { scheduleWork(run); });
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () { scheduleWork(run); });
  } else {
    scheduleWork(run);
  }
})();
