# Quick Start Guide

## Installation

1. **Navigate to the project directory:**
```bash
cd pgp-tool
```

2. **Activate the virtual environment:**
```bash
source venv/bin/activate
```

3. **Run the application:**
```bash
./run.sh
```

Or simply:
```bash
python app.py
```

4. **Open your browser:**
Navigate to: http://localhost:5000

## First Steps

### 1. Generate Your First Key Pair

1. Click on **"Keys"** in the navigation
2. Click **"Generate New Key Pair"**
3. Fill in your details:
   - **Full Name**: Your name
   - **Email**: Your email address
   - **Comment**: (Optional) Something like "My PGP Key"
   - **Passphrase**: Choose a strong passphrase (at least 8 characters)
   - **Key Length**: Keep 4096 bits (recommended)
4. Click **"Generate Key Pair"**

⏱️ Generation may take 10-30 seconds...

### 2. Import a Contact's Public Key

1. Get your contact's public key (they should send you an `.asc` file or the text)
2. Go to **"Keys"** page
3. Click **"Import Key"**
4. Either:
   - Upload the `.asc` file, OR
   - Paste the key text (starts with `-----BEGIN PGP PUBLIC KEY BLOCK-----`)
5. Click **"Import Key"**

### 3. Encrypt a Message

1. Go to **"Encrypt"** page
2. Select input type: **Text**
3. Write your message
4. Select the recipient(s) from the list
5. (Optional) Check "Sign with my key" and enter your passphrase
6. Click **"Encrypt"**
7. Copy the encrypted result or download it

### 4. Decrypt a Message

1. Go to **"Decrypt"** page
2. Paste the encrypted message (or upload file)
3. Enter your passphrase
4. Click **"Decrypt"**
5. View the decrypted message

### 5. Sign a Message

1. Go to **"Sign"** page
2. Enter your message
3. Select your signing key
4. Enter your passphrase
5. Choose signature type:
   - **Clear-sign**: Message remains readable with signature
   - **Detached**: Separate signature file
6. Click **"Sign"**

### 6. Verify a Signature

1. Go to **"Verify"** page
2. Paste the signed message
3. (If detached signature) Upload the `.sig` file
4. Click **"Verify Signature"**
5. See if the signature is valid ✓ or invalid ✗

## Common Workflows

### Secure Communication with a Friend

1. **You**: Generate your key pair, export your public key
2. **You**: Send your public key to your friend
3. **Friend**: Imports your public key
4. **Friend**: Generates their key pair, exports their public key
5. **Friend**: Sends you their public key
6. **You**: Import friend's public key
7. **Now**: You can both encrypt messages for each other!

### Sending an Encrypted Email

1. Import recipient's public key
2. Write your message in the Encrypt page
3. Select recipient
4. Sign with your key (so they know it's from you)
5. Copy the encrypted result
6. Paste into your email and send

### Verifying Downloaded Software

If a developer provides a `.sig` file:

1. Download the software file and the `.sig` signature file
2. Import the developer's public key
3. Go to Verify page
4. Upload the software file as "Signed File"
5. Upload the `.sig` as "Signature File"
6. Verify - if valid ✓, the file hasn't been tampered with

## Security Tips

🔐 **Passphrase**: Choose a strong, unique passphrase for your private key

🔑 **Private Key**: NEVER share your private key with anyone

📋 **Fingerprint**: Always verify key fingerprints before encrypting sensitive data

💾 **Backup**: Export and securely backup your keys

🗑️ **Revocation**: Create a revocation certificate (export private key) and store it safely

## Troubleshooting

### Can't generate keys?
- Make sure GnuPG is installed: `gpg --version`
- Check passphrase is at least 8 characters

### Import failed?
- Verify the key format (should start with `-----BEGIN PGP...`)
- Check for copy-paste errors

### Decryption failed?
- Verify you entered the correct passphrase
- Make sure the message was encrypted for YOUR public key
- Check that you have the corresponding private key

### No recipients available?
- You need to import public keys before encrypting
- Go to Keys → Import Key

## Files and Directories

- `/keys/` - Your GnuPG keyring (private keys stored here)
- `/data/` - Metadata and settings
- `.env` - Configuration (contains your secret key)

⚠️ **Never commit `/keys/`, `/data/`, or `.env` to git!**

## Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

## Next Steps

- Read the full [README.md](README.md) for more details
- Explore advanced signature types
- Learn about PGP best practices
- Share your public key with contacts

---

**Need Help?** Check the README.md or GnuPG documentation at https://gnupg.org/
