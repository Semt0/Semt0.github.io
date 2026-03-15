/* 个人介绍：先显示头像，再每个单词依次淡入 */
(function () {
  var WORD_DELAY = 0.065;
  var AVATAR_DURATION = 0.5;
  var AVATAR_DELAY = 0.1;
  var TEXT_START_DELAY = AVATAR_DELAY + AVATAR_DURATION + 0.15;

  function run() {
    var hero = document.querySelector(".home-hero");
    if (!hero) return;

    var title = hero.querySelector(".home-title");
    if (title && !title.querySelector(".home-intro-word")) {
      var parts = title.textContent.trim().split(/(\s+)/);
      var wordIndex = 0;
      var html = parts
        .map(function (p) {
          if (/\S/.test(p)) {
            var delay = TEXT_START_DELAY + wordIndex * WORD_DELAY;
            wordIndex++;
            return '<span class="home-intro-word" style="animation-delay:' + delay + 's">' + escapeHtml(p) + "</span>";
          }
          return escapeHtml(p);
        })
        .join("");
      title.innerHTML = html;
    }

    var subtitle = hero.querySelector(".home-subtitle");
    var badgeEndTime = 0;
    if (subtitle && !subtitle.querySelector(".home-intro-word")) {
      var titleWordCount = (title && title.textContent.trim().split(/\s+/).length) || 4;
      var subtitleStart = TEXT_START_DELAY + titleWordCount * WORD_DELAY;
      var result = wrapWordsRecursive(subtitle, subtitleStart, subtitle);
      subtitle.innerHTML = "";
      subtitle.appendChild(result.fragment);
      badgeEndTime = result.nextDelaySeconds - WORD_DELAY + 0.45;
    } else if (title) {
      var titleWordCount = title.textContent.trim().split(/\s+/).length || 4;
      badgeEndTime = TEXT_START_DELAY + titleWordCount * WORD_DELAY + 0.45;
    }
    var socialRow = hero.querySelector(".home-social-row");
    if (socialRow && badgeEndTime > 0) {
      socialRow.style.animationDelay = badgeEndTime + "s";
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
            span.style.animationDelay = delaySeconds + "s";
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

  function escapeHtml(s) {
    var div = document.createElement("div");
    div.textContent = s;
    return div.innerHTML;
  }

  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(run);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }
})();
