(function () {
  var state = {
    items: [],
    current: null,
    date: null,
    item: null,
    opener: null,
    pushed: false,
    suppressPop: false,
    scrollY: 0,
    toastTimer: 0
  };
  var reader;
  var noteLayer;
  var toast;

  function engage() {
    return window.DailyEngage;
  }

  function findItem(date) {
    for (var i = 0; i < state.items.length; i++) {
      if (state.items[i] && state.items[i].date === date) return state.items[i];
    }
    return null;
  }

  function plainVerse(verse) {
    return String(verse || "")
      .replace(/[“”]/g, '"')
      .trim()
      .replace(/^"+|"+$/g, "")
      .split(" — ")[0]
      .replace(/\s*\([^)]*NIV\)\s*$/, "")
      .trim();
  }

  function appendParagraphs(el, text) {
    String(text || "").split(/\n\n+/).forEach(function (part) {
      var trimmed = part.trim();
      if (!trimmed) return;
      var p = document.createElement("p");
      p.textContent = trimmed;
      el.appendChild(p);
    });
  }

  function iconShare() {
    return '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M12 3.2v8.6M8.7 6.4 12 3.2l3.3 3.2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><path d="M8 10.2H7.1A1.8 1.8 0 0 0 5.3 12v6.2A1.8 1.8 0 0 0 7.1 20h9.8a1.8 1.8 0 0 0 1.8-1.8V12a1.8 1.8 0 0 0-1.8-1.8H16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  }

  function iconHeart(filled) {
    return '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path d="M12.1 19.3s-6.4-3.9-6.4-8.2A3.6 3.6 0 0 1 12 8.2a3.6 3.6 0 0 1 6.3 2.9c0 4.3-6.2 8.2-6.2 8.2z" fill="' + (filled ? "currentColor" : "none") + '" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>';
  }

  function iconComment() {
    return '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path d="M6 6.5h12a2 2 0 0 1 2 2v6.2a2 2 0 0 1-2 2H11l-4.2 3v-3H6a2 2 0 0 1-2-2V8.5a2 2 0 0 1 2-2z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>';
  }

  function showToast(message) {
    if (!toast) return;
    toast.textContent = message;
    toast.hidden = false;
    window.clearTimeout(state.toastTimer);
    state.toastTimer = window.setTimeout(function () {
      toast.hidden = true;
    }, 1600);
  }

  function shareUrlFor(item) {
    var api = engage();
    var date = (item && item.date) || state.date;
    if (api && date) return api.buildDailyShareUrl(location.origin, date);
    return location.origin.replace(/\/+$/, "") + "/daily";
  }

  function shareItem(item) {
    var url = shareUrlFor(item);
    var title = (item && (item.silentTitle || item.title)) || "Daily Walk";
    var payload = { title: title, url: url };
    if (navigator.share) {
      navigator.share(payload).then(function () {}, function (err) {
        if (err && err.name === "AbortError") return;
        copyLink(url);
      });
      return;
    }
    copyLink(url);
  }

  function copyLink(url) {
    var done = function () { showToast("Link copied"); };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(url).then(done, function () { legacyCopy(url, done); });
      return;
    }
    legacyCopy(url, done);
  }

  function legacyCopy(url, done) {
    var field = document.createElement("textarea");
    field.value = url;
    field.setAttribute("readonly", "");
    field.style.position = "fixed";
    field.style.left = "-9999px";
    document.body.appendChild(field);
    field.select();
    try {
      if (document.execCommand("copy")) done();
    } catch (err) {}
    field.remove();
  }

  function focusables(root) {
    return Array.prototype.filter.call(
      root.querySelectorAll("button, a[href], textarea, input, select"),
      function (el) {
        if (el.disabled || el.getAttribute("aria-hidden") === "true") return false;
        if (el.closest("[hidden]")) return false;
        return true;
      }
    );
  }

  function lockBackground() {
    state.scrollY = window.scrollY || document.documentElement.scrollTop || 0;
    document.body.classList.add("reader-open");
    document.body.style.top = "-" + state.scrollY + "px";
    try { document.body.inert = true; } catch (err) {}
  }

  function unlockBackground() {
    document.body.classList.remove("reader-open");
    document.body.style.top = "";
    try { document.body.inert = false; } catch (err) {}
    var root = document.documentElement;
    var prev = root.style.scrollBehavior;
    root.style.scrollBehavior = "auto";
    window.scrollTo(0, state.scrollY);
    root.style.scrollBehavior = prev;
  }

  function pathWithDay(date) {
    var url = new URL(location.href);
    url.searchParams.set("day", date);
    if (/day=/.test(url.hash) || /^#\d{4}-\d{2}-\d{2}$/.test(url.hash)) url.hash = "";
    return url.pathname + url.search + url.hash;
  }

  function stripDay() {
    var url = new URL(location.href);
    var hashed = /day=/.test(url.hash) || /^#\d{4}-\d{2}-\d{2}$/.test(url.hash);
    if (!url.searchParams.has("day") && !hashed) return;
    url.searchParams.delete("day");
    if (hashed) url.hash = "";
    history.replaceState({}, "", url.pathname + url.search + url.hash);
  }

  function scrollToAnchor(anchor) {
    var scroller = reader.querySelector(".reader-scroll");
    if (!scroller) return;
    if (anchor !== "challenge") {
      scroller.scrollTop = 0;
      return;
    }
    var target = reader.querySelector("#reader-challenge");
    if (!target) {
      scroller.scrollTop = 0;
      return;
    }
    var top = target.getBoundingClientRect().top - scroller.getBoundingClientRect().top + scroller.scrollTop - 88;
    scroller.scrollTop = Math.max(0, top);
  }

  function paintLike(on) {
    var button = reader.querySelector("[data-reader-like]");
    var slot = reader.querySelector("[data-heart]");
    button.setAttribute("aria-pressed", on ? "true" : "false");
    slot.innerHTML = iconHeart(!!on);
  }

  function refreshEngage(date) {
    var api = engage();
    if (!api) return;
    api.getLike(date).then(function (on) {
      if (state.date === date) paintLike(on);
    }).catch(function () {});
  }

  function render(item, date) {
    state.date = date;
    state.item = item;
    var title = reader.querySelector("#reader-title");
    var body = reader.querySelector("[data-reader-body]");
    body.replaceChildren();
    body.hidden = false;
    if (!item) {
      title.textContent = "This day is not in the walk yet.";
      appendParagraphs(body, "This day is not in the walk yet.");
    } else {
      title.textContent = item.silentTitle || item.title || "Daily walk";
      appendParagraphs(body, plainVerse(item.verse));
      var ref = String(item.verseRef || "").replace(/\s*NIV\s*$/i, "").trim();
      if (ref) appendParagraphs(body, ref + " NIV");
      appendParagraphs(body, item.silentBody || item.body || "");
      var challenge = document.createElement("div");
      challenge.id = "reader-challenge";
      appendParagraphs(challenge, item.carryBody || item.body || "");
      body.appendChild(challenge);
      appendParagraphs(body, item.reflection || "");
      appendParagraphs(body, item.prayer || "");
    }
    refreshEngage(date);
  }

  function closeNote() {
    if (!noteLayer || noteLayer.hidden) return;
    noteLayer.hidden = true;
    var comment = reader.querySelector("[data-reader-comment]");
    if (comment) {
      comment.setAttribute("aria-expanded", "false");
      comment.focus({ preventScroll: true });
    }
  }

  function renderPinnedQuestion() {
    var question = state.item && String(state.item.discussionQuestion || "").trim();
    if (!question) return null;
    var pinned = document.createElement("article");
    pinned.className = "comment comment-pinned";
    pinned.setAttribute("role", "listitem");
    var meta = document.createElement("div");
    meta.className = "comment-meta";
    var name = document.createElement("span");
    name.className = "comment-name";
    name.textContent = "Steadfast Team";
    var badge = document.createElement("span");
    badge.className = "team-badge";
    badge.textContent = "Team";
    meta.appendChild(name);
    meta.appendChild(badge);
    var body = document.createElement("p");
    body.className = "comment-text";
    body.textContent = question;
    pinned.appendChild(meta);
    pinned.appendChild(body);
    return pinned;
  }

  function renderComments(list) {
    var box = reader.querySelector("[data-comment-list]");
    var empty = reader.querySelector("[data-comment-empty]");
    var api = engage();
    box.replaceChildren();
    var pinned = renderPinnedQuestion();
    if (pinned) box.appendChild(pinned);
    var items = list || [];
    empty.hidden = items.length > 0;
    items.forEach(function (comment) {
      var article = document.createElement("article");
      article.className = "comment";
      article.setAttribute("role", "listitem");
      var meta = document.createElement("div");
      meta.className = "comment-meta";
      var name = document.createElement("span");
      name.className = "comment-name";
      name.textContent = comment.name;
      var time = document.createElement("time");
      time.dateTime = new Date(comment.createdAt).toISOString();
      time.textContent = api ? api.formatRelativeTime(comment.createdAt, Date.now()) : "";
      meta.appendChild(name);
      meta.appendChild(time);
      var body = document.createElement("p");
      body.className = "comment-text";
      body.textContent = comment.text;
      var report = document.createElement("button");
      report.type = "button";
      report.className = "comment-report";
      report.setAttribute("data-comment-report", comment.id);
      if (comment.reported) {
        report.textContent = "Reported";
        report.disabled = true;
      } else {
        report.textContent = "Report";
      }
      article.appendChild(meta);
      article.appendChild(body);
      article.appendChild(report);
      box.appendChild(article);
    });
  }

  function postComment(event) {
    if (event) event.preventDefault();
    var api = engage();
    var status = reader.querySelector("[data-note-status]");
    if (!api || !state.date) return;
    var name = reader.querySelector("[data-comment-name]").value;
    var text = reader.querySelector("[data-comment-text]").value;
    if (!String(name).trim() || !String(text).trim()) {
      status.textContent = "Add your name and a comment.";
      return;
    }
    api.setDisplayName(name).then(function () {
      return api.addComment(state.date, { name: name, text: text });
    }).then(function () {
      return api.getComments(state.date);
    }).then(function (list) {
      if (state.date) renderComments(list);
      reader.querySelector("[data-comment-text]").value = "";
      status.textContent = "Saved on this device.";
    }).catch(function () {
      status.textContent = "Could not save that comment.";
    });
  }

  function reportComment(id) {
    var api = engage();
    if (!api || !state.date || !id) return;
    api.reportComment(state.date, id).then(function (saved) {
      if (!saved) return;
      return api.getComments(state.date);
    }).then(function (list) {
      if (!list) return;
      renderComments(list);
      reader.querySelector("[data-note-status]").textContent = "Report saved on this device.";
    }).catch(function () {});
  }

  function openNote() {
    var api = engage();
    if (!api || !state.date) return;
    noteLayer.hidden = false;
    reader.querySelector("[data-reader-comment]").setAttribute("aria-expanded", "true");
    reader.querySelector("[data-note-status]").textContent = "";
    Promise.all([api.getComments(state.date), api.getDisplayName()]).then(function (result) {
      renderComments(result[0]);
      var nameField = reader.querySelector("[data-comment-name]");
      if (!nameField.value) nameField.value = result[1] || "";
      (nameField.value ? reader.querySelector("[data-comment-text]") : nameField).focus();
    }).catch(function () {
      reader.querySelector("[data-comment-name]").focus();
    });
  }

  function open(date, opts) {
    opts = opts || {};
    if (!state.items.length && opts.history !== "load") {
      state.pending = { date: date, opts: opts };
      return;
    }
    render(findItem(date), date);
    var wasHidden = reader.hidden;
    reader.hidden = false;
    if (wasHidden) {
      lockBackground();
      var closeBtn = reader.querySelector("[data-reader-close]");
      closeBtn.focus({ preventScroll: true });
    }
    if (opts.opener) state.opener = opts.opener;
    requestAnimationFrame(function () { scrollToAnchor(opts.anchor); });
    if (opts.history === "push") {
      var next = pathWithDay(date);
      var here = location.pathname + location.search + location.hash;
      if (next !== here) {
        history.pushState({ dailyReader: date }, "", next);
        state.pushed = true;
      }
    }
  }

  function close() {
    if (!reader || reader.hidden) return;
    if (!noteLayer.hidden) {
      closeNote();
      return;
    }
    reader.hidden = true;
    unlockBackground();
    var opener = state.opener;
    state.opener = null;
    if (state.pushed) {
      state.pushed = false;
      state.suppressPop = true;
      history.back();
    } else {
      stripDay();
    }
    if (opener && typeof opener.focus === "function") opener.focus({ preventScroll: true });
  }

  function onKeydown(event) {
    if (!reader || reader.hidden) return;
    if (event.key === "Escape") {
      event.preventDefault();
      event.stopPropagation();
      close();
      return;
    }
    if ((event.metaKey || event.ctrlKey) && String(event.key).toLowerCase() === "k") {
      event.preventDefault();
      event.stopPropagation();
      return;
    }
    if (event.key !== "Tab") return;
    var root = noteLayer.hidden ? reader : noteLayer.querySelector(".note-sheet");
    var items = focusables(root);
    if (!items.length) {
      event.preventDefault();
      return;
    }
    var first = items[0];
    var last = items[items.length - 1];
    var active = document.activeElement;
    if (event.shiftKey) {
      if (active === first || !root.contains(active)) {
        event.preventDefault();
        last.focus();
      }
    } else if (active === last || !root.contains(active)) {
      event.preventDefault();
      first.focus();
    }
  }

  function mount() {
    if (reader) return;
    reader = document.createElement("div");
    reader.className = "reader";
    reader.hidden = true;
    reader.setAttribute("role", "dialog");
    reader.setAttribute("aria-modal", "true");
    reader.setAttribute("aria-labelledby", "reader-title");
    reader.innerHTML = [
      '<button class="reader-close" type="button" data-reader-close aria-label="Close">',
      '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
      "</button>",
      '<button class="reader-share-bubble" type="button" data-reader-share aria-label="Share">',
      iconShare(),
      "</button>",
      '<div class="reader-scrim" aria-hidden="true"></div>',
      '<div class="reader-scroll">',
      '<article class="reader-measure">',
      '<h1 id="reader-title" class="reader-sr"></h1>',
      '<div data-reader-body></div>',
      '<div class="reader-actions" data-reader-actions>',
      '<button type="button" data-reader-like aria-pressed="false"><span data-heart></span><span>Like</span></button>',
      '<button type="button" data-reader-comment aria-haspopup="dialog" aria-controls="reader-comments" aria-expanded="false"><span>' + iconComment() + '</span><span>Comment</span></button>',
      '<button type="button" data-reader-share-row><span>' + iconShare() + '</span><span>Share</span></button>',
      "</div>",
      "</article>",
      "</div>",
      '<div class="note-layer" data-reader-note-layer hidden>',
      '<div class="note-sheet" id="reader-comments" role="dialog" aria-modal="true" aria-labelledby="reader-note-title">',
      '<div class="comment-head">',
      '<h2 id="reader-note-title">Comments</h2>',
      '<button type="button" class="comment-dismiss" data-note-close aria-label="Close comments">',
      '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
      "</button>",
      "</div>",
      '<p class="note-help">Public comments are coming soon. For now, comments stay on this device.</p>',
      '<div class="comment-list" data-comment-list role="list"></div>',
      '<p class="comment-empty" data-comment-empty>Be the first to comment.</p>',
      '<form class="comment-composer" data-comment-form>',
      '<label class="comment-label">Name<input type="text" name="name" data-comment-name maxlength="40" autocomplete="nickname" enterkeyhint="next"></label>',
      '<label class="comment-label">Comment<textarea name="text" data-comment-text maxlength="500" rows="3" enterkeyhint="send"></textarea></label>',
      '<p class="note-status" data-note-status role="status"></p>',
      '<div class="note-actions">',
      '<button type="submit" data-note-save>Post</button>',
      "</div>",
      "</form>",
      "</div>",
      "</div>"
    ].join("");
    document.documentElement.appendChild(reader);
    noteLayer = reader.querySelector("[data-reader-note-layer]");
    reader.querySelector("[data-heart]").innerHTML = iconHeart(false);
    toast = document.createElement("p");
    toast.className = "reader-toast";
    toast.setAttribute("role", "status");
    toast.hidden = true;
    document.documentElement.appendChild(toast);

    reader.querySelector("[data-reader-close]").addEventListener("click", close);
    reader.querySelector("[data-reader-share]").addEventListener("click", function () {
      shareItem(state.item);
    });
    reader.querySelector("[data-reader-share-row]").addEventListener("click", function () {
      shareItem(state.item);
    });
    reader.querySelector("[data-reader-like]").addEventListener("click", function () {
      var api = engage();
      if (!api || !state.date) return;
      var next = reader.querySelector("[data-reader-like]").getAttribute("aria-pressed") !== "true";
      api.setLike(state.date, next).then(function (on) { paintLike(on); }).catch(function () {});
    });
    reader.querySelector("[data-reader-comment]").addEventListener("click", openNote);
    reader.querySelector("[data-comment-form]").addEventListener("submit", postComment);
    reader.querySelector("[data-comment-list]").addEventListener("click", function (event) {
      var button = event.target.closest("[data-comment-report]");
      if (!button || button.disabled) return;
      reportComment(button.getAttribute("data-comment-report"));
    });
    reader.querySelector("[data-note-close]").addEventListener("click", closeNote);
    noteLayer.addEventListener("click", function (event) {
      if (event.target === noteLayer) closeNote();
    });
    document.addEventListener("keydown", onKeydown, true);
    window.addEventListener("popstate", function () {
      if (state.suppressPop) {
        state.suppressPop = false;
        return;
      }
      state.pushed = false;
      var api = engage();
      var day = api ? api.parseDailyDay(location.search, location.hash) : null;
      if (day) open(day, { history: "pop" });
      else if (!reader.hidden) {
        closeNote();
        reader.hidden = true;
        unlockBackground();
      }
    });
    document.querySelectorAll("[data-open-reader]").forEach(function (button) {
      button.addEventListener("click", function () {
        var date = (state.current && state.current.date) || (engage() && engage().parseDailyDay(location.search, location.hash));
        if (!date) return;
        var anchor = button.getAttribute("data-open-reader");
        open(date, { history: "push", opener: button, anchor: anchor });
      });
    });
    var pageShare = document.getElementById("share-walk");
    if (pageShare && !pageShare.dataset.readerBound) {
      pageShare.dataset.readerBound = "1";
      pageShare.addEventListener("click", function () { shareCurrent(); });
    }
  }

  function setFeed(items, current) {
    state.items = items || [];
    state.current = current || null;
    var api = engage();
    var day = api ? api.parseDailyDay(location.search, location.hash) : null;
    if (day && reader && reader.hidden) open(day, { history: "load" });
    else if (state.pending) {
      var pending = state.pending;
      state.pending = null;
      open(pending.date, pending.opts);
    }
  }

  function shareCurrent() {
    var api = engage();
    var day = api ? api.parseDailyDay(location.search, location.hash) : null;
    shareItem(findItem(day) || state.item || state.current);
  }

  document.addEventListener("DOMContentLoaded", mount);
  document.addEventListener("steadfast:daily", function (event) {
    var detail = event.detail || {};
    setFeed(detail.items, detail.current);
  });

  window.DailyReader = {
    mount: mount,
    setFeed: setFeed,
    shareCurrent: shareCurrent
  };
})();
