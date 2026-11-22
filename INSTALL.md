# StreamHub - install steps

Every release on https://github.com/xspeen/StreamHub/releases is built by
GitHub Actions from the source at that tag: real native builds, no
simulators, no mocks. Each release ships:

| File | Platform |
|---|---|
| `StreamHub-<version>.apk` | Android phone / tablet / Android TV |
| `StreamHub-<version>-ios.ipa` | iPhone / iPad |
| `StreamHub-<version>-windows-x64-setup.exe` | Windows laptop / desktop |
| `StreamHub-<version>-src.zip` | Full source tree at the tag |
| `SHA256SUMS.txt` | Checksums for all of the above |

Verify a download: `sha256sum -c SHA256SUMS.txt`

## Android (phones, tablets, Android TV)

1. Download `StreamHub-<version>.apk` to the device.
2. Open the file and allow installs from unknown sources.
3. Updates: install over the previous version - same signing key, no
   uninstall needed.

Android TV: copy the APK to the device (USB/adb) and install it; the app
registers a leanback launcher entry with a TV banner and full D-pad
navigation.

Troubleshooting:

- "problem parsing the package" / "app not installed" - almost always a
  truncated download: compare the file size with `SHA256SUMS.txt`.
- Signature error while updating - an older build with a different key is
  installed: uninstall first, then install the new APK.

## iOS (iPhone / iPad)

`StreamHub-<version>-ios.ipa` is a real Release build for devices. Apple
requires every install to be signed, so the IPA is packaged unsigned and
your sideloader re-signs it with **your own Apple ID**:

- **SideStore / AltStore** (recommended) - install the sideloader once,
  then drop the IPA in; certificates refresh automatically every 7 days.
- **Sideloadly** (Windows/macOS) - enter your Apple ID, pick the IPA.
- **TrollStore** - supported devices only; permanent install, no refresh.
- **Xcode** - Window > Devices and Simulators, drag the app in.

Requirements: iOS 15.0 or newer. Free Apple ID certificates expire after
7 days (SideStore/AltStore refresh this automatically).

## Windows (laptop / desktop, x64)

1. Run `StreamHub-<version>-windows-x64-setup.exe`.
2. The WebView2 runtime installs automatically if it is missing.
3. If Windows SmartScreen appears: More info > Run anyway. (The installer
   is unsigned; sign it with your own code-signing certificate to remove
   the warning.)

## Building from source

All builds are automated in GitHub Actions (`.github/workflows/`):

- `android-ci.yml` - debug build on every push to `main`.
- `release.yml` - on a `v*` tag (or manual dispatch): builds the signed
  Android APK, archives a real-device iOS app and packages the Windows
  NSIS installer, then publishes one GitHub Release with checksums.

Locally: Android needs JDK 17 + Android SDK (`./gradlew assembleRelease`);
iOS needs XcodeGen (`xcodegen --project ios` then `xcodebuild -scheme
StreamHub -destination 'generic/platform=iOS' archive`); Windows needs
Rust + Node (`cd windows && npm install && npx tauri build`).

The three original HTML pages (`web/splash.html`, `web/landing.html`,
`web/app.html`) are the shared app core - identical on every platform.
