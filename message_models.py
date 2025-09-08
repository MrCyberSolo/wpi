from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict


class ButtonType(Enum):
    REPLY = "reply"
    CALL = "call"
    URL = "url"
    COPY = "copy"


@dataclass
class Button:
    """Represents a button in the message"""
    type: ButtonType
    display_text: str
    phone_number: Optional[str] = None
    url: Optional[str] = None
    copy_code: Optional[str] = None

    def to_dict(self) -> Dict:
        """Convert button to dictionary format for API"""
        button_dict = {
            "type": self.type.value,
            "displayText": self.display_text
        }

        if self.type == ButtonType.CALL and self.phone_number:
            button_dict["phoneNumber"] = self.phone_number
        elif self.type == ButtonType.URL and self.url:
            button_dict["url"] = self.url
        elif self.type == ButtonType.COPY and self.copy_code:
            button_dict["copyCode"] = self.copy_code

        return button_dict
