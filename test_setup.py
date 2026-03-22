#!/usr/bin/env python3
"""
Test script to verify PGP Tool setup
"""

import sys
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    try:
        import flask
        print("✓ Flask")
        import gnupg
        print("✓ python-gnupg")
        from flask_wtf.csrf import CSRFProtect
        print("✓ Flask-WTF")
        from dotenv import load_dotenv
        print("✓ python-dotenv")
        from werkzeug.utils import secure_filename
        print("✓ Werkzeug")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_modules():
    """Test that custom modules can be imported"""
    print("\nTesting custom modules...")
    try:
        from modules.key_manager import KeyManager
        print("✓ KeyManager")
        from modules.pgp_operations import PGPOperations
        print("✓ PGPOperations")
        from modules.storage import JSONStorage, KeysMetadataStorage, SettingsStorage
        print("✓ Storage modules")
        from modules.utils import validate_email, format_fingerprint
        print("✓ Utils")
        return True
    except ImportError as e:
        print(f"✗ Module import failed: {e}")
        return False

def test_config():
    """Test configuration"""
    print("\nTesting configuration...")
    try:
        from config import Config
        print(f"✓ Config loaded")
        print(f"  - GNUPG_HOME: {Config.GNUPG_HOME}")
        print(f"  - DATA_DIR: {Config.DATA_DIR}")
        print(f"  - HOST: {Config.HOST}")
        print(f"  - PORT: {Config.PORT}")
        return True
    except Exception as e:
        print(f"✗ Config failed: {e}")
        return False

def test_app():
    """Test Flask app initialization"""
    print("\nTesting Flask app...")
    try:
        from app import app
        print("✓ Flask app initialized")
        print(f"  - Routes: {len(app.url_map._rules)} registered")
        return True
    except Exception as e:
        print(f"✗ App initialization failed: {e}")
        return False

def test_gnupg():
    """Test GnuPG availability"""
    print("\nTesting GnuPG...")
    try:
        import gnupg
        import tempfile
        import os

        # Create temporary directory for test
        with tempfile.TemporaryDirectory() as tmpdir:
            gpg = gnupg.GPG(gnupghome=tmpdir)

            # Try to list keys (should be empty)
            keys = gpg.list_keys()
            print(f"✓ GnuPG accessible")
            print(f"  - Version: {gpg.version}")
            return True
    except Exception as e:
        print(f"✗ GnuPG test failed: {e}")
        return False

def test_directories():
    """Test that required directories exist or can be created"""
    print("\nTesting directories...")
    try:
        from config import Config

        # Check/create directories
        Config.init_app()

        if Config.GNUPG_HOME.exists():
            print(f"✓ Keys directory: {Config.GNUPG_HOME}")
        else:
            print(f"✗ Keys directory missing: {Config.GNUPG_HOME}")
            return False

        if Config.DATA_DIR.exists():
            print(f"✓ Data directory: {Config.DATA_DIR}")
        else:
            print(f"✗ Data directory missing: {Config.DATA_DIR}")
            return False

        return True
    except Exception as e:
        print(f"✗ Directory test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("PGP Tool - Setup Verification")
    print("=" * 60)

    tests = [
        ("Python Dependencies", test_imports),
        ("Custom Modules", test_modules),
        ("Configuration", test_config),
        ("Flask Application", test_app),
        ("GnuPG Integration", test_gnupg),
        ("Directory Structure", test_directories),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} failed with exception: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} {name}")

    print(f"\nPassed: {passed}/{total}")

    if passed == total:
        print("\n🎉 All tests passed! Your PGP Tool is ready to use.")
        print("\nTo start the application:")
        print("  ./run.sh")
        print("\nOr:")
        print("  python app.py")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please review the errors above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
