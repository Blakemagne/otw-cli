# OTW CLI – OverTheWire Wargame Companion

🛠 A lightweight, zero-dependency Python CLI for managing passwords, notes, and progress while playing [OverTheWire](https://overthewire.org/wargames/) wargames.

## 🎯 Features

- 🔐 Save and retrieve passwords by level
- 📝 Open Markdown notes per level
- 📂 Organized by game (`bandit`, `natas`, `leviathan`, etc.)
- 🚀 Secure SSH launch with password guidance (no `sshpass`)
- ☁️ Git push your notes and password progress (optional)
- 🔧 Configurable vault location with zero dependencies

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/otw-cli.git
cd otw-cli
pip install -e .
```

> Then configure your vault path:
```bash
otw config ~/Documents/otw-wargame-passwords
```

---

## 🗂 Folder Structure (expected)

```
~/Documents/otw-wargame-passwords/
├── bandit/
│   ├── level0.txt
│   ├── level0.md
│   └── ...
├── narnia/
│   └── level1.txt
└── ...
```

---

## 🧪 Usage

### 📥 Save a password
```bash
otw save <wargame> <level> <password>
```

### 🔓 Show a saved password
```bash
otw pw <wargame> <level> 
```

### 📝 Open notes (Markdown)
```bash
otw note <wargame> <level> 
```

### 📜 List saved levels
```bash
otw ls <wargame>
```

### 🔐 SSH into level
```bash
otw ssh <wargame> <level> 
```

### ☁️ Git push notes and passwords
```bash
otw push <wargame>
```

---

## 🚀 First-Time Setup: Starting from Level 0

If you're just getting started with **Bandit Level 0**, and haven't created your password vault yet, follow this workflow:

### 🛠️ 1. Create Your Vault Directory

You can either:

- **Clone a private Git repo** to store your passwords and notes:
  ```bash
  git clone git@github.com:yourusername/otw-wargame-passwords.git
  ```

- **Or create a local directory manually**:
  ```bash
  mkdir -p ~/Documents/otw-wargame-passwords
  cd ~/Documents/otw-wargame-passwords
  git init
  ```

> 🧠 Tip: Keep this repo **private** — it will contain your OverTheWire passwords.

### 🔧 2. Configure `otw` to point to your vault

Tell `otw` where your vault is:

```bash
otw config ~/Documents/otw-wargame-passwords
```

This creates a config file at:
```
~/.config/otw/config
```

With:
```
base_dir=/home/youruser/Documents/otw-wargame-passwords
```

### ✅ 3. Start Logging Progress

Now you're ready to use the CLI:

```bash
otw save bandit 0 ZjLjTmM6FvvyRnrb2rfNWOZOTa6ip5If
otw note bandit 0
```

These commands will:
- Automatically create the `bandit/` folder (if needed)
- Save your password as `level0.txt`
- Create an editable Markdown file for your notes: `level0.md`

### ☁️ 4. Push to GitHub (optional)

If your vault is a Git repo:

```bash
otw push bandit
```

This runs:
- `git add .`
- `git commit -m "Progress update ..."`
- `git push origin main`

So your notes and passwords stay synced.

### 🚨 What if you skip config?

If you try to use the tool before configuring:

```bash
otw save <wargame> <level> <password>
```

You’ll get:

```
❌ Config file not found. Run: otw config <path-to-vault>
```

No crash. Just guidance.

---

## ✅ Supported Games

- `bandit`
- `natas`
- `leviathan`
- `krypton`
- `narnia`
- `behemoth`
- `utumno`
- `maze`
- `vortex`
- `manpage`
- `drifter`
- `formulaone`

> Don’t see your favorite game? Edit the `WARGAMES` list in `cli.py`.

---

## 💻 Requirements

- Python 3.7+
- OpenSSH client (`ssh`)
- `git` (for version control)

---

## 🧠 Tips

- Set your default note editor:
  ```bash
  export EDITOR=vim   # or nano, code, etc.
  ```
- Store your repo safely with GitHub, GitLab, or your own backup
- Keep it private, but portable

---

## 🧑‍💻 Author

**Blakemagne**  
Builder of focused CLI workflows | CTF optimizer | Tools for thinking

---

## 🛡 Disclaimer

This tool is intended for ethical hacking and CTF use only. Never reuse OverTheWire credentials outside of practice environments.


