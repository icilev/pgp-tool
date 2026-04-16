# PGP Tool

A local web application for PGP cryptographic operations — encrypt, decrypt, sign, and verify, entirely on your machine.

## Quick Start

```bash
git clone https://github.com/icilev/pgp-tool.git
cd pgp-tool
npm start
```

That's it. The CLI handles everything automatically:

- Creates the Python virtual environment if missing
- Installs all dependencies
- Checks for updates (GitHub + pip) and applies them
- Starts the server and opens your browser

> **Requirement:** [GnuPG](https://gnupg.org/) must be installed.
> ```bash
> brew install gnupg   # macOS
> ```

---

## Features

- **Key Management** — Generate RSA key pairs (2048–4096 bits), import/export, delete
- **Encryption** — Encrypt text or files for one or multiple recipients, with optional signing
- **Decryption** — Decrypt messages or files, verify embedded signatures
- **Signing** — Clear-sign, detached, or binary signatures
- **Verification** — Verify signatures and display trust level + signer info

---

## CLI Commands

| Command | Description |
|---|---|
| `npm start` | Start the app (auto-setup + auto-update) |
| `npm run dev` | Same as start, in development mode |
| `npm run prod` | Start in production mode (no auto-update) |

---

## First Use

1. Open `http://localhost:5000`
2. Go to **Keys** → generate your first key pair
3. Import public keys from your contacts

**Basic workflow**

- **Encrypt** — Select recipients → enter message → copy result
- **Decrypt** — Paste encrypted message → enter passphrase → read
- **Sign** — Enter message → select key → copy signed result
- **Verify** — Paste signed message → see result

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
├── scripts/cli.mjs        # Dev CLI (npm start)
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

## License

MIT — see [LICENSE](LICENSE).
