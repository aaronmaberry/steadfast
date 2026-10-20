package com.walksteadfast.app.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.GridView
import androidx.compose.material.icons.outlined.Person
import androidx.compose.material.icons.outlined.ShoppingCart
import androidx.compose.material.icons.outlined.WbTwilight
import androidx.compose.material3.Icon
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.NavigationBarItemDefaults
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import com.walksteadfast.app.data.DevotionStore

@Composable
fun SteadfastApp(store: DevotionStore, openUrl: (String) -> Unit) {
    var tab by rememberSaveable { mutableIntStateOf(0) }
    Scaffold(
        containerColor = Bg,
        bottomBar = {
            NavigationBar(containerColor = Surface) {
                val items = listOf(
                    "Daily" to Icons.Outlined.WbTwilight,
                    "Library" to Icons.Outlined.GridView,
                    "Socials" to Icons.Outlined.GridView,
                    "Profile" to Icons.Outlined.Person
                )
                items.forEachIndexed { i, (label, icon) ->
                    NavigationBarItem(
                        selected = tab == i,
                        onClick = { tab = i },
                        icon = { Icon(icon, contentDescription = label) },
                        label = { Text(label) },
                        colors = NavigationBarItemDefaults.colors(
                            selectedIconColor = Text,
                            selectedTextColor = Text,
                            unselectedIconColor = Muted,
                            unselectedTextColor = Muted,
                            indicatorColor = Bg
                        )
                    )
                }
            }
        }
    ) { pad ->
        val mod = Modifier.padding(pad).background(Bg)
        when (tab) {
            0 -> TodayScreen(store, openUrl, mod)
            1 -> PathScreen(openUrl, mod)
            2 -> MoreScreen(openUrl, mod)
            else -> YouScreen(store, openUrl, mod)
        }
    }
}
