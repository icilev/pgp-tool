# Changelog

All notable changes to PGP Tool will be documented in this file.

## [1.0.0] - 2026-03-17

### 🎉 Initial Release

#### Added
- **Core Features**
  - Complete PGP key management (generate, import, export, delete)
  - Message and file encryption with multiple recipients
  - Message and file decryption with passphrase protection
  - Digital signature support (clear-sign, detached, binary)
  - Signature verification with trust level display

- **Infrastructure**
  - Flask web application with local-only access
  - GnuPG integration via python-gnupg
  - JSON-based metadata storage
  - CSRF protection for all forms
  - File upload support (10MB limit)

- **User Interface**
  - Dashboard with quick actions
  - Dedicated pages for each operation
  - Clean, modern CSS styling
  - Modal dialogs for key operations
  - Copy-to-clipboard functionality
  - Flash messages for user feedback

- **Security**
  - No passphrase storage
  - Secure key directory permissions (700)
  - Input validation (email, key IDs, fingerprints)
  - Filename sanitization
  - Git ignore for sensitive data

- **Documentation**
  - Comprehensive README
  - Quick start guide
  - Project overview
  - Setup verification script
  - Launch script

- **Developer Features**
  - Modular code organization
  - Type hints in critical functions
  - Docstrings for all modules
  - Configuration via .env file
  - Virtual environment support

### Dependencies
- Flask 3.0.0
- python-gnupg 0.5.0
- Flask-WTF 1.2.0
- python-dotenv 1.0.0
- Werkzeug 3.0.0

### Technical Details
- Python 3.8+ compatible
- GnuPG 2.5+ required
- RSA 4096-bit keys (default)
- ASCII armored output
- Local-only operation (127.0.0.1:5000)

### File Structure
```
23 total files created:
- 7 Python modules
- 7 HTML templates
- 2 static assets (CSS, JS)
- 7 documentation files
```

---

## Future Versions (Planned)

### [1.1.0] - TBD
- [ ] Key expiration management
- [ ] Revocation certificate wizard
- [ ] Batch encryption for multiple files
- [ ] Settings page for user preferences
- [ ] Export operation history

### [1.2.0] - TBD
- [ ] Dark mode
- [ ] Custom themes
- [ ] Keyboard shortcuts
- [ ] Drag-and-drop file upload
- [ ] Progressive web app support

### [2.0.0] - TBD
- [ ] Multiple keyring support
- [ ] Key server integration (optional)
- [ ] Web of trust visualization
- [ ] Smart card support
- [ ] Advanced key editing

---

## Notes

This project follows [Semantic Versioning](https://semver.org/):
- MAJOR version for incompatible API changes
- MINOR version for new functionality in a backwards compatible manner
- PATCH version for backwards compatible bug fixes

---

**Legend:**
- 🎉 Major feature
- ✨ New feature
- 🐛 Bug fix
- 📝 Documentation
- 🔒 Security
- ⚡ Performance
- 💄 UI/UX
- ♻️ Refactoring
