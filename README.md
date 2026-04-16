# PGP Tool

A local web application for PGP cryptographic operations — encrypt, decrypt, sign, and verify, entirely on your machine.

---

## Windows — Complete Beginner Guide

> You have nothing installed? Start here. This takes about 10 minutes.

### Step 1 — Install Python

1. Go to **https://www.python.org/downloads/**
2. Click the big yellow **"Download Python 3.x.x"** button
3. Run the installer
4. **IMPORTANT:** At the bottom of the first screen, check the box **"Add Python to PATH"**
   (this is easy to miss — do not skip it)
5. Click **"Install Now"**

### Step 2 — Install GnuPG (the encryption engine)

1. Go to **https://www.gpg4win.org/**
2. Click **"Download Gpg4win"** (it's free)
3. Run the installer, leave all options as default, click Next until done

### Step 3 — Download the project

1. Go to **https://github.com/icilev/pgp-tool**
2. Click the green **"Code"** button (top right)
3. Click **"Download ZIP"**
4. Once downloaded, **right-click** the ZIP file → **"Extract All..."**
5. Choose a folder you'll remember (e.g. `C:\Users\YourName\Desktop\pgp-tool`)
6. Click **"Extract"**

### Step 4 — Start the app

Open the extracted `pgp-tool` folder in File Explorer and **double-click `start.bat`**.

The script automatically:
- Creates the Python environment
- Installs all dependencies
- Starts the server and opens your browser

Your browser will open to **http://localhost:5000** — the app is running.

> To stop the app: close the black window, or press `Ctrl+C` in it.

---

## macOS / Linux — Quick Start

```bash
git clone https://github.com/icilev/pgp-tool.git
cd pgp-tool
npm start
```

Requirements: [Node.js](https://nodejs.org/) and [GnuPG](https://gnupg.org/)

```bash
brew install gnupg   # macOS
sudo apt install gnupg  # Ubuntu/Debian
```

---

## First Use

1. Open **http://localhost:5000**
2. Go to **Keys** → generate your first key pair
3. Import public keys from your contacts

**Basic workflow**

- **Encrypt** — Select recipients → enter message → copy result
- **Decrypt** — Paste encrypted message → enter passphrase → read
- **Sign** — Enter message → select key → copy signed result
- **Verify** — Paste signed message → see result

---

## Features

- **Key Management** — Generate RSA key pairs (2048–4096 bits), import/export, delete
- **Encryption** — Encrypt text or files for one or multiple recipients, with optional signing
- **Decryption** — Decrypt messages or files, verify embedded signatures
- **Signing** — Clear-sign, detached, or binary signatures
- **Verification** — Verify signatures and display trust level + signer info

---

## CLI Commands (macOS/Linux with npm)

| Command | Description |
|---|---|
| `npm start` | Start the app (auto-setup + auto-update) |
| `npm run dev` | Same as start, in development mode |
| `npm run prod` | Start in production mode (no auto-update) |

---

## Security Notes

- All operations run **locally** — nothing leaves your machine
- Private keys and passphrases are **never stored**
- Always verify key fingerprints before encrypting
- Back up your keys in a secure location

---

## Project Structure

```
pgp-tool/
├── app.py                 # Flask application
├── config.py              # Configuration
├── requirements.txt       # Python dependencies
├── start.bat              # Windows launcher (double-click)
├── scripts/cli.mjs        # macOS/Linux CLI (npm start)
├── modules/
│   ├── key_manager.py     # Key operations
│   ├── pgp_operations.py  # Encrypt / decrypt / sign / verify
│   ├── storage.py         # JSON storage
│   └── utils.py           # Utilities
├── templates/             # HTML templates
├── static/                # CSS and JavaScript
├── data/                  # Metadata (git-ignored)
└── keys/                  # GnuPG keyring (git-ignored)
```

---

## Tech Stack

- **Backend** — Flask 3, python-gnupg
- **Frontend** — HTML, CSS, Vanilla JS
- **Security** — Flask-WTF (CSRF protection)

---

## Troubleshooting

**"python is not recognized"**
→ Reinstall Python and check "Add Python to PATH" during installation. Then restart cmd.

**"gpg is not recognized"**
→ Reinstall Gpg4win and restart cmd.

**The browser doesn't open automatically**
→ Open it manually and go to http://localhost:5000

---

## License

MIT — see [LICENSE](LICENSE).
