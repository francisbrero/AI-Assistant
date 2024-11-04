import colorama
import json
from colorama import Fore, Style
from integration.gmail_integration import GmailIntegration
from utilities.llm_helper import LLMHelper

colorama.init(autoreset=True)  # Initialize colorama

class EmailAgent:
    def __init__(self, training_mode=False, model_choice="gpt-4-turbo"):
        self.gmail = GmailIntegration()
        self.training_mode = training_mode
        self.llm_helper = LLMHelper(model_choice=model_choice)

        # Load existing training data (if any)
        self.training_data = self.load_training_data()

    def load_training_data(self):
        """Load existing training data from a JSON file."""
        try:
            with open('training_data.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_training_data(self):
        """Save the current training data to a JSON file."""
        with open('training_data.json', 'w') as file:
            json.dump(self.training_data, file, indent=4)

    def process_emails(self):
        """Process emails based on the current mode (training/automatic)."""
        messages = self.gmail.list_messages(query="is:unread")
        
        for msg in messages:
            email_data = self.gmail.get_message(msg['id'])
            subject = self.get_subject(email_data)

            # Add section separator and subject header
            print(f"{Fore.CYAN}{'='*50}")
            print(f"{Fore.CYAN}Processing Email: {Fore.GREEN}{subject}")
            print(f"{Fore.CYAN}{'='*50}")

            # Check if we have training data for this subject
            if subject in self.training_data:
                # Apply the stored action
                action = self.training_data[subject]
                print(f"{Fore.YELLOW}Found stored action: {Fore.GREEN}{action}")
            else:
                # Use LLM to get a suggestion if no training data is found
                action, explanation = self.llm_helper.suggest_action(email_data)
                print(f"{Fore.YELLOW}LLM suggested action: {Fore.GREEN}{action}")

                # Output the explanation separately (optional)
                if explanation:
                    print(f"{Fore.CYAN}{'-'*50}")
                    print(f"{Fore.LIGHTBLACK_EX}Explanation: {explanation}")
                    print(f"{Fore.CYAN}{'-'*50}")

            if self.training_mode:
                self.process_email_with_training(msg['id'], email_data, subject, action)
            else:
                self.apply_instruction(msg['id'], action)
            print(f"{Fore.CYAN}{'='*50}\n")

    def process_email_with_training(self, message_id, email_data, subject, suggested_action):
        """Process each email in training mode with LLM-based suggestions and user feedback."""
        
        # Extract sender and recipients
        sender, recipients, cc_list = self.get_sender_and_recipients(email_data)

        # Display sender and recipient info
        print(f"{Fore.CYAN}From: {Fore.GREEN}{sender}")
        print(f"{Fore.CYAN}To: {Fore.GREEN}{', '.join(recipients)}")
        if cc_list:
            print(f"{Fore.CYAN}CC: {Fore.GREEN}{', '.join(cc_list)}")

        # Check if sender is in the dynamic 'always ignore' list
        if sender in self.always_ignore_senders():
            suggested_action = 'ignore'
            print(f"{Fore.RED}Note: This sender is in the 'always ignore' list. Auto-suggesting ignore.")

        # Check if user is CC'd and update suggestion
        if 'your_email@domain.com' in cc_list and suggested_action != 'ignore':
            suggested_action = 'ignore'
            print(f"{Fore.RED}Note: You are CC'd in this email. Auto-suggesting ignore.")

        # Display LLM suggested action
        print(f"{Fore.YELLOW}LLM suggested action for email '{subject}': {Fore.GREEN}{suggested_action}")
        
        # Ask for confirmation with Y/N and handle different responses
        confirmation = input(f"{Fore.CYAN}Do you want to proceed with this action? (Y/N) [Y]: ").strip().lower()

        if confirmation == 'exit':
            print(f"{Fore.RED}Exiting process.")
            exit()

        if confirmation == 'n':
            # Ask for the recommended action from the user
            action = input(f"{Fore.CYAN}What should the action be? (archive/reply/ignore): ").strip().lower()
            # Ask for the reason for the different action
            reason = input(f"{Fore.CYAN}Why are you recommending a different action?: ").strip()

            # If the user selects 'ignore', ask if this sender should always be ignored
            if action == 'ignore':
                add_to_ignore = input(f"{Fore.CYAN}Do you want to always ignore emails from {sender}? (Y/N) [N]: ").strip().lower()
                if add_to_ignore == 'y':
                    self.update_ignore_list(sender)
        else:
            # Use the suggested action if user confirms (or hits enter without input)
            action = suggested_action
            reason = ""  # No reason needed if the user confirms the suggested action

        # If user suggests a different action, update the training data with the reason
        if action != suggested_action:
            print(f"{Fore.YELLOW}Updating training data for email '{subject}' with action '{Fore.GREEN}{action}' and reason: '{reason}'.")
            self.training_data[subject] = {
                'action': action,
                'reason': reason,
                'sender': sender,
                'recipients': recipients,
                'cc_list': cc_list
            }
            self.save_training_data()

        # Apply the confirmed action
        self.apply_instruction(message_id, action)
        print(f"{Fore.YELLOW}Processed email '{subject}' with action '{Fore.GREEN}{action}'.")

    def get_sender_and_recipients(self, email_data):
        """Extract the sender, recipients, and CC list from the email headers."""
        headers = email_data['payload'].get('headers', [])
        
        sender = ""
        recipients = []
        cc_list = []

        for header in headers:
            if header['name'] == 'From':
                sender = header['value']
            elif header['name'] == 'To':
                recipients = header['value'].split(', ')
            elif header['name'] == 'Cc':
                cc_list = header['value'].split(', ')

        return sender, recipients, cc_list

    def always_ignore_senders(self):
        """Return the dynamic list of senders that should always be ignored."""
        # Load the ignore list from the training data if it exists, otherwise return an empty list
        return self.training_data.get('always_ignore_senders', [])

    def update_ignore_list(self, sender):
        """Update the dynamic ignore list with a new sender and save it in the training data."""
        ignore_list = self.training_data.get('always_ignore_senders', [])
        if sender not in ignore_list:
            ignore_list.append(sender)
            self.training_data['always_ignore_senders'] = ignore_list
            self.save_training_data()
            print(f"{Fore.GREEN}Added {sender} to the 'always ignore' list.")
        else:
            print(f"{Fore.YELLOW}{sender} is already in the 'always ignore' list.")


    def build_prompt_for_llm(self, email_data):
        """Construct a simple prompt for the LLM."""
        subject = self.get_subject(email_data)
        body = self.get_body(email_data)
        sender, recipients, cc_list = self.get_sender_and_recipients(email_data)

        prompt = f"Subject: {subject}\nFrom: {sender}\nTo: {', '.join(recipients)}\n"
        if cc_list:
            prompt += f"CC: {', '.join(cc_list)}\n"
        prompt += f"Body: {body}\n\nWhat action should be taken on this email (archive/reply/ignore)?"

        return prompt

    def apply_instruction(self, message_id, instruction):
        """Apply the user-provided instruction to the email."""
        if instruction == 'archive':
            self.archive_email(message_id)
        elif instruction == 'reply':
            self.mark_as_todo_and_draft_reply(message_id)
        elif instruction == 'ignore':
            self.ignore_email(message_id)
        else:
            print(f"{Fore.YELLOW}Ignored message {message_id}.")

    def get_subject(self, email_data):
        """Extract the subject from the email headers."""
        headers = email_data['payload'].get('headers', [])
        for header in headers:
            if header['name'] == 'Subject':
                return header['value']
        return "No Subject"

    def get_body(self, email_data):
        """Extract the body of the email."""
        if 'parts' in email_data['payload']:
            for part in email_data['payload']['parts']:
                if part['mimeType'] == 'text/plain':
                    return part['body'].get('data', '')
        return "No body content"

    def get_sender_and_recipients(self, email_data):
        """Extract the sender, recipients, and CC list from the email headers."""
        headers = email_data['payload'].get('headers', [])
        
        sender = ""
        recipients = []
        cc_list = []

        for header in headers:
            if header['name'] == 'From':
                sender = header['value']
            elif header['name'] == 'To':
                recipients = header['value'].split(', ')
            elif header['name'] == 'Cc':
                cc_list = header['value'].split(', ')

        return sender, recipients, cc_list

    def archive_email(self, message_id):
        """Archive an email by removing it from the inbox."""
        self.gmail.archive_message(message_id)

    def mark_as_todo_and_draft_reply(self, message_id):
        """Mark an email as to-do and draft a reply."""
        # In a real implementation, this would draft a reply and mark the message for follow-up
        print(f"{Fore.YELLOW}Marked email {message_id} as to-do and drafted a reply.")

    def ignore_email(self, message_id):
        """Ignore an email, which in practice could delete or mark it as read."""
        self.gmail.mark_as_read(message_id)
