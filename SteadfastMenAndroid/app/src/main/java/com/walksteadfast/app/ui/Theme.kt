package com.walksteadfast.app.ui

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

val Bg = Color(0xFF07070A)
val Surface = Color(0xFF121218)
val Text = Color(0xFFF4F4F5)
val Muted = Color(0xFFA1A1AA)
val Accent = Color(0xFF8B9CFF)
val Accent2 = Color(0xFF5B6EF5)
val IndigoCard = Color(0xFF1A2A4A)

val Navy = Bg
val Navy2 = Surface
val Bone = Text
val Brass = Accent

@Composable
fun SteadfastTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = darkColorScheme(
            background = Bg,
            surface = Surface,
            primary = Accent,
            onPrimary = Text,
            onBackground = Text,
            onSurface = Text
        ),
        content = content
    )
}
