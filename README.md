# StreamHub

Cross-platform live TV: phones, tablets and Android TV from one APK — built
around the original StreamHub **splash screen**, **landing page** and
**streamer** HTML files, preserved exactly as designed.

The three pages are the app. A thin native shell (Android WebView / iOS
WKWebView) hosts them with everything live TV needs: HLS playback, D-pad and
remote navigation, leanback launcher support, cleartext IPTV streams and
on-device profiles.

## What you get

- **Live stream playback** — HLS via hls.js with quality selection (Auto /
  1080p / 720p / 480p), buffering profiles, fit modes, floating mini player
  (PiP) with in-bubble channel switching, and the slide-out TV guide.
- **Channel organization** — DStv, GOtv and global live streams grouped into
  Global, Sports, Movies, News, Kids and Music, with genre chips, search,
  continent → country filtering and per-country channel counts.
- **Every screen preserved** — splash animation, landing page (onboarding
  wizard, profile capsule, motion icon pack, liquid-glass dock) and the
  full streamer app ship byte-for-byte from `web/`, plus only the two lines of
  navigation wiring (`splash → landing`, `Continue/Skip → app`).
- **Phone / tablet / TV** — responsive layouts already in the pages, plus a
  leanback launcher entry, 320×180 TV banner, no touchscreen requirement, and
  D-pad/remote spatial navigation (the pages' own arrow-key engine, with a
  native key-forwarding fallback in the shell).

## Repository layout

```
web/                     Shared cross-platform app (splash.html, landing.html, app.html)
app/                     Android project (Kotlin shell around web/)
  src/main/java/.../MainActivity.kt
  src/main/res/          Launcher icons, TV banner, theme
signing/streamhub.keystore  Release signing key (see Signing)
ios/                     iOS scaffold (XcodeGen project + SwiftUI WKWebView shell)
.github/workflows/       android-ci.yml, android-release.yml, ios.yml
```

The Gradle build maps `web/` straight into `assets/`, so the Android, iOS and
plain-browser builds all ship the identical HTML.

## Build the Android app

Requirements: JDK 17, Android SDK (compileSdk 35).

```bash
./gradlew :app:assembleDebug        # app/build/outputs/apk/debug/app-debug.apk
./gradlew :app:assembleRelease      # signed with signing/streamhub.keystore
```

Or let GitHub do it: every push to `main` runs **Android CI** and uploads a
debug APK as a workflow artifact.

## Install

1. Open the **Releases** page on GitHub and download `StreamHub-<version>.apk`.
2. On a phone/tablet: open the downloaded file and allow installs from unknown
   sources.
3. On Android TV: sideload with `adb install StreamHub-<version>.apk`, or copy
   the APK to the device and open it from a file manager.

Verify the download against `SHA256SUMS.txt` if anything complains.

## Cut a release

1. Bump `versionName` / `versionCode` defaults in `app/build.gradle.kts`
   (the tag overrides them, the defaults keep local builds honest).
2. Commit, push `main`, wait for **Android CI** to go green.
3. Tag and push:

   ```bash
   git tag v1.1.0
   git push origin v1.1.0
   ```

4. **Android Release** builds the signed APK, verifies the signature and the
   embedded `web/` assets, and publishes a GitHub Release with the APK,
   source zip and `SHA256SUMS.txt`.

## Signing

Every release is signed with `signing/streamhub.keystore` (alias
`streamhub`), which is committed to the repository **on purpose**: it is the
only way a GitHub-Actions-built APK and a locally built `assembleRelease` APK
stay on the same key, so updates never fail with `app not installed`
(signature mismatch). Certificate SHA-256:

```
1a264afc0cd58656eae8268b837cfa6847fcfae4787104312fe683c45a39bf3f
```

The release workflow re-checks this fingerprint on every build. To use your
own key instead, set `STREAMHUB_KEYSTORE_PATH`, `STREAMHUB_KEYSTORE_PASSWORD`,
`STREAMHUB_KEY_ALIAS` and `STREAMHUB_KEY_PASSWORD` as environment variables
(CI secrets) — they override the committed file.

## iOS

The iOS target is an XcodeGen scaffold around the same `web/` folder:

```bash
brew install xcodegen
xcodegen --project ios
open ios/StreamHub.xcodeproj
```

Run on a simulator or device from Xcode. ATS allows arbitrary loads because
most IPTV feeds are plain `http://`. The **iOS Build** workflow
(`workflow_dispatch`) compiles it unsigned on a macOS runner.

## Plain web

`web/` is a normal static site — open `web/splash.html` in a browser, or host
the folder on any static host (GitHub Pages, Netlify…). The streamer page
needs network access for the channel lists and streams.

## Troubleshooting

- **"Problem parsing the package"** — the APK download is truncated. Compare
  the file size with `SHA256SUMS.txt` and re-download.
- **"App not installed"** — usually a signature conflict with a build from a
  different key; uninstall the old build first, or check the checksum above.
- **No channels / streams won't load** — the app fetches
  `iptv-org.github.io` playlists and needs a network connection; the pages
  show their own retry state when offline.
- **Cleartext streams blocked** — already handled: the manifest sets
  `android:usesCleartextTraffic="true"` for `http://` IPTV feeds.

## License

MIT — see [LICENSE](LICENSE).
