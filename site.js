const devotionals = [
  {
    title: "Stand still before you stride",
    verse: "“Be watchful, stand firm in the faith, act like men, be strong. Let all that you do be done in love.” — 1 Corinthians 16:13–14",
    body: "A steadfast man does not confuse motion with obedience. Before the meeting, the commute, the argument you already rehearsed — stand. Watch. Then walk."
  },
  {
    title: "Reject the quiet drift",
    verse: "“Therefore we must pay much closer attention to what we have heard, lest we drift away from it.” — Hebrews 2:1",
    body: "Most men do not fall in a crash. They ease off the oars. Today, name one place you have gone passive and put your hand back on the work."
  },
  {
    title: "Carry what is yours",
    verse: "“But if anyone does not provide for his relatives, and especially for members of his household, he has denied the faith.” — 1 Timothy 5:8",
    body: "Responsibility is not a vibe. It is a name on a bill, a child who needs a father in the room, a word you said you would keep. Pick it up."
  },
  {
    title: "Lead from the front of the table",
    verse: "“Be strong and courageous. Do not be frightened, and do not be dismayed, for the Lord your God is with you wherever you go.” — Joshua 1:9",
    body: "Courage is rarely a battlefield. It is the first apology. The first prayer at dinner. The first no that protects your house."
  },
  {
    title: "Work for a better country",
    verse: "“For he was looking forward to the city that has foundations, whose designer and builder is God.” — Hebrews 11:10",
    body: "If the only reward you are building toward is comfort, you will fold when comfort is threatened. Lift your eyes. The greater reward holds when payday does not."
  },
  {
    title: "A soft answer is not a soft man",
    verse: "“A gentle answer turns away wrath, but a harsh word stirs up anger.” — Proverbs 15:1",
    body: "Steadfast is not loud. Strength that cannot be quiet is just ungoverned heat. Practice one gentle sentence in the hardest room of your day."
  },
  {
    title: "Finish the small obedience",
    verse: "“His master said to him, ‘Well done, good and faithful servant.’” — Matthew 25:21",
    body: "You do not become a steadfast man by intending a better decade. You become one by completing this morning’s assignment. Close the loop."
  },
  {
    title: "Put your house in order",
    verse: "“Set your house in order, for you shall die; you shall not recover.” — Isaiah 38:1",
    body: "Mortality makes a man honest. What would your son inherit tonight besides unfinished sentences? Write one thing down and finish it."
  },
  {
    title: "Love is a decision with a spine",
    verse: "“Husbands, love your wives, as Christ loved the church and gave himself up for her.” — Ephesians 5:25",
    body: "Affection is easy when she is easy. Covenant shows up when the room is cold. Give yourself up in one concrete way before noon."
  },
  {
    title: "Do not despise the small start",
    verse: "“For whoever has despised the day of small things shall rejoice.” — Zechariah 4:10",
    body: "Twenty-four weeks looks long until you have done week one. Open the passage. Do the act. Tomorrow can have tomorrow."
  },
  {
    title: "Watch your mouth in your own house",
    verse: "“Let no corrupting talk come out of your mouths, but only such as is good for building up.” — Ephesians 4:29",
    body: "The men you are raising will speak like the man they heard at dinner. Bless or rot. There is no third use of the tongue."
  },
  {
    title: "Work as if the Lord is the board",
    verse: "“Whatever you do, work heartily, as for the Lord and not for men.” — Colossians 3:23",
    body: "Half-done work is passivity in a collar. Finish the job in front of you as worship, not as a performance for a manager."
  }
];

function paintDevotion(root, d) {
  if (!root || !d) return;
  const date = d.date ? new Date(d.date + "T12:00:00") : new Date();
  const kicker = root.querySelector("[data-devotion-kicker]");
  const title = root.querySelector("[data-devotion-title]");
  const verse = root.querySelector("[data-devotion-verse]");
  const body = root.querySelector("[data-devotion-body]");
  const silentTitle = root.querySelector("[data-devotion-silent-title]");
  const silentLine = root.querySelector("[data-devotion-silent-line]");
  if (kicker) kicker.textContent = date.toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric" });
  root.querySelectorAll("[data-devotion-title]").forEach((el) => { el.textContent = d.carryTitle || d.title; });
  if (verse) {
    let plain = String(d.verse || "").replace(/[“”]/g, '"').trim();
    plain = plain.replace(/^"+|"+$/g, "").split(" — ")[0].replace(/\s*\([^)]*NIV\)\s*$/, "").trim();
    const ref = String(d.verseRef || "").replace(/\s*NIV\s*$/i, "").trim();
    verse.textContent = plain;
    const n = plain.length;
    verse.style.fontSize = n < 70 ? "22px" : n < 120 ? "20px" : n < 180 ? "18px" : "16px";
    root.querySelectorAll("[data-devotion-verse-ref]").forEach((el) => {
      el.textContent = ref ? (ref + " NIV") : "";
    });
  }
  if (body) body.textContent = d.silentBody || d.carryBody || d.body;
  root.querySelectorAll("[data-devotion-silent-title]").forEach((el) => { el.textContent = d.silentTitle || d.title; });
  if (silentLine) silentLine.textContent = d.silentLine || "";
  if (d.imageURL) {
    root.querySelectorAll("[data-devotion-img]").forEach((el) => {
      el.src = d.imageURL;
      if (!el.getAttribute("alt")) el.alt = d.silentTitle || d.title || "Daily walk";
    });
  }
  function fill(sel, text) {
    const box = root.querySelector(sel);
    if (!box) return;
    box.innerHTML = "";
    String(text || "").split(/\n\n+/).map(s => s.trim()).filter(Boolean).forEach(part => {
      const p = document.createElement("p");
      p.textContent = part;
      p.style.margin = "0 0 14px";
      p.style.color = "var(--muted)";
      box.appendChild(p);
    });
  }
  fill("[data-devotion-silent]", d.silentBody || d.body);
  fill("[data-devotion-challenge]", d.carryBody);
  fill("[data-devotion-prayer]", d.prayer);
  const refEl = root.querySelector("[data-devotion-reflection]");
  if (refEl) refEl.textContent = d.reflection || "";
  const tease = root.querySelector("[data-devotion-tease]");
  if (tease) {
    const first = String(d.carryBody || "").split(/\n\n+/)[0].trim();
    tease.textContent = first
      ? first.slice(0, 180) + (first.length > 180 ? "…" : "")
      : "Table talk on the act for today, then a guided prayer. Open the tile for the whole thing.";
  }
  const st = root.querySelector("[data-devotion-silent-tease]");
  if (st) {
    const first = String(d.silentBody || d.body || "").split(/\n\n+/)[0].trim();
    st.textContent = first
      ? first.slice(0, 180) + (first.length > 180 ? "…" : "")
      : "The full walk is behind this tile. Tap to read it.";
  }
}

function chicagoDateKey() {
  return new Intl.DateTimeFormat("en-CA", {
    timeZone: "America/Chicago",
    year: "numeric",
    month: "2-digit",
    day: "2-digit"
  }).format(new Date());
}

function pickDevotion(items) {
  if (!items || !items.length) return null;
  const key = chicagoDateKey();
  return items.find((i) => i.date === key) || items.find((i) => i.date <= key) || items[items.length - 1];
}

function fallbackDevotion() {
  const day = Math.floor(Date.now() / 86400000);
  return devotionals[day % devotionals.length];
}

function renderDevotion(root) {
  if (!root) return;
  paintDevotion(root, fallbackDevotion());
}

const LIVE_SOCIALS = [
  { id: "youtube", label: "YouTube", href: "https://youtube.com/@steadfastwalk" },
  { id: "instagram", label: "Instagram", href: "https://instagram.com/steadfastwalk" },
  { id: "x", label: "X", href: "https://x.com/steadfastwalk" },
  { id: "facebook", label: "Facebook", href: "https://facebook.com/steadfastwalk" },
  { id: "tiktok", label: "TikTok", href: "https://tiktok.com/@steadfastwalk" }
];

function applyLinks(cfg) {
  const socials = (cfg && cfg.socials && cfg.socials.length) ? cfg.socials : LIVE_SOCIALS;
  const hub = (cfg && cfg.hub) || "https://walksteadfast.com";
  document.querySelectorAll("[data-social]").forEach((el) => {
    const match = socials.find((s) => s.id === el.getAttribute("data-social"));
    if (!match || !match.href) return;
    el.href = match.href;
    el.target = "_blank";
    el.rel = "noopener noreferrer";
  });
  document.querySelectorAll("[data-social-links]").forEach((nav) => {
    const items = [{ label: "Hub", href: hub, external: false }].concat(
      socials.map((s) => ({ label: s.label, href: s.href, external: true }))
    );
    let links = [...nav.querySelectorAll("a")];
    if (links.length !== items.length) {
      nav.replaceChildren();
      items.forEach((item) => {
        const a = document.createElement("a");
        a.textContent = item.label;
        nav.appendChild(a);
      });
      links = [...nav.querySelectorAll("a")];
    }
    items.forEach((item, i) => {
      links[i].href = item.href;
      links[i].textContent = item.label;
      if (item.external) {
        links[i].target = "_blank";
        links[i].rel = "noopener noreferrer";
      } else {
        links[i].removeAttribute("target");
        links[i].removeAttribute("rel");
      }
    });
  });
}

function renderLinks() {
  applyLinks(null);
  fetch("app/links.json", { cache: "no-store" })
    .then((r) => (r.ok ? r.json() : Promise.reject()))
    .then(applyLinks)
    .catch(() => {});
}

function renderAllDevotions() {
  const roots = document.querySelectorAll("[data-devotion]");
  if (!roots.length) return;
  fetch("app/daily.json", { cache: "no-store" })
    .then((r) => (r.ok ? r.json() : Promise.reject()))
    .then((feed) => {
      const d = pickDevotion(feed.items) || fallbackDevotion();
      roots.forEach((root) => paintDevotion(root, d));
      if (document.getElementById("sheet-silent")) paintDevotion(document.body, d);
    })
    .catch(() => {
      const d = fallbackDevotion();
      roots.forEach((root) => paintDevotion(root, d));
      if (document.getElementById("sheet-silent")) paintDevotion(document.body, d);
    });
}

document.addEventListener("DOMContentLoaded", () => {
  renderLinks();
  renderAllDevotions();
  const here = document.getElementById("was-here");
  if (here) {
    const key = "steadfast-walk-" + new Date().toISOString().slice(0, 10);
    if (localStorage.getItem(key)) {
      here.classList.add("on");
      here.textContent = "Marked";
    }
    here.addEventListener("click", () => {
      localStorage.setItem(key, "1");
      here.classList.add("on");
      here.textContent = "Marked";
    });
  }
  const share = document.getElementById("share-walk");
  if (share) {
    share.addEventListener("click", async () => {
      const url = new URL("daily.html", location.href).href;
      if (navigator.share) {
        try { await navigator.share({ title: "Steadfast Daily Walk", url }); } catch (e) {}
      } else {
        try {
          await navigator.clipboard.writeText(url);
          share.textContent = "Copied";
        } catch (e) {}
      }
    });
  }
  let sheetScrollY = 0;
  let sheetOpener = null;
  document.querySelectorAll(".sheet").forEach((sheet) => {
    document.documentElement.appendChild(sheet);
  });
  function fitSheet(sheet) {
    const vv = window.visualViewport;
    if (!vv) {
      sheet.style.top = "";
      sheet.style.left = "";
      sheet.style.width = "";
      sheet.style.height = "";
      sheet.style.right = "";
      sheet.style.bottom = "";
      return;
    }
    sheet.style.top = vv.offsetTop + "px";
    sheet.style.left = vv.offsetLeft + "px";
    sheet.style.width = vv.width + "px";
    sheet.style.height = vv.height + "px";
    sheet.style.right = "auto";
    sheet.style.bottom = "auto";
  }
  function onViewport() {
    document.querySelectorAll(".sheet").forEach((sheet) => {
      if (!sheet.hidden) fitSheet(sheet);
    });
  }
  if (window.visualViewport) {
    visualViewport.addEventListener("resize", onViewport);
    visualViewport.addEventListener("scroll", onViewport);
  }
  function lockPage() {
    sheetScrollY = window.scrollY || document.documentElement.scrollTop || 0;
    document.body.classList.add("sheet-open");
    document.body.style.top = "-" + sheetScrollY + "px";
    document.body.style.position = "fixed";
    document.body.style.width = "100%";
  }
  function unlockPage() {
    if (!document.body.classList.contains("sheet-open")) return;
    document.body.classList.remove("sheet-open");
    document.body.style.position = "";
    document.body.style.top = "";
    document.body.style.width = "";
    const root = document.documentElement;
    const prev = root.style.scrollBehavior;
    root.style.scrollBehavior = "auto";
    window.scrollTo(0, sheetScrollY);
    root.style.scrollBehavior = prev;
  }
  function closeSheets(opts) {
    document.querySelectorAll(".sheet").forEach((el) => {
      el.hidden = true;
      el.style.top = "";
      el.style.left = "";
      el.style.width = "";
      el.style.height = "";
      el.style.right = "";
      el.style.bottom = "";
      const card = el.querySelector(".sheet-card");
      if (card) {
        card._closeToken = null;
        card.style.transform = "";
        card.style.transition = "";
      }
    });
    unlockPage();
    if (!opts || !opts.keepFocus) {
      if (sheetOpener && typeof sheetOpener.focus === "function") {
        sheetOpener.focus({ preventScroll: true });
      }
      sheetOpener = null;
    }
  }
  document.querySelectorAll("[data-open-sheet]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const id = "sheet-" + btn.getAttribute("data-open-sheet");
      const sheet = document.getElementById(id);
      if (!sheet) return;
      closeSheets({ keepFocus: true });
      sheetOpener = btn;
      sheet.hidden = false;
      lockPage();
      fitSheet(sheet);
      const scroller = sheet.querySelector(".sheet-body");
      if (scroller) {
        scroller.scrollTop = 0;
        scroller.style.touchAction = "none";
      }
      const closeBtn = sheet.querySelector("[data-close-sheet]");
      closeBtn?.focus({ preventScroll: true });
    });
  });
  document.querySelectorAll("[data-close-sheet]").forEach((btn) => {
    btn.addEventListener("click", () => closeSheets());
  });
  document.querySelectorAll(".sheet").forEach((sheet) => {
    const card = sheet.querySelector(".sheet-card");
    const scroller = sheet.querySelector(".sheet-body") || card;
    const handle = sheet.querySelector(".sheet-handle");
    let suppressClick = false;
    sheet.addEventListener("click", (e) => {
      if (suppressClick) {
        suppressClick = false;
        return;
      }
      if (e.target === sheet) closeSheets();
    });
    sheet.addEventListener("keydown", (e) => {
      if (e.key !== "Tab" || sheet.hidden) return;
      const focusable = [...sheet.querySelectorAll("button, a[href], input, textarea, select")].filter((el) => !el.disabled);
      if (!focusable.length) return;
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    });
    if (!card || !scroller) return;
    let drag = null;
    function atTop() {
      return scroller.scrollTop <= 1;
    }
    function syncTouchAction() {
      if (drag) return;
      scroller.style.touchAction = atTop() ? "none" : "pan-y";
    }
    scroller.addEventListener("scroll", syncTouchAction, { passive: true });
    syncTouchAction();
    function resetCard() {
      card.style.transition = "transform .22s ease";
      card.style.transform = "translateY(0)";
      drag = null;
      syncTouchAction();
    }
    function onPointerDown(e) {
      if (drag) return;
      if (e.pointerType === "mouse" && e.button !== 0) return;
      if (e.target.closest("[data-close-sheet], a, input, textarea, select, label")) return;
      const onHandle = !!(handle && (e.target === handle || handle.contains(e.target)));
      drag = {
        id: e.pointerId,
        y0: e.clientY,
        y: e.clientY,
        t: performance.now(),
        vel: 0,
        mode: null,
        handle: onHandle,
        top: atTop(),
        scroll0: scroller.scrollTop
      };
      card.style.transition = "none";
      if (drag.handle || drag.top) scroller.style.touchAction = "none";
    }
    function onPointerMove(e) {
      if (!drag || e.pointerId !== drag.id) return;
      const y = e.clientY;
      const now = performance.now();
      const dt = Math.max(1, now - drag.t);
      drag.vel = (y - drag.y) / dt;
      drag.y = y;
      drag.t = now;
      const dy = y - drag.y0;
      if (!drag.mode) {
        if (Math.abs(dy) < 8) return;
        drag.mode = (drag.handle || drag.top) && dy > 0 ? "dismiss" : "content";
        if (drag.mode === "dismiss") {
          try { card.setPointerCapture(e.pointerId); } catch (err) {}
        }
      }
      if (drag.mode === "dismiss") {
        if (e.cancelable) e.preventDefault();
        card.style.transform = "translateY(" + Math.max(0, dy) + "px)";
        return;
      }
      if (drag.handle || drag.top) {
        if (e.cancelable) e.preventDefault();
        scroller.scrollTop = Math.max(0, drag.scroll0 - dy);
      }
    }
    function onPointerEnd(e) {
      if (!drag || (e && e.pointerId != null && e.pointerId !== drag.id)) return;
      const dy = drag.y - drag.y0;
      const closing = drag.mode === "dismiss" && (dy > 96 || (dy > 40 && drag.vel > 0.55));
      if (Math.abs(dy) > 8) suppressClick = true;
      drag = null;
      syncTouchAction();
      if (closing) {
        card.style.transition = "transform .2s ease";
        card.style.transform = "translateY(110%)";
        const token = {};
        card._closeToken = token;
        window.setTimeout(() => {
          if (card._closeToken !== token) return;
          closeSheets();
        }, 180);
      } else {
        card._closeToken = null;
        resetCard();
      }
    }
    card.addEventListener("pointerdown", onPointerDown);
    card.addEventListener("pointermove", onPointerMove);
    card.addEventListener("pointerup", onPointerEnd);
    card.addEventListener("pointercancel", onPointerEnd);
    card.addEventListener("touchmove", (e) => {
      if (!drag) return;
      const own = drag.mode === "dismiss" || ((drag.handle || drag.top) && drag.mode !== "content");
      if (own && e.cancelable) e.preventDefault();
    }, { passive: false });
    scroller.addEventListener("touchstart", () => {
      if (!drag && atTop()) scroller.style.touchAction = "none";
    }, { passive: true });
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeSheets();
  });

  const toggle = document.querySelector(".nav-toggle");
  const links = document.querySelector(".nav-links");
  if (toggle && links) {
    toggle.setAttribute("aria-expanded", "false");
    toggle.addEventListener("click", () => {
      const open = links.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    });
  }

  document.querySelectorAll("main section, .rail-wrap, .hero-copy").forEach((el, i) => {
    el.classList.add("reveal");
    el.style.animationDelay = Math.min(i * 0.06, 0.36) + "s";
  });

  const destinations = [
    ["Training", "training.html"],
    ["Shop", "shop.html"],
    ["Book", "book.html"],
    ["Daily", "index.html#daily-walk"],
    ["Support", "give.html"],
    ["Login", "login.html"],
    ["Listen", "listen.html"],
    ["Path", "program.html"],
    ["Group kit", "group-kit.html"],
    ["Merch", "merch.html"],
    ["Groups", "groups.html"],
    ["Begin", "start.html"]
  ];
  const cmd = document.createElement("div");
  cmd.className = "cmd";
  cmd.innerHTML = '<div class="cmd-box"><input placeholder="Go to…" aria-label="Jump"><div data-cmd-list></div></div>';
  document.body.appendChild(cmd);
  const list = cmd.querySelector("[data-cmd-list]");
  const field = cmd.querySelector("input");
  destinations.forEach(([label, href]) => {
    const a = document.createElement("a");
    a.href = href;
    a.textContent = label;
    list.appendChild(a);
  });
  function openCmd() {
    cmd.classList.add("open");
    field.value = "";
    field.focus();
  }
  function closeCmd() { cmd.classList.remove("open"); }
  document.addEventListener("keydown", (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
      e.preventDefault();
      cmd.classList.contains("open") ? closeCmd() : openCmd();
    }
    if (e.key === "Escape") closeCmd();
  });
  cmd.addEventListener("click", (e) => { if (e.target === cmd) closeCmd(); });
  field.addEventListener("input", () => {
    const q = field.value.toLowerCase();
    list.querySelectorAll("a").forEach((a) => {
      a.style.display = a.textContent.toLowerCase().includes(q) ? "" : "none";
    });
  });

  document.querySelectorAll("a[href='#']").forEach((el) => {
    el.addEventListener("click", (e) => {
      if (el.getAttribute("href") === "#") e.preventDefault();
    });
  });

  document.querySelectorAll("[data-store]").forEach((el) => {
    if (!el.getAttribute("href") || el.getAttribute("href") === "#") {
      el.addEventListener("click", (e) => {
        e.preventDefault();
        alert("Paste the live store URL in the slot under this button when Apple or Google issues it.");
      });
    }
  });

  document.querySelectorAll("[data-social]").forEach((el) => {
    if (!el.getAttribute("href") || el.getAttribute("href") === "#") {
      el.addEventListener("click", (e) => {
        e.preventDefault();
        el.classList.add("awaiting");
        const label = el.getAttribute("aria-label") || "this channel";
        alert("Drop your " + label + " URL here when the channel is live. The button is already wired.");
      });
    }
  });

  const form = document.querySelector("[data-start-form]");
  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      form.innerHTML = "<p class='lede'>Received. When Stripe is connected, this becomes checkout. For now we have your name and the path you chose.</p>";
    });
  }

  const INQUIRE = "groups@walksteadfast.com";
  document.querySelectorAll("[data-inquire-form]").forEach((form) => {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const data = Object.fromEntries(new FormData(form).entries());
      const body = Object.entries(data).map(([k, v]) => k + ": " + v).join("\n");
      const href = "mailto:" + INQUIRE
        + "?subject=" + encodeURIComponent("Group delivery inquiry")
        + "&body=" + encodeURIComponent(body);
      form.innerHTML = "<p class='lede'>Your mail app should open to " + INQUIRE + ". If it does not, write that address and send the same note.</p>";
      location.href = href;
    });
  });
});
