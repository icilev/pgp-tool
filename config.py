import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).parent

class Config:
    """Application configuration"""

    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'

    # Server
    HOST = os.getenv('HOST', '127.0.0.1')
    PORT = int(os.getenv('PORT', 5000))

    # Upload settings
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_UPLOAD_SIZE', 10485760))  # 10MB
    ALLOWED_EXTENSIONS = {'txt', 'asc', 'gpg', 'pgp', 'sig'}

    # GnuPG settings
    GNUPG_HOME = BASE_DIR / os.getenv('GNUPG_HOME', 'keys')

    # Data storage
    DATA_DIR = BASE_DIR / 'data'
    KEYS_METADATA_FILE = DATA_DIR / 'keys_metadata.json'
    SETTINGS_FILE = DATA_DIR / 'settings.json'

    # Default key generation settings
    DEFAULT_KEY_TYPE = 'RSA'
    DEFAULT_KEY_LENGTH = 4096
    DEFAULT_SUBKEY_TYPE = 'RSA'
    DEFAULT_SUBKEY_LENGTH = 4096

    @classmethod
    def init_app(cls):
        """Initialize application directories"""
        cls.GNUPG_HOME.mkdir(parents=True, exist_ok=True)
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)

        # Set permissions for sensitive directories
        cls.GNUPG_HOME.chmod(0o700)
        cls.DATA_DIR.chmod(0o700)
