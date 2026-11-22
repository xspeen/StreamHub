#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

fn main() {
    // Let the bundled pages fetch IPTV playlists and stream segments from any
    // origin - the same policy as the Android shell's
    // allowUniversalAccessFromFileURLs. Many stream hosts send no CORS headers,
    // which would otherwise block hls.js in the WebView2 window.
    #[cfg(target_os = "windows")]
    std::env::set_var(
        "WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS",
        "--disable-web-security",
    );

    tauri::Builder::default()
        .run(tauri::generate_context!())
        .expect("error while running StreamHub");
}
