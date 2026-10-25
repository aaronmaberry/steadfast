package com.walksteadfast.app.data

import android.app.Application
import android.content.Context
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.AndroidViewModel
import com.walksteadfast.app.Config
import org.json.JSONObject
import java.net.URL
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class DevotionStore(app: Application) : AndroidViewModel(app) {
    var today: Devotion by mutableStateOf(bundled())
        private set
    var walkedToday: Boolean by mutableStateOf(false)
        private set
    var streak: Int by mutableIntStateOf(0)
        private set
    var pairName: String by mutableStateOf("")
    var pairPinged: String by mutableStateOf("")

    private val prefs get() = getApplication<Application>().getSharedPreferences("sm", Context.MODE_PRIVATE)

    suspend fun refresh() {
        val remote = withContext(Dispatchers.IO) {
            runCatching {
                URL(Config.DAILY_FEED).readText()
            }.getOrNull()
        }
        val items = parse(remote) ?: parse(assetJson()) ?: emptyList()
        today = pick(items) ?: bundled()
        walkedToday = prefs.getBoolean(walkKey(), false)
        streak = prefs.getInt("streak", 0)
        pairName = prefs.getString("pairName", "") ?: ""
        pairPinged = prefs.getString("pairPing", "") ?: ""
    }

    fun savePair(name: String) {
        pairName = name.trim()
        prefs.edit().putString("pairName", pairName).apply()
    }

    fun pingPair() {
        pairPinged = SimpleDateFormat("MMM d, h:mm a", Locale.US).format(Date())
        prefs.edit().putString("pairPing", pairPinged).apply()
    }

    fun markWalked() {
        if (walkedToday) return
        val last = prefs.getString("lastWalk", "")
        val nextStreak = if (last == yesterday()) streak + 1 else 1
        prefs.edit()
            .putBoolean(walkKey(), true)
            .putString("lastWalk", today.date)
            .putInt("streak", nextStreak)
            .apply()
        walkedToday = true
        streak = nextStreak
    }

    private fun walkKey() = "walked." + todayKey()

    private fun assetJson(): String? = runCatching {
        getApplication<Application>().assets.open("daily.json").bufferedReader().readText()
    }.getOrNull()

    companion object {
        private val fmt = SimpleDateFormat("yyyy-MM-dd", Locale.US)

        fun todayKey(): String = fmt.format(Date())

        fun yesterday(): String {
            val cal = java.util.Calendar.getInstance()
            cal.add(java.util.Calendar.DAY_OF_YEAR, -1)
            return fmt.format(cal.time)
        }

        fun pick(items: List<Devotion>): Devotion? {
            val key = todayKey()
            return items.firstOrNull { it.date == key } ?: items.maxByOrNull { it.date }
        }

        fun parse(raw: String?): List<Devotion>? {
            if (raw.isNullOrBlank()) return null
            return runCatching {
                val arr = JSONObject(raw).getJSONArray("items")
                buildList {
                    for (i in 0 until arr.length()) {
                        val o = arr.getJSONObject(i)
                        add(
                            Devotion(
                                date = o.optString("date"),
                                title = o.optString("title"),
                                verse = o.optString("verse"),
                                body = o.optString("body"),
                                videoURL = o.optString("videoURL"),
                                imageURL = o.optString("imageURL"),
                                reflection = o.optString("reflection"),
                                silentLine = o.optString("silentLine")
                            )
                        )
                    }
                }
            }.getOrNull()
        }

        fun bundled() = Devotion(
            date = todayKey(),
            title = "Stand still before you stride",
            verse = "“Be watchful, stand firm in the faith, act like men, be strong. Let all that you do be done in love.” — 1 Corinthians 16:13–14",
            body = "A steadfast man does not confuse motion with obedience. Before the meeting — stand. Watch. Then walk."
        )
    }
}
