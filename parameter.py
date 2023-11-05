import streamlit as st
import Models.customer as Customer
import Models.parameter as Parameter
import Controllers.parameterController as parameterC
import Controllers.customerController as customerC
import os
import Styles as sty
import subprocess

def rerun_script():
    subprocess.Popen(["python", "parameter.py"])
    st.experimental_rerun()

def adicionar_item():
    item_client = st.text_input("Name:")
    item_exchange_vl_month = st.number_input("Vlr month:")
    item_exchange_vl_year  = st.number_input("Vlr year:")
    item_exchange_vl_wire  = st.number_input("Vlr wire:")
    item_exchange_vl_comission  = st.number_input("Vlr comission:")
    item_fk_idclient = st.selectbox("Company:", customerC.get_all_customers(1, 1), format_func=lambda x: x[1])

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Add"):
            
            if item_client:
                new_parameter = Customer.Customer()
                new_parameter.client = item_client
                new_parameter.exchange_vl_month = item_exchange_vl_month
                new_parameter.exchange_vl_year = item_exchange_vl_year
                new_parameter.exchange_vl_wire = item_exchange_vl_wire
                new_parameter.exchange_vl_comission = item_exchange_vl_comission
                new_parameter.fk_idclient = item_fk_idclient[0]
                
                parameterC.add_parameter(new_parameter)
                st.success("Parameter added!")

                st.success("Added!")
                items = parameterC.get_items()
            else:
                st.warning("Fill the filed Parameter.")
    with col2:
        if st.button("Update", key="sParameter"):
            items = parameterC.get_items()
            st.success("Updated!")

def mainParameter():

    pCol1, pCol2,pCol3 = st.columns([1,1,1])
    with pCol1:
        i_det = parameterC.get_det_parameter()
        
        Parameter.client = i_det['client'] if i_det['client']!=None else 'client...'
        Parameter.exchange_vl_month = i_det['exchange_vl_month']  
        Parameter.exchange_vl_year = i_det['exchange_vl_year']
        Parameter.exchange_vl_wire = i_det['exchange_vl_wire']
        Parameter.exchange_comission = i_det['exchange_comission']
        Parameter.fk_idclient = i_det['fk_idclient']

        # selectbox city ------------------------------------------------------------------
        Parameter.client = sty.overlaid_input("Empresa", Parameter.client)
        Parameter.exchange_vl_month = sty.overlaid_input("Vlr Month", Parameter.exchange_vl_month)
        Parameter.exchange_vl_year = sty.overlaid_input("Vlr Year", Parameter.exchange_vl_year)
        Parameter.exchange_vl_wire = sty.overlaid_input("Vlr Wire", Parameter.exchange_vl_wire)
        Parameter.exchange_comission = sty.overlaid_input("% Comission", Parameter.exchange_comission)

        # Selectbox company -------------------------------------------------------
        items = customerC.get_all_customers(1,1)
        x=format_func=lambda x: x[1]
        if (Parameter.fk_idclient is not None) and (Parameter.fk_idclient > 0):
            indice = next((i for i, item in enumerate(items) if item[0] == Parameter.fk_idclient), None)            
            selected_item_id = sty.overlaid_selectbox("Client:", items, indice, x)
        else:
            selected_item_id = sty.overlaid_selectbox("Client:", items, 0, x)
        if selected_item_id: Parameter.fk_idclient = selected_item_id[0]
            
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Save"):
                parameterC.update_parameter(Parameter)
                items = parameterC.get_det_parameter()
                st.success("Saved!")
                rerun_script()
        with col2:
            if st.button("Update", key="uCustomer"):
                items = parameterC.get_det_parameter()
                st.success("Updated!")
