/* Paywall door. Sign-in is checked on the server (api/login.js), which sets a signed HttpOnly cookie.
   Paid files under /private/ are gated by middleware.js on that cookie. This file only keeps the page UX. */
(function () {
  const KEY = "sm-auth";
  window.SMAuth = {
    session() {
      let sess = null;
      try { sess = JSON.parse(localStorage.getItem(KEY) || "null"); } catch { return null; }
      return sess && sess.server && sess.email ? sess : null;
    },
    async login(email, password) {
      let r;
      try {
        r = await fetch("/api/login", {
          method: "POST", credentials: "same-origin",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: (email || "").trim(), password: password || "" })
        });
      } catch { return null; }
      if (!r.ok) return null;
      const data = await r.json().catch(() => null);
      if (!data || !data.ok) return null;
      const sess = { email: data.email, role: data.role, ent: data.ent, server: true, at: Date.now() };
      localStorage.setItem(KEY, JSON.stringify(sess));
      return sess;
    },
    logout() {
      localStorage.removeItem(KEY);
      return fetch("/api/logout", { method: "POST", credentials: "same-origin" }).catch(() => {});
    },
    require(next) {
      if (this.session()) return true;
      const dest = next || (location.pathname.split("/").pop() || "program.html");
      location.href = "login.html?next=" + encodeURIComponent(dest);
      return false;
    }
  };

  document.addEventListener("click", async (e) => {
    const a = e.target.closest("#logout");
    if (!a) return;
    e.preventDefault();
    await SMAuth.logout();
    location.href = "login.html";
  });
})();
