# PGP Tool

A local web application for PGP cryptographic operations — encrypt, decrypt, sign, and verify, entirely on your machine.

---

## Windows — Complete Beginner Guide

> You have nothing installed? Start here. This takes about 10 minutes.

### Step 1 — Open a terminal

Press **Windows key + R**, type `powershell`, press Enter.

### Step 2 — Install Python and GnuPG

Copy and paste these two lines one by one, pressing Enter after each:

```powershell
winget install -e --id Python.Python.3.13
winget install -e --id GnuPG.Gpg4win
```

> `winget` is built into Windows 10/11 — no need to install anything first.
> Follow the on-screen prompts and accept the licenses.

**Close and reopen PowerShell** after this step so the new tools are recognized.

### Step 3 — Download and launch the project

Copy and paste this entire block at once, then press Enter:

```powershell
Invoke-WebRequest -Uri "https://github.com/icilev/pgp-tool/archive/refs/heads/main.zip" -OutFile "$env:TEMP\pgp-tool.zip"
Expand-Archive "$env:TEMP\pgp-tool.zip" "$env:USERPROFILE\Desktop\"
cd "$env:USERPROFILE\Desktop\pgp-tool-main"
.\start.bat
```

This downloads the project to your Desktop, extracts it, and starts the app.

Your browser will open to **http://localhost:5000** — the app is running.

> To stop the app: close the terminal window, or press `Ctrl+C` in it.
>
> Next time: just double-click `start.bat` in the `pgp-tool-main` folder on your Desktop.

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

**"python is not recognized"** or **"gpg is not recognized"**
→ Close and reopen PowerShell after the `winget` installs. If still failing, restart your computer.

**The browser doesn't open automatically**
→ Open it manually and go to http://localhost:5000

---

## License

MIT — see [LICENSE](LICENSE).
