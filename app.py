import socket
import streamlit as st
import sys
from Components.city import mainCity
from Components.country import mainCountry
from Components.classc import mainClass
from Components.exchange import mainExchange
from Components.bank import mainBank
from Components.customer import mainCustomer
from Components.identification import mainIdentification
from Components.parameter import mainParameter
from Components.status import mainStatus
from Components.login import mainLogin
from Components.percentcheck import mainPercentcheck
from Components.storeip import mainStoreip
from Components.rpexchange import mainRpExchange
import Controllers.storeipController as storeipC
import Controllers.storeController as storeC
import Controllers.loginController as loginC

st.set_page_config(layout='wide')
hide_streamlit_style = """<style> #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}</style>"""
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

st.markdown("""
    <style>
    .stTextInput [data-baseweb=base-input] [disabled=""]{-webkit-text-fill-color: black;}
    .stNumberInput [data-baseweb=base-input] [disabled=""]{-webkit-text-fill-color: black;}
    </style>
    """, unsafe_allow_html=True)
   
def main():
    
    # cImg1, cImg2, cImg3 = st.columns([.2,1,1])
    # with cImg2:
    #     st.image('./assets/Luna.png', width=1000)

    st.sidebar.image('./assets/LunaLogo.png', width=165)
    host_name = socket.gethostname()
    local_ip = socket.gethostbyname(host_name)
    sStore = storeipC.get_det_storeip(local_ip)
    
    # st.write(local_ip)

    nmuser = st.sidebar.text_input("User:", "")
    vLogin = loginC.verify_login(nmuser)
    gsenha = st.sidebar.text_input('Psw:', type='password')
 
    loginOk = False
    
    if (nmuser!='admin' and nmuser!='' and vLogin==None):
        st.sidebar.error('User does not exist!')
    
    if nmuser and gsenha and vLogin:
        st.session_state['gsenha'] = gsenha
        st.session_state['perfil'] = vLogin[2]
        st.session_state['sStore'] = sStore
        
        loginOk = loginC.check_password(gsenha, vLogin[1])

        if not loginOk:
            st.sidebar.error('Password is incorrect!')
        else:
            if (nmuser == 'admin') and (loginOk) and (sStore == None):
                st.sidebar.warning('Unregistered computer. Ask the administrator to register the computer!')
            else:
                st.session_state['idstore'] = storeC.get_det_store(sStore[1])[0]

            if (nmuser == 'admin'):
                menu = ["Exchange", "Bank", "City", "Class", "Country", "Customer",
                        "Identification", "Login", "Parameter", "PercentCheck", "Status", "StoreIP","Report"]
            else:    
                menu = ["Exchange", "Bank", "City", "Class", "Country", "Customer",
                        "Identification"]
            
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
            elif choice == "Login":
                mainLogin()
            elif choice == "Bank":
                mainBank()
            elif choice == "Parameter" and gsenha:
                mainParameter()
            elif choice == "Status":
                mainStatus()
            elif choice == "Country":
                mainCountry()
            elif choice == "PercentCheck":
                mainPercentcheck()
            elif choice == "StoreIP":
                mainStoreip()
            elif choice == "Report":
                mainRpExchange()

            st.sidebar.divider()
            if (sStore != None):
                st.sidebar.success(storeC.get_det_store(sStore[1])[1])
            else:
                if (nmuser != "admin"):
                    st.sidebar.error('User does not exist!')
    st.sidebar.write("V-" + sys.version[:4])    # versão do python
if __name__ == '__main__':
    main()


