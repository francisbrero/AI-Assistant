import streamlit as st
import json
from datetime import datetime
from main import load_contacts, save_contacts, settings

contacts = load_contacts()

st.title("Contact Management Agent")
st.sidebar.header("Settings")

# Modify settings
for category, data in settings['categories'].items():
    sla = st.sidebar.number_input(f"{category.capitalize()} SLA (days)", min_value=1, value=data['sla'])
    vip_sla = st.sidebar.number_input(f"{category.capitalize()} VIP SLA (days)", min_value=1, value=data['vip_sla'])
    settings['categories'][category]['sla'] = sla
    settings['categories'][category]['vip_sla'] = vip_sla

# Save settings
with open('settings.json', 'w') as file:
    json.dump(settings, file)

# Display contacts for categorization
st.subheader("Categorize Contacts")
for contact_id, contact in contacts.items():
    # Concatenate first name and last name for display
    contact_name = f"{contact.get('first_name', '')} {contact.get('last_name', '')}".strip()
    st.write(f"**{contact_name}** - Last interaction: {contact.get('last_interaction', 'N/A')}")
    
    category = st.selectbox("Category", options=list(settings['categories'].keys()), index=0, key=contact_id)
    vip = st.checkbox("VIP", key=f"vip_{contact_id}")

    contacts[contact_id]['category'] = category
    contacts[contact_id]['vip'] = vip
    contacts[contact_id]['last_interaction'] = datetime.now().isoformat()

save_contacts(contacts)
st.success("Contacts updated successfully.")
