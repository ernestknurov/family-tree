import streamlit as st
import json
from datetime import datetime
import locale

def get_person_from_db(name: str, surname: str, db: list, patronymic: str=None) -> dict:
    """Return persons which names or surnames match with given names"""
    matches = []
    for person in db:
            # print(f"Name: {name}; Name type: {type(name)}")
            # print(f"Surname: {surname}; Surname type: {type(surname)}")
            if (not name or name.lower() in person['name'].lower()) and \
                (not surname or surname.lower() in person['surname'].lower()) and \
                (not patronymic or patronymic.lower() in person['patronymic'].lower()):
                matches.append(person)

    return matches

def get_person_from_db_by_id(id: int,  db: list) -> dict:
    for person in db:
        if person['id'] == id:
            return person
    return {}


def delete_person_from_db(person: dict, db: list) -> bool:

    def delete_links(from_whom: str, whom: str, person: dict=person, db: list=db) -> bool:
        if isinstance(person['links'][from_whom], list):
            for relative_id in person['links'][from_whom]:
                relative_id_in_list = [relative_id == person['id'] for person in db].index(True)
                db[relative_id_in_list]['links'][whom].remove(person['id'])
        elif isinstance(person['links'][from_whom], int):
            relative_id = person['links'][from_whom]
            relative_id_in_list = [relative_id == person['id'] for person in db].index(True)
            db[relative_id_in_list]['links'][whom].remove(person['id'])
        return True
    
    delete_links('mother', 'childs')
    delete_links('father', 'childs')
    delete_links('childs', 'father' if person['is_male'] else 'mother')
    delete_links('siblings', 'siblings')
    delete_links('partners', 'partners')
    db.remove(person)
    return True


def get_person_id_from_full_name(full_name: str, persons: list) -> int:
    name, surname, patronymic = full_name.split()
    match = get_person_from_db(name, surname, persons, patronymic=patronymic)[0]
    return match['id']

def get_person_full_name_from_id(id: int, db: list) -> str:
    person = get_person_from_db_by_id(id, db)
    full_name = " ".join([person[field] for field in ['surname', 'name', 'patronymic'] if person[field]])
    return full_name

def beautify_person_info(person: dict, db: list) -> dict:
    
    locale.setlocale(locale.LC_TIME, 'ru_RU.utf8')
    beautified_person = {}
    # for key, value in beautified_person['links'].items():
    #     if isinstance(value, list):
    #         beautified_person['links'][key] = [get_person_full_name_from_id(v, db) for v in value]
    #     elif isinstance(value, int):
    #         beautified_person['links'][key] = get_person_full_name_from_id(value, db)
    
    # map fields to readble russian
    beautified_person['ФИО'] = get_person_full_name_from_id(person['id'], db)
    if not person['is_male']:
        beautified_person['Девичья фамилия'] = person['maiden_name']
    beautified_person['Пол'] = 'мужчина' if person['is_male'] else 'женщина'
    beautified_person['Дата рождения'] = person['date_of_birth']
    beautified_person['Дата смерти'] = person['date_of_death']
    beautified_person['Неформальная роль'] = person['date_of_death']
    beautified_person['Место рождения'] = person['place_of_birth']
    beautified_person['Место проживания'] = person['place_of_residance']
    beautified_person['Образование'] = person['education']
    beautified_person['Занятость'] = person['occupation']
    beautified_person['Родственники'] = {
        'Отец': get_person_full_name_from_id(person['links']['father'], db) if person['links']['father'] is not None else None,
        'Мать': get_person_full_name_from_id(person['links']['mother'], db) if person['links']['mother'] is not None else None,
        'Братья/сёстры': ", ".join([get_person_full_name_from_id(sib, db) for sib in person['links']['siblings']]) if person['links']['siblings'] is not None else None,
        'Дети': ", ".join([get_person_full_name_from_id(ch, db) for ch in person['links']['childs']]) if person['links']['childs'] is not None else None,
        'Супруги': ", ".join([get_person_full_name_from_id(pt, db) for pt in person['links']['partners']]) if person['links']['partners'] is not None else None
    }
    beautified_person['Контакты'] = person['contacts']
    beautified_person['Другое'] = person['notes']


    if beautified_person['Дата рождения']:
        beautified_person['Дата рождения'] = datetime.strptime(beautified_person['Дата рождения'], '%Y-%m-%d')
    if beautified_person['Дата смерти']:
        beautified_person['Дата смерти'] = datetime.strptime(beautified_person['Дата смерти'], '%Y-%m-%d')

    final_info = ''
    for key, value in beautified_person.items():
        if value is None:
            final_info += f"**{key}**: \-  \n"
        elif isinstance(value, datetime):
            final_info += f"**{key}**: {value.strftime('%d %B %Y')}  \n"
        elif isinstance(value, dict):
            final_info += f'**{key}**:  \n'
            for inner_key, inner_value in value.items():
                # print(f"Inner value: {inner_value}, type: {type(inner_value)}")
                if inner_value is None or inner_value == []:
                    final_info += f"* {inner_key}: \-  \n"
                else:
                    final_info += f'* {inner_key}: {inner_value}  \n'
            final_info += "\n"
        else:
            final_info += f"**{key}**: {value}  \n"
    print(final_info)
    return final_info


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

def my_fun(db: dict):
    st.write(db['text'])
    db['text'] = "blalbalba"