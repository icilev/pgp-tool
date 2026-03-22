"""Utility functions for the PGP tool"""

import re
from datetime import datetime
from werkzeug.utils import secure_filename as werkzeug_secure_filename


def secure_filename(filename):
    """Sanitize filename for safe storage"""
    return werkzeug_secure_filename(filename)


def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_key_id(key_id):
    """Validate PGP key ID format (8 or 16 hex characters)"""
    pattern = r'^[A-Fa-f0-9]{8}$|^[A-Fa-f0-9]{16}$'
    return bool(re.match(pattern, key_id))


def validate_fingerprint(fingerprint):
    """Validate PGP fingerprint format (40 hex characters, spaces optional)"""
    # Remove spaces
    fp = fingerprint.replace(' ', '')
    pattern = r'^[A-Fa-f0-9]{40}$'
    return bool(re.match(pattern, fp))


def format_fingerprint(fingerprint):
    """Format fingerprint with spaces for readability"""
    # Remove existing spaces
    fp = fingerprint.replace(' ', '')

    # Add spaces every 4 characters
    formatted = ' '.join([fp[i:i+4] for i in range(0, len(fp), 4)])
    return formatted


def format_timestamp(timestamp):
    """Format Unix timestamp to readable date"""
    if not timestamp:
        return 'N/A'

    try:
        dt = datetime.fromtimestamp(int(timestamp))
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, OSError):
        return 'Invalid date'


def truncate_text(text, max_length=100):
    """Truncate text with ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + '...'


def format_key_size(key_length):
    """Format key size with unit"""
    return f"{key_length} bits"


def get_trust_level_display(trust_level):
    """Convert trust level code to display text"""
    trust_map = {
        'o': 'Unknown',
        'i': 'Invalid',
        'd': 'Disabled',
        'r': 'Revoked',
        'e': 'Expired',
        'q': 'Undefined',
        'n': 'Not trusted',
        'm': 'Marginally trusted',
        'f': 'Fully trusted',
        'u': 'Ultimately trusted',
        '-': 'Unknown',
    }
    return trust_map.get(trust_level, 'Unknown')


def get_key_type_display(algorithm):
    """Convert algorithm code to display text"""
    algo_map = {
        '1': 'RSA',
        '17': 'DSA',
        '18': 'ECDH',
        '19': 'ECDSA',
        '22': 'EdDSA',
    }
    return algo_map.get(str(algorithm), f'Algorithm {algorithm}')


def format_file_size(size_bytes):
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def sanitize_user_input(text):
    """Basic sanitization for user input"""
    if not text:
        return ''

    # Remove null bytes
    text = text.replace('\x00', '')

    # Strip leading/trailing whitespace
    text = text.strip()

    return text
