import sys
import os
import unittest
from unittest.mock import patch

# Ensure the parent directory is in the Python path to access agents
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'agents')))

from email_drafting_agent import EmailDraftingAgent

class TestEmailDraftingAgent(unittest.TestCase):
    def setUp(self):
        """Set up the drafting agent for each test."""
        self.agent = EmailDraftingAgent()

    def test_load_templates(self):
        """Test that templates are loaded correctly from the external file."""
        templates = self.agent.load_templates()
        self.assertIn('follow_up', templates)
        self.assertIn('meeting_request', templates)
        self.assertIn('status_update', templates)

    def test_select_template(self):
        """Test the correct template is selected based on context."""
        follow_up_template = self.agent.select_template('Please follow up with the client')
        meeting_template = self.agent.select_template('We need to schedule a meeting')
        status_template = self.agent.select_template('Here is an update on the project')

        self.assertIn('follow up', follow_up_template)
        self.assertIn('schedule a meeting', meeting_template)
        self.assertIn('update', status_template)

    @patch('openai.Completion.create')
    def test_refine_email_with_llm(self, mock_openai):
        """Test that the LLM is called to refine the email template and print the generated email."""
        mock_openai.return_value.choices = [unittest.mock.Mock(text="Refined email content")]

        # Generate a refined email
        refined_email = self.agent.draft_email(
            email_context="Please follow up with the client",
            recipient_name="John Doe",
            your_name="Francis"
        )

        # Print the generated email to see the output
        print("Generated Email Content:\n", refined_email)
        
        # Check the mock was called
        mock_openai.assert_called_once()
        # Ensure the refined email contains the expected content
        self.assertIn("Refined email content", refined_email)

if __name__ == '__main__':
    unittest.main()
