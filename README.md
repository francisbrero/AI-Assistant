# AI Executive Assistants

## Overview

The AI Executive Assistant system is designed to help streamline workflow management for executives by automating various routine tasks such as email management, contact organization, calendar scheduling, and personal task tracking. 
The system comprises multiple specialized agents, each focusing on a specific aspect of workflow management and is managed by a central Coordinator Agent. The main features include:

- Email Management: Automate triaging (deleting, unsubscribing, archiving) and drafting responses using NLP.

- LinkedIn Integration: Automate message triage and responses via Chrome extension or session cookie.

- Contact Management: Extract, organize, and maintain contact information from multiple sources.

- Calendar Scheduling: Optimize scheduling for meetings and personal appointments.

- Personal Task Management: Track administrative tasks like passport renewals or medical appointments.

The system features a Streamlit-based dashboard that allows user interaction, providing a centralized place for reviewing agent activities, approving actions, and managing tasks.

## Project Structure

## Installation

### Prerequisites

- Python 3.8+

- Chrome Browser (for LinkedIn automation)

- Google Workspace API Credentials (for accessing Gmail)

### Setup Instructions

Clone the Repository:

Set Up Virtual Environment:

Install Dependencies:

Set Up API Credentials:

Create a file called credentials.json for Google Workspace access and place it in the root directory.

Update LinkedIn credentials as required for the session cookie.

Run the Dashboard:

Usage
```bash 
python main.py -model gpt-4-turbo -training
```


Starting the System

Dashboard Interface: The dashboard provides options for initiating tasks such as email triage, LinkedIn message handling, and scheduling personal appointments. The Coordinator Agent manages the workflow between agents.

Agents and Tasks

Email Agent: Handles the triaging of emails, identifies important messages, and drafts replies. This agent can automatically archive or delete promotional content.

LinkedIn Agent: Accesses LinkedIn messages through session cookies to triage and draft responses.

Contact Management Agent: Extracts contacts from multiple sources and maintains them in a central database for easy access and categorization.

Calendar Agent: Connects with Google Calendar API to schedule meetings and personal tasks efficiently.

Security & Privacy

Sensitive Data Handling: Sensitive data such as Social Security Numbers are handled using placeholder tokens, and encryption techniques are used for storage and transmission (AES-256).

Encryption: Custom utility scripts in /utilities/encryption_utils.py are used to manage encryption/decryption of sensitive information.

Technology Stack

Programming Language: Python

NLP Tools: SpaCy, HuggingFace Transformers

Web Automation: Selenium, Playwright

Database: SQLite for local development, PostgreSQL for production use

Frontend Interface: Streamlit

Roadmap

Phase 1: Implement basic agents for email triage and LinkedIn message handling.

Phase 2: Expand contact management capabilities and integrate with WhatsApp.

Phase 3: Develop and optimize calendar scheduling and personal task reminders.

Contributing

Contributions are welcome! Please feel free to submit a Pull Request or create an issue for any suggestions or improvements.

License

This project is licensed under the MIT License.