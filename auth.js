/* Accounts are not connected. No passwords live in this file. */
(function () {
  const KEY = "sm-auth";
  try { localStorage.removeItem(KEY); } catch (e) {}

  window.SMAuth = {
    session() { return null; },
    login() { return null; },
    logout() {
      try { localStorage.removeItem(KEY); } catch (e) {}
    },
    require() { return true; }
  };
})();
