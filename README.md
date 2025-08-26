# OTW CLI – OverTheWire Wargame Companion

🛠 A lightweight, zero-dependency Python CLI for managing passwords, notes, and progress while playing [OverTheWire](https://overthewire.org/wargames/) wargames.

## 🎯 Features

- 🔐 Save and retrieve passwords by level
- 📝 Open Markdown notes per level
- 📂 Organized by game (`bandit`, `natas`, `leviathan`, etc.)
- 📊 Track your progress across all games with `otw status`
- 🚀 Secure SSH launch with automatic clipboard copy (using `fip`)
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

### 📊 Check your progress
```bash
otw status  # Shows highest level reached for each game
```

### 🔐 SSH into level
```bash
otw ssh <wargame> <level>  # Auto-copies password to clipboard via fip
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

All OverTheWire wargames are supported! SSH ports are pre-configured for each game.

### 🔐 SSH-based Games
| Game | Port | Status |
|------|------|--------|
| `bandit` | 2220 | ✅ Fully supported |
| `leviathan` | 2223 | ✅ Fully supported |
| `narnia` | 2226 | ✅ Fully supported |
| `behemoth` | 2221 | ✅ Fully supported |
| `utumno` | 2227 | ✅ Fully supported |
| `maze` | 2225 | ✅ Fully supported |
| `manpage` | 2224 | ✅ Fully supported |
| `formulaone` | 2232 | ✅ Fully supported |
| `vortex` | 2228 | ✅ Fully supported |
| `drifter` | 2230 | ✅ Fully supported |
| `krypton` | 2231 | ✅ Fully supported |

### 🌐 Web-based Games
| Game | Access Method | Status |
|------|---------------|--------|
| `natas` | Web browser | ✅ Password/note storage only |

> Note: For `natas`, use `otw save` and `otw pw` to manage passwords, but SSH is not available.

---

## 💻 Requirements

- Python 3.7+
- OpenSSH client (`ssh`)
- `git` (for version control)
- `fip` (for clipboard support) - [fip installation guide](https://github.com/Blakemagne/fip-fop)

---

## 🔗 Global CLI Access (Without Activating Virtualenv)

If you want to run `otw` from **anywhere** without activating your virtual environment every time, you can create a symlink:

### ✅ 1. Locate your CLI inside the virtual environment

If you used a virtual environment like this:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

Then your CLI will be located at:

```
venv/bin/otw
```

### ✅ 2. Create a symlink into your local bin

```bash
ln -s ~/path/to/your/otw-cli/venv/bin/otw ~/.local/bin/otw
```

Replace `~/path/to/your/otw-cli/` with your actual path.

### ✅ 3. Make sure `~/.local/bin` is in your `$PATH`

Check with:

```bash
echo $PATH | tr ':' '\n' | grep .local/bin
```

If not, add this to your `~/.bashrc`, `~/.zshrc`, or `~/.profile`:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Then reload:

```bash
source ~/.bashrc  # or ~/.zshrc
```

### ✅ 4. Test it globally

Now you can run:

```bash
otw --help
```

From **anywhere**, even without activating the virtualenv.

> This works because the symlink points directly to the CLI binary inside the virtual environment.

---

## 🧑‍💻 Author

**Blakemagne**  
stonks god

---


