package com.walksteadfast.app

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.viewModels
import androidx.compose.runtime.LaunchedEffect
import com.walksteadfast.app.data.DevotionStore
import com.walksteadfast.app.ui.SteadfastApp
import com.walksteadfast.app.ui.SteadfastTheme

class MainActivity : ComponentActivity() {
    private val store: DevotionStore by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            LaunchedEffect(Unit) { store.refresh() }
            SteadfastTheme {
                SteadfastApp(
                    store = store,
                    openUrl = { url ->
                        val target = url.ifBlank { Config.SITE }
                        startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(target)))
                    }
                )
            }
        }
    }
}
