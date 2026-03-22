# PGP Tool - Local Web Application

A local web application for PGP cryptographic operations: encryption, decryption, signing, and signature verification.

## Features

- **Key Management**
  - Generate RSA key pairs (2048-4096 bits)
  - Import/Export public and private keys
  - Delete keys

- **Encryption**
  - Encrypt text or files
  - Support for multiple recipients
  - Optional signing during encryption

- **Decryption**
  - Decrypt encrypted messages or files
  - Verify embedded signatures

- **Signing**
  - Clear-sign messages (readable text)
  - Detached signatures
  - Normal binary signatures

- **Verification**
  - Verify inline signatures
  - Verify detached signatures
  - Display trust levels and signer information

## Requirements

- Python 3.8 or higher
- GnuPG (comes pre-installed on macOS)

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/icilev/pgp-tool.git
cd pgp-tool
```

2. **Create a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
```

Edit `.env` and set your `SECRET_KEY`:
```bash
# Generate a secure secret key
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and add it to `.env`:
```
SECRET_KEY=your-generated-secret-key-here
```

## Usage

1. **Start the application**
```bash
python app.py
```

2. **Open your browser**
Navigate to: `http://localhost:5000`

3. **First-time setup**
   - Go to the "Keys" page
   - Generate your first key pair
   - Import public keys from your contacts

4. **Basic workflow**
   - **Encrypt**: Select recipients → Enter message → Copy encrypted result
   - **Decrypt**: Paste encrypted message → Enter passphrase → View decrypted text
   - **Sign**: Enter message → Select signing key → Copy signed result
   - **Verify**: Paste signed message → View verification result

## Security Considerations

⚠️ **Important Security Notes:**

- **Private Keys**: Never share your private key or passphrase
- **Passphrases**: Not stored anywhere - entered only when needed
- **Local Only**: All operations happen locally on your machine
- **Backups**: Backup your keys in a secure location
- **Fingerprints**: Always verify key fingerprints before encrypting
- **Revocation**: Create a revocation certificate for your keys

### What This Tool Does NOT Do

- **Memory Security**: Python cannot securely wipe memory
- **Network Operations**: No key servers or online features
- **Advanced Key Management**: No key signing, trust paths, or web of trust

## File Structure

```
pgp-tool/
├── app.py                  # Main Flask application
├── config.py               # Configuration
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not in git)
├── modules/
│   ├── key_manager.py     # Key operations
│   ├── pgp_operations.py  # Encrypt/decrypt/sign/verify
│   ├── storage.py         # JSON storage
│   └── utils.py           # Utility functions
├── templates/             # HTML templates
├── static/                # CSS and JavaScript
├── data/                  # JSON metadata (not in git)
└── keys/                  # GnuPG keyring (not in git)
```

## Troubleshooting

### GnuPG not found
```bash
# Check if GnuPG is installed
gpg --version

# macOS: Install with Homebrew if needed
brew install gnupg
```

### Permission errors
```bash
# Fix permissions for keys directory
chmod 700 keys
chmod 700 data
```

### Import errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

## Development

### Tech Stack
- **Backend**: Flask 3.0
- **PGP**: python-gnupg (wrapper for GnuPG)
- **Frontend**: HTML, CSS, Vanilla JavaScript
- **Security**: Flask-WTF (CSRF protection)

### Adding Features

The modular structure makes it easy to extend:

- **New operations**: Add to `modules/pgp_operations.py`
- **New routes**: Add to `app.py`
- **New templates**: Add to `templates/`
- **New styles**: Add to `static/css/style.css`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This software is provided "as is", without warranty of any kind. Use at your own risk.

## Support

For issues or questions:
1. Check the GnuPG documentation: https://gnupg.org/documentation/
2. Check python-gnupg docs: https://gnupg.readthedocs.io/
3. Review Flask documentation: https://flask.palletsprojects.com/

## Acknowledgments

- GnuPG for the cryptographic backend
- python-gnupg for the Python wrapper
- Flask for the web framework
