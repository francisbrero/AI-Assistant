# AI Executive Assistants

## Overview

The AI Executive Assistant system is designed to help streamline workflow management for executives by automating various routine tasks such as email management, contact organization, calendar scheduling, and personal task tracking. 
The system comprises multiple specialized email_agents, each focusing on a specific aspect of workflow management and is managed by a central Coordinator Agent. The main features include:

- Email Management: Automate triaging (deleting, unsubscribing, archiving) and drafting responses using NLP.

- LinkedIn Integration: Automate message triage and responses via Chrome extension or session cookie.

- Contact Management: Extract, organize, and maintain contact information from multiple sources.

- Calendar Scheduling: Optimize scheduling for meetings and personal appointments.

- Personal Task Management: Track administrative tasks like passport renewals or medical appointments.

The system features a Streamlit-based dashboard that allows user interaction, providing a centralized place for reviewing agent activities, approving actions, and managing tasks.



## Installation

### Prerequisites

- Python 3.8+

- Chrome Browser (for LinkedIn automation)

- Google Workspace API Credentials (for accessing Gmail)

### Setup Instructions

Set Up Virtual Environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install Dependencies:

```bash
pip install -r requirements.txt
```

Set Up API Credentials:

1. Credentials for Google Workspace API:

Create a file called credentials.json for Google Workspace access and place it in the root directory.

```bash
touch credentials.json
```


Update LinkedIn credentials as required for the session cookie.

## Using the System:

To run the system, execute the following command:

```bash
python run main.py
```

## email_agents and Tasks

- Email Agent: Handles the triaging of emails, identifies important messages, and drafts replies. This agent can automatically archive or delete promotional content.
More details on training and running the email agent can be found in the [email agent documentation](email_agents/email_agent_readme.md).

- LinkedIn Agent: Accesses LinkedIn messages through session cookies to triage and draft responses.

- Contact Management Agent: Extracts contacts from multiple sources and maintains them in a central database for easy access and categorization.

- Calendar Agent: Connects with Google Calendar API to schedule meetings and personal tasks efficiently.

## Security & Privacy

- Sensitive Data Handling: Sensitive data such as Social Security Numbers are handled using placeholder tokens, and encryption techniques are used for storage and transmission (AES-256).

- Encryption: Custom utility scripts in /utilities/encryption_utils.py are used to manage encryption/decryption of sensitive information.

## Roadmap

Phase 1: Implement basic email_agents for email triage.

Phase 2: Contact management capabilities and integrate with WhatsApp.

Phase 3: Develop and optimize calendar scheduling and personal task reminders.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or create an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License.

Author: [Francis Brero]("https:www.linkedin.com/in/francis-brero")