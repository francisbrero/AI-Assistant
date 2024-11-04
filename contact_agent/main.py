import json
import os
from datetime import datetime, timedelta
import pandas as pd

# Load settings
with open('settings.json', 'r') as file:
    settings = json.load(file)

# Load contact data (local JSON)
DATA_PATH = 'data/contact_data.json'

def load_contacts():
    # Check if file exists and is non-empty
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, 'r') as file:
            try:
                data = json.load(file)
                return data
            except json.JSONDecodeError:
                print("Warning: contact_data.json is empty or corrupted. Initializing a new contact data file.")
                return {}
    return {}


def save_contacts(contacts):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, 'w') as file:
        json.dump(contacts, file)

# Updated function for importing contacts from Gmail export format
def import_contacts_from_csv(csv_path='contacts.csv'):
    if not os.path.exists(csv_path):
        print("CSV file not found. Please upload a CSV to start.")
        return {}
    
    contacts = load_contacts()
    new_contacts = pd.read_csv(csv_path)
    
    for _, row in new_contacts.iterrows():
        # Generate a unique contact ID (can be customized)
        contact_id = f"{row['First Name']}_{row['Last Name']}_{row['E-mail 1 - Value']}"
        
        # Skip contacts without at least one email
        email = row.get('E-mail 1 - Value') or row.get('E-mail 2 - Value')
        if pd.isna(email):
            continue
        
        # Add contact if it doesn't exist already
        if contact_id not in contacts:
            contacts[contact_id] = {
                "first_name": row['First Name'] if not pd.isna(row['First Name']) else "",
                "middle_name": row['Middle Name'] if not pd.isna(row['Middle Name']) else "",
                "last_name": row['Last Name'] if not pd.isna(row['Last Name']) else "",
                "nickname": row['Nickname'] if not pd.isna(row['Nickname']) else "",
                "organization": row['Organization Name'] if not pd.isna(row['Organization Name']) else "",
                "title": row['Organization Title'] if not pd.isna(row['Organization Title']) else "",
                "email": email,
                "category": None,
                "vip": False,
                "last_interaction": None,
                "created": datetime.now().isoformat()
            }
    
    save_contacts(contacts)
    return contacts

# SLA and notifications
def get_sla_for_contact(contact):
    category = contact.get("category")
    if contact.get("vip"):
        return settings["categories"].get(category, {}).get("vip_sla", 30)
    return settings["categories"].get(category, {}).get("sla", 60)

def check_sla_notifications():
    contacts = load_contacts()
    today = datetime.now()
    notifications = []

    for contact_id, contact in contacts.items():
        last_interaction = datetime.fromisoformat(contact['last_interaction']) if contact['last_interaction'] else None
        sla_days = get_sla_for_contact(contact)
        if last_interaction and (today - last_interaction).days >= sla_days:
            notifications.append((contact['name'], sla_days))

    return notifications

# Placeholder for future incremental data fetching
def fetch_incremental_updates():
    last_run_path = "data/last_run.txt"
    last_run = None

    if os.path.exists(last_run_path):
        with open(last_run_path, "r") as file:
            last_run = datetime.fromisoformat(file.read().strip())
    
    # Update last run date
    with open(last_run_path, "w") as file:
        file.write(datetime.now().isoformat())

    return last_run

if __name__ == "__main__":
    # Initial import (if CSV provided)
    import_contacts_from_csv()

    # Check for SLA notifications
    notifications = check_sla_notifications()
    for contact, sla in notifications:
        print(f"Reminder: Contact {contact} - SLA of {sla} days reached.")
