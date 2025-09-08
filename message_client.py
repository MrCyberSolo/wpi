import requests
import json
from typing import List, Dict, Optional, Union
from message_validator import MessageValidator
from message_models import Button, ButtonType


class MessageClient:
    """Client for sending button messages via the BlackServer API"""
    
    def __init__(self, api_key: str, sender: str, base_url: str = "https://clients.blackserver.in"):
        """
        Initialize the message client
        
        Args:
            api_key: Your API key
            sender: Your device number
            base_url: Base URL for the API (default: https://clients.blackserver.in)
        """
        self.api_key = api_key
        self.sender = sender
        self.base_url = base_url
        self.session = requests.Session()
        
    def create_reply_button(self, display_text: str) -> Button:
        """Create a reply button"""
        return Button(ButtonType.REPLY, display_text)
    
    def create_call_button(self, display_text: str, phone_number: str) -> Button:
        """Create a call button"""
        return Button(ButtonType.CALL, display_text, phone_number=phone_number)
    
    def create_url_button(self, display_text: str, url: str) -> Button:
        """Create a URL button"""
        return Button(ButtonType.URL, display_text, url=url)
    
    def create_copy_button(self, display_text: str, copy_code: str) -> Button:
        """Create a copy button"""
        return Button(ButtonType.COPY, display_text, copy_code=copy_code)
    
    def send_button_message(
        self,
        recipient: str,
        message: str,
        buttons: List[Button],
        media_url: str,
        footer: Optional[str] = None,
        method: str = "POST"
    ) -> Dict:
        """
        Send a button message
        
        Args:
            recipient: Recipient phone number (e.g., 72888xxxx or 62888xxxx)
            message: Text message content
            buttons: List of Button objects (max 5)
            media_url: Image or video URL for media attachment
            footer: Optional footer text
            method: HTTP method (POST or GET)
            
        Returns:
            API response as dictionary
            
        Raises:
            ValueError: If validation fails
            requests.RequestException: If API request fails
        """
        # Validate inputs using MessageValidator
        is_valid, errors = MessageValidator.validate_send_request(
            self.api_key, self.sender, recipient, message, buttons, media_url, footer
        )
        
        if not is_valid:
            raise ValueError(f"Validation failed: {'; '.join(errors)}")
        
        # Prepare request data
        data = {
            "api_key": self.api_key,
            "sender": self.sender,
            "number": recipient,
            "message": message,
            "url": media_url,
            "button": [button.to_dict() for button in buttons]
        }
        
        if footer:
            data["footer"] = footer
        
        # Send request
        endpoint = f"{self.base_url}/send-button"
        
        try:
            if method.upper() == "POST":
                response = self.session.post(
                    endpoint,
                    json=data,
                    headers={"Content-Type": "application/json"}
                )
            else:  # GET
                response = self.session.get(endpoint, params=data)
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise requests.RequestException(f"API request failed: {str(e)}")
    
    def send_simple_message(
        self,
        recipient: str,
        message: str,
        media_url: str,
        reply_button_text: str = "Reply",
        footer: Optional[str] = None
    ) -> Dict:
        """
        Send a simple message with just a reply button
        
        Args:
            recipient: Recipient phone number
            message: Text message content
            media_url: Image or video URL
            reply_button_text: Text for the reply button
            footer: Optional footer text
            
        Returns:
            API response as dictionary
        """
        buttons = [self.create_reply_button(reply_button_text)]
        return self.send_button_message(recipient, message, buttons, media_url, footer)
    
    def send_contact_message(
        self,
        recipient: str,
        message: str,
        media_url: str,
        call_number: str,
        website_url: Optional[str] = None,
        footer: Optional[str] = None
    ) -> Dict:
        """
        Send a contact message with call and optional website buttons
        
        Args:
            recipient: Recipient phone number
            message: Text message content
            media_url: Image or video URL
            call_number: Phone number for the call button
            website_url: Optional website URL
            footer: Optional footer text
            
        Returns:
            API response as dictionary
        """
        buttons = [
            self.create_reply_button("Reply"),
            self.create_call_button("Call Us", call_number)
        ]
        
        if website_url:
            buttons.append(self.create_url_button("Visit Website", website_url))
        
        return self.send_button_message(recipient, message, buttons, media_url, footer)
