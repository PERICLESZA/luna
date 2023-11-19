import streamlit as st
import Models.exchange as Exchange
import Models.bank as Bank
import Controllers.exchangeController as exchangeC
import Controllers.customerController as customerC
import Controllers.cityController as cityC
import Controllers.bankController as bankC
import Controllers.idController as idC
import Controllers.classController as classC
import os
import Styles as sty
import subprocess
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import Styles as sty


def mainExchange():

    i_id = 0
    items = customerC.get_all_customers(0, 0)
    selected_i_id = st.selectbox(
        "Phone No./Name", items, format_func=lambda x: x[1])
    st.write('')
    if selected_i_id:
        i_id = selected_i_id[0]

    if i_id==0:
        st.write('novo')
    else:        
        exchangeValues(items)
        tab_cashflow(i_id)

def rerun_script():
    subprocess.Popen(["python", "exchange.py"])
    st.experimental_rerun()

def add_new_exchange():

    pnCol1, pnCol2, pnCol3, pnCol4, pnCol5, pnCol6, pnCol7 = st.columns([
                                                                        1, 1, 1, 1, 1, 1, 1])
    with pnCol1:
        # Usuário insere os detalhes do novo cliente
        items = customerC.get_all_customers(1, 1)
        def x(x): return x[1]
        sel_item_id = sty.overlaid_selectbox('Company', items, 0, x)
        if sel_item_id:
            Exchange.fk_idcustomer = sel_item_id[0]

        items = bankC.get_all_bank(1)
        def x(x): return x[1]
        sel_item_id = sty.overlaid_selectbox('Bank', items, 0, x)
        if sel_item_id:
            Bank.fk_idcustomer = sel_item_id[0]

    with pnCol2:
        Exchange.dtcashflow = sty.overlaid_input("Date", '')
    with pnCol3:
        Exchange.tcashflow = sty.overlaid_input("Time", '')


def tab_cashflow(i_id):

    cashflow_data = exchangeC.get_cashflow(i_id)
    
    df = pd.DataFrame(cashflow_data, columns=[
        'Date',
        'Time',
        'Check',
        'Value',
        'Cents1',
        '% Comiss',
        'Comiss',
        'Cents2',
        'Wire',
        'Reciev',
        'Pay',
        'Status'
    ])
    
    nTValue = format(sum(df.Value), "000,.2f")
    nTCents1 = format(sum(df.Cents1), "000,.2f")
    nTCents2 = format(sum(df.Cents2), "000,.2f")
    nTComiss = format(sum(df.Comiss), "000,.2f")
    nTReciev = format(sum(df.Reciev), "000,.2f")
    
    df['Value'] = df['Value'].apply(lambda x: format(round(x, 2), ".2f"))
    df['Cents1'] = df['Cents1'].apply(lambda x: format(round(x, 2), ".2f"))
    df['% Comiss'] = df['% Comiss'].apply(lambda x: format(round(x, 2), ".2f"))
    df['Comiss'] = df['Comiss'].apply(lambda x: format(round(x, 2), ".2f"))
    df['Cents2'] = df['Cents2'].apply(lambda x: format(round(x, 2), ".2f"))
    df['Reciev'] = df['Reciev'].apply(lambda x: format(round(x, 2), ".2f"))
    df['Pay'] = df['Pay'].apply(lambda x: format(round(x, 2), ".2f"))

    # Selectbox company -------------------------------------------------------
    # items = tuple(customerC.get_all_customers(1,1))
    items = (1,2,3,4,5)
    # x=format_func=lambda x: x[1]
    # if (Exchange.fk_idcustomer is not None) and (Exchange.fk_idcustomer > 0):
    #     indice = next((i for i, item in enumerate(items)
    #                   if item[0] == Exchange.fk_idcustomer), None)
    #     selected_item_id = sty.overlaid_selectbox("Company:", items, indice, x)
    # else:
    #     selected_item_id = sty.overlaid_selectbox("Company:", items, 0, x)
    # if selected_item_id:
    #     Exchange.fk_idcustomer = selected_item_id[0]
    # --------------------------------------------------------------------------------


    gd = GridOptionsBuilder.from_dataframe(df)
    gd.configure_pagination(enabled=True, paginationAutoPageSize=10)
    # gd.configure_default_column(editable=True, groupable=True)
    gd.configure_selection(selection_mode="multiple", use_checkbox=True)
    
    # sel_mode = st.radio('Selection Type', options=['single', 'multiple'])
    # gd.configure_selection(selection_mode=sel_mode, use_checkbox=True)
    
    cellstyle_jscode = None
    
    cellstyle_jscode = JsCode("""
        function(params) {
            if (params.data['Status'] > '0') {
                return {
                    'color': 'Black',
                    'backgroundColor': '#DDC17E'
                }
            }
        };
    """)
    
    # gd.configure_columns(df, cellStyle=cellstyle_jscode)
    # gd.configure_column('Company', editable=True, cellEditor='agSelectCellEditor',
    #                     cellEditorParams={'values': items})

    # gd.configure_column('Bank', editable=True, cellEditor='agSelectCellEditor',
    #                     cellEditorParams={'values': iBank})
    
    gridoptions = gd.build()

    grid_table = AgGrid(df, gridOptions=gridoptions,
                    enable_enterprise_modules=True,
                    fit_columns_on_grid_load=True,
                    height=400,
                    width='100%',
                    update_mode=GridUpdateMode.SELECTION_CHANGED,
                    reload_data=True,
                    allow_unsafe_jscode=True,
                    )
    
    sel_row = grid_table["selected_rows"]
    #st.write(sel_row)
    
    # totalização da lista de valores
    #-------------------------------------------------------------------------------------------
    tc1, tc2, tc3, tc4, tc5, tc6, tc7, tc8, tc9, tc10, tc11, tc12, tc13, tc14 = st.columns(14)
    with tc5:
        cleaned_value = nTValue.replace(',', '')
        if (float(cleaned_value) > 0):
            st.write('Total:')
            
    with tc6:
        cleaned_value = nTValue.replace(',', '')
        if (float(cleaned_value)>0):st.text(nTValue)
    with tc7:
        cleaned_value = nTCents1.replace(',', '')
        if (float(nTCents1) > 0):
            st.text(cleaned_value)
    with tc9:
        cleaned_value = nTComiss.replace(',', '')
        if (float(nTComiss) > 0):
            st.text(cleaned_value)
    with tc10:
        cleaned_value = nTCents2.replace(',', '')
        if (float(nTCents2)>0):st.text(cleaned_value)
    with tc12:
        cleaned_value = nTReciev.replace(',', '')
        if (float(nTReciev) > 0):
            st.text(cleaned_value)

def exchangeValues(iCustomer):
    with st.form(key='form1'):
        cEv1, cEv2, cEv3, cEv4, cEv5,cEv6,cEv7,cEv8,cEv9,cEv10,cEv11,cEv12 = st.columns([1.5,1,.6,.6,.7,.6,.7,.8,1,1,.7,1])
        with cEv1:
            x = format_func = lambda x: x[1]
            selected_item_id = sty.overlaid_selectbox("Company:", iCustomer, 0, x)
            if selected_item_id:
                Exchange.fk_idbankmaster = selected_item_id[0]
        with cEv2:
            Exchange.valuecashflow = sty.overlaid_input("Value", '')
        with cEv3:
            Exchange.centsflow = sty.overlaid_input("Cents 1", '')
        with cEv4:
            Exchange.percentflow = sty.overlaid_input("%Comis", '')
        with cEv5:
            Exchange.valuepercentflow = sty.overlaid_input("% Value", '')
        with cEv6:
            Exchange.cents2flow = sty.overlaid_input("Cents 2", '')
        with cEv7:
            Exchange.wire = st.checkbox("Wire")
        with cEv8:
            Exchange.totalflow = sty.overlaid_input("Recieve", '')
        with cEv9:
            Exchange.totaltopay = sty.overlaid_input("Pay", '')
        with cEv10:
            Exchange.ok = st.checkbox("Ok")
        with cEv11:
            subtmit_button = st.form_submit_button(label='Save')


