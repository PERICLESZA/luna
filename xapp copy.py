import streamlit as st
import pandas as pd
import Controllers.customerController as customerController
import Models.customer as Customer
from city import CityForm

st.set_page_config(layout='wide')

# desabilita os botões de avanço no campo número----------
st.markdown("""
<style> 
    button.step-up {display: none;} button.step-down {display: none;} div[data-baseweb] {border-radius: 4px;}
</style>""",
            unsafe_allow_html=True)
# ---------------------------------------------------------

# st.expander(True)

menuLuna, menuExchange, menuCustomer, menuCity = st.tabs(["Exchange","History", "Customer", "City"])
    
def main():
    # Remove whitespace from the top of the page and sidebar

    # new_title = '<p style="font-family:sans-serif; color:#FFF; font-size: 30px;">Exchange</p>'
    # st.markdown(new_title, unsafe_allow_html=True)

    # redefine as margins do html --------------------------------------------------------------------
    st.markdown("""
        <style>
        .sidebar {padding-top: -10px; padding-bottom: 0rem; padding-left: 1rem; padding-right: 1rem;}
        </style>
        """, unsafe_allow_html=True)
    # #  ---------------------------------------------------------------------------------------------


    menu = ["Home", "About", "Contact"]
    st.sidebar.image('./assets/LunaLogo.png', width=200)
    choice = st.sidebar.selectbox("Menu", menu)

    # redefine as margins do html --------------------------------------------------------------------
    st.markdown("""
        <style>
        .block-container {padding-top: 2rem; padding-bottom: 0rem; padding-left: 1rem; padding-right: 1rem;}
        </style>
        """, unsafe_allow_html=True)
    #  ---------------------------------------------------------------------------------------------

    with menuLuna:        
        if choice == "Home":
            # Metod 1: Context Manager Approach
            tCol1, tCol2, tcol3 = st.columns([4, 1.5,1])
            with tCol1:
                cl1, cl2, cl3 = st.columns([1, 1,.5])
                with st.form(key='form1'):
                    with cl1:
                        firstname = st.text_input("Phone No/Name", label_visibility='collapsed', placeholder='Phone No/Name')
                        phone = st.text_input("Phone", label_visibility='collapsed', placeholder="Phone")
                    with cl2:
                        company = st.text_input("Company", label_visibility='collapsed', placeholder='Company')
                        bank = st.text_input("Our Bank", label_visibility='collapsed', placeholder='Our Bank')
                    with cl3:
                        dateTime = st.date_input("Date/Time", label_visibility='collapsed')
                    clf1, clf2,clf3 = st.columns([.7, .7,.1])
                    with clf1:
                        value = st.number_input("Value")
                        percValue = st.number_input("% Value")
                        wire = st.number_input("Wire")
                        cents1 = st.number_input("Cents 1")
                        pay = st.number_input("Pay")
                    with clf2:
                        cents2 = st.number_input("Cents 2")
                        Recieve = st.number_input("Recieve")
                        comPerc = st.number_input("Comission %")
                        subTotal = st.number_input("Sub Total")
                        ok = st.checkbox("Ok")
                        subtmit_button = st.form_submit_button(label='SignUp')
                    # with clf3:
                    #     # if subtmit_button:
                    #     # st.success(
                    #     #     "Hello {} you ve created an account".format(firstname)
                    #     # )

            with tCol2:
                with st.form(key='form2'):
                    c1,c2,c3 = st.columns([.1,2,.1])
                    with c2: 
                        st.image('./assets/Capturar.png', use_column_width=True)
                        subtmit_button = st.form_submit_button(label='Atualizar')
                        # if subtmit_button:
                        #     st.success(
                        #         "Hello {} you ve created an account".format(firstname))

        elif choice == "About":
            st.subheader("About")
        else:
            st.subheader("Contact")
    # with menuExchange:
    # with menuCustomer:
    with menuCity:
        CityForm()        


if __name__ == '__main__':
    main()
