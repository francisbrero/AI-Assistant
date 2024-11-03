import openai
import json

class LLMHelper:
    def __init__(self, model_choice="gpt-4-turbo"):
        # Load configuration from the OAI_CONFIG_LIST file
        with open('OAI_CONFIG_LIST', 'r') as file:
            config = json.load(file)

        # Find the model config based on the model_choice
        self.model_config = self.get_model_config(config, model_choice)

        # If using an OpenAI model, set up the API key and OpenAI client
        if self.model_config['api_type'] == "openai":
            self.client = openai.Client(api_key=self.model_config['api_key'])
            self.use_openai = True
        else:
            # For local models, store the base URL and other config
            self.use_openai = False
            self.base_url = self.model_config['base_url']
            self.api_key = self.model_config['api_key']
            self.model = self.model_config['model']

    def get_model_config(self, config, model_choice):
        """Get the model configuration for the specified model_choice."""
        for model in config:
            if model['model'] == model_choice:
                return model
        raise ValueError(f"Model {model_choice} not found in the configuration")

    def suggest_action(self, email_data):
        """Query the selected LLM to suggest an action for the email."""
        subject = self.extract_subject(email_data)
        body = self.extract_body(email_data)
        
        if self.use_openai:
            return self.query_openai(subject, body)
        else:
            return self.query_local_model(subject, body)

    def query_openai(self, subject, body):
        """Query OpenAI's API for a suggested action using the OpenAI client."""
        response = self.client.chat.completions.create(
            model=self.model_config['model'],  # Model from config (e.g., "gpt-4")
            messages=[
                {"role": "system", "content": "You are an assistant helping process emails."},
                {"role": "user", "content": f"Subject: {subject}\nBody: {body}\n\nPlease respond with an action suggestion (archive/reply/ignore), followed by an explanation under 50 words. Format your answer as: **suggestion action** \n explanation."}
            ]
        )

        # Extract the completion from the response using dot notation
        action_response = response.choices[0].message.content

        # Split the response into the recommended action and an optional explanation
        suggested_action, explanation = self.extract_suggestion_and_explanation(action_response)

        return suggested_action.strip().lower(), explanation.strip()


    def query_local_model_with_prompt(self, prompt):
        """Query the locally hosted LLM."""
        import requests

        data = {
            "model": self.model,  # The local model to query
            "prompt": prompt
        }
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        response = requests.post(f"{self.base_url}/completions", json=data, headers=headers)
        response_data = response.json()

        if 'choices' in response_data and len(response_data['choices']) > 0:
            action_response = response_data['choices'][0]['text']
            suggested_action, explanation = self.extract_suggestion_and_explanation(action_response)
            return suggested_action.strip().lower(), explanation.strip()
        else:
            raise ValueError("Invalid response from local LLM")

    def extract_suggestion_and_explanation(self, response_text):
        """Extract the action suggestion and optional explanation from the response."""
        # Split the response by the first sentence (assuming it's the action) and the rest as the explanation
        lines = response_text.strip().split('\n')
        if len(lines) > 1:
            # First line is the suggested action, the rest is the explanation
            return lines[0], ' '.join(lines[1:])
        else:
            # Only one line (the action), no explanation
            return lines[0], ""

    def extract_subject(self, email_data):
        """Extract the subject of the email."""
        headers = email_data['payload'].get('headers', [])
        for header in headers:
            if header['name'] == 'Subject':
                return header['value']
        return "No Subject"

    def extract_body(self, email_data):
        """Extract the body of the email."""
        if 'parts' in email_data['payload']:
            for part in email_data['payload']['parts']:
                if part['mimeType'] == 'text/plain':
                    return part['body'].get('data', '')
        return "No body content"
