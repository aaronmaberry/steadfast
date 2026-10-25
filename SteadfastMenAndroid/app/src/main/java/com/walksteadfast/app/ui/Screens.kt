package com.walksteadfast.app.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.ui.Alignment
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.unit.dp
import androidx.compose.foundation.Image
import com.walksteadfast.app.R
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Switch
import androidx.compose.material3.SwitchDefaults
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.material3.TextFieldDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.viewinterop.AndroidView
import android.webkit.WebView
import android.webkit.WebViewClient

@Composable
fun InAppWeb(url: String, modifier: Modifier = Modifier) {
    AndroidView(
        factory = { ctx ->
            WebView(ctx).apply {
                webViewClient = WebViewClient()
                settings.javaScriptEnabled = true
                loadUrl(url)
            }
        },
        modifier = modifier.fillMaxSize()
    )
}
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.walksteadfast.app.Config
import com.walksteadfast.app.data.DevotionStore
import com.walksteadfast.app.data.Product
import com.walksteadfast.app.data.Social
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

@Composable
fun TodayScreen(store: DevotionStore, openUrl: (String) -> Unit, modifier: Modifier) {
    val d = store.today
    Column(
        modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(24.dp)
    ) {
        Text("Today", color = Muted, fontSize = 13.sp)
        Spacer(Modifier.height(4.dp))
        Text(greeting(), color = Text, fontSize = 24.sp)
        Spacer(Modifier.height(14.dp))
        Box(
            Modifier
                .fillMaxWidth()
                .height(340.dp)
                .clip(RoundedCornerShape(18.dp))
        ) {
            Image(
                painter = painterResource(R.drawable.social_banner),
                contentDescription = null,
                contentScale = ContentScale.Crop,
                modifier = Modifier.fillMaxSize()
            )
            Box(Modifier.fillMaxSize().background(Color.Black.copy(alpha = 0.58f)))
            Column(Modifier.padding(20.dp)) {
                Text("TODAY’S TEXT", color = Color.White.copy(alpha = 0.72f), fontSize = 11.sp, letterSpacing = 1.2.sp)
                Spacer(Modifier.height(12.dp))
                Row(verticalAlignment = Alignment.Top) {
                    Box(Modifier.width(4.dp).height(72.dp).background(Accent, RoundedCornerShape(2.dp)))
                    Spacer(Modifier.width(14.dp))
                    Text(versePlain(d.verse), color = Color.White, fontSize = 20.sp, lineHeight = 28.sp)
                }
                if (verseRef(d.verse).isNotEmpty()) {
                    Spacer(Modifier.height(10.dp))
                    Text(verseRef(d.verse), color = Color.White.copy(alpha = 0.62f), fontSize = 12.sp, modifier = Modifier.padding(start = 18.dp))
                }
                if (d.reflection.isNotBlank()) {
                    Spacer(Modifier.height(16.dp))
                    Text(d.reflection, color = Color.White, fontSize = 16.sp, lineHeight = 22.sp)
                }
                if (d.silentLine.isNotBlank()) {
                    Spacer(Modifier.height(8.dp))
                    Text(d.silentLine, color = Color.White.copy(alpha = 0.78f), fontSize = 14.sp, lineHeight = 20.sp)
                }
            }
        }
        Spacer(Modifier.height(16.dp))
        Text(d.title, color = Text, fontSize = 28.sp, lineHeight = 34.sp)
        if (store.walkedToday) {
            Spacer(Modifier.height(8.dp))
            Text("Walked today · ${store.streak} day streak", color = Brass, fontSize = 13.sp)
        }
        Spacer(Modifier.height(16.dp))
        Text(d.verse, color = Bone.copy(alpha = 0.88f), fontSize = 20.sp, fontFamily = FontFamily.Serif, fontStyle = FontStyle.Italic)
        Spacer(Modifier.height(16.dp))
        Text(d.body, color = Bone.copy(alpha = 0.72f), fontSize = 17.sp, lineHeight = 26.sp)
        Spacer(Modifier.height(24.dp))
        if (d.videoURL.isNotBlank()) {
            BrassButton("Watch today’s film") { openUrl(d.videoURL) }
            Spacer(Modifier.height(10.dp))
        }
        BrassButton(if (store.walkedToday) "Walked." else "I walked this morning") { store.markWalked() }
        Spacer(Modifier.height(20.dp))
        PairBlock(store, openUrl)
        Spacer(Modifier.height(12.dp))
        Text(
            "Open the daily page on the site",
            color = Brass,
            modifier = Modifier.clickable { openUrl(Config.DAILY_WEB) }
        )
    }
}

@Composable
fun PathScreen(openUrl: (String) -> Unit, modifier: Modifier) {
    var member by remember { mutableStateOf(false) }
    var webUrl by remember { mutableStateOf<String?>(null) }
    val weeks = listOf(
        "01" to "Name the drift in your own house.",
        "02" to "Stop waiting for someone else to captain the room.",
        "03" to "Put the phone down at the table.",
        "04" to "Tell the truth about the quiet sins.",
        "05" to "Show up to church as a man, not a guest.",
        "06" to "Close the first mark.",
        "07" to "Write what is yours.",
        "08" to "Provide without theater.",
        "09" to "Confess what you have left half-done.",
        "10" to "Carry the calendar of your house.",
        "11" to "Make a plan a boy can see.",
        "12" to "Close the second mark.",
        "13" to "Go first in the hard conversation.",
        "14" to "Pray out loud where your people can hear it.",
        "15" to "Protect what you will not joke about.",
        "16" to "Discipline without rage.",
        "17" to "Lead when it costs you the easy room.",
        "18" to "Close the third mark.",
        "19" to "Lift your eyes past payday.",
        "20" to "Work as worship, not as a brand.",
        "21" to "Stay when leaving would be simpler.",
        "22" to "Bless your son with a future, not a mood.",
        "23" to "Hold the greater city in view.",
        "24" to "Finish. Begin again as a different man."
    )
    Column(
        modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(24.dp)
    ) {
        Text("The path", color = Text, fontSize = 32.sp)
        Spacer(Modifier.height(8.dp))
        Text("Sign in if you bought the 24 lessons. An ebook or audiobook on its own does not use this door. Those files go to the email on the receipt. The daily walk is free.", color = Muted, fontSize = 14.sp)
        Spacer(Modifier.height(16.dp))
        if (!member) {
            BrassButton("I bought the 24 lessons") { member = true }
            Spacer(Modifier.height(8.dp))
            Text("Bought only the book? Check the receipt email.", color = Muted, fontSize = 13.sp)
            Spacer(Modifier.height(8.dp))
            Text("Sign in", color = Brass, modifier = Modifier.clickable { webUrl = Config.LOGIN })
        } else {
            Text("IN THE PLAN", color = Accent, fontSize = 11.sp, letterSpacing = 0.8.sp)
            Spacer(Modifier.height(8.dp))
            Text("Audiobook player", color = Text, fontSize = 20.sp)
            Text("Play", color = Muted, fontSize = 14.sp, modifier = Modifier.clickable { webUrl = Config.PROGRAM })
            Spacer(Modifier.height(8.dp))
            Text("Ebook is not read here. Path on the web, or the receipt if you only bought the file.", color = Muted, fontSize = 14.sp)
            Spacer(Modifier.height(8.dp))
            Text("Lead a room · scripts and bulk paper", color = Text, modifier = Modifier.clickable { openUrl(Config.GROUP_KIT) })
            Spacer(Modifier.height(16.dp))
            weeks.forEach { (n, title) ->
                Column(
                    Modifier
                        .fillMaxWidth()
                        .padding(bottom = 8.dp)
                        .background(Navy2)
                        .clickable { webUrl = Config.week(n) }
                        .padding(16.dp)
                ) {
                    Text("LESSON $n", color = Accent, fontSize = 11.sp)
                    Text(title, color = Text, fontSize = 16.sp)
                }
            }
        }
        webUrl?.let { url ->
            Spacer(Modifier.height(12.dp))
            InAppWeb(url, Modifier.height(560.dp))
        }
    }
}

@Composable
fun GiveScreen(openUrl: (String) -> Unit, modifier: Modifier) {
    Column(
        modifier
            .fillMaxWidth()
            .padding(bottom = 16.dp)
    ) {
        Text("Support", color = Text, fontSize = 28.sp)
        Spacer(Modifier.height(8.dp))
        Text("Help us expand the mission and make steadfast men.", color = Text, fontSize = 18.sp)
        Spacer(Modifier.height(8.dp))
        Text("Visit the website to see ways to help contribute. Your support helps us reach more men who need this content.", color = Muted, fontSize = 15.sp)
        Spacer(Modifier.height(14.dp))
        BrassButton("See ways to contribute") { openUrl(Config.GIVE) }
    }
}

@Composable
fun MoreScreen(openUrl: (String) -> Unit, modifier: Modifier) {
    val socials = listOf(
        Social("YouTube", Config.YOUTUBE),
        Social("Instagram", Config.INSTAGRAM),
        Social("X", Config.X),
        Social("Facebook", Config.FACEBOOK),
        Social("TikTok", Config.TIKTOK),
        Social("Podcast", Config.PODCAST)
    )
    Column(
        modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(24.dp)
    ) {
        Text("The house", color = Bone, fontSize = 32.sp, fontFamily = FontFamily.Serif)
        Spacer(Modifier.height(12.dp))
        LinkCard("Website", Config.SITE, openUrl)
        LinkCard("Privacy · the pair", Config.PRIVACY, openUrl)
        LinkCard("Daily on the web", Config.DAILY_WEB, openUrl)
        LinkCard("Training", Config.TRAINING, openUrl)
        LinkCard("The book", Config.BOOK, openUrl)
        Spacer(Modifier.height(18.dp))
        Text("SOCIAL", color = Brass, fontSize = 11.sp, letterSpacing = 1.2.sp)
        Spacer(Modifier.height(8.dp))
        socials.forEach { s ->
            LinkCard(s.name, s.url.ifBlank { Config.SITE }, openUrl, if (s.url.isBlank()) "Add URL" else "Open")
        }
    }
}

@Composable
private fun LinkCard(title: String, url: String, openUrl: (String) -> Unit, hint: String? = null) {
    Column(
        Modifier
            .fillMaxWidth()
            .padding(bottom = 8.dp)
            .background(Navy2)
            .clickable { openUrl(url) }
            .padding(16.dp)
    ) {
        Text(title, color = Bone, fontSize = 20.sp, fontFamily = FontFamily.Serif)
        if (hint != null) Text(hint, color = Brass, fontSize = 12.sp)
    }
}

@Composable
private fun PairBlock(store: DevotionStore, openUrl: (String) -> Unit) {
    var draft by remember { mutableStateOf(store.pairName) }
    Column(
        Modifier
            .fillMaxWidth()
            .background(IndigoCard)
            .padding(18.dp)
    ) {
        Text("THE PAIR · SIX LESSONS", color = Accent, fontSize = 11.sp, letterSpacing = 0.8.sp)
        Spacer(Modifier.height(8.dp))
        Text("One brother. No board.", color = Text, fontSize = 22.sp)
        Spacer(Modifier.height(8.dp))
        Text(
            "Name one man for this mark. Midweek you ask: did you do the act? The table only hears done. Shame stays off the stage.",
            color = Muted,
            fontSize = 14.sp,
            lineHeight = 20.sp
        )
        Spacer(Modifier.height(12.dp))
        TextField(
            value = draft,
            onValueChange = { draft = it },
            placeholder = { Text("His first name") },
            modifier = Modifier.fillMaxWidth(),
            colors = TextFieldDefaults.colors()
        )
        Spacer(Modifier.height(10.dp))
        BrassButton("Save the pair") { store.savePair(draft) }
        Spacer(Modifier.height(8.dp))
        BrassButton("Ask him: did you do the act?") {
            store.savePair(draft)
            store.pingPair()
            val body = java.net.URLEncoder.encode("Did you do the act this week? Phone down at the table. — Steadfast", "UTF-8")
            openUrl("sms:?body=$body")
        }
        if (store.pairPinged.isNotBlank()) {
            Spacer(Modifier.height(8.dp))
            Text("Last ping ${store.pairPinged}. Still just you two.", color = Muted, fontSize = 12.sp)
        }
    }
}

@Composable
private fun BrassButton(label: String, onClick: () -> Unit) {
    Button(
        onClick = onClick,
        modifier = Modifier.fillMaxWidth().height(50.dp),
        colors = ButtonDefaults.buttonColors(containerColor = Brass, contentColor = Navy)
    ) { Text(label) }
}

@Composable
fun WordScreen(store: DevotionStore, openUrl: (String) -> Unit, modifier: Modifier) {
    Column(modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(24.dp)) {
        Text("Word", color = Text, fontSize = 28.sp)
        Spacer(Modifier.height(12.dp))
        Text(store.today.verse, color = Text, fontSize = 18.sp, lineHeight = 26.sp)
        Spacer(Modifier.height(16.dp))
        Text(store.today.body, color = Muted, fontSize = 16.sp, lineHeight = 24.sp)
        Spacer(Modifier.height(20.dp))
        BrassButton("Open daily on the site") { openUrl(Config.DAILY_WEB) }
    }
}

@Composable
fun DiscoverScreen(openUrl: (String) -> Unit, modifier: Modifier) {
    val tiles = listOf(
        "Training" to Config.TRAINING,
        "Book" to Config.BOOK,
        "Groups" to Config.GROUPS,
        "Merch" to Config.MERCH,
        "Daily" to Config.DAILY_WEB,
        "The table" to Config.SITE
    )
    Column(modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(24.dp)) {
        Text("Discover", color = Text, fontSize = 28.sp)
        Spacer(Modifier.height(12.dp))
        tiles.forEach { (title, url) ->
            Text(
                title,
                color = Text,
                fontSize = 18.sp,
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(bottom = 8.dp)
                    .background(Surface)
                    .clickable { openUrl(url) }
                    .padding(18.dp)
            )
        }
    }
}

@Composable
fun YouScreen(store: DevotionStore, openUrl: (String) -> Unit, modifier: Modifier) {
    Column(modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(24.dp)) {
        Text("You", color = Text, fontSize = 28.sp)
        Spacer(Modifier.height(8.dp))
        Text("Walk streak · ${store.streak}", color = Muted)
        Spacer(Modifier.height(16.dp))
        PairBlock(store, openUrl)
        Spacer(Modifier.height(16.dp))
        GiveScreen(openUrl, Modifier)
        MoreScreen(openUrl, Modifier)
    }
}

private fun headerDate(): String =
    SimpleDateFormat("EEEE, MMMM d", Locale.US).format(Date()).uppercase(Locale.US)

private fun greeting(): String {
    val h = SimpleDateFormat("H", Locale.US).format(Date()).toInt()
    val w = if (h < 12) "morning" else if (h < 17) "afternoon" else "evening"
    return "Good $w"
}

private fun versePlain(raw: String): String {
    var s = raw.replace("“", "\"").replace("”", "\"")
    val cut = s.indexOf(" — ")
    if (cut >= 0) s = s.substring(0, cut)
    return s.trim().trim('"')
}

private fun verseRef(raw: String): String {
    val cut = raw.indexOf(" — ")
    if (cut < 0) return ""
    var tail = raw.substring(cut + 3).trim()
    if (!tail.contains("NIV", ignoreCase = true)) tail += " NIV"
    return tail
}
