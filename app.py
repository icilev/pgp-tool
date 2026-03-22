"""
PGP Tool - Local Web Application for PGP Operations
A Flask application for encrypting, decrypting, signing, and verifying PGP messages
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file, Response
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
from pathlib import Path
import tempfile
import os

from config import Config
from modules.key_manager import KeyManager
from modules.pgp_operations import PGPOperations
from modules.storage import KeysMetadataStorage, SettingsStorage
from modules.utils import (
    validate_email,
    format_fingerprint,
    format_timestamp,
    sanitize_user_input
)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Initialize directories
Config.init_app()

# Initialize components
key_manager = KeyManager(Config.GNUPG_HOME)
pgp_ops = PGPOperations(Config.GNUPG_HOME)
keys_metadata = KeysMetadataStorage(Config.KEYS_METADATA_FILE)
settings = SettingsStorage(Config.SETTINGS_FILE)


@app.route('/')
def index():
    """Dashboard page"""
    public_keys = key_manager.get_public_keys_list()
    private_keys = key_manager.get_private_keys_list()

    return render_template(
        'index.html',
        public_keys_count=len(public_keys),
        private_keys_count=len(private_keys)
    )


@app.route('/keys')
def keys():
    """Key management page"""
    public_keys = key_manager.get_public_keys_list()
    private_keys = key_manager.get_private_keys_list()

    # Format fingerprints for display
    for key in public_keys + private_keys:
        key['fingerprint'] = format_fingerprint(key['fingerprint'])
        key['created'] = format_timestamp(key['created'])
        if key.get('expires') and key['expires'] != 'Never':
            key['expires'] = format_timestamp(key['expires'])

    return render_template(
        'keys.html',
        public_keys=public_keys,
        private_keys=private_keys
    )


@app.route('/keys/generate', methods=['POST'])
def generate_key():
    """Generate a new PGP key pair"""
    name = sanitize_user_input(request.form.get('name', ''))
    email = sanitize_user_input(request.form.get('email', ''))
    comment = sanitize_user_input(request.form.get('comment', ''))
    passphrase = request.form.get('passphrase', '')
    key_length = int(request.form.get('key_length', 4096))

    # Validation
    if not name or not email:
        flash('Name and email are required', 'error')
        return redirect(url_for('keys'))

    if not validate_email(email):
        flash('Invalid email address', 'error')
        return redirect(url_for('keys'))

    if not passphrase or len(passphrase) < 8:
        flash('Passphrase must be at least 8 characters', 'error')
        return redirect(url_for('keys'))

    # Generate key
    success, message, fingerprint = key_manager.generate_key(
        name=name,
        email=email,
        comment=comment,
        passphrase=passphrase,
        key_length=key_length
    )

    if success:
        flash(f'Key pair generated successfully! Fingerprint: {format_fingerprint(fingerprint)}', 'success')
    else:
        flash(f'Failed to generate key: {message}', 'error')

    # Clear passphrase from memory
    passphrase = None

    return redirect(url_for('keys'))


@app.route('/keys/import', methods=['POST'])
def import_key():
    """Import a PGP key"""
    key_data = None

    # Check if uploaded via file
    if 'key_file' in request.files:
        file = request.files['key_file']
        if file and file.filename:
            key_data = file.read().decode('utf-8', errors='ignore')

    # Check if pasted as text
    if not key_data:
        key_data = request.form.get('key_data', '')

    if not key_data:
        flash('No key data provided', 'error')
        return redirect(url_for('keys'))

    # Import key
    success, message, fingerprints = key_manager.import_key(key_data)

    if success:
        flash(f'{message}. Fingerprints: {", ".join([format_fingerprint(fp) for fp in fingerprints])}', 'success')
    else:
        flash(f'Failed to import key: {message}', 'error')

    return redirect(url_for('keys'))


@app.route('/keys/export/<fingerprint>')
def export_key(fingerprint):
    """Export a public key"""
    fingerprint = fingerprint.replace(' ', '')

    success, message, key_data = key_manager.export_public_key(fingerprint)

    if success:
        # Return as downloadable file
        return Response(
            key_data,
            mimetype='text/plain',
            headers={
                'Content-Disposition': f'attachment; filename=public_key_{fingerprint[:8]}.asc'
            }
        )
    else:
        flash(f'Failed to export key: {message}', 'error')
        return redirect(url_for('keys'))


@app.route('/keys/export_private', methods=['POST'])
def export_private_key():
    """Export a private key"""
    fingerprint = request.form.get('fingerprint', '').replace(' ', '')
    passphrase = request.form.get('passphrase', '')

    if not passphrase:
        flash('Passphrase is required', 'error')
        return redirect(url_for('keys'))

    success, message, key_data = key_manager.export_private_key(fingerprint, passphrase)

    # Clear passphrase from memory
    passphrase = None

    if success:
        return Response(
            key_data,
            mimetype='text/plain',
            headers={
                'Content-Disposition': f'attachment; filename=private_key_{fingerprint[:8]}.asc'
            }
        )
    else:
        flash(f'Failed to export private key: {message}', 'error')
        return redirect(url_for('keys'))


@app.route('/keys/delete/<fingerprint>', methods=['POST'])
def delete_key(fingerprint):
    """Delete a key"""
    fingerprint = fingerprint.replace(' ', '')
    data = request.get_json()
    key_type = data.get('key_type', 'public')

    is_private = key_type == 'private'

    success, message = key_manager.delete_key(fingerprint, secret=is_private)

    return jsonify({'success': success, 'message': message})


@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt():
    """Encrypt message page"""
    public_keys = key_manager.get_public_keys_list()
    private_keys = key_manager.get_private_keys_list()

    if request.method == 'POST':
        input_type = request.form.get('input_type', 'text')
        recipients = request.form.getlist('recipients')
        sign_enabled = request.form.get('sign') == 'on'

        if not recipients:
            flash('Please select at least one recipient', 'error')
            return redirect(url_for('encrypt'))

        # Get message/file
        message = None
        if input_type == 'text':
            message = request.form.get('message', '')
            if not message:
                flash('Please enter a message', 'error')
                return redirect(url_for('encrypt'))
        else:
            if 'file' not in request.files:
                flash('No file uploaded', 'error')
                return redirect(url_for('encrypt'))
            file = request.files['file']
            if file.filename == '':
                flash('No file selected', 'error')
                return redirect(url_for('encrypt'))
            message = file.read().decode('utf-8', errors='ignore')

        # Get signing options
        signing_key = None
        signing_passphrase = None
        if sign_enabled:
            signing_key = request.form.get('signing_key')
            signing_passphrase = request.form.get('signing_passphrase', '')
            if not signing_passphrase:
                flash('Passphrase required for signing', 'error')
                return redirect(url_for('encrypt'))

        # Encrypt
        success, msg, encrypted_data = pgp_ops.encrypt(
            data=message,
            recipients=recipients,
            sign=signing_key,
            passphrase=signing_passphrase
        )

        # Clear passphrase
        signing_passphrase = None

        if success:
            flash('Message encrypted successfully!', 'success')
            return render_template(
                'encrypt.html',
                public_keys=public_keys,
                private_keys=private_keys,
                encrypted_data=encrypted_data,
                filename='encrypted.asc'
            )
        else:
            flash(f'Encryption failed: {msg}', 'error')

    return render_template(
        'encrypt.html',
        public_keys=public_keys,
        private_keys=private_keys
    )


@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt():
    """Decrypt message page"""
    if request.method == 'POST':
        input_type = request.form.get('input_type', 'text')
        passphrase = request.form.get('passphrase', '')

        if not passphrase:
            flash('Passphrase is required', 'error')
            return redirect(url_for('decrypt'))

        # Get encrypted message/file
        encrypted_data = None
        if input_type == 'text':
            encrypted_data = request.form.get('encrypted_message', '')
            if not encrypted_data:
                flash('Please enter an encrypted message', 'error')
                return redirect(url_for('decrypt'))
        else:
            if 'file' not in request.files:
                flash('No file uploaded', 'error')
                return redirect(url_for('decrypt'))
            file = request.files['file']
            if file.filename == '':
                flash('No file selected', 'error')
                return redirect(url_for('decrypt'))
            encrypted_data = file.read().decode('utf-8', errors='ignore')

        # Decrypt
        success, msg, decrypted_data, signature_info = pgp_ops.decrypt(
            encrypted_data=encrypted_data,
            passphrase=passphrase
        )

        # Clear passphrase
        passphrase = None

        if success:
            flash('Message decrypted successfully!', 'success')
            return render_template(
                'decrypt.html',
                decrypted_data=decrypted_data,
                signature_info=signature_info,
                filename='decrypted.txt'
            )
        else:
            flash(f'Decryption failed: {msg}', 'error')

    return render_template('decrypt.html')


@app.route('/sign', methods=['GET', 'POST'])
def sign():
    """Sign message page"""
    private_keys = key_manager.get_private_keys_list()

    if request.method == 'POST':
        input_type = request.form.get('input_type', 'text')
        signing_key = request.form.get('signing_key')
        passphrase = request.form.get('passphrase', '')
        signature_type = request.form.get('signature_type', 'clearsign')

        if not signing_key or not passphrase:
            flash('Signing key and passphrase are required', 'error')
            return redirect(url_for('sign'))

        # Get message/file
        message = None
        if input_type == 'text':
            message = request.form.get('message', '')
            if not message:
                flash('Please enter a message', 'error')
                return redirect(url_for('sign'))
        else:
            if 'file' not in request.files:
                flash('No file uploaded', 'error')
                return redirect(url_for('sign'))
            file = request.files['file']
            if file.filename == '':
                flash('No file selected', 'error')
                return redirect(url_for('sign'))
            message = file.read().decode('utf-8', errors='ignore')

        # Determine signature options
        detach = signature_type == 'detach'
        clearsign = signature_type == 'clearsign'

        # Sign
        success, msg, signed_data = pgp_ops.sign(
            data=message,
            keyid=signing_key,
            passphrase=passphrase,
            detach=detach,
            clearsign=clearsign
        )

        # Clear passphrase
        passphrase = None

        if success:
            flash('Message signed successfully!', 'success')
            filename = 'signed.sig' if detach else 'signed.asc'
            return render_template(
                'sign.html',
                private_keys=private_keys,
                signed_data=signed_data,
                filename=filename
            )
        else:
            flash(f'Signing failed: {msg}', 'error')

    return render_template('sign.html', private_keys=private_keys)


@app.route('/verify', methods=['GET', 'POST'])
def verify():
    """Verify signature page"""
    if request.method == 'POST':
        input_type = request.form.get('input_type', 'text')

        # Get signed message/file
        signed_data = None
        if input_type == 'text':
            signed_data = request.form.get('signed_message', '')
            if not signed_data:
                flash('Please enter a signed message', 'error')
                return redirect(url_for('verify'))
        else:
            if 'file' not in request.files:
                flash('No file uploaded', 'error')
                return redirect(url_for('verify'))
            file = request.files['file']
            if file.filename == '':
                flash('No file selected', 'error')
                return redirect(url_for('verify'))
            signed_data = file.read().decode('utf-8', errors='ignore')

        # Check for detached signature
        signature = None
        if 'signature_file' in request.files:
            sig_file = request.files['signature_file']
            if sig_file and sig_file.filename:
                signature = sig_file.read().decode('utf-8', errors='ignore')

        # Verify
        success, msg, verification_info = pgp_ops.verify(
            signed_data=signed_data,
            signature=signature
        )

        if verification_info:
            if verification_info.get('timestamp'):
                verification_info['timestamp'] = format_timestamp(verification_info['timestamp'])

            return render_template(
                'verify.html',
                verification_result=verification_info
            )
        else:
            flash(f'Verification error: {msg}', 'error')

    return render_template('verify.html')


@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    flash('File is too large (maximum 10MB)', 'error')
    return redirect(request.url)


if __name__ == '__main__':
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
