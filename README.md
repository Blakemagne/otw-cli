# OTW CLI – OverTheWire Wargame Companion

🛠 A lightweight, zero-dependency Python CLI for managing passwords, notes, and progress while playing [OverTheWire](https://overthewire.org/wargames/) wargames.

## 🎯 Features

- 🔐 Save and retrieve passwords by level
- 📝 Open Markdown notes per level
- 📂 Organized by game (`bandit`, `natas`, `leviathan`, etc.)
- 🚀 SSH directly into a level (with `sshpass`)
- ☁️ Git push your notes and password progress (optional)

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/otw-cli.git
cd otw-cli
pip install -e .
```

> Make sure you have your `otw-wargame-passwords` repo located at:
> `~/workspace/github.com/Blakemagne/otw-wargame-passwords`

---

## 📁 Folder Structure (expected)

```
~/workspace/github.com/Blakemagne/otw-wargame-passwords/
├── bandit/
│   ├── level0.txt
│   ├── level0.md
│   └── ...
├── leviathan/
│   └── level0.txt
└── ...
```

---

## 🧪 Usage

### 📥 Save a password
```bash
otw bandit save 3 abc123
```

### 🔓 Show a saved password
```bash
otw bandit pw 3
```

### 📝 Open notes (Markdown)
```bash
otw bandit note 3
```

### 📜 List saved levels
```bash
otw bandit ls
```

### 🔐 SSH into level (requires `sshpass`)
```bash
otw bandit ssh 3
```

### ☁️ Git push notes and passwords
```bash
otw bandit push
```

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

> Don’t see your favorite game? [Submit a pull request](https://github.com/yourusername/otw-cli/pulls) or edit the `WARGAMES` list in `cli.py`.

---

## 📥 Requirements

- Python 3.7+
- `sshpass` (for `ssh` command)
- `git` (if you use `push`)

---

## 🧪 Tips

- Set your default editor with:
  ```bash
  export EDITOR=vim   # or nano, code, etc.
  ```
- Keep your password repo private and version-controlled.

---

## 🧑‍💻 Author

**Blakemagne**  
Wargame optimizer | Builder of tools for focused hacking workflows

---

## ⛨ Disclaimer

This tool is intended for ethical hacking and CTF use only. Respect the rules of each wargame and never reuse passwords from these challenges elsewhere.

