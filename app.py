import time
import json
import shutil
import graphviz
import streamlit as st
from datetime import datetime
from streamlit_functions import get_person, delete_person, add_person, modify_person
from functions import get_person_full_name_from_id
import os

st.set_page_config(layout="wide")
PATH_TO_DATABASE = st.secrets['path_to_database']

if 'init' not in st.session_state:
    st.session_state['submit_add_person'] = False
    st.session_state['submit_find_person_to_delete'] = False
    st.session_state['submit_delete_person'] = False
    st.session_state['submit_get_person'] = False
    st.session_state['submit_find_person_to_modify'] = False
    st.session_state['submit_choose_person_to_modify'] = False
    st.session_state['submit_modify_person_info'] = False
    st.session_state['submit_save_person_info_changes'] = False
    st.session_state['finished_modify_person_info'] = False
    st.session_state['person'] = {}
    st.session_state['init'] = True
    with open(PATH_TO_DATABASE, 'r', encoding='utf-8') as f:
        st.session_state.persons = json.load(f)
    st.session_state.full_names = [get_person_full_name_from_id(person['id'], st.session_state.persons) for person in st.session_state.persons]
    st.session_state.id_to_list_index = {person['id']:index for index, person in enumerate(st.session_state.persons)}

st.title("Family Tree")

with st.sidebar:
    # ADD PERSON
    with st.container(border=True):
        st.subheader("Add person")
        if st.toggle("show/hide", key=1):
            add_person()

    # FIND PERSON
    with st.container(border=True):
        st.subheader("Find person")
        if st.toggle("show/hide", key=2):
            get_person()

    # DELETE PERSON
    with st.container(border=True):
        st.subheader("Delete person")
        if st.toggle("show/hide", key=3):
            delete_person()

    # MODIFY PERSON
    with st.container(border=True):
        st.subheader("Modify person's info")
        if st.toggle("show/hide", key=4):
            modify_person()

    # SYNC OPTIONS
    with st.container(border=True):
        st.subheader("Sync Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Sync with database"):
                # 1. Make backup
                timestamp_format = "%Y-%m-%d-%H:%M"
                timestamp = datetime.now().strftime(timestamp_format)
                
                # Create backups directory if it doesn't exist
                if not os.path.exists("backups"):
                    os.makedirs("backups")

                source_path = "person.json" 
                destination_path = f"backups/person_backup({timestamp}).json"
                shutil.copy(source_path, destination_path)  # Use copy instead of move

                # 2. Save new version of persons.json
                with open("person.json", "w") as f:
                    json.dump(st.session_state.persons, f, indent=4, ensure_ascii=False)
                
                st.success("Successfully synchronized with local database!")
                time.sleep(2)
                st.rerun()
        
        with col2:
            if st.button("Sync with Notion"):
                from notion_sync import sync_to_notion
                
                # First sync local database
                with open("person.json", "w") as f:
                    json.dump(st.session_state.persons, f, indent=4, ensure_ascii=False)
                
                # Then sync to Notion
                if sync_to_notion(st.session_state.persons):
                    st.success("Successfully synchronized with Notion!")
                else:
                    st.error("Failed to sync with Notion. Check your API key and database ID.")
                time.sleep(2)
                st.rerun()

graph = graphviz.Digraph()

for person in st.session_state.persons:
    graph.node(f"-{person['id']}-", person['name'])

for person in st.session_state.persons:
    if person['links']['childs']:
        for child in person['links']['childs']:
            graph.edge(f"-{person['id']}-", f'-{child}-') # to childs


st.graphviz_chart(graph)
