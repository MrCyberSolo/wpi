"""
Configuration file for the MessageClient
"""

import os
from typing import Optional


class Config:
    """Configuration class for MessageClient"""
    
    def __init__(self):
        # Load from environment variables or set defaults
        self.API_KEY = os.getenv('MESSAGE_API_KEY', 'gnKgGkEGSETyHw2HkT0SmYgjSYno1U')
        self.SENDER = os.getenv('MESSAGE_SENDER', '918303017391')
        self.BASE_URL = os.getenv('MESSAGE_BASE_URL', 'https://clients.blackserver.in')
        
    @classmethod
    def from_env(cls) -> 'Config':
        """Create config from environment variables"""
        return cls()
    
    @classmethod
    def from_dict(cls, config_dict: dict) -> 'Config':
        """Create config from dictionary"""
        config = cls()
        config.API_KEY = config_dict.get('api_key', config.API_KEY)
        config.SENDER = config_dict.get('sender', config.SENDER)
        config.BASE_URL = config_dict.get('base_url', config.BASE_URL)
        return config
    
    def is_valid(self) -> bool:
        """Check if configuration is valid"""
        return (
            self.API_KEY and self.API_KEY != 'your_api_key_here' and
            self.SENDER and self.SENDER != '6281222xxxxxx'
        )
    
    def get_missing_fields(self) -> list:
        """Get list of missing or invalid configuration fields"""
        missing = []
        if not self.API_KEY or self.API_KEY == 'your_api_key_here':
            missing.append('API_KEY')
        if not self.SENDER or self.SENDER == '6281222xxxxxx':
            missing.append('SENDER')
        return missing


# Default configuration instance
default_config = Config()
