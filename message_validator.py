"""
Message validation utilities for the MessageClient
"""

import re
from typing import List, Dict, Any
from message_models import Button, ButtonType


class MessageValidator:
    """Validates message content and structure"""
    
    @staticmethod
    def validate_phone_number(phone: str) -> bool:
        """Validate phone number format"""
        if not phone:
            return False
        
        # Remove any whitespace
        phone = phone.strip()
        
        # Check if it starts with + and has digits
        if phone.startswith('+'):
            return phone[1:].isdigit() and len(phone) >= 10
        
        # Check if it's just digits
        return phone.isdigit() and len(phone) >= 10
    
    @staticmethod
    def validate_message_content(message: str) -> bool:
        """Validate message content"""
        if not message or not message.strip():
            return False
        
        # Check message length (typical SMS limit)
        return len(message.strip()) <= 1600
    
    @staticmethod
    def validate_buttons(buttons: List[Button]) -> bool:
        """Validate button configuration"""
        if not buttons:
            return True
        
        if len(buttons) > 3:
            return False
        
        for button in buttons:
            if not button.display_text or not button.display_text.strip():
                return False
            
            if button.type == ButtonType.URL and not button.url:
                return False
            
            if button.type == ButtonType.CALL and not button.phone_number:
                return False
            
            if button.type == ButtonType.COPY and not button.copy_code:
                return False
        
        return True
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format"""
        if not url:
            return False
        
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        return url_pattern.match(url) is not None
    
    @classmethod
    def validate_message_request(cls, recipient: str, message: str, buttons: List[Button] = None, 
                                media_url: str = None, footer: str = None) -> Dict[str, Any]:
        """Validate complete message request"""
        errors = []
        
        if not cls.validate_phone_number(recipient):
            errors.append("Invalid recipient phone number")
        
        if not cls.validate_message_content(message):
            errors.append("Invalid message content")
        
        if buttons and not cls.validate_buttons(buttons):
            errors.append("Invalid button configuration")
        
        if media_url and not cls.validate_url(media_url):
            errors.append("Invalid media URL")
        
        if footer and len(footer.strip()) > 60:
            errors.append("Footer text too long (max 60 characters)")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    @classmethod
    def validate_send_request(cls, api_key: str, sender: str, recipient: str, message: str, 
                             buttons: List[Button] = None, media_url: str = None, footer: str = None):
        """Validate send request parameters and return tuple (is_valid, errors)"""
        errors = []
        
        if not api_key or not api_key.strip():
            errors.append("API key is required")
        
        if not sender or not sender.strip():
            errors.append("Sender is required")
        
        validation_result = cls.validate_message_request(recipient, message, buttons, media_url, footer)
        errors.extend(validation_result["errors"])
        
        return len(errors) == 0, errors
