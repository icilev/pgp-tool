#!/usr/bin/env python3
"""
Quick demo script to test PGP operations
This script demonstrates the core functionality without running the web server
"""

import tempfile
from pathlib import Path
from modules.key_manager import KeyManager
from modules.pgp_operations import PGPOperations

def demo():
    print("=" * 60)
    print("PGP Tool - Quick Demo")
    print("=" * 60)
    print()

    # Create temporary keyring
    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"📁 Using temporary keyring: {tmpdir}")
        print()

        # Initialize managers
        key_manager = KeyManager(Path(tmpdir))
        pgp_ops = PGPOperations(Path(tmpdir))

        # 1. Generate a key pair
        print("1️⃣  Generating key pair...")
        success, message, fingerprint = key_manager.generate_key(
            name="Demo User",
            email="demo@example.com",
            passphrase="demo-passphrase-123",
            comment="Demo Key"
        )

        if success:
            print(f"   ✅ {message}")
            print(f"   🔑 Fingerprint: {fingerprint[:16]}...")
        else:
            print(f"   ❌ {message}")
            return

        print()

        # 2. List keys
        print("2️⃣  Listing keys...")
        keys = key_manager.get_private_keys_list()
        print(f"   📋 Found {len(keys)} key(s)")
        for key in keys:
            print(f"   - {key['name']} <{key['email']}>")

        print()

        # 3. Encrypt a message
        print("3️⃣  Encrypting a message...")
        message_text = "Hello, this is a secret message!"
        print(f"   📝 Original: {message_text}")

        success, msg, encrypted_data = pgp_ops.encrypt(
            data=message_text,
            recipients=[fingerprint],
            sign=fingerprint,
            passphrase="demo-passphrase-123"
        )

        if success:
            print(f"   ✅ Encryption successful")
            print(f"   🔐 Encrypted (first 50 chars): {encrypted_data[:50]}...")
        else:
            print(f"   ❌ {msg}")
            return

        print()

        # 4. Decrypt the message
        print("4️⃣  Decrypting the message...")
        success, msg, decrypted_data, sig_info = pgp_ops.decrypt(
            encrypted_data=encrypted_data,
            passphrase="demo-passphrase-123"
        )

        if success:
            print(f"   ✅ Decryption successful")
            print(f"   📝 Decrypted: {decrypted_data}")
            if sig_info:
                print(f"   ✍️  Signed by: {sig_info.get('username', 'Unknown')}")
        else:
            print(f"   ❌ {msg}")
            return

        print()

        # 5. Sign a message
        print("5️⃣  Signing a message...")
        message_to_sign = "I certify this message!"

        success, msg, signed_data = pgp_ops.sign(
            data=message_to_sign,
            keyid=fingerprint,
            passphrase="demo-passphrase-123",
            clearsign=True
        )

        if success:
            print(f"   ✅ Signing successful")
            print(f"   ✍️  Signed data (first 50 chars): {signed_data[:50]}...")
        else:
            print(f"   ❌ {msg}")
            return

        print()

        # 6. Verify the signature
        print("6️⃣  Verifying signature...")
        success, msg, verification_info = pgp_ops.verify(
            signed_data=signed_data
        )

        if success:
            print(f"   ✅ Signature is VALID")
            print(f"   👤 Signed by: {verification_info.get('username', 'Unknown')}")
            print(f"   🔑 Key ID: {verification_info.get('key_id', 'Unknown')}")
            print(f"   🔒 Trust: {verification_info.get('trust_text', 'Unknown')}")
        else:
            print(f"   ❌ {msg}")

        print()
        print("=" * 60)
        print("✅ Demo completed successfully!")
        print("=" * 60)
        print()
        print("🚀 Ready to use the web interface?")
        print("   Run: ./run.sh")
        print("   Open: http://localhost:5000")

if __name__ == '__main__':
    try:
        demo()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
