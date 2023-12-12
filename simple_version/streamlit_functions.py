import streamlit as st
from datetime import datetime
from functions import get_person_from_db, beautify_person_info, delete_person_from_db, \
    get_person_id_from_full_name, add_person_to_db, get_person_full_name_from_id, get_person_full_name \
    , modify_person_in_db
    

def get_person() -> None:
    with st.form("get_person"):
        name = st.text_input("name")
        surname = st.text_input("surname")
        st.session_state['submit_get_person'] = st.form_submit_button("Submit")

    if st.session_state['submit_get_person']:
        matches = get_person_from_db(name, surname, st.session_state.persons)
        st.markdown('### Found people:')
        if len(matches):
            st.markdown(f"**{len(matches)} persons were found**")
            for match in matches:
                beautified_person_info = beautify_person_info(match, db=st.session_state.persons)
                with st.container(border=True):
                    st.markdown(beautified_person_info)
        else:
            st.write("No person was found")


def delete_person() -> None:
    with st.form("delete_person"):
        st.write("**Find person to delete**")
        name = st.text_input("name")
        surname = st.text_input("surname")
        st.session_state['submit_find_person_to_delete'] = st.form_submit_button("Submit") 

    if st.session_state['submit_find_person_to_delete'] or st.session_state['submit_delete_person']:
        matches = get_person_from_db(name, surname, st.session_state.persons)
        if len(matches):
            st.session_state['submit_delete_person'] = True
            # st.write(matches)
            st.write("Click on the person to delete it:")
            btns = []
            for match in matches:
                mini_description = f"Name: {match['name']}  \n"\
                                    f"Surname: {match['surname']}  \n"\
                                    f"Patronymic: {match['patronymic']}  \n"\
                                    f"Date of birth: {match['date_of_birth']}"
                btns.append(st.button(mini_description))
            
            # print(json.dumps(st.session_state.persons, indent=4, ensure_ascii=False))
            if any(btns):
                matches_id = btns.index(True)
                person = matches[matches_id]
                if delete_person_from_db(person, db=st.session_state.persons):
                    st.success(f"{matches[matches_id]['name']} was succesfully deleted!")
                else:
                    st.error("Some error was occured while deleting")
                st.session_state['submit_delete_person'] = False
        else:
            st.warning("No persons were found")


def add_person() -> None:
    with st.form("add_person"):
        name = st.text_input("Name")
        surname = st.text_input("Surname")
        maiden_name = st.text_input("Maiden name")
        patronymic = st.text_input("Patronymic")
        sex = st.selectbox("Sex", ['Male', 'Female'])
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
                "name": name,
                "surname": surname,
                "patronymic": patronymic,
                "is_male": True if sex == 'Male' else False,
                "date_of_birth": date_of_birth.strftime("%Y-%m-%d") if date_of_birth else None,
                "date_of_death": date_of_death.strftime("%Y-%m-%d") if date_of_death else None,
                "maiden_name": maiden_name,
                "informal_role": informal_role,
                "place_of_birth": place_of_birth,
                "place_of_residance": place_of_residance,
                "education": education,
                "occupation": occupation,
                "contacts": contacts,
                "links": {
                    "mother": get_person_id_from_full_name(mother, st.session_state.persons) if mother else None,
                    "father": get_person_id_from_full_name(father, st.session_state.persons) if father else None,
                    "siblings": [get_person_id_from_full_name(sibling, st.session_state.persons) for sibling in siblings],
                    "childs": [get_person_id_from_full_name(child, st.session_state.persons) for child in childs],
                    "partners": [get_person_id_from_full_name(partner, st.session_state.persons) for partner in partners]
                },
                "notes": notes
            }
        if add_person_to_db(new_person, st.session_state.persons):
            st.success('Successfully added!')
            st.markdown(beautify_person_info(new_person, st.session_state.persons))


def modify_person() -> None:
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
                mini_description = f"**Name**: {match['name']}  \n"\
                                    f"**Surname**: {match['surname']}  \n"\
                                    f"**Patronymic**: {match['patronymic']}  \n"\
                                    f"**Date of birth**: {match['date_of_birth']}"
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
                    sex = st.selectbox("Sex", ['Male', 'Female'], index=0 if person['is_male'] else 1)
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

                    st.write("**Links**")
                    mother = st.selectbox("Mother", st.session_state.full_names, 
                                          placeholder="Type full name or choose from the list", 
                                          index=st.session_state.id_to_list_index[person['links']['mother']] if person['links']['mother'] else None) 
                    father = st.selectbox("Father", st.session_state.full_names, 
                                          placeholder="Type full name or choose from the list", 
                                          index=st.session_state.id_to_list_index[person['links']['father']] if person['links']['father'] else None)
                    siblings = st.multiselect("Siblings", st.session_state.full_names, 
                                              placeholder="Type full name or choose from the list", 
                                              default=[get_person_full_name_from_id(sib, st.session_state.persons) for sib in person['links']['siblings']])
                    childs = st.multiselect("Childs", st.session_state.full_names, 
                                            placeholder="Type full name or choose from the list", 
                                            default=[get_person_full_name_from_id(ch, st.session_state.persons) for ch in person['links']['childs']])
                    partners = st.multiselect("Partners", st.session_state.full_names, 
                                              placeholder="Type full name or choose from the list", 
                                              default=[get_person_full_name_from_id(pt, st.session_state.persons) for pt in person['links']['partners']])

                    notes = st.text_area("Notes", value=person['notes'])
                    st.session_state['submit_save_person_info_changes'] = st.form_submit_button("Confirm changes")
            

            if st.session_state['submit_save_person_info_changes']:
                person = st.session_state.person
                modified_person = {
                        "id": person['id'],
                        "name": name,
                        "surname": surname,
                        "patronymic": patronymic,
                        "is_male": True if sex == 'Male' else False,
                        "date_of_birth": date_of_birth.strftime('%Y-%m-%d') if date_of_birth else None,
                        "date_of_death": date_of_death.strftime('%Y-%m-%d') if date_of_death else None,
                        "maiden_name": maiden_name,
                        "informal_role": informal_role,
                        "place_of_birth": place_of_birth,
                        "place_of_residance": place_of_residance,
                        "education": education,
                        "occupation": occupation,
                        "contacts": contacts,
                        "links": {
                            "mother": get_person_id_from_full_name(mother, st.session_state.persons) if mother else None,
                            "father": get_person_id_from_full_name(father, st.session_state.persons) if father else None,
                            "siblings": [get_person_id_from_full_name(sibling, st.session_state.persons) for sibling in siblings],
                            "childs": [get_person_id_from_full_name(child, st.session_state.persons) for child in childs],
                            "partners": [get_person_id_from_full_name(partner, st.session_state.persons) for partner in partners]
                        },
                        "notes": notes
                    }
                
                modify_person_in_db(st.session_state.person, modified_person, st.session_state.persons)
                
                st.session_state['submit_modify_person_info'] = False
                st.session_state['submit_save_person_info_changes'] = False
                st.session_state['finished_modify_person_info'] = True
                st.rerun()

            if st.session_state['finished_modify_person_info']:
                st.success(f"{st.session_state.person['name']} info successfully modified!")
                st.session_state['finished_modify_person_info'] = False