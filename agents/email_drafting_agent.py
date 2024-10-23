import openai
import json

class EmailDraftingAgent:
    def __init__(self, model_choice="gpt-4"):
        # Load the OpenAI model and any specific templates or instructions
        self.model_choice = model_choice
        self.templates = self.load_templates()

    def load_templates(self):
        """Load email templates from an external file (templates.json)."""
        try:
            with open('templates.json', 'r') as file:
                templates = json.load(file)
                return templates
        except FileNotFoundError:
            print("Error: Template file not found.")
            return {}

    def select_template(self, email_context):
        """Select an appropriate template based on the context of the email."""
        # Basic logic to choose a template based on the email context
        if 'follow up' in email_context.lower():
            return self.templates.get('follow_up', "No template available for follow-up.")
        elif 'meeting' in email_context.lower():
            return self.templates.get('meeting_request', "No template available for meeting requests.")
        else:
            return self.templates.get('status_update', "No template available for status updates.")

    def draft_email(self, email_context, recipient_name, your_name):
        """Draft an email based on the context using an LLM to refine the template."""
        # Select the appropriate template
        template = self.select_template(email_context)

        # Use LLM to refine the email if necessary
        refined_email = self.refine_email_with_llm(template, email_context, recipient_name, your_name)

        return refined_email

    def refine_email_with_llm(self, template, email_context, recipient_name, your_name):
        """Refine the email template with OpenAI for customization."""
        prompt = (
            f"Please customize the following email template based on this context: '{email_context}'. "
            f"Make sure to include the recipient's name '{recipient_name}' and the sender's name '{your_name}':\n\n"
            f"{template}"
        )

        response = openai.Completion.create(
            model=self.model_choice,
            prompt=prompt,
            max_tokens=150
        )

        return response.choices[0].text.strip()

# Example usage
if __name__ == "__main__":
    agent = EmailDraftingAgent()
    drafted_email = agent.draft_email(
        email_context="We need to follow up on the pricing discussion",
        recipient_name="John Doe",
        your_name="Francis"
    )
    print(drafted_email)
