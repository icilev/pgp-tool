"""JSON storage for application data"""

import json
from pathlib import Path
from typing import Dict, Any, Optional


class JSONStorage:
    """Simple JSON file storage"""

    def __init__(self, file_path: Path):
        self.file_path = Path(file_path)
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Create file with empty dict if it doesn't exist"""
        if not self.file_path.exists():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            self.save({})

    def load(self) -> Dict[str, Any]:
        """Load data from JSON file"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def save(self, data: Dict[str, Any]):
        """Save data to JSON file"""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # Secure permissions
        self.file_path.chmod(0o600)

    def get(self, key: str, default: Any = None) -> Any:
        """Get a value by key"""
        data = self.load()
        return data.get(key, default)

    def set(self, key: str, value: Any):
        """Set a value by key"""
        data = self.load()
        data[key] = value
        self.save(data)

    def delete(self, key: str):
        """Delete a key"""
        data = self.load()
        if key in data:
            del data[key]
            self.save(data)

    def update(self, updates: Dict[str, Any]):
        """Update multiple keys"""
        data = self.load()
        data.update(updates)
        self.save(data)

    def clear(self):
        """Clear all data"""
        self.save({})


class KeysMetadataStorage(JSONStorage):
    """Storage for keys metadata"""

    def add_key_metadata(self, fingerprint: str, metadata: Dict[str, Any]):
        """Add metadata for a key"""
        data = self.load()
        data[fingerprint] = metadata
        self.save(data)

    def get_key_metadata(self, fingerprint: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a key"""
        return self.get(fingerprint)

    def remove_key_metadata(self, fingerprint: str):
        """Remove metadata for a key"""
        self.delete(fingerprint)

    def list_all_keys(self) -> Dict[str, Dict[str, Any]]:
        """List all keys metadata"""
        return self.load()


class SettingsStorage(JSONStorage):
    """Storage for application settings"""

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value"""
        return self.get(key, default)

    def set_setting(self, key: str, value: Any):
        """Set a setting value"""
        self.set(key, value)

    def get_all_settings(self) -> Dict[str, Any]:
        """Get all settings"""
        return self.load()

    def reset_settings(self):
        """Reset all settings to defaults"""
        defaults = {
            'default_key_type': 'RSA',
            'default_key_length': 4096,
            'armor_output': True,
            'show_warnings': True,
        }
        self.save(defaults)
