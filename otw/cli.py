#!/usr/bin/env python3

import os
import sys
import argparse
import subprocess
from datetime import datetime

# 🎮 Supported OTW games
WARGAMES = [
    "bandit", "natas", "leviathan", "krypton", "narnia", "behemoth",
    "utumno", "maze", "vortex", "manpage", "drifter", "formulaone"
]

# 📄 Load BASE_DIR from config file
def load_config():
    config_file = os.path.expanduser("~/.config/otw/config")
    if not os.path.exists(config_file):
        print("❌ Config file not found. Run: otw config <path-to-vault>")
        sys.exit(1)

    with open(config_file) as f:
        for line in f:
            if line.strip().startswith("base_dir="):
                return os.path.expanduser(line.strip().split("=", 1)[1])

    print("❌ base_dir not set in config file.")
    sys.exit(1)

# 🛠 Path builders
def pw_path(game, level): return os.path.join(load_config(), game, f"level{level}.txt")
def note_path(game, level): return os.path.join(load_config(), game, f"level{level}.md")
def game_dir(game): return os.path.join(load_config(), game)

# 🔐 Save a password
def save_password(game, level, password):
    os.makedirs(game_dir(game), exist_ok=True)
    with open(pw_path(game, level), 'w') as f:
        f.write(password)
    print(f"✅ Saved password for {game} level {level}")

# 📥 Show a password
def show_password(game, level):
    path = pw_path(game, level)
    if not os.path.exists(path):
        print(f"❌ No password found for {game} level {level}")
        return
    with open(path) as f:
        print(f.read().strip())

# 📝 Open a note
def edit_note(game, level):
    os.makedirs(game_dir(game), exist_ok=True)
    path = note_path(game, level)
    editor = os.environ.get("EDITOR", "nano")
    subprocess.call([editor, path])

# 📜 List saved levels
def list_levels(game):
    directory = game_dir(game)
    if not os.path.exists(directory):
        print(f"⚠️ No data yet for {game}")
        return
    files = sorted(f for f in os.listdir(directory) if f.endswith(".txt"))
    for f in files:
        print(f)

# 🔐 Secure SSH (manual password entry)
def ssh_to_game(game, level):
    path = pw_path(game, level)
    if not os.path.exists(path):
        print(f"❌ No password found for {game} level {level}")
        return

    with open(path) as f:
        pw = f.read().strip()

    user = f"{game}{level}"
    host = f"{game}.labs.overthewire.org"
    port = "2220"

    print(f"\n🔑 Password for {user}: {pw}")
    print(f"👉 Starting SSH session (copy & paste password when prompted):\n")
    subprocess.run(["ssh", f"{user}@{host}", "-p", port])

# ☁️ Git push changes
def git_push(game):
    game_path = game_dir(game)
    try:
        subprocess.run(["git", "-C", game_path, "add", "."], check=True)
        subprocess.run(["git", "-C", game_path, "commit", "-m", f"Progress update {datetime.now()}"], check=True)
        subprocess.run(["git", "-C", game_path, "push", "origin", "main"], check=True)
        print(f"✅ Pushed changes for {game}")
    except subprocess.CalledProcessError:
        print("❌ Git push failed. Is this a git repo with a remote?")

# 🧭 Save config
def save_config(base_dir):
    config_dir = os.path.expanduser("~/.config/otw")
    os.makedirs(config_dir, exist_ok=True)
    with open(os.path.join(config_dir, "config"), "w") as f:
        f.write(f"base_dir={base_dir.strip()}\n")
    print(f"✅ Config saved to {config_dir}/config")

# 🚀 Entry Point
def main():
    parser = argparse.ArgumentParser(description="OTW Wargame CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # save
    save_cmd = subparsers.add_parser("save", help="Save a password")
    save_cmd.add_argument("game", choices=WARGAMES)
    save_cmd.add_argument("level")
    save_cmd.add_argument("password")

    # pw
    pw_cmd = subparsers.add_parser("pw", help="Show saved password")
    pw_cmd.add_argument("game", choices=WARGAMES)
    pw_cmd.add_argument("level")

    # note
    note_cmd = subparsers.add_parser("note", help="Edit level notes")
    note_cmd.add_argument("game", choices=WARGAMES)
    note_cmd.add_argument("level")

    # ls
    ls_cmd = subparsers.add_parser("ls", help="List saved levels")
    ls_cmd.add_argument("game", choices=WARGAMES)

    # ssh
    ssh_cmd = subparsers.add_parser("ssh", help="Secure SSH into level (manual password entry)")
    ssh_cmd.add_argument("game", choices=WARGAMES)
    ssh_cmd.add_argument("level")

    # push
    push_cmd = subparsers.add_parser("push", help="Git push changes for a game")
    push_cmd.add_argument("game", choices=WARGAMES)

    # config
    config_cmd = subparsers.add_parser("config", help="Set base directory for your password vault")
    config_cmd.add_argument("base_dir", help="Path to your vault (e.g., ~/Documents/otw-vault)")

    # Dispatch
    args = parser.parse_args()
    match args.command:
        case "save":
            save_password(args.game, args.level, args.password)
        case "pw":
            show_password(args.game, args.level)
        case "note":
            edit_note(args.game, args.level)
        case "ls":
            list_levels(args.game)
        case "ssh":
            ssh_to_game(args.game, args.level)
        case "push":
            git_push(args.game)
        case "config":
            save_config(args.base_dir)

if __name__ == "__main__":
    main()
