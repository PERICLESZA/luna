import streamlit as st
import Models.customer as Customer
import Controllers.customerController as customerC
import Controllers.cityController as cityC
import Controllers.idController as idC
import Controllers.classController as classC
from PIL import Image
import os
import Styles as sty
import subprocess

# def rerun_script():
#     subprocess.Popen(["python", "customer.py"])
#     st.experimental_rerun()
    
def adicionar_item():
    item_name = st.text_input("Name:")
    item_phone = st.text_input("Phone:")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Add"):
            if item_name:
                Customer.idCustomer = 0
                Customer.name = item_name
                Customer.phone = item_phone
                Customer.add_or_update_item(Customer)
                st.success("Added!")
                items = customerC.get_items()
            else:
                st.warning("Fill the filed City.")
    with col2:
        if st.button("Update", key="sCustomer"):
            items = customerC.get_items()
            st.success("Updated!")

def mainCustomer():
    pCol1, pCol2, pCol3  = st.columns(3)
    with pCol1:

        items = customerC.get_items(0)
        selected_i_id = st.selectbox("Select Customer:", items, format_func=lambda x: x[1])
        if selected_i_id:
            i_id = selected_i_id[0]
            
        st.write('')
        if i_id > 0:
            resetModel()
            # st.write(Customer)
            i_det = customerC.get_item_details(i_id)
            
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
            Customer.comissionpercent = i_det['comissionpercent'] if i_det['comissionpercent']!=None else '% comission...'
            Customer.restriction = i_det['restriction'] 
            Customer.attention = i_det['attention'] if i_det['attention']!=None else 'Observations...'
            Customer.picture_path = i_det['picture_path'] if i_det['picture_path']!=None else 'picture path...'
            Customer.name = sty.overlaid_input("Nome", Customer.name)
            Customer.andress = sty.overlaid_input("Address", Customer.andress)

            # selectbox city ------------------------------------------------------------------
            items = cityC.get_items(1)
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
            items = idC.get_items(1)
            ident_mapping = {ident[1]: ident[0] for ident in items if ident[1][0] != ""}
            # if (Customer.fk_ididentification is not None) and (Customer.fk_ididentification > 0):
            #     identName = idC.get_item_details(Customer.fk_ididentification)
            #     Customer.fk_ididentification =  sty.overlaid_selectbox("Identification", [item[1] for item in items], index=items.index(identName))
            # else:
            #     identName = sty.overlaid_selectbox("Identification", list(ident_mapping.keys()),0)                                
            #     Customer.fk_ididentification = ident_mapping.get(identName)
            # Selectbox company -------------------------------------------------------
            items = customerC.get_items(1)
            companyName=''
            # if (Customer.fk_idcustomer is not None) and (Customer.fk_idcustomer > 0):
            #     companyName = idC.get_item_details(Customer.fk_idcustomer)
            #     Customer.fk_idcustomer =  sty.overlaid_selectbox("Company", [item[1] for item in items], index=items.index(companyName))
            # else:
            #     Customer.fk_idcustomer =  sty.overlaid_selectbox("Company", [item[1] for item in items],0)
            # --------------------------------------------------------------------------------
            
            # Botão para salvar as alterações ou adicionar um novo item

            col1, col2, col3, col4 = st.columns([.8,1,1,.8])
            with col1:
                if st.button("Save"):
                    # customerC.add_or_update_item(Customer)
                    customerC.update_customer(Customer)
                    items = customerC.get_items(0)
                    # # rerun_script()
                    st.success("Saved!")
            with col2:
                # Botão para excluir o item
                if st.button("Delete", key="dCcustomer"):
                    customerC.delete_item(i_id)
                    st.success("Deleted!")
            with col3:
                if st.button("Update", key="uCustomer"):
                    items = customerC.get_items()
                    st.success("Updated!")
            # with col4:
            with col4:
                if st.button("New", key="nCustomer"):
                   selected_item_id=None
        else:
            # Adicionar um novo item
            adicionar_item()
            
    with pCol2:
        st.write(''); st.write('')
        cCb1, cCb2  = st.columns(2)
        with cCb1:
            Customer.active = st.checkbox("Active", False, key=None)
        with cCb2:    
            Customer.restriction = st.checkbox("Restriction", False, key=None)
        st.write('')
        st.write('')
        # selectbox ClassCustomer---------------------------------------------------------
        # items = classC.get_items(1)
        # className=''
        # if (Customer.fk_idclasscustomer is not None) and (Customer.fk_idclasscustomer > 0):
        #     className = classC.get_item_details(Customer.fk_idclasscustomer)
        #     Customer.fk_idclasscustomer = sty.overlaid_selectbox("Class", [item[1] for item in items], index=items.index(className))
        # else:
        #     Customer.fk_idclasscustomer = sty.overlaid_selectbox("Class", [item[1] for item in items],0)
        # --------------------------------------------------------------------------------
        Customer.zipcode = sty.overlaid_input("Zipcode", Customer.zipcode)
        Customer.state = sty.overlaid_input("State", Customer.state)
        Customer.phone2 = sty.overlaid_input("State", Customer.phone2)
        Customer.dtbirth = sty.overlaid_input("Birthday", Customer.dtbirth)
        Customer.numidentification = sty.overlaid_input("Num Identification", Customer.numidentification)
        Customer.comissionpercent = sty.overlaid_number("% Comission", Customer.comissionpercent)
    
    with pCol3:
        st.write(''); st.write('')

        Customer.attention = sty.overlaid_input("Obs:", Customer.attention)
        Customer.picture_path = sty.overlaid_input("Picture Path:", Customer.picture_path)

        img_path ='customer_pic/'    
        img_name = ''
        
        if (Customer.picture_path != 'picture path...' ):
            parts = Customer.picture_path.split("/")
            img_name = parts[1]
        # else:    
        uploaded_image = st.file_uploader("Upload picture", type=["jpg", "jpeg", "png"])
        if uploaded_image is not None:
            img_name = os.path.basename(uploaded_image.name)
            if uploaded_image is not None:
                if not os.path.exists(img_path):
                    os.makedirs(img_path)
        
        if (os.path.exists(img_path) and img_name!="") or Customer.picture_path=='':
            save_path = os.path.join(img_path,img_name)
            st.image(save_path, width=300)

           
    # Customer.idcustomer = i_det['idcustomer']
    
    
def resetModel():
    Customer.idcustomer =''
    Customer.name=''
    Customer.phone='' 
    Customer.andress='' 
    Customer.fk_idcity=0 
    Customer.email=''
    Customer.fk_ididentification=0
    Customer.fk_idcustomer=0
    Customer.active=False
    Customer.fk_idclasscustomer=0
    Customer.zipcode=''
    Customer.state=''
    Customer.phone2=''
    Customer.dtbirth=''
    Customer.numidentification=''
    Customer.comissionpercent=0.00
    Customer.restriction=False
    Customer.attention=False
    Customer.picture_path=''
