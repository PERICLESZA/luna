import streamlit as st
import Models.exchange as Exchange
import Models.bank as Bank
import Models.customer as Customer
import Controllers.exchangeController as exchangeC
import Controllers.customerController as customerC
import Controllers.bankController as bankC
import Controllers.idController as idC
import Controllers.countryController as countryC
import Controllers.parameterController as parameterC
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
        newCustromer()
    else:        
        exchangeValues(items, i_id)
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

def exchangeValues(iCustomer,i_id):
    
    nPercComiss = float(parameterC.get_det_parameter()["exchange_comission"])
    calc_percvalue = 0
    conv_value = 0 
    
    with st.form(key='form1'):
        cEv1, cEv2, cEv3, cEv4, cEv5,cEv6,cEv7,cEv8,cEv9,cEv10,cEv11,cEv12 = st.columns([1.5,1,.6,.6,.7,.6,.7,.8,1,1,.7,1])
        with cEv1:
            x = format_func = lambda x: x[1]
            selected_item_id = sty.overlaid_selectbox("Company:", iCustomer, 0, x)
            if selected_item_id:
                Exchange.fk_idbankmaster = selected_item_id[0]
        with cEv2:
            Exchange.valuecashflow = sty.overlaid_number("Value", "%.2f")
        with cEv3:
            calc_cents1 = 0
            if Exchange.valuecashflow: 
                conv_value = Exchange.valuecashflow
                calc_cents1 = round(conv_value - int(conv_value),2)
            Exchange.centsflow = sty.overlaid_input("Cents 1", calc_cents1)
        with cEv4:
            Exchange.percentflow = sty.overlaid_input("%Comis", nPercComiss)
        with cEv5:
            if Exchange.valuecashflow: 
                calc_percvalue = abs(round(conv_value - (conv_value * (1 + nPercComiss / 100)), 2))
            Exchange.valuepercentflow = sty.overlaid_input(
                "% Value", calc_percvalue)
        with cEv6:
            calc_cents2 = (conv_value - calc_cents1) - calc_percvalue
            calc_cents2 = round(calc_cents2 - int(calc_cents2), 2)
            Exchange.cents2flow = sty.overlaid_input("Cents 2", calc_cents2)
        with cEv7:
            Exchange.wire = st.checkbox("Wire")
        with cEv8:
            calc_reciev = round(calc_cents1 + calc_cents2 + calc_percvalue,2)
            Exchange.totalflow = sty.overlaid_input("Recieve", calc_reciev)
        with cEv9:
            calc_pay = round(conv_value - calc_reciev,2)
            Exchange.totaltopay = sty.overlaid_input("Pay", calc_pay)
        with cEv10:
            Exchange.ok = st.checkbox("Ok")
        with cEv11:
            subtmit_button = st.form_submit_button(label='Save')

def newCustromer():
        with st.form(key='form1'):
            
            Customer.name = ''
            Customer.dtbirth = ''
            Customer.fk_idcountry = 0
            Customer.phone = ''
            
            cEv1, cEv2, cEv3, cEv4, cEv5, cEv6, cEv7 = st.columns([3,1.2,1.2,2,2,1,1])
            with cEv1:
                Customer.name = sty.overlaid_input("Nome", Customer.name)
            with cEv2:
                Customer.phone = sty.overlaid_input("Phone", Customer.phone)
            with cEv3:
                Customer.dtbirth = sty.overlaid_input("Birthday", Customer.dtbirth)                # x = format_func = lambda x: x[1]
            with cEv4:
                itCountry = countryC.get_all_country(1)
                x = format_func = lambda x: x[1]
                selected_item_id = sty.overlaid_selectbox(
                    "Country:", itCountry, 0, x)
                if selected_item_id:
                    Customer.fk_idcountry = selected_item_id[0]
            with cEv5:
                itId = idC.get_all_ids(1)
                x = format_func = lambda x: x[1]
                selected_item_id = sty.overlaid_selectbox(
                    "Id:", itId, 0, x)
                if selected_item_id:
                    Customer.fk_ididentification = selected_item_id[0]
            with cEv6:
                Customer.numidentification = sty.overlaid_input("Num Id", '')
            with cEv7:
                subtmit_button = st.form_submit_button(label='Save')
                if subtmit_button:
                    customerC.insert_customer(Customer)
                    st.success("Saved!")

        
