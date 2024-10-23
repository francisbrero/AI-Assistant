import argparse
from agents.email_agent import EmailAgent

def main(training=False, model="gpt-4"):
    # Initialize Email Agent with training mode and selected model
    email_agent = EmailAgent(training_mode=training, model_choice=model)

    # Process unread emails
    email_agent.process_emails()

if __name__ == '__main__':
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description='Run Email Agent with optional training mode and model selection.')

    # Add the `-training` flag
    parser.add_argument(
        '-training',
        action='store_true',  # This makes it a flag, setting it to True when provided
        help='Enable training mode for the Email Agent'
    )

    # Add the `-model` argument to specify the model to use
    parser.add_argument(
        '-model',
        type=str,
        default='gpt-4-turbo',  # Default model is 'gpt-4-turbo' if no model is specified
        help='Choose which model to use for LLM processing (e.g., gpt-4, gpt-3.5-turbo, or TheBloke/Llama-2-13B-chat-GGUF)'
    )

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the main function with the training flag and selected model
    main(training=args.training, model=args.model)
