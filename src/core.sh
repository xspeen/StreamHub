#!/usr/bin/env bash
# StreamHub Core Functions
# Shared utilities used by the launcher script
# Sourced by bin/streamhub if needed for additional functionality

# ---- Utility: check if a command exists ----
has_cmd() {
    command -v "$1" >/dev/null 2>&1
}

# ---- Utility: get file size in bytes ----
file_size() {
    local f="$1"
    if [ -f "$f" ]; then
        wc -c < "$f" 2>/dev/null | tr -d ' '
    else
        echo "0"
    fi
}

# ---- Utility: check if port is in use ----
port_in_use() {
    local port="$1"
    if has_cmd ss; then
        ss -tln 2>/dev/null | grep -q ":$port "
    elif has_cmd netstat; then
        netstat -tln 2>/dev/null | grep -q ":$port "
    elif has_cmd lsof; then
        lsof -i ":$port" >/dev/null 2>&1
    else
        return 1
    fi
}

# ---- Utility: generate SHA-256 hash ----
sha256_hash() {
    local input="$1"
    local py
    py=$(find_python 2>/dev/null || echo "python3")
    echo -n "$input" | "$py" -c "import sys,hashlib;print(hashlib.sha256(sys.stdin.buffer.read()).hexdigest())" 2>/dev/null
}

# ---- Utility: get current timestamp ----
now_iso() {
    local py
    py=$(find_python 2>/dev/null || echo "python3")
    "$py" -c "import datetime;print(datetime.datetime.utcnow().isoformat()+'Z')" 2>/dev/null
}
