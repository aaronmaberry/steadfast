const AsyncStorage = require("@react-native-async-storage/async-storage").default;
const engage = require("./dailyEngage");

const KEYS = ["steadfast.daily.likes", "steadfast.daily.comments", "steadfast.daily.name"];
const cache = Object.create(null);
let hydrated = false;
let pending = null;

function facade() {
  return {
    getItem: function (key) {
      return Object.prototype.hasOwnProperty.call(cache, key) ? cache[key] : null;
    },
    setItem: function (key, value) {
      cache[key] = String(value);
      AsyncStorage.setItem(key, cache[key]).catch(function () {});
    }
  };
}

function hydrateEngage() {
  if (hydrated) return Promise.resolve(engage);
  if (!pending) {
    pending = Promise.all(KEYS.map(function (key) {
      return AsyncStorage.getItem(key).then(function (value) {
        if (value != null && !Object.prototype.hasOwnProperty.call(cache, key)) cache[key] = value;
      });
    })).then(function () {
      hydrated = true;
      engage.setAdapter(engage.createStorageAdapter(facade()));
      return engage;
    });
  }
  return pending;
}

module.exports = { hydrateEngage: hydrateEngage };
