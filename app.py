import streamlit as st
from Components.city import mainCity
from Components.country import mainCountry
from Components.classc import mainClass
from Components.exchange import mainExchange
from Components.bank import mainBank
from Components.exchange1 import mainExchange1
from Components.customer import mainCustomer
from Components.identification import mainIdentification
from Components.parameter import mainParameter
from Components.status import mainStatus

st.set_page_config(layout='wide')
hide_streamlit_style = """<style> #MainMenu {visibility: hidden;}
            footer {visibility: hidden;} </style>"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

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

def main():

    menu = ["Exchange", "Bank", "City", "Class", "Country", "Customer", "Identification", "Parameter","Exchange1","Status"]
    # menu = ["Exchange", "City"]
    st.sidebar.image('./assets/LunaLogo.png', width=150)
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Customer":
        mainCustomer()
    elif choice == "City":
        mainCity()
    elif choice == "Class":
        mainClass()
    elif choice == "Identification":
        mainIdentification()
    elif choice == "Exchange":
        mainExchange()
    elif choice == "Exchange1":
        mainExchange1()
    elif choice == "Bank":
        mainBank()
    elif choice == "Parameter":
        mainParameter()
    elif choice == "Status":
        mainStatus()
    elif choice == "Country":
        mainCountry()

if __name__ == '__main__':
    main()
