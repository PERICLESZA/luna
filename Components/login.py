import streamlit as st
import pandas as pd
import Controllers.loginController as loginC
import Models.login as Login
import bcrypt

def mainLogin():
    pCol1, pCol2 = st.columns(2)
    with pCol1:
        # Carregar todos os itens da tabela
        item_id = 0
        items = loginC.get_all_login(0)
        # x =
        selected_item_id = st.selectbox(
            "Select Login:", items, format_func=lambda x: x[1])
        if selected_item_id:
            item_id = selected_item_id[0]

       # active, email, login, nome, perfil, senha
        if item_id > 0:
            item_details = loginC.get_det_login(item_id)
            item_active = item_details[1]
            item_email  = item_details[2]
            item_login  = item_details[3]
            item_nome   = item_details[4]
            item_perfil = item_details[5]
            item_senha  = item_details[6]

            new_active = st.checkbox("Active:", False, item_active)
            new_email = st.text_input("Email:", item_email)
            new_login = st.text_input("Login:", item_login)
            new_nome = st.text_input("Name:", item_nome)
            new_perfil = st.text_input("Access:", item_perfil)
            new_senha = st.text_input("Password:", item_senha, type= 'password')

            # Customer.active = st.checkbox("Active", False, key="bActive")
            Login.idlogin = item_id
            Login.active = new_active
            Login.email = new_email
            Login.login = new_login
            Login.nome = new_nome
            Login.perfil = new_perfil
            Login.senha = hash_password(new_senha)
            
            # Botão para salvar as alterações ou adicionar um novo item
            col1, col2, col3, col4 = st.columns([1.2, 1.2, 1.2, .5])
            with col1:
                if st.button("Save", key="sStatus"):
                    loginC.update_login(Login)
                    st.success("Saved!")
            with col2:
                # Botão para excluir o item
                if st.button("Delete", key="dStatus"):
                    loginC.delete_status(item_id)
                    st.success("Deleted!")
            with col3:
                if st.button("Update", key="uStatus"):
                    items = loginC.get_all_login(0)
                    st.success("Updated!")
            with col4:
                if st.button("New", key="nStatus"):
                    items = loginC.get_all_login(0)
                    selected_item_id = None

        else:
            # Adicionar um novo item
            adicionar_item()

    with pCol2:
        st.write('')
        st.write('')
        rows = loginC.get_all_login(0)
                                  #  idlogin,   active,   email,  login,    nome,  perfil, s enha
        df = pd.DataFrame(
            rows, columns=['Id', 'Name', 'Active', 'Email', 'Login', 'Level', 'Psw'])
        df['Active'] = df['Active'].astype(bool)
        df['Psw'] = ""

        left_aligned_df = df.style.set_properties(**{'text-align': 'center'})

        # Get dataframe row-selections from user with st.data_editor
        edited_df = st.data_editor(left_aligned_df,
                                   hide_index=True,
                                   disabled=df.columns,
                                   width=600,
                                   height=500)
        
def adicionar_item():
    item_name = st.text_input("Name:")
    item_email = st.text_input("Email:")
    item_login = st.text_input("Login:")
    item_perfil = st.text_input("Type:")
    item_senha = st.text_input("Passwird:")
    item_active = st.checkbox("Active:")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Add"):
            if item_name:
                Login.idlogin = 0
                Login.active = item_active
                Login.email = item_email
                Login.login = item_login
                Login.nome = item_name
                Login.perfil = item_perfil
                Login.senha = hash_password(item_senha)
                loginC.insert_login(Login)

                st.success("Added!")
                items = loginC.get_all_login(1)
            else:
                st.warning("Fill the filed Login.")
    with col2:
        if st.button("Update"):
            items = loginC.get_all_login(0)
            st.success("Updated!")


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
