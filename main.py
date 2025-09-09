import time
import random
import json
from message_client import MessageClient
from message_models import Button, ButtonType
from message_templates import load_promotional_templates, get_random_image_url
from config import default_config

def live_countdown(seconds: int):
    """Displays a live countdown timer in the terminal."""
    while seconds > 0:
        mins, secs = divmod(seconds, 60)
        timer = f"⏳ Waiting for {mins:02d}:{secs:02d}..."
        print(timer, end='\r')
        time.sleep(1)
        seconds -= 1
    print("\n") # Newline after countdown finishes

def load_numbers(file_path: str = "number.txt") -> list[str]:
    """Loads phone numbers from a text file."""
    try:
        with open(file_path, 'r') as f:
            numbers = [line.strip() for line in f if line.strip()]
            print(f"✅ Loaded {len(numbers)} numbers from {file_path}")
            return numbers
    except FileNotFoundError:
        print(f"❌ Error: The file {file_path} was not found.")
        return []

def move_number_to_sent(number: str, source_file: str = "number.txt", sent_file: str = "sent_numbers.txt"):
    """Move a number from source file to sent file after successful send."""
    try:
        # Read all numbers from source file
        with open(source_file, 'r', encoding='utf-8') as f:
            numbers = [line.strip() for line in f if line.strip()]
        
        # Remove the sent number from the list
        if number in numbers:
            numbers.remove(number)
        
        # Write remaining numbers back to source file
        with open(source_file, 'w', encoding='utf-8') as f:
            for num in numbers:
                f.write(num + '\n')
        
        # Append sent number to sent file
        with open(sent_file, 'a', encoding='utf-8') as f:
            f.write(number + '\n')
        
        print(f"📝 Moved {number} to {sent_file}")
        
    except Exception as e:
        print(f"❌ Error moving number {number}: {e}")

def main():
    """Main function to run the bulk messaging script."""
    print("🚀 Starting Bulk Promotional Messaging Script")

    # --- Configuration ---
    if not default_config.is_valid():
        missing = default_config.get_missing_fields()
        print(f"❌ Configuration is invalid. Please set: {', '.join(missing)} in config.py")
        return

    client = MessageClient(api_key=default_config.API_KEY, sender=default_config.SENDER)

    # --- Load Data ---
    numbers = load_numbers()
    templates = load_promotional_templates()

    if not numbers or not templates:
        print("❌ Cannot proceed without numbers and templates. Exiting.")
        return

    # --- Main Sending Loop ---
    print("📨 Starting the sending loop...")
    try:
        # Shuffle only templates for variety, keep numbers in original order
        random.shuffle(templates)

        for i, number in enumerate(numbers):
            # Ensure we have a template for each number
            template = templates[i % len(templates)]
            
            print(f"\n---")
            print(f"Sending to: {number}")
            print(f"Using template: {template['name']}")

            try:
                # Convert button dictionaries to Button objects
                template_buttons = []
                for btn_data in template.get("buttons", []):
                    button_type = ButtonType(btn_data["type"])
                    button = Button(
                        type=button_type,
                        display_text=btn_data["displayText"],
                        phone_number=btn_data.get("phoneNumber"),
                        url=btn_data.get("url"),
                        copy_code=btn_data.get("copyCode")
                    )
                    template_buttons.append(button)

                # Send the message
                response = client.send_button_message(
                    recipient=number,
                    message=template["message"],
                    buttons=template_buttons,
                    media_url=get_random_image_url(),
                    footer=template["footer"]
                )
                print(f"✅ Message sent successfully to {number}!")
                print(f"   Response: {json.dumps(response, indent=2)}")
                
                # Move number to sent file after successful send
                move_number_to_sent(number)

            except Exception as e:
                print(f"❌ Failed to send message to {number}: {e}")

            # Wait for a random time before the next message
            if i < len(numbers) - 1: # No need to wait after the last number
                next_number = numbers[i + 1]
                print(f"\n➡️ Next message will be sent to: {next_number}")
                sleep_duration = random.randint(60, 300)  # 1 to 5 minutes
                live_countdown(sleep_duration)
        
        print("\n✅ All messages sent successfully! Script completed.")

    except KeyboardInterrupt:
        print("\n🛑 Script interrupted by user. Exiting gracefully.")

if __name__ == "__main__":
    main()
