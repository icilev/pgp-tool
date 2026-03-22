"""PGP operations: encrypt, decrypt, sign, verify"""

import gnupg
from pathlib import Path
from typing import Tuple, Optional, Dict, Any


class PGPOperations:
    """Handles PGP cryptographic operations"""

    def __init__(self, gnupg_home: Path):
        """Initialize GnuPG instance"""
        self.gnupg_home = Path(gnupg_home)
        self.gpg = gnupg.GPG(gnupghome=str(self.gnupg_home))

    def encrypt(
        self,
        data: str,
        recipients: list,
        sign: Optional[str] = None,
        passphrase: Optional[str] = None,
        armor: bool = True
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Encrypt data for recipients

        Args:
            data: Data to encrypt
            recipients: List of recipient key IDs or fingerprints
            sign: Optional fingerprint of key to sign with
            passphrase: Passphrase for signing key
            armor: ASCII armor output (default: True)

        Returns:
            Tuple of (success, message, encrypted_data)
        """
        try:
            encrypted = self.gpg.encrypt(
                data,
                recipients,
                sign=sign,
                passphrase=passphrase,
                armor=armor,
                always_trust=True  # For local use
            )

            if encrypted.ok:
                return True, 'Encryption successful', str(encrypted)
            else:
                return False, f'Encryption failed: {encrypted.status}', None

        except Exception as e:
            return False, f'Error during encryption: {str(e)}', None

    def decrypt(
        self,
        encrypted_data: str,
        passphrase: str
    ) -> Tuple[bool, str, Optional[str], Optional[Dict]]:
        """
        Decrypt encrypted data

        Args:
            encrypted_data: Encrypted data
            passphrase: Passphrase for private key

        Returns:
            Tuple of (success, message, decrypted_data, signature_info)
        """
        try:
            decrypted = self.gpg.decrypt(encrypted_data, passphrase=passphrase)

            if decrypted.ok:
                # Check for signature information
                signature_info = None
                if decrypted.fingerprint:
                    signature_info = {
                        'fingerprint': decrypted.fingerprint,
                        'username': decrypted.username,
                        'key_id': decrypted.key_id,
                        'signature_id': decrypted.signature_id,
                        'trust_level': decrypted.trust_level,
                        'trust_text': decrypted.trust_text,
                        'timestamp': decrypted.timestamp,
                    }

                return True, 'Decryption successful', str(decrypted), signature_info
            else:
                return False, f'Decryption failed: {decrypted.status}', None, None

        except Exception as e:
            return False, f'Error during decryption: {str(e)}', None, None

    def sign(
        self,
        data: str,
        keyid: str,
        passphrase: str,
        detach: bool = False,
        clearsign: bool = False
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Sign data

        Args:
            data: Data to sign
            keyid: Key ID or fingerprint to sign with
            passphrase: Passphrase for private key
            detach: Create detached signature (default: False)
            clearsign: Create clear-text signature (default: False)

        Returns:
            Tuple of (success, message, signed_data)
        """
        try:
            signed = self.gpg.sign(
                data,
                keyid=keyid,
                passphrase=passphrase,
                detach=detach,
                clearsign=clearsign
            )

            if signed.data:
                return True, 'Signing successful', str(signed)
            else:
                return False, f'Signing failed: {signed.status}', None

        except Exception as e:
            return False, f'Error during signing: {str(e)}', None

    def verify(
        self,
        signed_data: str,
        signature: Optional[str] = None
    ) -> Tuple[bool, str, Optional[Dict]]:
        """
        Verify a signature

        Args:
            signed_data: Signed data or original data (if using detached signature)
            signature: Optional detached signature

        Returns:
            Tuple of (success, message, verification_info)
        """
        try:
            if signature:
                # Detached signature verification
                verified = self.gpg.verify_data(signature, signed_data.encode())
            else:
                # Inline signature verification
                verified = self.gpg.verify(signed_data)

            if verified.valid:
                verification_info = {
                    'valid': True,
                    'fingerprint': verified.fingerprint,
                    'username': verified.username,
                    'key_id': verified.key_id,
                    'signature_id': verified.signature_id,
                    'trust_level': verified.trust_level,
                    'trust_text': verified.trust_text,
                    'timestamp': verified.timestamp,
                    'creation_date': verified.creation_date,
                    'status': verified.status,
                }
                return True, 'Signature is VALID', verification_info
            else:
                verification_info = {
                    'valid': False,
                    'status': verified.status,
                }
                return False, f'Signature is INVALID: {verified.status}', verification_info

        except Exception as e:
            return False, f'Error during verification: {str(e)}', None

    def encrypt_file(
        self,
        file_path: Path,
        recipients: list,
        output_path: Optional[Path] = None,
        sign: Optional[str] = None,
        passphrase: Optional[str] = None,
        armor: bool = True
    ) -> Tuple[bool, str, Optional[Path]]:
        """
        Encrypt a file

        Args:
            file_path: Path to file to encrypt
            recipients: List of recipient key IDs or fingerprints
            output_path: Optional output path (default: file_path.gpg)
            sign: Optional fingerprint of key to sign with
            passphrase: Passphrase for signing key
            armor: ASCII armor output (default: True)

        Returns:
            Tuple of (success, message, output_file_path)
        """
        try:
            if not file_path.exists():
                return False, 'Input file does not exist', None

            if output_path is None:
                suffix = '.asc' if armor else '.gpg'
                output_path = file_path.with_suffix(file_path.suffix + suffix)

            with open(file_path, 'rb') as f:
                encrypted = self.gpg.encrypt_file(
                    f,
                    recipients,
                    sign=sign,
                    passphrase=passphrase,
                    armor=armor,
                    always_trust=True,
                    output=str(output_path)
                )

            if encrypted.ok:
                return True, 'File encryption successful', output_path
            else:
                return False, f'File encryption failed: {encrypted.status}', None

        except Exception as e:
            return False, f'Error during file encryption: {str(e)}', None

    def decrypt_file(
        self,
        file_path: Path,
        passphrase: str,
        output_path: Optional[Path] = None
    ) -> Tuple[bool, str, Optional[Path], Optional[Dict]]:
        """
        Decrypt a file

        Args:
            file_path: Path to encrypted file
            passphrase: Passphrase for private key
            output_path: Optional output path (default: removes .gpg/.asc extension)

        Returns:
            Tuple of (success, message, output_file_path, signature_info)
        """
        try:
            if not file_path.exists():
                return False, 'Input file does not exist', None, None

            if output_path is None:
                # Try to determine output path
                if file_path.suffix in ['.gpg', '.asc']:
                    output_path = file_path.with_suffix('')
                else:
                    output_path = file_path.with_suffix('.decrypted')

            with open(file_path, 'rb') as f:
                decrypted = self.gpg.decrypt_file(
                    f,
                    passphrase=passphrase,
                    output=str(output_path)
                )

            if decrypted.ok:
                # Check for signature information
                signature_info = None
                if decrypted.fingerprint:
                    signature_info = {
                        'fingerprint': decrypted.fingerprint,
                        'username': decrypted.username,
                        'key_id': decrypted.key_id,
                        'timestamp': decrypted.timestamp,
                    }

                return True, 'File decryption successful', output_path, signature_info
            else:
                return False, f'File decryption failed: {decrypted.status}', None, None

        except Exception as e:
            return False, f'Error during file decryption: {str(e)}', None, None
