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

  function formatDate(date) {
    var parsed = new Date(date + "T12:00:00");
    if (isNaN(parsed.getTime())) return date || "";
    return parsed.toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric" });
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

  function fillParagraphs(el, text) {
    el.replaceChildren();
    String(text || "").split(/\n\n+/).forEach(function (part) {
      var trimmed = part.trim();
      if (!trimmed) return;
      var p = document.createElement("p");
      p.textContent = trimmed;
      el.appendChild(p);
    });
  }

  function iconShare() {
    return '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M12 4.5v9M8.5 8 12 4.5 15.5 8M6 13.5v4.2A1.8 1.8 0 0 0 7.8 19.5h8.4a1.8 1.8 0 0 0 1.8-1.8v-4.2" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>';
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
    var top = target.getBoundingClientRect().top - scroller.getBoundingClientRect().top + scroller.scrollTop - 8;
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
    api.getNote(date).then(function (note) {
      if (state.date !== date) return;
      var button = reader.querySelector("[data-reader-comment]");
      button.setAttribute("aria-expanded", note ? "true" : "false");
    }).catch(function () {});
  }

  function render(item, date) {
    state.date = date;
    state.item = item;
    reader.querySelector("[data-reader-kicker]").textContent = formatDate(date);
    var title = reader.querySelector("#reader-title");
    var body = reader.querySelector("[data-reader-body]");
    if (!item) {
      title.textContent = "This day is not in the walk yet.";
      body.hidden = true;
    } else {
      body.hidden = false;
      title.textContent = item.silentTitle || item.title || "Daily walk";
      reader.querySelector("[data-reader-verse]").textContent = plainVerse(item.verse);
      var ref = String(item.verseRef || "").replace(/\s*NIV\s*$/i, "").trim();
      reader.querySelector("[data-reader-ref]").textContent = ref ? ref + " NIV" : "";
      fillParagraphs(reader.querySelector("[data-reader-silent]"), item.silentBody || item.body || "");
      reader.querySelector("[data-reader-carry-title]").textContent = item.carryTitle || item.title || "";
      fillParagraphs(reader.querySelector("[data-reader-challenge]"), item.carryBody || item.body || "");
      reader.querySelector("[data-reader-reflection]").textContent = item.reflection || "";
      fillParagraphs(reader.querySelector("[data-reader-prayer]"), item.prayer || "");
    }
    refreshEngage(date);
  }

  function closeNote() {
    if (!noteLayer || noteLayer.hidden) return;
    noteLayer.hidden = true;
    var comment = reader.querySelector("[data-reader-comment]");
    if (comment) comment.focus({ preventScroll: true });
  }

  function persistNote() {
    var api = engage();
    if (!api || !state.date) return Promise.resolve("");
    var value = reader.querySelector("[data-reader-note]").value;
    return api.setNote(state.date, value).then(function (saved) {
      reader.querySelector("[data-note-status]").textContent = "Saved on this device.";
      reader.querySelector("[data-reader-comment]").setAttribute("aria-expanded", saved ? "true" : "false");
      return saved;
    });
  }

  function openNote() {
    var api = engage();
    if (!api || !state.date) return;
    noteLayer.hidden = false;
    reader.querySelector("[data-note-status]").textContent = "";
    api.getNote(state.date).then(function (note) {
      var field = reader.querySelector("[data-reader-note]");
      field.value = note || "";
      field.focus();
    }).catch(function () {
      reader.querySelector("[data-reader-note]").focus();
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
      persistNote();
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
      '<div class="reader-scroll">',
      '<article class="reader-measure">',
      '<p class="reader-kicker" data-reader-kicker></p>',
      '<h1 id="reader-title"></h1>',
      '<div data-reader-body>',
      '<p class="reader-verse" data-reader-verse></p>',
      '<p class="reader-ref" data-reader-ref></p>',
      '<p class="reader-k">Silent touch</p>',
      '<div data-reader-silent></div>',
      '<h2 id="reader-challenge" class="reader-k">Today\'s challenge</h2>',
      '<h3 data-reader-carry-title></h3>',
      '<div data-reader-challenge></div>',
      '<p class="reader-k">Reflection</p>',
      '<p class="reader-reflection" data-reader-reflection></p>',
      '<p class="reader-k">Guided prayer</p>',
      '<div data-reader-prayer></div>',
      "</div>",
      '<div class="reader-actions" data-reader-actions>',
      '<button type="button" data-reader-like aria-pressed="false"><span data-heart></span><span>Like</span></button>',
      '<button type="button" data-reader-comment aria-haspopup="dialog" aria-controls="reader-note" aria-expanded="false"><span>' + iconComment() + '</span><span>Comment</span></button>',
      '<button type="button" data-reader-share-row><span>' + iconShare() + '</span><span>Share</span></button>',
      "</div>",
      "</article>",
      "</div>",
      '<div class="note-layer" data-reader-note-layer hidden>',
      '<div class="note-sheet" id="reader-note" role="dialog" aria-modal="true" aria-labelledby="reader-note-title">',
      '<h2 id="reader-note-title">Private note</h2>',
      '<p class="note-help">This stays on your device. It is saved in this browser only, and nobody else can read it.</p>',
      '<textarea data-reader-note aria-label="Private note"></textarea>',
      '<p class="note-status" data-note-status role="status"></p>',
      '<div class="note-actions">',
      '<button type="button" data-note-save>Save</button>',
      '<button type="button" data-note-close>Close</button>',
      "</div>",
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
    reader.querySelector("[data-note-save]").addEventListener("click", function () { persistNote(); });
    reader.querySelector("[data-note-close]").addEventListener("click", function () {
      persistNote().then(function () { closeNote(); });
    });
    noteLayer.addEventListener("click", function (event) {
      if (event.target === noteLayer) persistNote().then(function () { closeNote(); });
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
