package com.xspeen.streamhub

import android.annotation.SuppressLint
import android.app.Activity
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.view.KeyEvent
import android.view.View
import android.view.ViewGroup
import android.view.WindowManager
import android.webkit.ValueCallback
import android.webkit.WebChromeClient
import android.webkit.WebResourceRequest
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.activity.OnBackPressedCallback
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat

/**
 * Single-activity shell that runs the shared StreamHub web app
 * (web/splash.html -> web/landing.html -> web/app.html) inside a WebView.
 *
 * Everything the pages need is enabled here: JavaScript + DOM storage for the
 * profile/theme/preferences, file access from file:// URLs so hls.js can pull
 * live streams from any http/https origin without CORS blocking, cleartext
 * traffic for http:// IPTV feeds, and D-pad key forwarding for Android TV
 * remotes.
 */
class MainActivity : AppCompatActivity() {

    private lateinit var webView: WebView

    private var fileCallback: ValueCallback<Array<Uri>>? = null
    private var customView: View? = null
    private var customViewCallback: WebChromeClient.CustomViewCallback? = null
    private var savedSystemUiVisibility = 0

    private val fileChooserLauncher =
        registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result ->
            val callback = fileCallback
            fileCallback = null
            callback?.onReceiveValue(
                WebChromeClient.FileChooserParams.parseResult(result.resultCode, result.data)
            )
        }

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // Keep the screen on while watching live TV.
        window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
        window.statusBarColor = ContextCompat.getColor(this, R.color.window_bg)
        window.navigationBarColor = ContextCompat.getColor(this, R.color.window_bg)

        webView = WebView(this)
        setContentView(webView)

        webView.settings.apply {
            javaScriptEnabled = true
            domStorageEnabled = true
            databaseEnabled = true
            // Autoplay: streams start as soon as hls.js has the manifest.
            mediaPlaybackRequiresUserGesture = false
            // The pages are served from file:///android_asset/. Explicitly
            // allow file access (default became false on API 30+) and allow
            // file:// pages to fetch any origin, which is what lets hls.js
            // read http:// IPTV playlists and segments without CORS errors.
            allowFileAccess = true
            @Suppress("DEPRECATION")
            allowFileAccessFromFileURLs = true
            @Suppress("DEPRECATION")
            allowUniversalAccessFromFileURLs = true
            // http:// streams loaded from the page must never be blocked.
            mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
            cacheMode = WebSettings.LOAD_DEFAULT
            useWideViewPort = true
            loadWithOverviewMode = true
            setSupportZoom(false)
            builtInZoomControls = false
            displayZoomControls = false
            setGeolocationEnabled(false)
            // Keep the stock user agent: stream CDNs gate on it.
        }

        webView.setBackgroundColor(ContextCompat.getColor(this, R.color.window_bg))
        webView.isFocusable = true
        webView.isFocusableInTouchMode = true

        webView.webViewClient = object : WebViewClient() {
            override fun shouldOverrideUrlLoading(
                view: WebView,
                request: WebResourceRequest
            ): Boolean = !isAssetUrl(request.url.toString())

            @Deprecated("Deprecated in Java")
            override fun shouldOverrideUrlLoading(view: WebView, url: String): Boolean =
                !isAssetUrl(url)
        }

        webView.webChromeClient = object : WebChromeClient() {
            // Profile / background photo pickers inside the settings screens.
            override fun onShowFileChooser(
                view: WebView,
                filePathCallback: ValueCallback<Array<Uri>>,
                fileChooserParams: FileChooserParams
            ): Boolean {
                fileCallback?.onReceiveValue(null)
                fileCallback = filePathCallback
                return try {
                    fileChooserLauncher.launch(fileChooserParams.createIntent())
                    true
                } catch (e: Exception) {
                    fileCallback = null
                    false
                }
            }

            // Fullscreen video: the page's Fullscreen API request arrives here.
            override fun onShowCustomView(
                view: View?,
                callback: CustomViewCallback?
            ) {
                if (customView != null) {
                    callback?.onCustomViewHidden()
                    return
                }
                customView = view ?: return
                customViewCallback = callback
                savedSystemUiVisibility = window.decorView.systemUiVisibility
                addContentView(
                    customView,
                    ViewGroup.LayoutParams(
                        ViewGroup.LayoutParams.MATCH_PARENT,
                        ViewGroup.LayoutParams.MATCH_PARENT
                    )
                )
                @Suppress("DEPRECATION")
                window.decorView.systemUiVisibility =
                    View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY or
                        View.SYSTEM_UI_FLAG_FULLSCREEN or
                        View.SYSTEM_UI_FLAG_HIDE_NAVIGATION or
                        View.SYSTEM_UI_FLAG_LAYOUT_STABLE or
                        View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN or
                        View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                webView.visibility = View.GONE
            }

            override fun onHideCustomView() {
                hideCustomView()
            }
        }

        if (savedInstanceState != null) {
            val restored = webView.restoreState(savedInstanceState)
            if (restored == null || restored.size == 0) {
                webView.loadUrl(ENTRY_URL)
            }
        } else {
            webView.loadUrl(ENTRY_URL)
        }

        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() = handleBack()
        })
    }

    private fun isAssetUrl(url: String): Boolean =
        url.startsWith("file:///android_asset/") || url.startsWith("about:")

    /**
     * TV remote / phone back:
     * 1. leave fullscreen video first,
     * 2. if the page has an open layer (settings, drawer, player, wizard...)
     *    send Escape so the page's own back-chain closes it,
     * 3. otherwise exit the app.
     */
    private fun handleBack() {
        if (customView != null) {
            hideCustomView()
            return
        }
        webView.evaluateJavascript(JS_HAS_OVERLAY) { result ->
            if (result == "true") {
                webView.evaluateJavascript(JS_SEND_ESCAPE, null)
            } else {
                finish()
            }
        }
    }

    private fun hideCustomView() {
        customView?.let { view ->
            (view.parent as? ViewGroup)?.removeView(view)
        }
        customView = null
        customViewCallback?.onCustomViewHidden()
        customViewCallback = null
        @Suppress("DEPRECATION")
        window.decorView.systemUiVisibility = savedSystemUiVisibility
        webView.visibility = View.VISIBLE
    }

    /**
     * D-pad fallback for Android TV remotes: if the WebView did not consume a
     * directional / center key, inject it into the page so the HTML spatial
     * navigation (landing.html and app.html both ship their own) runs.
     */
    override fun dispatchKeyEvent(event: KeyEvent): Boolean {
        val handled = super.dispatchKeyEvent(event)
        if (!handled && event.action == KeyEvent.ACTION_DOWN && event.repeatCount == 0) {
            val key = when (event.keyCode) {
                KeyEvent.KEYCODE_DPAD_UP -> "ArrowUp"
                KeyEvent.KEYCODE_DPAD_DOWN -> "ArrowDown"
                KeyEvent.KEYCODE_DPAD_LEFT -> "ArrowLeft"
                KeyEvent.KEYCODE_DPAD_RIGHT -> "ArrowRight"
                KeyEvent.KEYCODE_DPAD_CENTER, KeyEvent.KEYCODE_ENTER -> "Enter"
                else -> null
            }
            if (key != null && ::webView.isInitialized) {
                webView.evaluateJavascript(
                    "document.dispatchEvent(new KeyboardEvent('keydown'," +
                        "{key:'$key',bubbles:true,cancelable:true}))",
                    null
                )
                return true
            }
        }
        return handled
    }

    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        if (::webView.isInitialized) webView.saveState(outState)
    }

    override fun onPause() {
        super.onPause()
        if (::webView.isInitialized) webView.onPause()
    }

    override fun onResume() {
        super.onResume()
        if (::webView.isInitialized) webView.onResume()
    }

    override fun onDestroy() {
        if (::webView.isInitialized) {
            webView.stopLoading()
            webView.destroy()
        }
        super.onDestroy()
    }

    private companion object {
        const val ENTRY_URL = "file:///android_asset/splash.html"

        // True when any page-level overlay is open (app.html settings / guide /
        // player / mini player / location sheet, landing.html onboarding
        // wizard or profile menu). Booleans are returned so the WebView
        // callback arrives as the literal "true" / "false".
        val JS_HAS_OVERLAY = """
            (function(){
              try{
                if(window.SET && SET.open) return true;
                if(window.pipMode) return true;
                if(window.qpopOpen) return true;
                if(window.drawerOpen) return true;
                if(window.locOpen) return true;
                if(window.isPlayerOpen && isPlayerOpen()) return true;
                if(window.onboard && onboard.classList.contains('open')) return true;
                if(window.capsMenu && capsMenu.classList.contains('open')) return true;
              }catch(e){}
              return false;
            })()
        """.trimIndent()

        val JS_SEND_ESCAPE =
            "document.dispatchEvent(new KeyboardEvent('keydown'," +
                "{key:'Escape',bubbles:true,cancelable:true}))"
    }
}
