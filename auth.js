/* TEST GATE ONLY. Visible in page source. Replace with Stripe Customer Portal. */
(function () {
  const KEY = "sm-auth";
  const ACCOUNTS = {
    "admin@walksteadfast.com": { pass: "SteadfastTable26", role: "admin" },
    "member@walksteadfast.com": { pass: "WalkThePath26", role: "member" }
  };

  window.SMAuth = {
    session() {
      try { return JSON.parse(localStorage.getItem(KEY) || "null"); } catch { return null; }
    },
    login(email, password) {
      const row = ACCOUNTS[(email || "").trim().toLowerCase()];
      if (!row || row.pass !== password) return null;
      const sess = { email: email.trim().toLowerCase(), role: row.role, at: Date.now() };
      localStorage.setItem(KEY, JSON.stringify(sess));
      return sess;
    },
    logout() {
      localStorage.removeItem(KEY);
    },
    require(next) {
      if (this.session()) return true;
      const dest = next || (location.pathname.split("/").pop() || "program.html");
      location.href = "login.html?next=" + encodeURIComponent(dest);
      return false;
    }
  };

  document.addEventListener("click", (e) => {
    const a = e.target.closest("#logout");
    if (!a) return;
    e.preventDefault();
    SMAuth.logout();
    location.href = "login.html";
  });
})();

