import streamlit as st
import Controllers.customerController as customerController
import Models.customer as Customer
# import Styles as sty

def mainExchange():
    # new_title = '<p style="font-family:sans-serif; color:#FFF; font-size: 30px;">Exchange</p>'
    # st.markdown(new_title, unsafe_allow_html=True)

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
                subtmit_button = st.form_submit_button(label='Save')

    with tCol2:
        with st.form(key='form2'):
            c1,c2,c3 = st.columns([.1,2,.1])
            with c2: 
                st.image('./assets/Capturar.png', use_column_width=True)
                subtmit_button = st.form_submit_button(label='Atualizar')