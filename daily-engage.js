(function (root, factory) {
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.DailyEngage = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  var DATE = /^\d{4}-\d{2}-\d{2}$/;
  var LIKES_KEY = "steadfast.daily.likes";
  var COMMENTS_KEY = "steadfast.daily.comments";
  var NAME_KEY = "steadfast.daily.name";
  var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
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

  function cleanName(name) {
    return String(name == null ? "" : name).replace(/\s+/g, " ").trim().slice(0, 40);
  }

  function cleanText(text) {
    return String(text == null ? "" : text).replace(/\r\n/g, "\n").trim().slice(0, 500);
  }

  function copyComment(comment) {
    return {
      id: comment.id,
      name: comment.name,
      text: comment.text,
      createdAt: comment.createdAt,
      reported: !!comment.reported
    };
  }

  function normalizeComment(raw) {
    if (!raw || typeof raw !== "object") return null;
    var id = String(raw.id || "").trim();
    var name = cleanName(raw.name);
    var text = cleanText(raw.text);
    var createdAt = Number(raw.createdAt);
    if (!id || !name || !text || !isFinite(createdAt)) return null;
    return {
      id: id,
      name: name,
      text: text,
      createdAt: createdAt,
      reported: !!raw.reported
    };
  }

  function readComments(storage, date) {
    var list = readMap(storage, COMMENTS_KEY)[date];
    if (!Array.isArray(list)) return [];
    return list.map(normalizeComment).filter(Boolean);
  }

  function nextId() {
    return "c" + Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
  }

  function formatRelativeTime(createdAt, now) {
    var then = Number(createdAt);
    var current = Number(now);
    if (!isFinite(then) || !isFinite(current)) return "";
    var delta = current - then;
    if (delta < 0) delta = 0;
    var sec = Math.floor(delta / 1000);
    if (sec < 60) return "just now";
    var min = Math.floor(sec / 60);
    if (min < 60) return min + "m ago";
    var hours = Math.floor(min / 60);
    if (hours < 24) return hours + "h ago";
    var days = Math.floor(hours / 24);
    if (days < 7) return days + "d ago";
    var weeks = Math.floor(days / 7);
    if (weeks < 5) return weeks + "w ago";
    var date = new Date(then);
    return MONTHS[date.getUTCMonth()] + " " + date.getUTCDate();
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
      getComments: function (date) {
        var day = assertDate(date);
        return Promise.resolve(readComments(storage, day).map(copyComment));
      },
      addComment: function (date, draft) {
        var day = assertDate(date);
        var name = cleanName(draft && draft.name);
        var text = cleanText(draft && draft.text);
        if (!name) return Promise.reject(new Error("name required"));
        if (!text) return Promise.reject(new Error("text required"));
        var comment = {
          id: nextId(),
          name: name,
          text: text,
          createdAt: Date.now(),
          reported: false
        };
        var map = readMap(storage, COMMENTS_KEY);
        var list = readComments(storage, day);
        list.push(comment);
        map[day] = list;
        writeMap(storage, COMMENTS_KEY, map);
        return Promise.resolve(copyComment(comment));
      },
      reportComment: function (date, id) {
        var day = assertDate(date);
        var map = readMap(storage, COMMENTS_KEY);
        var list = readComments(storage, day);
        var found = null;
        for (var i = 0; i < list.length; i++) {
          if (list[i].id === String(id || "")) {
            list[i].reported = true;
            found = list[i];
            break;
          }
        }
        if (!found) return Promise.resolve(null);
        map[day] = list;
        writeMap(storage, COMMENTS_KEY, map);
        return Promise.resolve(copyComment(found));
      },
      getDisplayName: function () {
        return Promise.resolve(cleanName(storage.getItem(NAME_KEY) || ""));
      },
      setDisplayName: function (name) {
        var value = cleanName(name);
        storage.setItem(NAME_KEY, value);
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
    formatRelativeTime: formatRelativeTime,
    getLike: function (date) { return currentAdapter().getLike(date); },
    setLike: function (date, liked) { return currentAdapter().setLike(date, liked); },
    getComments: function (date) { return currentAdapter().getComments(date); },
    addComment: function (date, draft) { return currentAdapter().addComment(date, draft); },
    reportComment: function (date, id) { return currentAdapter().reportComment(date, id); },
    getDisplayName: function () { return currentAdapter().getDisplayName(); },
    setDisplayName: function (name) { return currentAdapter().setDisplayName(name); }
  };
});
