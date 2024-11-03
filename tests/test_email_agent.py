import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Ensure the parent directory is in the Python path to access agents and integration
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'agents')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'integration')))

from email_agent import EmailAgent

class TestEmailAgent(unittest.TestCase):
    def setUp(self):
        """Set up the email agent for each test."""
        self.agent = EmailAgent(training_mode=True)

    @patch('integration.gmail_integration.GmailIntegration')  # Corrected path to integration
    def test_process_email_with_training(self, MockGmailIntegration):
        """Test the email processing in training mode."""
        mock_gmail = MockGmailIntegration.return_value
        mock_gmail.get_message.return_value = {
            'payload': {
                'headers': [
                    {'name': 'From', 'value': 'test_sender@example.com'},
                    {'name': 'To', 'value': 'francis@domain.com'}
                ]
            }
        }

        with patch('builtins.input', side_effect=['n', 'reply', 'Urgent task to follow up']):
            self.agent.process_email_with_training(
                message_id="12345",
                email_data=mock_gmail.get_message("12345"),
                subject="Follow Up Task",
                suggested_action="archive"
            )

        self.assertEqual(self.agent.training_data["Follow Up Task"]['action'], 'reply')
        self.assertEqual(self.agent.training_data["Follow Up Task"]['reason'], 'Urgent task to follow up')

    @patch('integration.gmail_integration.GmailIntegration')  # Corrected path to integration
    def test_auto_ignore_when_cc(self, MockGmailIntegration):
        """Test that the agent auto-suggests ignore when the user is CC'd."""
        mock_gmail = MockGmailIntegration.return_value
        mock_gmail.get_message.return_value = {
            'payload': {
                'headers': [
                    {'name': 'From', 'value': 'test_sender@example.com'},
                    {'name': 'To', 'value': 'primary_recipient@domain.com'},
                    {'name': 'Cc', 'value': 'your_email@domain.com'}
                ]
            }
        }

        with patch('builtins.input', side_effect=['y']):
            self.agent.process_email_with_training(
                message_id="12345",
                email_data=mock_gmail.get_message("12345"),
                subject="Jesus just messaged you",
                suggested_action="reply"
            )

        self.assertEqual(self.agent.training_data["Jesus just messaged you"]['action'], 'ignore')

if __name__ == '__main__':
    unittest.main()
