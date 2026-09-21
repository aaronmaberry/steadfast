const devotionals = [
  {
    title: "Stand still before you stride",
    verse: "'Be watchful, stand firm in the faith, act like men, be strong. Let all that you do be done in love.', 1 Corinthians 16:13-14",
    body: "A steadfast man does not confuse motion with obedience. Before the meeting, the commute, the argument you already rehearsed, stand. Watch. Then walk."
  },
  {
    title: "Reject the quiet drift",
    verse: "'Therefore we must pay much closer attention to what we have heard, lest we drift away from it.', Hebrews 2:1",
    body: "Most men do not fall in a crash. They ease off the oars. Today, name one place you have gone passive and put your hand back on the work."
  },
  {
    title: "Carry what is yours",
    verse: "'But if anyone does not provide for his relatives, and especially for members of his household, he has denied the faith.', 1 Timothy 5:8",
    body: "Responsibility is not a vibe. It is a name on a bill, a child who needs a father in the room, a word you said you would keep. Pick it up."
  },
  {
    title: "Lead from the front of the table",
    verse: "'Be strong and courageous. Do not be frightened, and do not be dismayed, for the Lord your God is with you wherever you go.', Joshua 1:9",
    body: "Courage is rarely a battlefield. It is the first apology. The first prayer at dinner. The first no that protects your house."
  },
  {
    title: "Work for a better country",
    verse: "'For he was looking forward to the city that has foundations, whose designer and builder is God.', Hebrews 11:10",
    body: "If the only reward you are building toward is comfort, you will fold when comfort is threatened. Lift your eyes. The greater reward holds when payday does not."
  },
  {
    title: "A soft answer is not a soft man",
    verse: "'A gentle answer turns away wrath, but a harsh word stirs up anger.', Proverbs 15:1",
    body: "Steadfast is not loud. Strength that cannot be quiet is just ungoverned heat. Practice one gentle sentence in the hardest room of your day."
  },
  {
    title: "Finish the small obedience",
    verse: "'His master said to him, 'Well done, good and faithful servant.'', Matthew 25:21",
    body: "You do not become a steadfast man by intending a better decade. You become one by completing this morning's assignment. Close the loop."
  },
  {
    title: "Put your house in order",
    verse: "'Set your house in order, for you shall die; you shall not recover.', Isaiah 38:1",
    body: "Mortality makes a man honest. What would your son inherit tonight besides unfinished sentences? Write one thing down and finish it."
  },
  {
    title: "Love is a decision with a spine",
    verse: "'Husbands, love your wives, as Christ loved the church and gave himself up for her.', Ephesians 5:25",
    body: "Affection is easy when she is easy. Covenant shows up when the room is cold. Give yourself up in one concrete way before noon."
  },
  {
    title: "Do not despise the small start",
    verse: "'For whoever has despised the day of small things shall rejoice.', Zechariah 4:10",
    body: "Twenty-four weeks looks long until you have done week one. Open the passage. Do the act. Tomorrow can have tomorrow."
  },
  {
    title: "Watch your mouth in your own house",
    verse: "'Let no corrupting talk come out of your mouths, but only such as is good for building up.', Ephesians 4:29",
    body: "The men you are raising will speak like the man they heard at dinner. Bless or rot. There is no third use of the tongue."
  },
  {
    title: "Work as if the Lord is the board",
    verse: "'Whatever you do, work heartily, as for the Lord and not for men.', Colossians 3:23",
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
    let plain = String(d.verse || "").replace(/['']/g, '"').trim();
    plain = plain.replace(/^"+|"+$/g, "").split(", ")[0].replace(/\s*\([^)]*NIV\)\s*$/, "").trim();
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
    root.querySelectorAll("[data-devotion-img]").forEach((el) => { el.src = d.imageURL; });
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
      ? first.slice(0, 180) + (first.length > 180 ? "..." : "")
      : "Table talk on the act for today, then a guided prayer. Open the tile for the whole thing.";
  }
  const st = root.querySelector("[data-devotion-silent-tease]");
  if (st) {
    const first = String(d.silentBody || d.body || "").split(/\n\n+/)[0].trim();
    st.textContent = first
      ? first.slice(0, 180) + (first.length > 180 ? "..." : "")
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

const SOCIAL_ICON = {
  youtube: '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M23.5 6.2a3 3 0 0 0-2.1-2.2C19.5 3.6 12 3.6 12 3.6s-7.5 0-9.4.4A3 3 0 0 0 .5 6.2 31.5 31.5 0 0 0 0 12a31.5 31.5 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.2c1.9.4 9.4.4 9.4.4s7.5 0 9.4-.4a3 3 0 0 0 2.1-2.2A31.5 31.5 0 0 0 24 12a31.5 31.5 0 0 0-.5-5.8zM9.8 15.6V8.4L15.8 12z"/></svg>',
  instagram: '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M7 2h10a5 5 0 0 1 5 5v10a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5V7a5 5 0 0 1 5-5zm10 2H7a3 3 0 0 0-3 3v10a3 3 0 0 0 3 3h10a3 3 0 0 0 3-3V7a3 3 0 0 0-3-3zm-5 3.5A4.5 4.5 0 1 1 7.5 12 4.5 4.5 0 0 1 12 7.5zm0 2A2.5 2.5 0 1 0 14.5 12 2.5 2.5 0 0 0 12 9.5zM17.8 6.2a1.1 1.1 0 1 1-1.1 1.1 1.1 1.1 0 0 1 1.1-1.1z"/></svg>',
  x: '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M18.9 2H22l-6.8 7.8L23 22h-7.2l-5-6.6L5.2 22H2l7.3-8.4L1 2h7.4l4.6 6.1zm-1.3 18h2L6.5 3.9H4.3z"/></svg>',
  facebook: '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M14 9h3V6h-3c-2.2 0-4 1.8-4 4v2H8v3h2v7h3v-7h2.6l.4-3H13v-2c0-.6.4-1 1-1z"/></svg>',
  tiktok: '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M14.2 3c.4 2.6 1.8 4.3 4.3 4.6v2.6c-1.5 0-2.9-.5-4.2-1.4v6.6A6.4 6.4 0 1 1 8.8 9v2.7a3.8 3.8 0 1 0 2.7 3.6V3z"/></svg>'
};

function applyLinks(cfg) {
  if (!cfg) return;
  document.querySelectorAll("[data-social-dock]").forEach((nav) => {
    nav.replaceChildren();
    (cfg.socials || []).forEach((s) => {
      const a = document.createElement("a");
      a.className = "soc";
      a.href = s.href;
      a.rel = "noopener";
      a.target = "_blank";
      a.setAttribute("aria-label", s.label);
      a.title = s.label;
      a.innerHTML = SOCIAL_ICON[s.id] || "";
      nav.appendChild(a);
    });
  });
  const landings = [
    ["home", "Home", "index.html"],
    ["book", "Book", "book.html"],
    ["training", "Training", "training.html"],
    ["show", "Show", "listen.html"],
    ["about", "About", "about.html"],
    ["contact", "Contact", "contact.html"]
  ];
  document.querySelectorAll("[data-landing-links]").forEach((nav) => {
    nav.replaceChildren();
    landings.forEach((row) => {
      const a = document.createElement("a");
      a.setAttribute("data-cta", row[0]);
      a.href = row[2];
      a.textContent = row[1];
      nav.appendChild(a);
    });
  });
  document.querySelectorAll("[data-social-links]").forEach((nav) => {
    nav.replaceChildren();
    if (cfg.hub) {
      const hub = document.createElement("a");
      hub.href = cfg.hub;
      hub.textContent = "Hub";
      nav.appendChild(hub);
    }
    (cfg.socials || []).forEach((s) => {
      const a = document.createElement("a");
      a.href = s.href;
      a.textContent = s.label || s.id;
      a.rel = "noopener";
      a.target = "_blank";
      nav.appendChild(a);
    });
  });
  document.querySelectorAll("[data-social]").forEach((el) => {
    const id = el.getAttribute("data-social");
    const match = (cfg.socials || []).find((s) => s.id === id);
    if (match && match.href) el.setAttribute("href", match.href);
  });
  const host = location.hostname;
  const onHub = host === "walksteadfast.com" || host === "www.walksteadfast.com";
  if (!onHub) return;
  document.querySelectorAll("[data-cta]").forEach((el) => {
    const href = cfg.ctas && cfg.ctas[el.getAttribute("data-cta")];
    if (href) el.setAttribute("href", href);
  });
}

function renderLinks() {
  fetch("app/links.json", { cache: "no-store" })
    .then((r) => (r.ok ? r.json() : Promise.reject()))
    .then(applyLinks)
    .catch(() => {});
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
  function lockPage() {
    sheetScrollY = window.scrollY || 0;
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
    window.scrollTo(0, sheetScrollY);
  }
  function closeSheets() {
    document.querySelectorAll(".sheet").forEach((el) => {
      el.hidden = true;
      const card = el.querySelector(".sheet-card");
      if (card) {
        card.style.transform = "";
        card.style.transition = "";
      }
    });
    unlockPage();
  }
  document.querySelectorAll("[data-open-sheet]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const id = "sheet-" + btn.getAttribute("data-open-sheet");
      const sheet = document.getElementById(id);
      if (!sheet) return;
      closeSheets();
      sheet.hidden = false;
      lockPage();
      sheet.querySelector(".sheet-card")?.scrollTo(0, 0);
    });
  });
  document.querySelectorAll("[data-close-sheet]").forEach((btn) => {
    btn.addEventListener("click", closeSheets);
  });
  document.querySelectorAll(".sheet").forEach((sheet) => {
    const card = sheet.querySelector(".sheet-card");
    sheet.addEventListener("click", (e) => { if (e.target === sheet) closeSheets(); });
    if (!card) return;
    let startY = 0, lastY = 0, lastT = 0, dragging = false, decided = false, dismissDrag = false;
    function resetCard() {
      card.style.transition = "transform .22s ease";
      card.style.transform = "translateY(0)";
    }
    function onStart(y) {
      startY = lastY = y;
      lastT = performance.now();
      dragging = true;
      decided = false;
      dismissDrag = false;
      card.style.transition = "none";
    }
    function onMove(y, ev) {
      if (!dragging) return;
      const dy = y - startY;
      const atTop = card.scrollTop <= 1;
      if (!decided) {
        if (Math.abs(dy) < 8) return;
        decided = true;
        dismissDrag = atTop && dy > 0;
      }
      if (!dismissDrag) return;
      if (ev && ev.cancelable) ev.preventDefault();
      lastY = y;
      lastT = performance.now();
      card.style.transform = "translateY(" + Math.max(0, dy) + "px)";
    }
    function onEnd(y) {
      if (!dragging) return;
      dragging = false;
      const dy = y - startY;
      const dt = Math.max(16, performance.now() - lastT);
      const vel = (y - lastY) / dt;
      if (dismissDrag && (dy > 88 || vel > 0.65)) {
        card.style.transition = "transform .2s ease";
        card.style.transform = "translateY(110%)";
        setTimeout(closeSheets, 180);
      } else {
        resetCard();
      }
      dismissDrag = false;
    }
    sheet.addEventListener("touchstart", (e) => {
      const t = e.changedTouches[0];
      if (t) onStart(t.clientY);
    }, { passive: true });
    sheet.addEventListener("touchmove", (e) => {
      const t = e.changedTouches[0];
      if (t) onMove(t.clientY, e);
    }, { passive: false });
    sheet.addEventListener("touchend", (e) => {
      const t = e.changedTouches[0];
      if (t) onEnd(t.clientY);
    }, { passive: true });
    sheet.addEventListener("touchcancel", () => { dragging = false; resetCard(); });
  });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeSheets(); });

  const toggle = document.querySelector(".nav-toggle");
  const links = document.querySelector(".nav-links");
  if (toggle && links) {
    toggle.setAttribute("aria-expanded", "false");
    toggle.addEventListener("click", () => {
      const open = links.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    });
    links.querySelectorAll("a").forEach((a) => {
      a.addEventListener("click", () => {
        links.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.setAttribute("aria-label", "Open menu");
      });
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
  cmd.innerHTML = '<div class="cmd-box"><input placeholder="Go to..." aria-label="Jump"><div data-cmd-list></div></div>';
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

  const form = document.querySelector("[data-start-form]");
  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const data = new FormData(form);
      const name = data.get("name") || "";
      const offer = data.get("offer") || "the path";
      const email = data.get("email") || "";
      const body = "Name: " + name + "\nEmail: " + email + "\nProduct: " + offer;
      form.innerHTML = "<p class='lede'>Received. This form does not charge a card. Your mail app should open to hello@walksteadfast.com with the same note.</p>";
      location.href = "mailto:hello@walksteadfast.com?subject=" + encodeURIComponent("Steadfast Men, " + offer) + "&body=" + encodeURIComponent(body);
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
