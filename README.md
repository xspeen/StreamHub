<div align="center">

<img src="https://img.shields.io/badge/-StreamHub-00e5c8?style=for-the-badge&logo=television&logoColor=white&labelColor=080a0f" alt="StreamHub Logo" width="200">

<br>

# StreamHub

### Free Live TV Streaming -- 140+ Countries, Zero Cost

<br>

[![Version](https://img.shields.io/badge/Version-2.0.2-00e5c8?style=for-the-badge&labelColor=0e1118)](#)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge&labelColor=0e1118)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.7+-yellow?style=for-the-badge&logo=python&logoColor=white&labelColor=0e1118)](#prerequisites)
[![Platform](https://img.shields.io/badge/Platform-Linux_%7C_macOS_%7C_Windows_%7C_Android-00e5c8?style=for-the-badge&labelColor=0e1118)](#installation)

<br>

<img src="https://img.shields.io/badge/Linux-FCC624?style=flat&logo=linux&logoColor=black" alt="Linux"> &nbsp;
<img src="https://img.shields.io/badge/macOS-000000?style=flat&logo=apple&logoColor=white" alt="macOS"> &nbsp;
<img src="https://img.shields.io/badge/Windows-0078D4?style=flat&logo=windows&logoColor=white" alt="Windows"> &nbsp;
<img src="https://img.shields.io/badge/Android_Termux-3DDC84?style=flat&logo=android&logoColor=white" alt="Android"> &nbsp;
<img src="https://img.shields.io/badge/WSL-555555?style=flat&logo=windows-subsystem-for-linux&logoColor=white" alt="WSL"> &nbsp;

</div>

---

StreamHub is a lightweight, cross-platform CLI tool that turns your terminal into a live TV streaming hub. One command installs it. One command launches it. Watch thousands of free channels from around the world directly in your browser.

No account required. No subscription. No ads.

---

## First-Time Setup (Run This First)

Before installing StreamHub, make sure **git** and **Python 3** are installed. Run the commands below for your OS first.

### Linux (Debian / Ubuntu / Kali / Parrot / Mint)

```bash
sudo apt update && sudo apt upgrade -y && sudo apt install -y git python3 curl
```

### Linux (Fedora)

```bash
sudo dnf upgrade -y && sudo dnf install -y git python3 curl
```

### Linux (Arch / Manjaro)

```bash
sudo pacman -Syu && sudo pacman -S --needed git python curl
```

### Linux (CentOS / RHEL / AlmaLinux)

```bash
sudo yum update -y && sudo yum install -y git python3 curl
```

### Linux (openSUSE / Leap)

```bash
sudo zypper refresh && sudo zypper update -y && sudo zypper install -y git python3 curl
```

### macOS

```bash
xcode-select --install && brew update && brew install git python3 curl
```

If Homebrew is not installed, install it first:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Android (Termux)

```bash
pkg update -y && pkg upgrade -y && pkg install -y git python curl
```

### Windows (Git Bash)

```bash
pacman -Syu && pacman -S --needed git python curl
```

### Windows (CMD / PowerShell)

Git: download from [git-scm.com](https://git-scm.com/download/win) and install.

Python: download from [python.org](https://python.org/downloads) and install. **Check "Add Python to PATH"** during install.

---

### Verify Installation

Run these commands to confirm everything is installed correctly:

```bash
git --version
python3 --version
curl --version
```

If any command fails, go back to the correct OS section above and run the install command again.

---

### Common Errors & Fixes

| Error | Fix |
|-------|-----|
| `git: command not found` | Run the install command for your OS above to install git |
| `python3: command not found` | Run the install command for your OS above to install Python 3 |
| `python3: not found` (Windows) | Reinstall Python from python.org, check "Add Python to PATH" |
| `curl: command not found` | Run the install command for your OS above to install curl |
| `Permission denied` (Linux/macOS) | Prefix the command with `sudo` |
| `E: Unable to locate package` | Run `sudo apt update` first (Debian/Ubuntu) |
| `Unable to locate python3` | Try `python --version` instead; some systems use `python` |
| `pip: command not found` | Run `sudo apt install python3-pip` (Linux) or `brew install pipx` (macOS) |
| `command not found: streamhub` | Run `source ~/.bashrc` or restart your terminal |
| StreamHub server won't start | Run `streamhub --stop` then try again |
| Port 8080 already in use | Run `streamhub --stop` to kill the old process |
| Browser doesn't open | Copy the URL from terminal and open manually |

---

## Features

| Feature | Description |
|---------|-------------|
| **140+ Countries** | Channel sources from every continent -- Africa, Europe, Asia, Americas, Middle East, Oceania |
| **DStv / GOtv** | Aggregated African channel sources in a single tab |
| **HLS Streaming** | Adaptive bitrate via hls.js -- buffers fast, plays smooth |
| **Auto-Skip** | Failed streams automatically skip to the next channel -- no more "stream not available" |
| **Screen Cast** | Cast live TV to any Smart TV on your network via Chromecast or Presentation API |
| **Profile System** | Local admin passcode, display name, and photo/avatar -- all stored on your device |
| **Photo Upload** | Set a real photo from your gallery as your profile picture |
| **Passcode Security** | Strength validation, repeated character detection, username similarity check |
| **Dark / Light Theme** | Toggle with one click; preference persists across sessions |
| **Cross-Platform** | Works on Linux, macOS, Windows (CMD, PowerShell, Git Bash), Termux, WSL, Kali, Parrot |
| **Search & Filter** | Instant search across all loaded channels |
| **Keyboard Shortcuts** | Space (play/pause), Arrows (next/prev), F (fullscreen), M (mute) |
| **PiP Mode** | Picture-in-Picture support on compatible browsers |
| **Swipe Navigation** | Touch-friendly channel switching on mobile |
| **Landscape Fullscreen** | Tilt your phone -- video fills the entire screen with no black bars |
| **Zero Dependencies** | Python 3.7+ standard library only -- no pip install, no Node.js, no Docker |
| **Offline Cache** | Channel data cached locally for 6 hours to minimize re-fetching |

---

## Installation

<div align="center">

<img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" alt="Linux"> &nbsp;
<img src="https://img.shields.io/badge/macOS-000000?style=for-the-badge&logo=apple&logoColor=white" alt="macOS"> &nbsp;
<img src="https://img.shields.io/badge/Android_Termux-3DDC84?style=for-the-badge&logo=android&logoColor=white" alt="Android"> &nbsp;
<img src="https://img.shields.io/badge/Windows-0078D4?style=for-the-badge&logo=windows&logoColor=white" alt="Windows"> &nbsp;

</div>

### Linux / macOS / Termux / Kali / Debian / Parrot

```bash
curl -sSL https://raw.githubusercontent.com/xspeen/StreamHub/main/install.sh | bash
```

### Windows (CMD)

```cmd
curl -sSL https://raw.githubusercontent.com/xspeen/StreamHub/main/install.bat -o install.bat && install.bat
```

### Windows (PowerShell)

```powershell
irm https://raw.githubusercontent.com/xspeen/StreamHub/main/install.ps1 | iex
```

### Git Bash (Windows)

Same as the Linux command above.

### Prerequisites

- **Python 3.7 or higher** -- required
- **git** -- required for updates
- **curl or wget** -- used by the installer

If any are missing, run the **First-Time Setup** commands above.

The installer will:
1. Detect your operating system and architecture
2. Check for Python 3
3. Download all project files to `~/.streamhub/`
4. Configure your PATH so the `streamhub` command is available globally
5. Display a confirmation banner

---

## Usage

### Launch

```bash
streamhub
```

On first launch, you will be prompted to create an admin passcode and display name. On subsequent launches, the server starts automatically and your default browser opens with the streaming interface.

The server detects your machine's IP address (WiFi, mobile data, or Ethernet) and opens the browser at `http://your-ip:8080`.

### Commands

| Command | Description |
|---------|-------------|
| `streamhub` | Launch the server and open in browser |
| `streamhub --help` | Show help message |
| `streamhub --stop` | Stop any running StreamHub server |
| `streamhub --reset` | Reset profile and passcode (requires confirmation) |
| `streamhub --version` | Show version number |
| `streamhub --update` | Update StreamHub to latest version from GitHub |

### Keyboard Shortcuts (in browser)

| Key | Action |
|-----|--------|
| `Space` | Play / Pause |
| `Arrow Right` | Next channel |
| `Arrow Left` | Previous channel |
| `F` | Toggle fullscreen |
| `M` | Toggle mute |
| `Esc` | Exit fullscreen |

---

## Screen Cast to Smart TV

StreamHub supports casting live TV to any Smart TV on your network.

**How it works:**
1. Make sure your phone/computer and TV are on the same WiFi network
2. Play a channel in StreamHub
3. Click the TV icon (cast button) in the player controls
4. Select your TV from the list of available devices
5. The stream will start playing on your TV

**Supported devices:**
- Chromecast (1st gen and newer)
- Android Smart TVs with built-in Chromecast
- Samsung, LG, Sony, and other TVs with screen mirroring
- Any device that supports the Presentation API

---

## Auto-Skip & Error Handling

StreamHub automatically handles stream failures so you never see "stream not available" screens:

- **Auto-skip**: If a stream fails to load, StreamHub automatically moves to the next channel
- **Retry logic**: HLS errors are retried up to 3 times before skipping
- **Minimal errors**: Failed streams show a brief "Skipping..." spinner (800ms) then move on
- **No manual intervention**: You don't need to click any buttons -- it just works

---

## Landscape & Fullscreen Mode

When you tilt your phone to landscape:

- **Video fills the entire screen** -- no black bars, no letterboxing
- **UI hides automatically** -- header, sidebar, and controls disappear
- **Controls accessible** -- tap the screen to show controls, they auto-hide after 3 seconds
- **Fullscreen mode** -- press F or click the expand icon for true fullscreen

On small screens (< 500px height in landscape):
- The video takes up the entire viewport
- All UI elements are hidden for an immersive experience

---

## Security

### Passcode Protection

StreamHub uses a local passcode to protect access to the web interface. The passcode is stored as a SHA-256 hash on your device -- it is never transmitted over the network.

**Passcode requirements:**
- Minimum 4 characters
- Cannot be all repeated characters (e.g., `aaaa`, `1111`)
- Cannot be too similar to your display name
- Strength indicator shows Weak / Fair / Strong based on complexity

**What is checked:**
- Repeated character patterns (e.g., `aaaa`, `11111`)
- Sequential characters (e.g., `abcd`, `1234`)
- Similarity to your display name
- Mix of character types (letters, numbers, symbols)

### Profile Privacy

- All profile data (name, photo, passcode hash) is stored locally on your device in `~/.streamhub/data/`
- No data is sent to external servers
- Profile photos are stored as compressed base64 data (max 200x200px, JPEG quality 70%)
- The server only listens on your local network interface

---

## Project Structure

```
streamhub/
├── install.sh          # Linux/macOS/Termux installer
├── install.bat         # Windows CMD installer
├── install.ps1         # Windows PowerShell installer
├── bin/
│   └── streamhub       # Main launcher script
├── src/
│   ├── core.sh         # Shared shell utilities
│   ├── server.py       # Python HTTP server + API
│   ├── scanner.py      # M3U channel fetcher + parser
│   └── db.py           # Local JSON storage
├── web/
│   └── index.html      # Web UI (single-page application)
├── data/               # User data directory (created at runtime)
├── README.md
├── LICENSE
├── .gitignore
└── .gitattributes
```

---

## API Endpoints

The local server exposes these endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Serves the web interface |
| GET | `/api/profile` | Returns user profile as JSON |
| POST | `/api/profile` | Saves user profile (name, avatar, photo) |
| POST | `/api/auth` | Verifies passcode or changes passcode |
| GET | `/api/channels?category={id}` | Returns channels for a category |
| GET | `/api/categories` | Returns category list |

---

## Channels from 140+ Countries

<div align="center">

![South Africa](https://flagcdn.com/24x18/za.png) ![Nigeria](https://flagcdn.com/24x18/ng.png) ![Kenya](https://flagcdn.com/24x18/ke.png) ![Ghana](https://flagcdn.com/24x18/gh.png) ![Ethiopia](https://flagcdn.com/24x18/et.png) ![UK](https://flagcdn.com/24x18/gb.png) ![Germany](https://flagcdn.com/24x18/de.png) ![France](https://flagcdn.com/24x18/fr.png) ![Italy](https://flagcdn.com/24x18/it.png) ![Spain](https://flagcdn.com/24x18/es.png) ![Portugal](https://flagcdn.com/24x18/pt.png) ![USA](https://flagcdn.com/24x18/us.png) ![Canada](https://flagcdn.com/24x18/ca.png) ![Brazil](https://flagcdn.com/24x18/br.png) ![Mexico](https://flagcdn.com/24x18/mx.png) ![India](https://flagcdn.com/24x18/in.png) ![Japan](https://flagcdn.com/24x18/jp.png) ![South Korea](https://flagcdn.com/24x18/kr.png) ![China](https://flagcdn.com/24x18/cn.png) ![Turkey](https://flagcdn.com/24x18/tr.png) ![Saudi Arabia](https://flagcdn.com/24x18/sa.png) ![UAE](https://flagcdn.com/24x18/ae.png) ![Australia](https://flagcdn.com/24x18/au.png) ![New Zealand](https://flagcdn.com/24x18/nz.png)

</div>

---

## Changelog

### v2.0.2 -- Latest

**New Features:**
- Profile photo upload from gallery/camera
- Cast to Smart TV (Chromecast + Presentation API)
- Auto-skip failed streams
- Landscape fullscreen mode (video fills entire screen)
- Passcode strength indicator (Weak/Fair/Strong)
- Passcode validation (repeated chars, username similarity)

**Improvements:**
- IP detection works on all platforms (9 detection methods)
- Browser auto-opens on all platforms (Termux, macOS, Windows, Linux)
- Error overlay is minimal -- shows "Skipping..." spinner, auto-dismisses
- Failed streams auto-advance to next channel
- Fullscreen mode properly scales video to fill viewport

### v1.0.0

Initial release with channel browsing, HLS playback, profile system, and cross-platform installer.

---

## Contact

For support, feedback, or inquiries:

<a href="https://t.me/royexploit" target="_blank" rel="noopener">
  <img src="https://img.shields.io/badge/Telegram-%40royexploit-0088cc?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram @royexploit">
</a>

---

## Disclaimer

StreamHub is not affiliated with, endorsed by, or connected to DStv, GOtv, MultiChoice, or any other service provider. StreamHub is a tool that aggregates publicly available IPTV playlist sources. Channel availability and stream quality depend on the third-party sources. StreamHub does not host, store, or distribute any media content.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

<div align="center">

**StreamHub v2.0.2**

Built with care. Free forever.

</div>
