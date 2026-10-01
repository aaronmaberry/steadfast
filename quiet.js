(function () {
  var form = document.querySelector("[data-quiet-form]");
  if (!form) return;
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var data = new FormData(form);
    var row = {
      at: new Date().toISOString(),
      name: data.get("name") || "",
      email: data.get("email") || "",
      church: data.get("church") || "",
      door: data.get("door") || "man"
    };
    try {
      var key = "steadfast-quiet-leads";
      var list = JSON.parse(localStorage.getItem(key) || "[]");
      list.push(row);
      localStorage.setItem(key, JSON.stringify(list));
    } catch (err) {}
    var ok = form.querySelector("[data-quiet-ok]");
    if (ok) ok.hidden = false;
    form.querySelectorAll("input, button").forEach(function (el) {
      if (el.type !== "hidden") el.disabled = true;
    });
    var subject = encodeURIComponent("Quiet page · " + row.door + " · " + row.name);
    var body = encodeURIComponent(
      "Name: " + row.name + "\nEmail: " + row.email + "\nChurch: " + row.church + "\nDoor: " + row.door
    );
    window.location.href = "mailto:groups@walksteadfast.com?subject=" + subject + "&body=" + body;
  });
})();
