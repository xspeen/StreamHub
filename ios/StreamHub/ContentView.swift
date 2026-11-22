import SwiftUI
import UIKit
import WebKit

/// Runs the shared StreamHub web app (web/splash.html -> landing.html ->
/// app.html) inside a WKWebView - the same shell the Android app uses.
struct ContentView: View {
    var body: some View {
        StreamHubWebView()
            .ignoresSafeArea()
    }
}

struct StreamHubWebView: UIViewRepresentable {
    func makeUIView(context: Context) -> WKWebView {
        let configuration = WKWebViewConfiguration()
        configuration.allowsInlineMediaPlayback = true
        configuration.mediaTypesRequiringUserActionForPlayback = []

        // Same policy as the Android WebView: the pages load from file:// and
        // must fetch IPTV playlists and stream segments from any origin -
        // many stream hosts send no CORS headers. Guarded with responds(to:)
        // so a WebKit build without these knobs cannot crash the app.
        for key in ["allowFileAccessFromFileURLs", "allowUniversalAccessFromFileURLs"] {
            let setter = "set" + key.prefix(1).uppercased() + key.dropFirst() + ":"
            if configuration.responds(to: Selector(setter)) {
                configuration.setValue(true, forKey: key)
            }
        }

        let webView = WKWebView(frame: .zero, configuration: configuration)
        webView.navigationDelegate = context.coordinator
        webView.scrollView.contentInsetAdjustmentBehavior = .never
        webView.isOpaque = false
        let bg = UIColor(red: 0x04 / 255.0, green: 0x06 / 255.0, blue: 0x0C / 255.0, alpha: 1)
        webView.backgroundColor = bg
        webView.scrollView.backgroundColor = bg

        // Prefer the bundle root, fall back to a web/ subdirectory in case the
        // resources were copied with their folder structure preserved.
        if let url = Bundle.main.url(forResource: "splash", withExtension: "html")
            ?? Bundle.main.url(forResource: "splash", withExtension: "html", subdirectory: "web") {
            webView.loadFileURL(url, allowingReadAccessTo: url.deletingLastPathComponent())
        }
        return webView
    }

    func updateUIView(_ uiView: WKWebView, context: Context) {}

    func makeCoordinator() -> Coordinator { Coordinator() }

    final class Coordinator: NSObject, WKNavigationDelegate {
        /// Keep the app's own pages inside the WKWebView; hand any external
        /// link to the system browser so the shell never navigates away.
        func webView(_ webView: WKWebView,
                     decidePolicyFor navigationAction: WKNavigationAction,
                     decisionHandler: @escaping (WKNavigationActionPolicy) -> Void) {
            guard let url = navigationAction.request.url else {
                decisionHandler(.allow)
                return
            }
            switch url.scheme?.lowercased() {
            case "file", "about", "blob", "data":
                decisionHandler(.allow)
            case "http", "https":
                decisionHandler(.cancel)
                UIApplication.shared.open(url)
            default:
                decisionHandler(.cancel)
            }
        }
    }
}
