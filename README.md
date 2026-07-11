<div align="center">

<svg viewBox="0 0 120 120" fill="none" width="120" height="120">
  <rect width="120" height="120" rx="28" fill="url(#logoGrad)"/>
  <path d="M30 84L54 36H66L42 84H30Z" fill="#080a0f"/>
  <path d="M54 84L78 36H90L66 84H54Z" fill="#080a0f" opacity=".45"/>
  <defs>
    <linearGradient id="logoGrad" x1="0" y1="0" x2="120" y2="120">
      <stop stop-color="#00e5c8"/>
      <stop offset="1" stop-color="#006b5e"/>
    </linearGradient>
  </defs>
</svg>

<br>

# **StreamHub**

### Free Live TV Streaming -- 140+ Countries, Zero Cost

<br>

[![Version](https://img.shields.io/badge/Version-2.0.2-00e5c8?style=for-the-badge&labelColor=0e1118)](#)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge&labelColor=0e1118)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.7+-yellow?style=for-the-badge&logo=python&logoColor=white&labelColor=0e1118)](#prerequisites)

<br>

<img src="https://img.shields.io/badge/Linux-FCC624?style=flat&logo=linux&logoColor=black" alt="Linux"> &nbsp;
<img src="https://img.shields.io/badge/macOS-000000?style=flat&logo=apple&logoColor=white" alt="macOS"> &nbsp;
<img src="https://img.shields.io/badge/Windows-0078D4?style=flat&logo=windows&logoColor=white" alt="Windows"> &nbsp;
<img src="https://img.shields.io/badge/Android-3DDC84?style=flat&logo=android&logoColor=white" alt="Android"> &nbsp;

</div>

---

StreamHub is a lightweight, cross-platform CLI tool that turns your terminal into a live TV streaming hub. One command installs it. One command launches it. Watch thousands of free channels from around the world directly in your browser.

No account required. No subscription. No ads.

---

## Features

| Feature | Description |
|---------|-------------|
| **140+ Countries** | Channel sources from every continent -- Africa, Europe, Asia, Americas, Middle East, Oceania |
| **DStv / GOtv** | Aggregated African channel sources in a single tab |
| **HLS Streaming** | Adaptive bitrate via hls.js -- buffers fast, plays smooth |
| **Profile System** | Local admin passcode, display name, and photo/avatar -- all stored on your device |
| **Photo Upload** | Set a real photo from your gallery as your profile picture |
| **Passcode Security** | Strength validation, repeated character detection, username similarity check |
| **Dark / Light Theme** | Toggle with one click; preference persists across sessions |
| **Cross-Platform** | Works on Linux, macOS, Windows (CMD, PowerShell, Git Bash), Termux, WSL, Kali, Parrot |
| **Search & Filter** | Instant search across all loaded channels |
| **Keyboard Shortcuts** | Space (play/pause), Arrows (next/prev), F (fullscreen), M (mute) |
| **PiP Mode** | Picture-in-Picture support on compatible browsers |
| **Swipe Navigation** | Touch-friendly channel switching on mobile |
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

- **Python 3.7 or higher** -- required. Install from [python.org](https://python.org) or your package manager.
- **curl or wget** -- used by the installer to download files. Most systems have this pre-installed.

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

On first launch, you will be prompted to create an admin passcode and display name. On subsequent launches, you will see a welcome message, a fresh terminal session with the StreamHub banner, and the server starts automatically. Your default browser opens with the streaming interface.

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
- The server only listens on `127.0.0.1` (localhost) -- it is not accessible from the network

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
