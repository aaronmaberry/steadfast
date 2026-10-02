(function (root, factory) {
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.DailyEngage = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  var DATE = /^\d{4}-\d{2}-\d{2}$/;
  var LIKES_KEY = "steadfast.daily.likes";
  var NOTES_KEY = "steadfast.daily.notes";
  var adapter = null;

  function assertDate(date) {
    var value = String(date || "");
    if (!DATE.test(value)) throw new Error("Daily date must be YYYY-MM-DD");
    return value;
  }

  function buildDailyShareUrl(origin, date) {
    var day = assertDate(date);
    var base = String(origin || "").replace(/\/+$/, "");
    if (!base) throw new Error("origin required");
    return base + "/daily?day=" + day;
  }

  function parseDailyDay(search, hash) {
    var query = "";
    try {
      query = new URLSearchParams(String(search || "").replace(/^\?/, "")).get("day") || "";
    } catch (err) {
      query = "";
    }
    if (DATE.test(query)) return query;
    var raw = String(hash || "").replace(/^#/, "");
    var match = raw.match(/(?:^|[?&])day=(\d{4}-\d{2}-\d{2})\b/);
    if (match) return match[1];
    if (DATE.test(raw)) return raw;
    return null;
  }

  function readMap(storage, key) {
    try {
      var raw = storage.getItem(key);
      if (!raw) return {};
      var parsed = JSON.parse(raw);
      if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) return {};
      return parsed;
    } catch (err) {
      return {};
    }
  }

  function writeMap(storage, key, map) {
    storage.setItem(key, JSON.stringify(map));
  }

  function createStorageAdapter(storage) {
    if (!storage || typeof storage.getItem !== "function" || typeof storage.setItem !== "function") {
      throw new Error("storage adapter requires getItem and setItem");
    }
    return {
      getLike: function (date) {
        var day = assertDate(date);
        return Promise.resolve(!!readMap(storage, LIKES_KEY)[day]);
      },
      setLike: function (date, liked) {
        var day = assertDate(date);
        var map = readMap(storage, LIKES_KEY);
        if (liked) map[day] = true;
        else delete map[day];
        writeMap(storage, LIKES_KEY, map);
        return Promise.resolve(!!liked);
      },
      getNote: function (date) {
        var day = assertDate(date);
        var note = readMap(storage, NOTES_KEY)[day];
        return Promise.resolve(typeof note === "string" ? note : "");
      },
      setNote: function (date, text) {
        var day = assertDate(date);
        var map = readMap(storage, NOTES_KEY);
        var value = String(text == null ? "" : text);
        if (value) map[day] = value;
        else delete map[day];
        writeMap(storage, NOTES_KEY, map);
        return Promise.resolve(value);
      }
    };
  }

  function memoryStorage() {
    var data = Object.create(null);
    return {
      getItem: function (key) {
        return Object.prototype.hasOwnProperty.call(data, key) ? data[key] : null;
      },
      setItem: function (key, value) {
        data[key] = String(value);
      }
    };
  }

  function browserStorage() {
    try {
      if (typeof localStorage !== "undefined" && localStorage) return localStorage;
    } catch (err) {}
    return memoryStorage();
  }

  function currentAdapter() {
    if (!adapter) adapter = createStorageAdapter(browserStorage());
    return adapter;
  }

  function setAdapter(next) {
    adapter = next || null;
  }

  return {
    buildDailyShareUrl: buildDailyShareUrl,
    parseDailyDay: parseDailyDay,
    createStorageAdapter: createStorageAdapter,
    memoryStorage: memoryStorage,
    setAdapter: setAdapter,
    getLike: function (date) { return currentAdapter().getLike(date); },
    setLike: function (date, liked) { return currentAdapter().setLike(date, liked); },
    getNote: function (date) { return currentAdapter().getNote(date); },
    setNote: function (date, text) { return currentAdapter().setNote(date, text); }
  };
});
