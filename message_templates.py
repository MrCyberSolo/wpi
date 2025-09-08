"""
Message templates based on the Knowledge Base for BLACK SMS Service.
"""

import random
from message_models import Button, ButtonType
import json
from typing import Dict, List, Any

def load_promotional_templates(file_path: str = "promotional_templates.json") -> List[Dict[str, Any]]:
    """Loads promotional templates from a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {file_path}.")
        return []

def get_random_image_url() -> str:
    """Returns a random image URL from a predefined list."""
    image_number = random.randint(1, 15)
    return f"https://blacksms.in/assets/images/{image_number}.jpg"

def create_welcome_message() -> Dict[str, Any]:
    """Template for a welcome message to new users."""
    return {
        "message": "🎉 Welcome to BLACK SMS! We're excited to have you on board. As a thank you, we've added ₹10 free credit to your account to test our services.",
        "buttons": [
            Button(type=ButtonType.URL, display_text="Get Started", url="https://blacksms.in/signup"),
            Button(type=ButtonType.REPLY, display_text="Need Help?")
        ],
        "footer": "Your journey to better communication starts here!"
    }

def create_promotional_message(offer: str, promo_code: str) -> Dict[str, Any]:
    """Template for a promotional SMS with a custom offer."""
    return {
        "message": f"✨ Special Offer! {offer}. Use the code below to claim your discount.",
        "buttons": [
            Button(type=ButtonType.COPY, display_text=f"Copy Code: {promo_code}", copy_code=promo_code),
            Button(type=ButtonType.URL, display_text="View Pricing", url="https://blacksms.in/pricing")
        ],
        "footer": "Limited time offer. Don't miss out!"
    }

def create_pricing_info_message() -> Dict[str, Any]:
    """Template providing a summary of SMS pricing."""
    return {
        "message": "Lowest Price Guaranteed! Our bulk SMS rates start at just ₹0.30/SMS. We also offer WhatsApp messaging from ₹0.10/SMS. Check out our detailed pricing plan.",
        "buttons": [
            Button(type=ButtonType.URL, display_text="Full Pricing Table", url="https://blacksms.in/pricing"),
            Button(type=ButtonType.CALL, display_text="Contact Sales", phone_number="+918303017391"),
            Button(type=ButtonType.REPLY, display_text="Custom Plan?")
        ],
        "footer": "Volume discounts available."
    }

def create_otp_message(otp_code: str) -> Dict[str, Any]:
    """Template for sending a One-Time Password (OTP)."""
    return {
        "message": f"Your secure OTP is: {otp_code}. This code is valid for 10 minutes. Please do not share it with anyone.",
        "buttons": [
            Button(type=ButtonType.REPLY, display_text="Resend OTP")
        ],
        "footer": "Security is our priority."
    }

def create_support_contact_message() -> Dict[str, Any]:
    """Template with support contact options."""
    return {
        "message": "Need assistance? Our team is here to help! You can reach us via call or check our FAQ for quick answers.",
        "buttons": [
            Button(type=ButtonType.CALL, display_text="Call Support", phone_number="+918303017391"),
            Button(type=ButtonType.URL, display_text="Read FAQ", url="https://blacksms.in/faq"),
            Button(type=ButtonType.URL, display_text="Contact on Telegram", url="https://t.me/your_telegram_contact")
        ],
        "footer": "We're here to help 24/7."
    }
