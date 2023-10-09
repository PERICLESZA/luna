import streamlit as st
import pandas as pd
import Controllers.customerController as customerController
import Models.customer as Customer
from city import mainCity
from exchange import mainExchange
from customer import mainCustomer
import Styles as sty

st.set_page_config(layout='wide')
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
# st.set_option('Viewer', 'off')

# define a altura dos ccampos de entrada
# st.write(
#     """  <style>
#             .stTextInput > div > div > input {height: 25px;}
#             .stNumberInput input[type="number"] {height: 25px;}
#             .stSelectbox input[type="selectbox"] {height: 20px;}
#             .stDateInput input[type="date"] {height: 20px;}
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# desabilita os botões de avanço no campo número----------
st.markdown("""
<style> 
    button.step-up {display: none;} button.step-down {display: none;} div[data-baseweb] {border-radius: 4px;}
</style>""",
            unsafe_allow_html=True)
# ---------------------------------------------------------
# redefine as margins do html --------------------------------------------------------------------
st.markdown("""
    <style>
    .block-container {padding-top: 2rem; padding-bottom: 0rem; padding-left: 1rem; padding-right: 1rem;}
    </style>
    """, unsafe_allow_html=True)
#  ---------------------------------------------------------------------------------------------

# redefine as margins do html --------------------------------------------------------------------
st.markdown("""
    <style>
    .sidebar {padding-top: -10px; padding-bottom: 0rem; padding-left: 1rem; padding-right: 1rem;}
    </style>
    """, unsafe_allow_html=True)
# #  ---------------------------------------------------------------------------------------------

# st.expander(True)

# menuExchange, menuCustomer, menuCity = st.tabs(["Exchange", "Customer", "City"])
    
def main():

    menu = ["Exchange", "Customer", "City"]
    st.sidebar.image('./assets/LunaLogo.png', width=200)
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Customer":
        mainCustomer()
    elif choice == "City":
        mainCity()
    elif choice == "Exchange":
        mainExchange()

if __name__ == '__main__':
    main()
