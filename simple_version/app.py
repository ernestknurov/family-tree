import os
import json
import shutil
import graphviz
import streamlit as st
from datetime import datetime
from functions import get_person_from_db, get_person_full_name_from_id, get_person_id_from_full_name, get_person, delete_person


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
    with open('person.json', 'r') as f:
        st.session_state.persons = json.load(f)
    st.session_state.full_names = [get_person_full_name_from_id(person['id'], st.session_state.persons) for person in st.session_state.persons]

st.title("Family Tree")

with st.sidebar:
    # ADD PERSON
    with st.container(border=True):
        st.subheader("Add person")
        if st.toggle("show/hide", key=1):
            with st.form("add_person"):
                name = st.text_input("Name")
                surname = st.text_input("Surname")
                maiden_name = st.text_input("Maiden name")
                patronymic = st.text_input("Patronymic")
                date_of_birth = st.date_input("Date of birth", value=None)
                date_of_death = st.date_input("Date of death", value=None)
                informal_role = st.text_area("Informal Role")
                place_of_birth = st.text_input("Place of birth")
                place_of_residance = st.text_input("Place of residance")
                education = st.text_area("Education")
                occupation = st.text_area("Occupation")
                contacts = st.text_area("Contacts")
                notes = st.text_area("Notes")

                st.write("**Links**")
                mother = st.selectbox("Mother", st.session_state.full_names, placeholder="Type full name or choose from the list", index=None)
                father = st.selectbox("Father", st.session_state.full_names, placeholder="Type full name or choose from the list", index=None)
                siblings = st.multiselect("Siblings", st.session_state.full_names, placeholder="Type full name or choose from the list", default=None)
                childs = st.multiselect("Childs", st.session_state.full_names, placeholder="Type full name or choose from the list", default=None)
                partners = st.multiselect("Partners", st.session_state.full_names, placeholder="Type full name or choose from the list", default=None)

                st.session_state['submit_add_person'] = st.form_submit_button("Submit")

            if st.session_state['submit_add_person']:
                new_person = {
                        "id": max([person['id'] for person in st.session_state.persons]) + 1,
                        "name": name,
                        "surname": surname,
                        "patronymic": patronymic,
                        "date_of_birth": date_of_birth,
                        "date_of_death": date_of_death,
                        "maiden_name": maiden_name,
                        "informal_role": informal_role,
                        "place_of_birth": place_of_birth,
                        "place_of_residance": place_of_residance,
                        "education": education,
                        "occupation": occupation,
                        "contacts": {
                            "all": contacts
                        },
                        "links": {
                            "mother": get_person_id_from_full_name(mother, st.session_state.persons),
                            "father": get_person_id_from_full_name(father, st.session_state.persons),
                            "siblings": [get_person_id_from_full_name(sibling, st.session_state.persons) for sibling in siblings],
                            "childs": [get_person_id_from_full_name(child, st.session_state.persons) for child in childs],
                            "partner": [get_person_id_from_full_name(partner, st.session_state.persons) for partner in partners]
                        },
                        "notes": notes
                    }
                st.session_state.persons.append(new_person)
                st.success('Successfully added!')
                st.write(new_person)

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
        # print(json.dumps(st.session_state.persons, indent=4, ensure_ascii=False))


    # MODIFY PERSON
    with st.container(border=True):
        st.subheader("Modify person's info")
        if st.toggle("show/hide", key=4):
            with st.form("find_person_to_modify"):
                st.write("**Find person to modify**")
                name = st.text_input("name")
                surname = st.text_input("surname")
                st.session_state['submit_find_person_to_modify'] = st.form_submit_button("Submit")

            if st.session_state['submit_find_person_to_modify'] or\
               st.session_state['submit_choose_person_to_modify'] or\
               st.session_state['submit_modify_person_info'] or\
               st.session_state['submit_save_person_info_changes']:
                matches = get_person_from_db(name, surname, st.session_state.persons)
                if not len(matches):
                    st.warning("No persons were found")

                else:
                    st.session_state['submit_choose_person_to_modify'] = True

                    st.write("Click on the person to modify its information:")
                    btns = []
                    for match in matches:
                        mini_description = f"Name: {match['name']}  \n"\
                                            f"Surname: {match['surname']}  \n"\
                                            f"Patronymic: {match['patronymic']}  \n"\
                                            f"Date of birth: {match['date_of_birth']}"
                        btns.append(st.button(mini_description))

                    if any(btns):
                        person = matches[btns.index(True)]
                        st.session_state.person = person
                        st.session_state['submit_modify_person_info'] = True
                        # st.session_state['submit_choose_person_to_modify'] = False

                    if st.session_state['submit_modify_person_info']:
                        with st.form("modify_person"):
                            person = st.session_state.person
                            name = st.text_input("Name", value=person['name'])
                            surname = st.text_input("Surname", value=person['surname'])
                            maiden_name = st.text_input("Maiden name", value=person['maiden_name'])
                            patronymic = st.text_input("Patronymic", value=person['patronymic'])
                            date_of_birth_default_value = datetime.strptime(person['date_of_birth'], "%Y-%m-%d") if person['date_of_birth'] else None
                            date_of_birth = st.date_input("Date of birth", value=date_of_birth_default_value)
                            date_of_death_default_value = datetime.strptime(person['date_of_death'], "%Y-%m-%d") if person['date_of_death'] else None
                            date_of_death = st.date_input("Date of death", value=date_of_death_default_value)
                            informal_role = st.text_area("Informal Role", value=person['informal_role'])
                            place_of_birth = st.text_input("Place of birth", value=person['place_of_birth'])
                            place_of_residance = st.text_input("Place of residance", value=person['place_of_residance'])
                            education = st.text_area("Education", value=person['education'])
                            occupation = st.text_area("Occupation", value=person['occupation'])
                            contacts = st.text_area("Contacts", value=person['contacts'])
                            notes = st.text_area("Notes", value=person['notes'])
                            st.session_state['submit_save_person_info_changes'] = st.form_submit_button("Confirm changes")
                    

                    if st.session_state['submit_save_person_info_changes']:
                        person = st.session_state.person
                        modified_person = {
                                "id": person['id'],
                                "name": name,
                                "surname": surname,
                                "patronymic": patronymic,
                                "date_of_birth": date_of_birth.strftime('%Y-%m-%d') if date_of_birth else None,
                                "date_of_death": date_of_death.strftime('%Y-%m-%d') if date_of_death else None,
                                "maiden_name": maiden_name,
                                "informal_role": informal_role,
                                "place_of_birth": place_of_birth,
                                "place_of_residance": place_of_residance,
                                "education": education,
                                "occupation": occupation,
                                "contacts": {
                                    "all": contacts
                                },
                                "links": {
                                    "mother": -1,
                                    "father": -1,
                                    "childs": []
                                },
                                "notes": notes
                            }
                        person_index = [object['id'] == person['id'] for object in st.session_state.persons].index(True)
                        st.session_state.persons[person_index] = modified_person
                        st.session_state['submit_modify_person_info'] = False
                        st.session_state['submit_save_person_info_changes'] = False
                        st.session_state['finished_modify_person_info'] = True
                        st.rerun()

                    if st.session_state['finished_modify_person_info']:
                        st.success(f"{st.session_state.person['name']} info successfully modified!")
                        st.session_state['finished_modify_person_info'] = False


    if st.button("Sync with database"):
        # 1. Make backup
        timestamp_format = "%Y-%n-%d-%H:%M"
        timestamp = datetime.now().strftime(timestamp_format)

        source_path = "person.json" 
        destination_path = f"backups/person_backup({timestamp}).json"
        shutil.move(source_path, destination_path)

        # 2. Save new version of persons.json
        with open("person.json", "w") as f:
            json.dump(st.session_state.persons, f, indent=4, ensure_ascii=False)
        
        st.success("Successfully synchronized!")

    



graph = graphviz.Digraph()

for person in st.session_state.persons:
    graph.node(f"-{person['id']}-", person['name'])

for person in st.session_state.persons:
    if person['links']['childs']:
        for child in person['links']['childs']:
            graph.edge(f"-{person['id']}-", f'-{child}-') # to childs


st.graphviz_chart(graph)
