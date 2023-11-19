import streamlit as st
import Models.customer as Customer
import Controllers.customerController as customerC
import Controllers.cityController as cityC
import Controllers.idController as idC
import Controllers.classController as classC
import Controllers.countryController as countryC
import os
import Styles as sty
import subprocess

def rerun_script():
    subprocess.Popen(["python", "customer.py"])
    st.experimental_rerun()

def add_new_customer():

    pnCol1, pnCol2, pnCol3, pnCol4, pnCol5, pnCol6, pnCol7  = st.columns([0.1,2,.1,2,.01,3,.1])
    with pnCol1: st.write('')
    with pnCol2:
        # Usuário insere os detalhes do novo cliente
        Customer.name = sty.overlaid_input("Nome",'')
        Customer.andress = sty.overlaid_input("Adrress",'')
        items = cityC.get_all_cities(1)

        x = lambda x: x[1]
        selected_item_id = sty.overlaid_selectbox("City", items,0, x)
        if selected_item_id: Customer.fk_idcity = selected_item_id[0]

        Customer.phone = sty.overlaid_input("Phone",'')
        Customer.email = sty.overlaid_input("Email",'')
        
        items = idC.get_all_ids(1)
        x = lambda x: x[1]
        sel_item_id = sty.overlaid_selectbox('Identification', items, 0, x)
        if sel_item_id: Customer.fk_ididentification = sel_item_id[0]

        items = customerC.get_all_customers(1, 1)
        x = lambda x: x[1]
        sel_item_id = sty.overlaid_selectbox('Company', items, 0, x)
        if sel_item_id: Customer.fk_idcustomer = sel_item_id[0]

        cCb1, cCb2  = st.columns(2)
        with cCb1:
            Customer.active = st.checkbox("Active", False, key="bActive")
        with cCb2:    
            Customer.restriction = st.checkbox("Restriction", False, key="bRestriction")
    with pnCol3: st.write('')
    with pnCol4:
        
        items = classC.get_all_classes(1)
        x = lambda x: x[1]
        sel_item_id = sty.overlaid_selectbox('Class', items, 0, x)
        if sel_item_id: Customer.fk_idclasscustomer = sel_item_id[0]
        
        Customer.zipcode = sty.overlaid_input("Zipcode",'')
        Customer.state = sty.overlaid_input("State",'')
        Customer.phone2 = sty.overlaid_input("Phone2",'')
        Customer.dtbirth = sty.overlaid_input("Birthday",'')
        Customer.numidentification = sty.overlaid_input("Identification",'')
        Customer.comissionpercent = sty.overlaid_input("% Comission",'')
        
    with pnCol5: st.write('')
    with pnCol6:
        Customer.attention = sty.overlaid_area("Obs",'')

        img_path = 'customer_pic/'
        img_name = ''

        cPhoto1, cPhoto2, cPhoto3 = st.columns([1.5,4,1])
        with cPhoto1: st.write('')
        with cPhoto2: st.write('')
        with cPhoto3: st.write('')
        
        uploaded_image = st.file_uploader("", type=["jpg", "jpeg", "png"])
        if uploaded_image is not None:
            img_name = os.path.basename(uploaded_image.name)
            if not os.path.exists(img_path):
                os.makedirs(img_path)
            save_path = os.path.join(img_path, img_name)

            with open(save_path, "wb") as f:
                f.write(uploaded_image.read())
            Customer.picture_path = save_path

        # Botão para salvar o novo cliente
        if st.button("Salvar"):
            # Lógica para salvar o novo cliente no banco de dados
            customerC.insert_customer(Customer)

def mainCustomer():
    
    i_id= 0
    items = customerC.get_all_customers(0,0)
    selected_i_id = st.selectbox("Select Customer:", items, format_func=lambda x: x[1])
    st.write('')
    if selected_i_id:  i_id = selected_i_id[0]

    if i_id > 0:
    
        pCol1, pCol2, pCol3, pCol4, pCol5, pCol6, pCol7  = st.columns([0.1,2,.1,2,.01,3,.1])
        
        with pCol1:
            st.write('')
        with pCol2:

            i_det = customerC.get_det_customer(i_id)
            Customer.idcustomer = i_id
            Customer.name = i_det['name'] if i_det['name']!=None else 'name...'
            Customer.andress = i_det['andress']  if i_det['andress']!=None else 'adress...'
            Customer.fk_idcity = i_det['fk_idcity']
            Customer.phone = i_det['phone'] if i_det['phone']!=None else 'phone...'
            Customer.email = i_det['email'] if i_det['email']!=None else 'email...'
            Customer.fk_ididentification = i_det['fk_ididentification']
            Customer.fk_idcustomer = i_det['fk_idcustomer']
            Customer.active = i_det['active']
            Customer.fk_idclasscustomer = i_det['fk_idclasscustomer'] 
            Customer.zipcode = i_det['zipcode'] if i_det['zipcode']!=None else 'zipcode...'
            Customer.state = i_det['state'] if i_det['state']!=None else 'state...'
            Customer.phone2 = i_det['phone2'] if i_det['phone2']!=None else 'phone2...'
            Customer.dtbirth = i_det['dtbirth']
            Customer.numidentification = i_det['numidentification'] if i_det['numidentification']!=None else 'num id...'
            Customer.comissionpercent = i_det['comissionpercent'] if i_det['comissionpercent']!=None else 'comission...'
            Customer.restriction = i_det['restriction'] 
            Customer.attention = i_det['attention'] if i_det['attention']!=None else 'Observations...'
            Customer.picture_path = i_det['picture_path'] if i_det['picture_path']!=None else 'picture path...'

            # Begin Edition -------------------------------------------------------------------
            Customer.name = sty.overlaid_input("Nome", Customer.name)
            Customer.andress = sty.overlaid_input("Address", Customer.andress)

            # selectbox city ------------------------------------------------------------------
            items = cityC.get_all_cities(1)
            x=format_func=lambda x: x[1]
            if (Customer.fk_idcity is not None) and (Customer.fk_idcity > 0):
                indice = next((i for i, item in enumerate(items) if item[0] == Customer.fk_idcity), None)            
                selected_item_id = sty.overlaid_selectbox("City:", items, indice, x)
            else:
                selected_item_id = sty.overlaid_selectbox("City:", items,0, x)
                if selected_item_id: Customer.fk_idcity = selected_item_id[0]
            # --------------------------------------------------------------------------------
            Customer.phone = sty.overlaid_input("Phone", Customer.phone)
            if Customer.email == None:
                Customer.email =''
            Customer.email = sty.overlaid_input("Mail", Customer.email)

            # Selectbox identification -------------------------------------------------------
            items = idC.get_all_ids(1)
            x=format_func=lambda x: x[1]
            if (Customer.fk_ididentification is not None) and (Customer.fk_ididentification > 0):
                indice = next((i for i, item in enumerate(items) if item[0] == Customer.fk_ididentification), None)            
                selected_item_id = sty.overlaid_selectbox("Identification:", items, indice, x)
            else:
                selected_item_id = sty.overlaid_selectbox("Identification:", items,0, x)
            if selected_item_id: Customer.fk_ididentification = selected_item_id[0]

            # Selectbox company -------------------------------------------------------
            items = customerC.get_all_customers(1,1)
            x=format_func=lambda x: x[1]
            if (Customer.fk_idcustomer is not None) and (Customer.fk_idcustomer > 0):
                indice = next((i for i, item in enumerate(items) if item[0] == Customer.fk_idcustomer), None)            
                selected_item_id = sty.overlaid_selectbox("Company:", items, indice, x)
            else:
                selected_item_id = sty.overlaid_selectbox("Company:", items, 0, x)
            if selected_item_id: Customer.fk_idcustomer = selected_item_id[0]
            # --------------------------------------------------------------------------------

            cCb1, cCb2  = st.columns(2)
            with cCb1:
                Customer.active = st.checkbox("Active", False, key="bActive")
            with cCb2:    
                Customer.restriction = st.checkbox("Restriction", False, key="bRestriction")
                
        with pCol3:
            st.write('')

        with pCol4:
            # selectbox ClassCustomer---------------------------------------------------------
            items = classC.get_all_classes(1)
            x=format_func=lambda x: x[1]
            if (Customer.fk_idclasscustomer is not None) and (Customer.fk_idclasscustomer > 0):
                indice = next((i for i, item in enumerate(items) if item[0] == Customer.fk_idclasscustomer), None)            
                selected_item_id = sty.overlaid_selectbox("Class:", items, indice, x)
            else:
                selected_item_id = sty.overlaid_selectbox("Class:", items,0, x)
            if selected_item_id: Customer.fk_idclasscustomer = selected_item_id[0]
            # --------------------------------------------------------------------------------

            Customer.zipcode = sty.overlaid_input("Zipcode", Customer.zipcode)
            Customer.state = sty.overlaid_input("State", Customer.state)
            Customer.phone2 = sty.overlaid_input("Phone2", Customer.phone2)
            Customer.dtbirth = sty.overlaid_input("Birthday", Customer.dtbirth)
            Customer.numidentification = sty.overlaid_input("Num Identification", Customer.numidentification)
            Customer.comissionpercent = sty.overlaid_input("% Comission", Customer.comissionpercent)
        
        with pCol5:
            st.write('')

        with pCol6:

            # selectbox countryCustomer---------------------------------------------------------
            items = countryC.get_all_country(1)
            x = format_func = lambda x: x[1]
            if (Customer.fk_idcountry is not None) and (Customer.fk_idcountry > 0):
                indice = next((i for i, item in enumerate(items)
                              if item[0] == Customer.fk_idcountry), None)
                selected_item_id = sty.overlaid_selectbox(
                    "Country:", items, indice, x)
            else:
                selected_item_id = sty.overlaid_selectbox(
                    "Country:", items, 0, x)
            if selected_item_id:
                Customer.fk_idcountry = selected_item_id[0]
            # --------------------------------------------------------------------------------

            Customer.attention = sty.overlaid_area("Obs:", Customer.attention)

            img_path = 'customer_pic/'
            img_name = ''

            cPhoto1, cPhoto2, cPhoto3 = st.columns([1.5,4,1])
            with cPhoto1:
                st.write('')
            with cPhoto2:
                if (Customer.picture_path != 'picture path...' and os.path.exists(Customer.picture_path)):
                    parts = Customer.picture_path.split("/")
                    img_name = parts[1]
                    img_pasta = parts[0]
                    save_path = os.path.join(img_pasta, img_name)
                    st.image(save_path, width=300)
            with cPhoto3:
                st.write('')

            uploaded_image = st.file_uploader("Upload picture", type=["jpg", "jpeg", "png"])
            if uploaded_image is not None:
                img_name = os.path.basename(uploaded_image.name)
                if not os.path.exists(img_path):
                    os.makedirs(img_path)
                save_path = os.path.join(img_path, img_name)

                with open(save_path, "wb") as f:
                    f.write(uploaded_image.read())
                Customer.picture_path = save_path

        with pCol7:
            st.write('')
        col1, col2, col3, col4  = st.columns([.8,.8,1,7])
        with col1:
            if st.button("Save"):
                customerC.update_customer(Customer)
                items = customerC.get_all_customers(0,0)
                st.success("Saved!")
                rerun_script()
        with col2:
            # Botão para excluir o item
            if st.button("Delete", key="dCcustomer"):
                customerC.delete_item(i_id)
                st.success("Deleted!")
        with col3:
            if st.button("Update", key="uCustomer"):
                items = customerC.get_all_customers(0,0)
                st.success("Updated!")

    else:
        selected_item_id=None
        add_new_customer()                                
