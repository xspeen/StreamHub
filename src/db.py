#!/usr/bin/env python3
"""
StreamHub Database Module
Handles local JSON-based storage for user profile, passcode, settings, and channel cache.
Uses only Python standard library - no external packages.
"""

import json
import os
import sys
import hashlib
import datetime


class StreamHubDB:
    """Simple JSON-file database for StreamHub local storage."""

    def __init__(self, data_dir):
        """Initialize with the data directory path."""
        self.data_dir = data_dir
        self.config_path = os.path.join(data_dir, "config.json")
        self.profile_path = os.path.join(data_dir, "profile.json")
        self.cache_path = os.path.join(data_dir, "channels_cache.json")
        os.makedirs(data_dir, exist_ok=True)

    # ---- Config operations ----

    def get_config(self):
        """Load config from disk. Returns dict or default config."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {
            "passcode_hash": "",
            "port": 8080,
            "theme": "dark"
        }

    def save_config(self, config):
        """Save config dict to disk."""
        with open(self.config_path, "w") as f:
            json.dump(config, f, indent=2)

    def hash_passcode(self, passcode):
        """SHA-256 hash a passcode string."""
        return hashlib.sha256(passcode.encode("utf-8")).hexdigest()

    def verify_passcode(self, passcode):
        """Verify a passcode against the stored hash."""
        config = self.get_config()
        stored_hash = config.get("passcode_hash", "")
        if not stored_hash:
            return True  # No passcode set = first run
        return self.hash_passcode(passcode) == stored_hash

    def set_passcode(self, new_passcode):
        """Set a new passcode hash in config."""
        config = self.get_config()
        config["passcode_hash"] = self.hash_passcode(new_passcode)
        self.save_config(config)

    def has_passcode(self):
        """Check if a passcode has been set."""
        config = self.get_config()
        return bool(config.get("passcode_hash", ""))

    # ---- Profile operations ----

    def get_profile(self):
        """Load profile from disk. Returns dict or default profile."""
        if os.path.exists(self.profile_path):
            try:
                with open(self.profile_path, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        now = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
        return {
            "name": "User",
            "avatar": "U",
            "created_at": now,
            "last_login": now
        }

    def save_profile(self, profile):
        """Save profile dict to disk."""
        with open(self.profile_path, "w") as f:
            json.dump(profile, f, indent=2)

    def update_login(self):
        """Update last_login timestamp."""
        profile = self.get_profile()
        profile["last_login"] = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
        self.save_profile(profile)

    # ---- Channel cache operations ----

    def get_cached_channels(self):
        """Load cached channels if valid (within 6-hour TTL)."""
        if not os.path.exists(self.cache_path):
            return None
        try:
            with open(self.cache_path, "r") as f:
                cache = json.load(f)
            cached_at = cache.get("timestamp", "")
            if cached_at:
                cache_time = datetime.datetime.fromisoformat(cached_at.rstrip("Z"))
                now = datetime.datetime.now(datetime.timezone.utc)
                diff = (now - cache_time).total_seconds()
                if diff < 21600:  # 6 hours
                    return cache.get("channels", {})
            return None
        except (json.JSONDecodeError, IOError, ValueError):
            return None

    def save_channel_cache(self, channels_by_category):
        """Save channels cache with current timestamp."""
        cache = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
            "channels": channels_by_category
        }
        with open(self.cache_path, "w") as f:
            json.dump(cache, f)

    # ---- Profile exists check ----

    def has_profile(self):
        """Check if a profile file exists and has content."""
        return os.path.exists(self.profile_path) and os.path.getsize(self.profile_path) > 10

    # ---- Device management ----

    def get_devices_path(self):
        return os.path.join(self.data_dir, "allowed_devices.json")

    def get_allowed_devices(self):
        """Load allowed devices list. Returns list of device dicts."""
        path = self.get_devices_path()
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return []

    def save_allowed_devices(self, devices):
        """Save allowed devices list."""
        with open(self.get_devices_path(), "w") as f:
            json.dump(devices, f, indent=2)

    def add_device(self, ip, name=""):
        """Add a device to allowed list. Returns (success, message)."""
        devices = self.get_allowed_devices()
        ip = ip.strip()
        if not ip:
            return False, "IP address required"
        for d in devices:
            if d["ip"] == ip:
                return False, "IP already exists"
        devices.append({
            "ip": ip,
            "name": name or ip,
            "enabled": True,
            "added_at": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
        })
        self.save_allowed_devices(devices)
        return True, "Device added"

    def remove_device(self, ip):
        """Remove a device from allowed list."""
        devices = self.get_allowed_devices()
        devices = [d for d in devices if d["ip"] != ip]
        self.save_allowed_devices(devices)
        return True

    def toggle_device(self, ip):
        """Toggle a device enabled/disabled. Returns new state."""
        devices = self.get_allowed_devices()
        for d in devices:
            if d["ip"] == ip:
                d["enabled"] = not d["enabled"]
                self.save_allowed_devices(devices)
                return d["enabled"]
        return None

    def is_device_allowed(self, ip):
        """Check if a device IP is allowed to access."""
        devices = self.get_allowed_devices()
        if not devices:
            return True  # No devices configured = allow all
        for d in devices:
            if d["ip"] == ip:
                return d.get("enabled", True)
        return False


# Standalone usage for CLI operations
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: db.py <data_dir> <command> [args]")
        print("Commands: verify <passcode>, set_passcode <passcode>, get_profile, save_profile <json>")
        sys.exit(1)

    data_dir = sys.argv[1]
    command = sys.argv[2]
    db = StreamHubDB(data_dir)

    if command == "verify" and len(sys.argv) >= 4:
        result = db.verify_passcode(sys.argv[3])
        print("true" if result else "false")

    elif command == "set_passcode" and len(sys.argv) >= 4:
        db.set_passcode(sys.argv[3])
        print("ok")

    elif command == "get_profile":
        print(json.dumps(db.get_profile()))

    elif command == "save_profile" and len(sys.argv) >= 4:
        profile = json.loads(sys.argv[3])
        db.save_profile(profile)
        print("ok")

    elif command == "has_profile":
        print("true" if db.has_profile() else "false")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
