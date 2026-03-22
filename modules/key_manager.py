"""PGP Key Management using python-gnupg"""

import gnupg
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime


class KeyManager:
    """Manages PGP keys using GnuPG"""

    def __init__(self, gnupg_home: Path):
        """Initialize GnuPG instance"""
        self.gnupg_home = Path(gnupg_home)
        self.gnupg_home.mkdir(parents=True, exist_ok=True)
        self.gnupg_home.chmod(0o700)

        # Initialize GnuPG
        self.gpg = gnupg.GPG(gnupghome=str(self.gnupg_home))

    def generate_key(
        self,
        name: str,
        email: str,
        passphrase: str,
        comment: str = '',
        key_type: str = 'RSA',
        key_length: int = 4096,
        subkey_type: str = 'RSA',
        subkey_length: int = 4096,
        expire_date: str = '0'
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Generate a new PGP key pair

        Args:
            name: Real name
            email: Email address
            passphrase: Passphrase to protect private key
            comment: Optional comment
            key_type: Key algorithm (default: RSA)
            key_length: Key length in bits (default: 4096)
            subkey_type: Subkey algorithm (default: RSA)
            subkey_length: Subkey length in bits (default: 4096)
            expire_date: Expiration date (default: 0 = never)

        Returns:
            Tuple of (success, message, fingerprint)
        """
        try:
            input_data = self.gpg.gen_key_input(
                name_real=name,
                name_email=email,
                name_comment=comment,
                key_type=key_type,
                key_length=key_length,
                subkey_type=subkey_type,
                subkey_length=subkey_length,
                expire_date=expire_date,
                passphrase=passphrase
            )

            key = self.gpg.gen_key(input_data)

            if key.fingerprint:
                return True, 'Key generated successfully', str(key.fingerprint)
            else:
                return False, 'Failed to generate key', None

        except Exception as e:
            return False, f'Error generating key: {str(e)}', None

    def import_key(self, key_data: str) -> Tuple[bool, str, List[str]]:
        """
        Import a PGP key

        Args:
            key_data: ASCII armored key data

        Returns:
            Tuple of (success, message, list of fingerprints)
        """
        try:
            result = self.gpg.import_keys(key_data)

            if result.count > 0:
                fingerprints = result.fingerprints
                return True, f'Successfully imported {result.count} key(s)', fingerprints
            else:
                return False, 'No keys were imported', []

        except Exception as e:
            return False, f'Error importing key: {str(e)}', []

    def export_public_key(self, fingerprint: str) -> Tuple[bool, str, Optional[str]]:
        """
        Export a public key

        Args:
            fingerprint: Key fingerprint

        Returns:
            Tuple of (success, message, key_data)
        """
        try:
            key_data = self.gpg.export_keys(fingerprint)

            if key_data:
                return True, 'Public key exported successfully', key_data
            else:
                return False, 'Failed to export public key', None

        except Exception as e:
            return False, f'Error exporting public key: {str(e)}', None

    def export_private_key(self, fingerprint: str, passphrase: str) -> Tuple[bool, str, Optional[str]]:
        """
        Export a private key

        Args:
            fingerprint: Key fingerprint
            passphrase: Passphrase to unlock the key

        Returns:
            Tuple of (success, message, key_data)
        """
        try:
            key_data = self.gpg.export_keys(
                fingerprint,
                secret=True,
                passphrase=passphrase
            )

            if key_data:
                return True, 'Private key exported successfully', key_data
            else:
                return False, 'Failed to export private key (incorrect passphrase?)', None

        except Exception as e:
            return False, f'Error exporting private key: {str(e)}', None

    def list_keys(self, secret: bool = False) -> List[Dict]:
        """
        List all keys

        Args:
            secret: If True, list private keys; otherwise list public keys

        Returns:
            List of key dictionaries
        """
        try:
            keys = self.gpg.list_keys(secret=secret)
            return keys

        except Exception as e:
            return []

    def get_key_info(self, fingerprint: str, secret: bool = False) -> Optional[Dict]:
        """
        Get information about a specific key

        Args:
            fingerprint: Key fingerprint
            secret: If True, look for private key; otherwise public key

        Returns:
            Key information dictionary or None
        """
        try:
            keys = self.gpg.list_keys(secret=secret)

            for key in keys:
                if key['fingerprint'] == fingerprint:
                    return key

            return None

        except Exception as e:
            return None

    def delete_key(self, fingerprint: str, secret: bool = False, passphrase: str = None) -> Tuple[bool, str]:
        """
        Delete a key

        Args:
            fingerprint: Key fingerprint
            secret: If True, delete private key; otherwise public key
            passphrase: Passphrase (required for private keys)

        Returns:
            Tuple of (success, message)
        """
        try:
            result = self.gpg.delete_keys(
                fingerprint,
                secret=secret,
                passphrase=passphrase
            )

            if result.status == 'ok':
                key_type = 'private' if secret else 'public'
                return True, f'{key_type.capitalize()} key deleted successfully'
            else:
                return False, f'Failed to delete key: {result.status}'

        except Exception as e:
            return False, f'Error deleting key: {str(e)}'

    def get_public_keys_list(self) -> List[Dict]:
        """
        Get a simplified list of public keys for UI display

        Returns:
            List of dictionaries with key info
        """
        keys = self.list_keys(secret=False)
        result = []

        for key in keys:
            # Get primary user ID
            uids = key.get('uids', ['Unknown'])
            primary_uid = uids[0] if uids else 'Unknown'

            # Parse name and email from UID
            name = primary_uid
            email = ''
            if '<' in primary_uid and '>' in primary_uid:
                parts = primary_uid.split('<')
                name = parts[0].strip()
                email = parts[1].rstrip('>').strip()

            result.append({
                'fingerprint': key['fingerprint'],
                'keyid': key['keyid'],
                'name': name,
                'email': email,
                'uid': primary_uid,
                'length': key.get('length', 'Unknown'),
                'algo': key.get('algo', 'Unknown'),
                'created': key.get('date', 'Unknown'),
                'expires': key.get('expires', 'Never'),
                'trust': key.get('trust', 'Unknown'),
            })

        return result

    def get_private_keys_list(self) -> List[Dict]:
        """
        Get a simplified list of private keys for UI display

        Returns:
            List of dictionaries with key info
        """
        keys = self.list_keys(secret=True)
        result = []

        for key in keys:
            # Get primary user ID
            uids = key.get('uids', ['Unknown'])
            primary_uid = uids[0] if uids else 'Unknown'

            # Parse name and email from UID
            name = primary_uid
            email = ''
            if '<' in primary_uid and '>' in primary_uid:
                parts = primary_uid.split('<')
                name = parts[0].strip()
                email = parts[1].rstrip('>').strip()

            result.append({
                'fingerprint': key['fingerprint'],
                'keyid': key['keyid'],
                'name': name,
                'email': email,
                'uid': primary_uid,
                'length': key.get('length', 'Unknown'),
                'algo': key.get('algo', 'Unknown'),
                'created': key.get('date', 'Unknown'),
                'expires': key.get('expires', 'Never'),
            })

        return result

    def has_private_key(self, fingerprint: str) -> bool:
        """
        Check if a private key exists for the given fingerprint

        Args:
            fingerprint: Key fingerprint

        Returns:
            True if private key exists
        """
        key = self.get_key_info(fingerprint, secret=True)
        return key is not None
