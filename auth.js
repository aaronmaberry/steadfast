/* Client-side gate only. Never put credentials here: this file is public. Stays closed until real member auth replaces it. */
(function () {
  const KEY = "sm-auth";
  const ACCOUNTS = {};

  window.SMAuth = {
    session() {
      let sess = null;
      try { sess = JSON.parse(localStorage.getItem(KEY) || "null"); } catch { return null; }
      return sess && Object.prototype.hasOwnProperty.call(ACCOUNTS, sess.email) ? sess : null;
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
