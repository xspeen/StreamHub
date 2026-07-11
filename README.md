<div align="center">

<svg viewBox="0 0 40 40" fill="none" width="80" height="80"><rect width="40" height="40" rx="10" fill="url(#lAR)"/><path d="M10 28L18 12H24L16 28H10Z" fill="#080a0f"/><path d="M18 28L26 12H32L24 28H18Z" fill="#080a0f" opacity=".45"/><defs><linearGradient id="lAR" x1="0" y1="0" x2="40" y2="40"><stop stop-color="#00e5c8"/><stop offset="1" stop-color="#006b5e"/></linearGradient></defs></svg>

# StreamHub

**Free Live TV Streaming — 140+ Countries, Zero Cost**

[![License: MIT](https://img.shields.io/badge/License-MIT-00e5c8.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-blue.svg)](#)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows%20%7C%20Android-00e5c8.svg)](#installation)

</div>

---

StreamHub is a lightweight, cross-platform CLI tool that turns your terminal into a live TV streaming hub. One command installs it. One command launches it. Watch thousands of free channels from around the world directly in your browser.

No account required. No subscription. No ads.

---

## Features

| Feature | Description |
|---------|-------------|
| **140+ Countries** | Channel sources from every continent — Africa, Europe, Asia, Americas, Middle East, Oceania |
| **DStv / GOtv** | Aggregated African channel sources in a single tab |
| **HLS Streaming** | Adaptive bitrate via hls.js — buffers fast, plays smooth |
| **Profile System** | Local admin passcode, display name, and avatar — all stored on your device |
| **Dark / Light Theme** | Toggle with one click; preference persists across sessions |
| **Cross-Platform** | Works on Linux, macOS, Windows (CMD, PowerShell, Git Bash), Termux, WSL, Kali, Parrot |
| **Search & Filter** | Instant search across all loaded channels |
| **Keyboard Shortcuts** | Space (play/pause), Arrows (next/prev), F (fullscreen), M (mute) |
| **PiP Mode** | Picture-in-Picture support on compatible browsers |
| **Swipe Navigation** | Touch-friendly channel switching on mobile |
| **Zero Dependencies** | Python 3.7+ standard library only — no pip install, no Node.js, no Docker |
| **Offline Cache** | Channel data cached locally for 6 hours to minimize re-fetching |

---

## Installation

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

- **Python 3.7 or higher** — required. Install from [python.org](https://python.org) or your package manager.
- **curl or wget** — used by the installer to download files. Most systems have this pre-installed.

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

On first launch, you will be prompted to create an admin passcode and display name. On subsequent launches, you will see a welcome message and the server starts automatically.

The web interface opens in your default browser at `http://127.0.0.1:8080`.

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
| POST | `/api/profile` | Saves user profile |
| POST | `/api/auth` | Verifies passcode or changes passcode |
| GET | `/api/channels?category={id}` | Returns channels for a category |
| GET | `/api/categories` | Returns category list |

---

## Channels from 140+ Countries

<div align="center">

![South Africa](https://flagcdn.com/24x18/za.png) ![Nigeria](https://flagcdn.com/24x18/ng.png) ![Kenya](https://flagcdn.com/24x18/ke.png) ![Ghana](https://flagcdn.com/24x18/gh.png) ![Egypt](https://flagcdn.com/24x18/eg.png) ![Ethiopia](https://flagcdn.com/24x18/et.png) ![UK](https://flagcdn.com/24x18/gb.png) ![Germany](https://flagcdn.com/24x18/de.png) ![France](https://flagcdn.com/24x18/fr.png) ![Italy](https://flagcdn.com/24x18/it.png) ![Spain](https://flagcdn.com/24x18/es.png) ![Portugal](https://flagcdn.com/24x18/pt.png) ![USA](https://flagcdn.com/24x18/us.png) ![Canada](https://flagcdn.com/24x18/ca.png) ![Brazil](https://flagcdn.com/24x18/br.png) ![Mexico](https://flagcdn.com/24x18/mx.png) ![India](https://flagcdn.com/24x18/in.png) ![Japan](https://flagcdn.com/24x18/jp.png) ![South Korea](https://flagcdn.com/24x18/kr.png) ![China](https://flagcdn.com/24x18/cn.png) ![Turkey](https://flagcdn.com/24x18/tr.png) ![Saudi Arabia](https://flagcdn.com/24x18/sa.png) ![UAE](https://flagcdn.com/24x18/ae.png) ![Australia](https://flagcdn.com/24x18/au.png) ![New Zealand](https://flagcdn.com/24x18/nz.png)

</div>

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

**StreamHub v1.0.0**

Built with care. Free forever.

</div>
