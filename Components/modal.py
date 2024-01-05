import streamlit as st
import streamlit.components.v1 as components
from streamlit_modal import Modal


modal = Modal("Demo Modal", key='mod1')

open_modal = st.button("Open")
if open_modal:
    modal.open()

if modal.is_open():
    with modal.container():

        modalString = 'teste'

        value = st.checkbox("Check me")
        st.write(f"Checkbox checked: {value}")