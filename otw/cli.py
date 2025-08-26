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

# 🔌 SSH port configuration for each game
SSH_PORTS = {
    "bandit": 2220,
    "leviathan": 2223,
    "narnia": 2226,
    "behemoth": 2221,
    "utumno": 2227,
    "maze": 2225,
    "manpage": 2224,
    "formulaone": 2232,
    "vortex": 2228,
    "drifter": 2230,
    "krypton": 2231,
}

# 🌐 Non-SSH games (web-based)
WEB_GAMES = ["natas"]

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

# 📊 Show current status for all games
def show_status():
    vault = load_config()
    has_progress = False
    
    for game in WARGAMES:
        directory = game_dir(game)
        if os.path.exists(directory):
            # Find all password files (level*.txt)
            files = [f for f in os.listdir(directory) if f.startswith("level") and f.endswith(".txt")]
            if files:
                # Extract level numbers and find the highest
                levels = []
                for f in files:
                    try:
                        level_num = int(f[5:-4])  # Extract number from "levelN.txt"
                        levels.append(level_num)
                    except ValueError:
                        continue
                
                if levels:
                    max_level = max(levels)
                    print(f"🎮 {game}: Level {max_level}")
                    has_progress = True
    
    if not has_progress:
        print("⚠️ No progress saved yet. Start with: otw save <game> <level> <password>")

# 🔐 Secure SSH with automatic clipboard copy via fip
def ssh_to_game(game, level):
    # Check if game uses SSH
    if game in WEB_GAMES:
        print(f"❌ {game} is a web-based game and doesn't use SSH.")
        print(f"💡 Access {game} at: http://{game}{level}.{game}.labs.overthewire.org")
        return
    
    if game not in SSH_PORTS:
        print(f"⚠️ SSH port not configured for {game}. This game might not support SSH.")
        return

    path = pw_path(game, level)
    if not os.path.exists(path):
        print(f"❌ No password found for {game} level {level}")
        return

    # Run otw pw | fip in background to copy password to clipboard
    try:
        # Use shell=True to enable piping
        subprocess.Popen(f"otw pw {game} {level} | fip", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"📋 Password copied to clipboard!")
    except Exception:
        # If fip fails, just continue - password will be shown anyway
        pass

    user = f"{game}{level}"
    host = f"{game}.labs.overthewire.org"
    port = str(SSH_PORTS[game])
    
    print(f"👉 Starting SSH session to {user}@{host} on port {port}...\n")
    subprocess.run(["ssh", f"{user}@{host}", "-p", port])

# ☁️ Git push changes
def git_push(game):
    vault = load_config()
    os.chdir(vault)

    if game == "all":
        subprocess.run(["git", "add", "."], check=True)
        result = subprocess.run(["git", "diff", "--cached", "--name-only"], capture_output=True, text=True)
        files = result.stdout.strip().split("\n")
        levels = set()
        for f in files:
            if "/" in f and "level" in f:
                parts = f.split("/")
                if len(parts) >= 2:
                    game = parts[0]
                    level = parts[1].split(".")[0]
                    levels.add(f"{game} {level}")
        if levels:
            msg = "🔐 Progress: " + ", ".join(sorted(levels))
        else:
            msg = f"📦 Updated vault – {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", msg])
    else:
        game_path = game_dir(game)
        subprocess.run(["git", "add", game], check=True)
        subprocess.run(["git", "commit", "-m", f"Progress update {game} – {datetime.now()}"], check=True)

    subprocess.run(["git", "push", "origin", "main"], check=True)
    print(f"✅ Pushed changes for {game}")

# ☁️ Git pull changes
def git_pull(game):
    vault = load_config()
    os.chdir(vault)
    subprocess.run(["git", "pull", "origin", "main"], check=True)
    print("✅ Pulled latest changes from GitHub")

# 🧭 Save config
def save_config(base_dir):
    config_dir = os.path.expanduser("~/.config/otw")
    os.makedirs(config_dir, exist_ok=True)
    with open(os.path.join(config_dir, "config"), "w") as f:
        f.write(f"base_dir={base_dir.strip()}\n")
    print(f"✅ Config saved to {config_dir}/config")

# 🚀 Entry Point
def main():
    parser = argparse.ArgumentParser(
        description="🎮 OTW CLI - Your OverTheWire Wargame Companion\n\nManage passwords and notes for OverTheWire wargames with ease!",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""📚 EXAMPLES:
  Getting Started:
    otw config ~/Documents/otw-vault      # Set up your password vault
    otw save bandit 0 password123         # Save your first password
    otw note bandit 0                     # Write notes about the level
    otw ssh bandit 1                      # SSH to next level (auto-copies password)

  Track Progress:
    otw status                             # See your progress in all games
    otw ls bandit                          # List all saved bandit levels
    otw pw bandit 5                        # Show password for bandit level 5

  Sync with Git:
    otw push bandit                        # Push bandit progress to GitHub
    otw pull all                           # Pull latest changes from GitHub

🎯 GAME PROGRESSION:
  bandit → natas → leviathan → krypton → narnia → behemoth → ...

💡 TIP: Start with 'otw config' to set up your vault location!
        """
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # save
    save_cmd = subparsers.add_parser(
        "save", 
        help="💾 Save a password for a game level",
        description="Save a password for a specific game and level.\nCreates the game directory if it doesn't exist.",
        epilog="Example: otw save bandit 5 'UsvVyFSfZZWbi6wgC7dAFyFuR6jQQUhR'"
    )
    save_cmd.add_argument("game", choices=WARGAMES, help="The wargame name")
    save_cmd.add_argument("level", help="Level number (e.g., 0, 1, 2...)")
    save_cmd.add_argument("password", help="The password to save")

    # pw
    pw_cmd = subparsers.add_parser(
        "pw", 
        help="🔑 Show saved password for a level",
        description="Display the saved password for a specific game and level.",
        epilog="Example: otw pw bandit 5\nTip: Pipe to fip for clipboard: otw pw bandit 5 | fip"
    )
    pw_cmd.add_argument("game", choices=WARGAMES, help="The wargame name")
    pw_cmd.add_argument("level", help="Level number")

    # note
    note_cmd = subparsers.add_parser(
        "note", 
        help="📝 Edit notes for a level (opens editor)",
        description="Open your default editor to write/edit Markdown notes for a level.",
        epilog="Example: otw note bandit 5\nTip: Set $EDITOR environment variable to use your preferred editor"
    )
    note_cmd.add_argument("game", choices=WARGAMES, help="The wargame name")
    note_cmd.add_argument("level", help="Level number")

    # ls
    ls_cmd = subparsers.add_parser(
        "ls", 
        help="📋 List all saved levels for a game",
        description="Show all levels with saved passwords for a specific game.",
        epilog="Example: otw ls bandit"
    )
    ls_cmd.add_argument("game", choices=WARGAMES, help="The wargame name")

    # ssh
    ssh_cmd = subparsers.add_parser(
        "ssh", 
        help="🔐 SSH into a level (auto-copies password)",
        description="Connect to a wargame level via SSH.\nAutomatically copies password to clipboard using fip.",
        epilog="Example: otw ssh bandit 5\nNote: Paste password when prompted by SSH"
    )
    ssh_cmd.add_argument("game", choices=WARGAMES, help="The wargame name")
    ssh_cmd.add_argument("level", help="Level number")

    # push
    push_cmd = subparsers.add_parser(
        "push", 
        help="⬆️  Push your progress to GitHub",
        description="Commit and push your passwords/notes to a Git repository.",
        epilog="Examples:\n  otw push bandit    # Push only bandit progress\n  otw push all       # Push all changes"
    )
    push_cmd.add_argument("game", help="Game name or 'all' for everything")

    # pull
    pull_cmd = subparsers.add_parser(
        "pull", 
        help="⬇️  Pull latest changes from GitHub",
        description="Pull the latest passwords/notes from your Git repository.",
        epilog="Example: otw pull all"
    )
    pull_cmd.add_argument("game", help="Game name or 'all' (currently only 'all' works)")

    # config
    config_cmd = subparsers.add_parser(
        "config", 
        help="⚙️  Configure your password vault location",
        description="Set the base directory where passwords and notes will be stored.\nRun this first to set up OTW CLI!",
        epilog="Example: otw config ~/Documents/otw-vault\nTip: Use a Git repository for easy syncing"
    )
    config_cmd.add_argument("base_dir", help="Path to your vault directory")

    # status
    status_cmd = subparsers.add_parser(
        "status", 
        help="📊 Show your progress across all games",
        description="Display the highest level reached in each wargame based on saved passwords.",
        epilog="Example: otw status"
    )

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
        case "pull":
            git_pull(args.game)
        case "config":
            save_config(args.base_dir)
        case "status":
            show_status()

if __name__ == "__main__":
    main()
