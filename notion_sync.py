import json
import os
from notion_client import Client
from datetime import datetime
from typing import List, Dict, Any
import streamlit as st


def init_notion_client():
    """Initialize the Notion client with the API key from secrets."""
    notion_api_key = os.environ.get("NOTION_API_KEY") or st.secrets.get("notion_api_key")
    if not notion_api_key:
        raise ValueError("Notion API key not found. Please add it to .env or .streamlit/secrets.toml")
    return Client(auth=notion_api_key)


def get_notion_database_id():
    """Get the Notion database ID from secrets."""
    database_id = os.environ.get("NOTION_DATABASE_ID") or st.secrets.get("notion_database_id")
    if not database_id:
        raise ValueError("Notion database ID not found. Please add it to .env or .streamlit/secrets.toml")
    return database_id


def format_person_for_notion(person: Dict[str, Any]) -> Dict[str, Any]:
    """Format a person's data for Notion database."""
    
    # Convert links objects to string lists for easier storage in Notion
    links = person.get('links', {}) or {}
    siblings_names = []
    children_names = []
    partners_names = []
    mother_name = None
    father_name = None
    
    from functions import get_person_full_name_from_id
    
    # Get names from session state persons
    import streamlit as st
    
    if links.get('mother') is not None:
        mother_name = get_person_full_name_from_id(links['mother'], st.session_state.persons)
    
    if links.get('father') is not None:
        father_name = get_person_full_name_from_id(links['father'], st.session_state.persons)
    
    for sibling_id in links.get('siblings', []):
        siblings_names.append(get_person_full_name_from_id(sibling_id, st.session_state.persons))
    
    for child_id in links.get('childs', []):
        children_names.append(get_person_full_name_from_id(child_id, st.session_state.persons))
    
    for partner_id in links.get('partners', []):
        partners_names.append(get_person_full_name_from_id(partner_id, st.session_state.persons))
    
    # Format dates correctly for Notion
    date_of_birth = person.get('date_of_birth')
    date_of_death = person.get('date_of_death')
    
    # Helper function to ensure string values
    def ensure_string(value):
        if value is None:
            return ""
        return str(value)
    
    # Prepare the notion properties object with ID as title
    notion_person = {
        "ID": {"title": [{"text": {"content": str(person.get('id', 0))}}]},
        "Name": {"rich_text": [{"text": {"content": ensure_string(person.get('name'))}}]},
        "Surname": {"rich_text": [{"text": {"content": ensure_string(person.get('surname'))}}]},
        "Patronymic": {"rich_text": [{"text": {"content": ensure_string(person.get('patronymic'))}}]},
        "Gender": {"select": {"name": "Male" if person.get('is_male', True) else "Female"}},
        "Mother": {"rich_text": [{"text": {"content": ensure_string(mother_name)}}]},
        "Father": {"rich_text": [{"text": {"content": ensure_string(father_name)}}]},
        "Siblings": {"rich_text": [{"text": {"content": ", ".join(siblings_names)}}]},
        "Children": {"rich_text": [{"text": {"content": ", ".join(children_names)}}]},
        "Partners": {"rich_text": [{"text": {"content": ", ".join(partners_names)}}]},
        "Maiden Name": {"rich_text": [{"text": {"content": ensure_string(person.get('maiden_name'))}}]},
        "Place of Birth": {"rich_text": [{"text": {"content": ensure_string(person.get('place_of_birth'))}}]},
        "Place of Residence": {"rich_text": [{"text": {"content": ensure_string(person.get('place_of_residance'))}}]},
        "Education": {"rich_text": [{"text": {"content": ensure_string(person.get('education'))}}]},
        "Occupation": {"rich_text": [{"text": {"content": ensure_string(person.get('occupation'))}}]},
        "Hobby": {"rich_text": [{"text": {"content": ensure_string(person.get('hobby'))}}]},
        "Health": {"rich_text": [{"text": {"content": ensure_string(person.get('health'))}}]},
        "Contacts": {"rich_text": [{"text": {"content": ensure_string(person.get('contacts'))}}]},
        "Notes": {"rich_text": [{"text": {"content": ensure_string(person.get('notes'))}}]},
    }
    
    # Add dates if present
    if date_of_birth:
        notion_person["Date of Birth"] = {"date": {"start": date_of_birth}}
    
    if date_of_death:
        notion_person["Date of Death"] = {"date": {"start": date_of_death}}
    
    # Add physical characteristics
    phys = person.get('physical_characteristics', {}) or {}
    physical_desc = (
        f"Eye Color: {ensure_string(phys.get('eye_color'))}\n"
        f"Hair Color: {ensure_string(phys.get('hair_color'))}\n"
        f"Height: {ensure_string(phys.get('height'))}\n"
        f"Weight: {ensure_string(phys.get('weight'))}\n"
        f"Appearance: {ensure_string(phys.get('appearance_description'))}"
    )
    notion_person["Physical Characteristics"] = {"rich_text": [{"text": {"content": physical_desc}}]}
    
    return notion_person


def sync_to_notion(persons: List[Dict[str, Any]]) -> bool:
    """Sync all persons to Notion database.
    
    Returns True if successful, False otherwise.
    """
    try:
        notion = init_notion_client()
        database_id = get_notion_database_id()
        
        # First, query existing entries to avoid duplicates
        existing_pages = []
        query_response = notion.databases.query(database_id=database_id)
        existing_pages.extend(query_response["results"])
        
        while query_response.get("has_more", False):
            query_response = notion.databases.query(
                database_id=database_id,
                start_cursor=query_response["next_cursor"]
            )
            existing_pages.extend(query_response["results"])
        
        # Extract IDs from existing pages (now ID is a title property)
        existing_ids = {}
        for page in existing_pages:
            try:
                title_content = page["properties"]["ID"]["title"]
                if title_content and len(title_content) > 0:
                    person_id_str = title_content[0]["text"]["content"]
                    # Convert string ID back to integer for comparison
                    person_id = int(person_id_str)
                    existing_ids[person_id] = page["id"]
            except (KeyError, TypeError, ValueError):
                continue
        
        # Sync each person
        for person in persons:
            person_id = person.get('id')
            notion_person = format_person_for_notion(person)
            
            if person_id in existing_ids:
                # Update existing page
                notion.pages.update(
                    page_id=existing_ids[person_id],
                    properties=notion_person
                )
            else:
                # Create new page
                notion.pages.create(
                    parent={"database_id": database_id},
                    properties=notion_person
                )
        
        return True
    except Exception as e:
        import streamlit as st
        st.error(f"Error syncing to Notion: {str(e)}")
        return False