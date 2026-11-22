import SwiftUI
import WebKit

/// Runs the shared StreamHub web app (web/splash.html -> landing.html ->
/// app.html) inside a WKWebView, the same shell the Android app uses.
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

        let webView = WKWebView(frame: .zero, configuration: configuration)
        webView.scrollView.contentInsetAdjustmentBehavior = .never
        webView.isOpaque = false
        webView.backgroundColor = UIColor(red: 0x07 / 255.0, green: 0x09 / 255.0, blue: 0x0F / 255.0, alpha: 1)

        // Prefer the bundle root, fall back to a web/ subdirectory in case the
        // resources were copied with their folder structure preserved.
        if let url = Bundle.main.url(forResource: "splash", withExtension: "html")
            ?? Bundle.main.url(forResource: "splash", withExtension: "html", subdirectory: "web") {
            webView.loadFileURL(url, allowingReadAccessTo: url.deletingLastPathComponent())
        }
        return webView
    }

    func updateUIView(_ uiView: WKWebView, context: Context) {}
}
