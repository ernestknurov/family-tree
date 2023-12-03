import streamlit as st

if 'submit_add_person' not in st.session_state:
    st.session_state['submit_add_person'] = False
st.title("Family Tree")

with st.sidebar:
    # add_person_btn = st.button("Add person")
    with st.container(border=True):
        st.subheader("Add person")
        if st.toggle("show/hide", key=1):
            with st.form("add_person"):
                name = st.text_input("name")
                surname = st.text_input("surname")
                st.session_state['submit_add_person'] = st.form_submit_button("Submit")

                if st.session_state['submit_add_person']:
                    st.write('You submitted!')
    
    with st.container(border=True):
        st.subheader("Delete person")
        if st.toggle("show/hide", key=2):
            with st.form("add_person"):
                name = st.text_input("name")
                surname = st.text_input("surname")
                st.session_state['submit_add_person'] = st.form_submit_button("Submit")

                if st.session_state['submit_add_person']:
                    st.write('You submitted!')
    
    with st.container(border=True):
        st.subheader("Modify person's info")
        if st.toggle("show/hide", key=3):
            with st.form("add_person"):
                name = st.text_input("name")
                surname = st.text_input("surname")
                st.session_state['submit_add_person'] = st.form_submit_button("Submit")

                if st.session_state['submit_add_person']:
                    st.write('You submitted!')

