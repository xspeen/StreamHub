#!/usr/bin/env bash
# StreamHub Installer - Linux / macOS / Termux / Kali / Debian / Git Bash
# One-command install: curl -sSL https://raw.githubusercontent.com/xspeen/StreamHub/main/install.sh | bash
set -euo pipefail

# ---- Configuration ----
REPO="https://github.com/xspeen/StreamHub"
RAW="https://raw.githubusercontent.com/xspeen/StreamHub/main"
INSTALL_DIR=""
VERSION="3.3.9"

# ---- ANSI Colors (with terminal support check) ----
setup_colors() {
    if [ -t 1 ] && [ -n "${TERM:-}" ] && [ "${TERM:-}" != "dumb" ]; then
        RED='\033[0;31m'
        GREEN='\033[0;32m'
        YELLOW='\033[1;33m'
        BLUE='\033[0;34m'
        CYAN='\033[0;36m'
        WHITE='\033[1;37m'
        DIM='\033[2m'
        BOLD='\033[1m'
        NC='\033[0m'
    else
        RED='' GREEN='' YELLOW='' BLUE='' CYAN='' WHITE='' DIM='' BOLD='' NC=''
    fi
}
setup_colors

# ---- Detect environment ----
detect_env() {
    IS_TERMUX=0
    IS_MACOS=0
    IS_GITBASH=0
    IS_WSL=0
    OS_NAME="$(uname -s 2>/dev/null || echo 'Unknown')"
    ARCH="$(uname -m 2>/dev/null || echo 'unknown')"

    case "$OS_NAME" in
        Linux)
            if [ -n "${PREFIX:-}" ] && echo "$PREFIX" | grep -q "com.termux" 2>/dev/null; then
                IS_TERMUX=1
            elif grep -qi "microsoft" /proc/version 2>/dev/null; then
                IS_WSL=1
            fi
            ;;
        Darwin)
            IS_MACOS=1
            ;;
        MINGW*|MSYS*|CYGWIN*)
            IS_GITBASH=1
            ;;
    esac

    if [ "$IS_TERMUX" -eq 1 ]; then
        INSTALL_DIR="$HOME/.streamhub"
    elif [ "$IS_GITBASH" -eq 1 ]; then
        INSTALL_DIR="$HOME/.streamhub"
    else
        INSTALL_DIR="$HOME/.streamhub"
    fi
}

# ---- Check prerequisites ----
check_python() {
    PY=""
    for candidate in python3 python; do
        if command -v "$candidate" >/dev/null 2>&1; then
            PY_VER=$("$candidate" --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
            PY_MAJOR=$(echo "$PY_VER" | cut -d. -f1)
            PY_MINOR=$(echo "$PY_VER" | cut -d. -f2)
            if [ "$PY_MAJOR" -ge 3 ] && [ "$PY_MINOR" -ge 7 ]; then
                PY="$candidate"
                return 0
            fi
        fi
    done
    echo -e "${RED}[ERROR] Python 3.7+ is required but not found.${NC}"
    echo -e "${WHITE}Install it from https://python.org or your package manager, then run this installer again.${NC}"
    exit 1
}

check_curl() {
    if command -v curl >/dev/null 2>&1; then
        FETCHER="curl"
    elif command -v wget >/dev/null 2>&1; then
        FETCHER="wget"
    else
        echo -e "${RED}[ERROR] Neither curl nor wget found. Install one and try again.${NC}"
        exit 1
    fi
}

# ---- Progress bar ----
BAR_WIDTH=40
print_bar() {
    local pct=$1
    local status="${2:-}"
    local filled=$((pct * BAR_WIDTH / 100))
    local empty=$((BAR_WIDTH - filled))
    local bar=""
    local i
    for ((i=0; i<filled; i++)); do bar="${bar}#"; done
    for ((i=0; i<empty; i++)); do bar="${bar}-"; done
    printf "\r  ${CYAN}[${bar}]${NC} ${WHITE}%3d%%${NC}  ${DIM}%s${NC}          " "$pct" "$status"
}

# ---- Download helper ----
download() {
    local url="$1"
    local dest="$2"
    if [ "$FETCHER" = "curl" ]; then
        curl -sSL --retry 3 --retry-delay 2 -o "$dest" "$url"
    else
        wget -q --tries=3 -O "$dest" "$url"
    fi
}

# ---- Install files ----
install_files() {
    echo ""
    echo -e "  ${BOLD}${CYAN}StreamHub Installer v${VERSION}${NC}"
    echo -e "  ${DIM}Installing to ${INSTALL_DIR}${NC}"
    echo ""

    # Create directories
    print_bar 5 "Creating directories..."
    mkdir -p "$INSTALL_DIR"/{bin,src,web,data}
    sleep 0.1

    # Download files
    local files=(
        "VERSION:VERSION"
        "bin/streamhub:bin/streamhub"
        "src/core.sh:src/core.sh"
        "src/server.py:src/server.py"
        "src/scanner.py:src/scanner.py"
        "src/db.py:src/db.py"
        "web/index.html:web/index.html"
    )

    local total=${#files[@]}
    local idx=0

    for entry in "${files[@]}"; do
        local remote="${entry%%:*}"
        local local_path="${entry##*:}"
        idx=$((idx + 1))
        local pct=$((idx * 80 / total + 10))

        case $idx in
            1) status="Downloading version info..." ;;
            2) status="Downloading core modules..." ;;
            3) status="Setting up launcher..." ;;
            4) status="Configuring server..." ;;
            5) status="Setting up channel scanner..." ;;
            6) status="Setting up database..." ;;
            *) status="Downloading web interface..." ;;
        esac

        print_bar "$pct" "$status"
        download "${RAW}/${remote}" "${INSTALL_DIR}/${local_path}" 2>/dev/null || {
            echo ""
            echo -e "${RED}[ERROR] Failed to download ${remote}. Check your internet connection.${NC}"
            exit 1
        }
    done

    # Ensure .gitkeep
    touch "$INSTALL_DIR/data/.gitkeep" 2>/dev/null

    print_bar 90 "Configuring permissions..."
    chmod +x "$INSTALL_DIR/bin/streamhub" 2>/dev/null || true
    chmod +x "$INSTALL_DIR/install.sh" 2>/dev/null || true

    # Setup PATH
    print_bar 95 "Configuring PATH..."
    setup_path

    print_bar 100 "Finalizing..."
    echo ""
    echo ""

    # Success banner
    echo -e "  ${BLUE}${BOLD}============================================${NC}"
    echo -e "  ${BLUE}${BOLD}       INSTALLATION COMPLETE${NC}"
    echo -e "  ${BLUE}${BOLD}============================================${NC}"
    echo ""
    echo -e "  ${CYAN} _____  _                            _   _       _     ${NC}"
    echo -e "  ${CYAN}| ___ || |_ _ __ ___  __ _ _ __ ___ | | | |_   _| |__  ${NC}"
    echo -e "  ${CYAN}| ___ || __| '__/ _ \\/ _\` | '_ \` _ \\\\| |_| | | | | '_ \\ ${NC}"
    echo -e "  ${CYAN}| ___ || |_| | |  __/ (_| | | | | | |  _  | |_| | |_) |${NC}"
    echo -e "  ${CYAN}|_____ | \\__|_|  \\___|\\__,_|_| |_| |_|_| |_|\\__,_|_.__/ ${NC}"
    echo ""
    echo -e "  ${WHITE}Type ${CYAN}streamhub${WHITE} in your terminal to launch${NC}"
    echo ""
}

# ---- Setup PATH ----
setup_path() {
    if [ "$IS_TERMUX" -eq 1 ]; then
        # Termux: bin is already in PATH via $PREFIX/bin
        ln -sf "$INSTALL_DIR/bin/streamhub" "$PREFIX/bin/streamhub" 2>/dev/null || true
    elif [ "$IS_GITBASH" -eq 1 ]; then
        # Git Bash: create .bat wrapper and add to PATH via profile
        # Find bash.exe for the wrapper
        local bash_exe=""
        for bp in "C:/Program Files/Git/bin/bash.exe" "C:/Program Files (x86)/Git/bin/bash.exe" "$LOCALAPPDATA/Programs/Git/bin/bash.exe"; do
            if [ -f "$bp" ]; then bash_exe="$bp"; break; fi
        done
        if [ -z "$bash_exe" ]; then
            bash_exe="$(command -v bash 2>/dev/null || echo bash)"
        fi
        # Create .bat wrapper
        cat > "$INSTALL_DIR/streamhub.bat" <<BATEOF
@echo off
setlocal
"$bash_exe" "$INSTALL_DIR/bin/streamhub" %*
BATEOF
        cp -f "$INSTALL_DIR/streamhub.bat" "$INSTALL_DIR/bin/streamhub.bat" 2>/dev/null || true
        # Add to PATH via profile
        local bin_line="export PATH=\"${INSTALL_DIR}:\$PATH\""
        local profile="$HOME/.bash_profile"
        [ ! -f "$profile" ] && profile="$HOME/.profile"
        if ! grep -qF "streamhub" "$profile" 2>/dev/null; then
            echo "" >> "$profile"
            echo "# StreamHub" >> "$profile"
            echo "$bin_line" >> "$profile"
        fi
        export PATH="${INSTALL_DIR}:$PATH"
    elif [ "$IS_MACOS" -eq 1 ]; then
        # macOS: try /usr/local/bin, fall back to ~/.local/bin
        if ln -sf "$INSTALL_DIR/bin/streamhub" "/usr/local/bin/streamhub" 2>/dev/null; then
            true
        else
            mkdir -p "$HOME/.local/bin"
            ln -sf "$INSTALL_DIR/bin/streamhub" "$HOME/.local/bin/streamhub"
            local profile="$HOME/.zshrc"
            [ ! -f "$profile" ] && profile="$HOME/.bash_profile"
            if ! grep -qF ".local/bin" "$profile" 2>/dev/null; then
                echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$profile"
            fi
        fi
    else
        # Linux: try /usr/local/bin, fall back to ~/.local/bin
        if ln -sf "$INSTALL_DIR/bin/streamhub" "/usr/local/bin/streamhub" 2>/dev/null; then
            true
        else
            mkdir -p "$HOME/.local/bin"
            ln -sf "$INSTALL_DIR/bin/streamhub" "$HOME/.local/bin/streamhub"
            local profile="$HOME/.bashrc"
            [ ! -f "$profile" ] && profile="$HOME/.profile"
            if ! grep -qF ".local/bin" "$profile" 2>/dev/null; then
                echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$profile"
            fi
        fi
    fi
}

# ---- Main ----
main() {
    detect_env
    check_python
    check_curl
    install_files
    exit 0
}

main "$@"
