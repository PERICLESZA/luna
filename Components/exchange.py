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
import Controllers.percentcheckController as percentC
import Controllers.loginController as loginC
import Controllers.statusController as statusC
import Styles as sty
import subprocess
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode, JsCode, ColumnsAutoSizeMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from datetime import date, datetime
import Styles as sty

def mainExchange():
    if (st.session_state.sStore == None):
        st.warning("Unregistered computer. Ask the administrator to register the computer!!!")
    else:
        i_id = 0
        i_idEx = 0
        
        cEx1, cEx2 = st.columns(2)
        with cEx1:
            i_customer = customerC.get_all_customers(0, 0)
            selected_i_id = st.selectbox(
                "Phone No./Name", i_customer, format_func=lambda x: x[1])
            if selected_i_id: i_id = selected_i_id[0]
        with cEx2:
            if i_id:
                i_exchange = exchangeC.get_cashflow(i_id,'idstatus')
                i_exchange.append([0, '<<New>>','','',0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00])
                i_exchange.sort(key=lambda x: x[0])
                x = format_func = lambda x: x[1] + ' ' + x[2] + " " + str(x[4])
                sel_i_idEx = st.selectbox("Select Check to edit", i_exchange, 0, x)
                if sel_i_idEx: i_id_Ex = sel_i_idEx[0]
        if i_id == 0:
            newCustromer()
        else:
            exchangeValues(i_customer, i_id, sel_i_idEx)
            tab_cashflow(i_customer, i_id)

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
        Exchange.dtcashflow = sty.overlaid_input("Date", '', False)
    with pnCol3:
        Exchange.tcashflow = sty.overlaid_input("Time", '', False)

def tab_cashflow(iCustomer, i_id):
  
    edit_disable = False
    if st.session_state.perfil == 'A':
        edit_disable = True

    cashflow_data = exchangeC.get_cashflow(i_id,None)

    df = pd.DataFrame(cashflow_data, columns=[
        'Id',
        'Date',
        'Time',
        'Check',
        'Value',
        'Cents1',
        'pComiss',
        'Comiss',
        'Cents2',
        'Wire',
        'Reciev',
        'Pay',
        'Status',
        'Store',
    ])

    total_row = pd.DataFrame({
        # 'Date':   [''],
        # 'Time':   [''],
        'Check':   ['Total'],
        'Value':   [format(df['Value'].sum(), ",.2f")],
        'Cents1':  [format(df['Cents1'].sum(), ",.2f")],
        'pComiss': [format(0.00, ",.2f")],
        'Comiss':  [format(df['Comiss'].sum(),",.2f")],
        'Cents2':  [format(df['Cents2'].sum(),",.2f")],
        'Wire':    [format(df['Wire'].sum(),",.2f")],
        'Reciev':  [format(df['Reciev'].sum(),",.2f")],
        'Pay':     [format(df['Pay'].sum(),",.2f")],
        # 'Status': ['']
    })
    # st.write(total_row)
    # column_widths = {'Date': .8, 'Time': 1, 'Check': 1, 'Value':1,'Cents1':1,'% Comiss':1,'Comiss':1,'Cents2':1,'Wire':1,'Reciev':1,'Pay':1,'Status':1}

    df['Value']   = df['Value'].apply(lambda x: format(round(x, 2), ".2f"))
    df['Cents1']  = df['Cents1'].apply(lambda x: format(round(x, 2), ".2f"))
    df['pComiss'] = df['pComiss'].apply(lambda x: format(round(x, 2), ".2f"))
    df['Comiss']  = df['Comiss'].apply(lambda x: format(round(x, 2), ".2f"))
    df['Cents2']  = df['Cents2'].apply(lambda x: format(round(x, 2), ".2f"))
    df['Wire']    = df['Wire'].apply(lambda x: format(round(x, 2), ".2f"))
    df['Reciev']  = df['Reciev'].apply(lambda x: format(round(x, 2), ".2f"))
    df['Pay']     = df['Pay'].apply(lambda x: format(round(x, 2), ".2f"))
    
    # df = pd.concat([df, total_row])

    # styled_df = df.style.applymap(highlight_totalRow)

    gd = GridOptionsBuilder.from_dataframe(df)
    gd.configure_selection(selection_mode="single")
    gd.configure_default_column(editable=edit_disable)
    
    # gd.configure_pagination(enabled=True)
    # sel_mode = st.radio('Selection Type', options=['single', 'multiple'])
    # gd.configure_selection(selection_mode=sel_mode, use_checkbox=True)

    cellstyle_jscode = None
    cellstyle_jscode = JsCode("""
        function(params) {
            if (params.data['Status'] != 'ok') {
                return {
                    'color': 'Black',
                    'backgroundColor': '#DDC17E'
                    
                }
            }
            if (params.data['Check'] == 'Total') {
                return {
                    'color': 'Black',
                    'backgroundColor': '#66CCFF'
                }
            }
        };
    """)
    # js_value   = JsCode("""
    #     function (params) {
    #         var value = params.data.Value; 
    #         return value.toLocaleString(undefined,
    #         {minimumFractionDigits: 2, maximumFractionDigits: 2});
    #         }
    #     """)
    # js_pComiss = JsCode("""
    #     function (params) {
    #         var pComiss = params.data.pComiss; 
    #         return pComiss.toLocaleString(undefined,
    #         {minimumFractionDigits: 2, maximumFractionDigits: 2});
    #         }
    #     """)
    # # js_cents1  = JsCode("""
    # #     function (params) {
    # #         var value = params.data.Value; 
    # #         var cents1 = (value % 1);
    # #         return cents1.toLocaleString('en-us',
    # #         {minimumFractionDigits: 2, maximumFractionDigits: 2});
    # #         }
    # #     """)
    # js_comiss  = JsCode("""
    #     function (params) {
    #         var value = params.data.Value - params.data.Cents1;
    #         var pcomiss = params.data.pComiss;
    #         return ((value * pcomiss)/100).toLocaleString(undefined, 
    #         {minimumFractionDigits: 2, maximumFractionDigits: 2});
    #         }
    #     """)
    # js_cents2  = JsCode("""
    #     function (params) {
    #         var value = params.data.Value - params.data.Cents1;
    #         var pcomiss = params.data.pComiss;
    #         var numero = ((value * pcomiss)/100);
    #         var cents2 = numero % 1;
    #         return cents2.toLocaleString(undefined,
    #         {minimumFractionDigits: 2, maximumFractionDigits: 2});
    #         }
    #     """)
    # js_wire    = JsCode("""
    #     function (params) {
    #         var wire = params.data.Wire; 
    #         return wire.toLocaleString(undefined,
    #         {minimumFractionDigits: 2, maximumFractionDigits: 2});
    #         }
    #     """)
    # js_reciev  = JsCode("""
    #     function (params) {
    #         var reciev = params.data.Reciev; 
    #         return reciev.toLocaleString(undefined,
    #         {minimumFractionDigits: 2, maximumFractionDigits: 2});
    #         }
    #     """)
    # js_pay     = JsCode("""
    #     function (params) {
    #         var pay = params.data.Pay; 
    #         return pay.toLocaleString(undefined,
    #         {minimumFractionDigits: 2, maximumFractionDigits: 2});
    #         }
    #     """)

    # gd.configure_column("Value", header_name='Value',
    #                     type=["numericColumn","numberColumnFilter"], 
    #                     cellstyle={'text-align': "left"},
    #                     editable=False,
    #                     valueGetter=js_value) 
    # gd.configure_column("pComiss", header_name='pComiss',
    #                     type=["numericColumn","numberColumnFilter"], 
    #                     cellstyle={'text-align': "left"},
    #                     editable=False,
    #                     valueGetter=js_pComiss) 
    # # gd.configure_column("Cents1", header_name='Cents1',
    # #                     type=["numericColumn","numberColumnFilter"], 
    # #                     cellstyle={'text-align': "left"},
    # #                     editable=False,
    # #                     valueGetter=js_cents1) 
    # gd.configure_column("Comiss", header_name='Comiss',
    #                     type=["numericColumn", "numberColumnFilter"],
    #                     editable=False,
    #                     valueGetter=js_comiss)  
    # gd.configure_column("Cents2", header_name='Cents2',
    #                     type=["numericColumn","numberColumnFilter"], 
    #                     cellstyle = {'text-align':"left"},
    #                     editable=False, 
    #                     valueGetter=js_cents2) 
    # gd.configure_column("Wire", header_name='Wire',
    #                     type=["numericColumn","numberColumnFilter"], 
    #                     cellstyle = {'text-align':"left"},
    #                     editable=False, 
    #                     valueGetter=js_wire) 
    # gd.configure_column("Reciev", header_name='Reciev',
    #                     type=["numericColumn","numberColumnFilter"], 
    #                     cellstyle = {'text-align':"left"},
    #                     editable=False, 
    #                     valueGetter=js_reciev) 
    # gd.configure_column("Pay", header_name='Pay',
    #                     type=["numericColumn","numberColumnFilter"], 
    #                     cellstyle = {'text-align':"left"},
    #                     editable=False, 
    #                     valueGetter=js_pay) 

    # cell_button_add = JsCode('''
    # class BtnAddCellRenderer {
    #     init(params) {
    #         this.params = params;
    #         this.eGui = document.createElement('div');
    #         this.eGui.innerHTML = `
    #          <span>
    #             <style>
    #             .btn_add {
    #               background-color: limegreen;
    #               border: none;
    #               color: white;
    #               text-align: center;
    #               text-decoration: none;
    #               display: inline-block;
    #               font-size: 10px;
    #               font-weight: bold;
    #               height: 2.5em;
    #               width: 3em;
    #               cursor: pointer;
    #             }

    #             .btn_add :hover {
    #               background-color: #05d588;
    #             }
    #             </style>
    #             <button id='click-button' 
    #                 class="btn_add" 
    #                 >Add</button>
    #          </span>
    #       `;
    #     }

    #     getGui() {
    #         return this.eGui;
    #     }

    # };
    # ''')
    # cell_button_delete = JsCode('''
    # class BtnCellRenderer {
    #     init(params) {
    #         console.log(params.api.getSelectedRows());
    #         this.params = params;
    #         this.eGui = document.createElement('div');
    #         this.eGui.innerHTML = `
    #          <span>
    #             <style>
    #             .btn {
    #               background-color: #F94721;
    #               border: none;
    #               color: white;
    #               font-size: 10px;
    #               font-weight: bold;
    #               height: 2.5em;
    #               width: 3em;
    #               cursor: pointer;
    #             }

    #             .btn:hover {
    #               background-color: #FB6747;
    #             }
    #             </style>
    #             <button id='click-button'
    #                 class="btn"
    #                 >X</button>
    #          </span>
    #       `;
    #     }

    #     getGui() {
    #         return this.eGui;
    #     }

    # };
    # ''')
   
    # string_to_delete = "\n\n function(e) { \n \
        # let api = e.api; \n \
        # let sel = api.getSelectedRows(); \n \
        # api.applyTransaction({remove: sel}); \n \
        #     }; \n \n"
            
    # string_to_add_row = "\n\n function(e) { \n \
    #     let api = e.api; \n \
    #     let rowIndex = e.rowIndex + 1; \n \
    #     api.applyTransaction({addIndex: rowIndex, add: [{}]}); \n \
    #         }; \n \n"
            
    gd.configure_columns(df, cellStyle=cellstyle_jscode)
    
    # gd.configure_column('X', headerTooltip='Click on Button to remove row',
                                    # editable=False, filter=False, onCellClicked=JsCode(string_to_delete),
                                    # cellRenderer=cell_button_delete,
                                    # autoHeight=True, suppressMovable='true')    
    
    gridoptions = gd.build()

    grid_table = AgGrid(
                        df, gridOptions=gridoptions,
                        enable_enterprise_modules=True,
                        fit_columns_on_grid_load=True,
                        height=300,
                        width='50%',
                        GridUpdateMode=GridUpdateMode.SELECTION_CHANGED,
                        reload_data=True,
                        allow_unsafe_jscode=True,
                        )

    sel_row = grid_table["selected_rows"]
    st.write(total_row)

    # grid_table["selected_rows"][0]['Comiss']=10*10
    # st.write(grid_table["selected_rows"][0]['Wire'])
    # sel_row[0]["wire"] =  10*2
    # sel_row = grid_table["selected_rows"]

    # cBt1, cBt2, cBt3,cBt4, cBt5 = st.columns([.6,.6,2,2,.1])
    
    # editar o check num form abaixo da tabela    --------------------
    if (sel_row):
       if sel_row[0]['Check'] != "Total":
           delExchange(sel_row)
        #   editExchangeValues(iCustomer, i_id, sel_row, gd) 
    #-----------------------------------------------------------------
        # with cBt1:
        #     if st.button("Salvar", disabled=not edit_disable):
        #         st.write('Salvar')
        #         st.write(sel_row[0]["Date"])
        #         st.write(sel_row[0]["Value"])
        # with cBt2:
        #     if st.button("Editar", disabled=not edit_disable):
        #         st.write('Editar')
        # with cBt3:
        #     if st.button("Excluir", disabled=not edit_disable):
        #         st.write('Excluir')
        # with cBt4:
        #     total_row.set_index('', inplace=True)
        #     st.write(total_row)

        # if sel_row:
        #     # st.write(sel_row)
            # exchangeC.update_exchange(sel_row)
        #     #editExchangeValues(iCustomer, i_id, gsenha, sel_row)

def exchangeValues(iCustomer, i_id, sel_Exchange):

    if st.session_state.perfil == 'A':
        wire_disable = False
        comis_disable = False
    else:
        wire_disable = True
        comis_disable = False
    if sel_Exchange[1] != '<<New>>':
        Exchange.idcashflow = sel_Exchange[0]
        Exchange.dtcashflow = datetime.strptime(sel_Exchange[1], '%Y/%m/%d')
        Exchange.tchaflow = datetime.strptime(sel_Exchange[2], '%H:%M')
        Exchange.fk_idcustomer = i_id
        Exchange.valueflow = sel_Exchange[4]
        Exchange.valuewire = sel_Exchange[9]
        Exchange.valuepercentflow = 0.00
        Exchange.totaltopay = 0.00
        Exchange.totalflow = 0.00
        Exchange.centsflow = 0.00
        Exchange.percentflow = 0.00
        st.write(sel_Exchange[14])
        Exchange.fk_idstatus = sel_Exchange[14]
    else:
        # st.write(nPercentCheck)
        Exchange.idcashflow=0
                                     
        new_dt = datetime.now().date()
        new_tm = datetime.now().time()
        Exchange.dtcashflow = new_dt
        Exchange.tchaflow = new_tm
        Exchange.fk_idcustomer = i_id
        Exchange.valueflow = 0.00
        Exchange.valuewire = 0.00
        Exchange.valuepercentflow = 0.00
        Exchange.totaltopay = 0.00
        Exchange.totalflow = 0.00
        Exchange.centsflow = 0.00
        Exchange.percentflow = 0.00
        Exchange.fk_idstore = st.session_state.idstore
        Exchange.fk_idstatus = 3
        
    with st.form(key='form1'):
        cEv1, cEv2, cEv3, cEv4, cEv5, cEv6, cEv7, cEv8, cEv9, cEv10, cEv11, cEv12, cEv13 = st.columns(
            [1.04, 1.1, 2, 1, .7, .7, .8, .8, 1, 1, 1, 1.3, 1])
        with cEv1:  #date
            Exchange.dtcashflow = sty.overlaid_date("Date", Exchange.dtcashflow)
        with cEv2:  #time
            Exchange.tchaflow = sty.overlaid_time("Time", Exchange.tchaflow)
        with cEv3:  #company
            x = format_func = lambda x: x[1]
            selected_item_id = sty.overlaid_selectbox(
                "Company:", iCustomer, 0, x)
            if selected_item_id:
                Exchange.fk_idbankmaster = selected_item_id[0]
        with cEv4:  #valueflow
            Exchange.valueflow = sty.overlaid_number(
                "Value", Exchange.valueflow, "%.2f", False)
        with cEv5:  #cents1
            if Exchange.valueflow:
                Exchange.centsflow = Exchange.valueflow - \
                    int(Exchange.valueflow)
            Exchange.centsflow = sty.overlaid_number(
                "Cents 1", Exchange.centsflow, "%.2f", True)
        with cEv6:  #percentflow
            # st.write(findComiss(Exchange.valueflow))
            Exchange.percentflow = float(findComiss(Exchange.valueflow))
            if Exchange.valueflow > 0.00 and Exchange.valueflow <= 200:
                Exchange.valuepercentflow = Exchange.percentflow
                Exchange.percentflow = sty.overlaid_number(
                    "pComis", 0.00, "%.2f", comis_disable
                )
            else:
                Exchange.percentflow = sty.overlaid_number(
                    "pComis", Exchange.percentflow, "%.2f", comis_disable)
        with cEv7:  # %value
            if Exchange.percentflow > 0.00:
                Exchange.valuepercentflow = abs(round(
                    Exchange.valueflow - (Exchange.valueflow * (1.00 + Exchange.percentflow / 100)), 2))

            Exchange.valuepercentflow = sty.overlaid_number(
                "%Value", Exchange.valuepercentflow, "%.2f", True)
        with cEv8:  # cents2
            Exchange.cents2flow = (
                Exchange.valueflow - Exchange.centsflow) - Exchange.valuepercentflow
            Exchange.cents2flow = round(
                Exchange.cents2flow - int(Exchange.cents2flow), 2)
            Exchange.cents2flow = sty.overlaid_number(
                "Cents 2", Exchange.cents2flow, "%.2f", True)
        with cEv9:  # valueWire
            Exchange.valuewire = sty.overlaid_number("Wire", Exchange.valuewire, "%.2f", wire_disable)
        with cEv10: # recieve
            Exchange.totalflow = round(
                Exchange.centsflow + Exchange.cents2flow + Exchange.valuepercentflow + Exchange.valuewire, 2)
            Exchange.totalflow = sty.overlaid_number(
                "Recieve", Exchange.totalflow, "%.2f", True)
        with cEv11: # totaltopay
            Exchange.totaltopay = Exchange.valueflow - Exchange.totalflow
            Exchange.totaltopay = sty.overlaid_number(
                "Pay", Exchange.totaltopay, "%.2f", True)
        # with cEv12: #ok 
        #     Exchange.cashflowok = st.checkbox("Ok")
        with cEv12: #status
            i_status = statusC.get_all_status(2)
            x = format_func = lambda x: x[1]
            indice = next((i for i, item in enumerate(i_status) if item[0] == Exchange.fk_idstatus), None)            
            selected_item_id = sty.overlaid_selectbox("Status:", i_status, indice, x)
            if selected_item_id:
                Exchange.fk_idstatus = selected_item_id[0]
        with cEv13: # button save
            subtmit_button = st.form_submit_button(label='Save')
            if subtmit_button:
                if Exchange.idcashflow > 0:
                    exchangeC.update_exchange(Exchange)
                else:    
                    Exchange.dtcashflow = Exchange.dtcashflow.strftime(
                        '%Y-%m-%d')
                    Exchange.tchaflow = Exchange.tchaflow.strftime(
                        '%H:%M')
                    exchangeC.insert_exchange(Exchange)
    
def newCustromer():
    with st.form(key='form1'):

        Customer.name = ''
        Customer.dtbirth = ''
        Customer.fk_idcountry = 0
        Customer.phone = ''

        cEv1, cEv2, cEv3, cEv4, cEv5, cEv6, cEv7, cEv8 = st.columns([3, 1.2, 1.2, 2, 2, 1, 1,1])
        with cEv1:
            Customer.name = sty.overlaid_input("Nome", Customer.name, True)
        with cEv2:
            Customer.phone = sty.overlaid_input("Phone", Customer.phone, True)
        with cEv3:
            # x = format_func = lambda x: x[1]
            Customer.dtbirth = sty.overlaid_input(
                "Birthday", Customer.dtbirth, True)
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
            Customer.numidentification = sty.overlaid_input(
                "Num Id", '', True)
        with cEv7:
            subtmit_button = st.form_submit_button(label='Save')
            if subtmit_button:
                customerC.insert_customer(Customer)
                st.success("Saved!")

def findComiss(valueflow):
    nPercentCheck = percentC.get_all_percentcheck(3)
    for item in nPercentCheck:
        try:
            index, formula, valuereturn, valuereturntype = item
            resultado = eval(formula.replace('x', str(valueflow)))
            if resultado:
                if valueflow == 0:
                    return 0
                else:
                    return f"{valuereturn}"

        except Exception as e:
            st.warning(
                f"Error evaluating formula '{formula}': {str(e)}")
    return None

# def editExchangeValues(eCustomer, i_id, sel_row, gd):

#     edit_disable = True
#     if st.session_state.perfil == 'A':
#         edit_disable = False

#     new_dt = datetime.now().date()
#     new_tm = datetime.now().time()
    
#     Exchange.idcashflow = sel_row[0]['Id']
#     Exchange.dtcashflow = "Date"
#     Exchange.tchaflow = "Time"
#     Exchange.fk_idcustomer = i_id
#     Exchange.valueflow = float(sel_row[0]["Value"])
#     Exchange.valuepercentflow = sel_row[0]["pComiss"]
#     Exchange.totaltopay = ["Pay"]
#     Exchange.totalflow = sel_row[0]["Reciev"]
#     Exchange.valuewire = float(sel_row[0]["Wire"])
#     Exchange.centsflow = sel_row[0]["Cents1"]
#     Exchange.percentflow = sel_row[0]["pComiss"]

#     cEv1, cEv2, cEv3, cEv4, cEv5, cEv6, cEv7, cEv8, cEv9, cEv10, cEv11 = st.columns(
#         [1.5, .8, .6, .7, .7, .6, .7, .8, 1, 1, 2])
#     with cEv1:
#         x = format_func = lambda x: x[1]
#         edit_item_id = sty.overlaid_selectbox(" Company:", eCustomer, 0, x)
#         if edit_item_id:
#             Exchange.fk_idbankmaster = edit_item_id[0]
#     with cEv2:
#         Exchange.valueflow = sty.overlaid_number(" Value", Exchange.valueflow, "%.2f", edit_disable)
#     with cEv3:
#         if Exchange.valueflow:
#             Exchange.centsflow = Exchange.valueflow - \
#                 int(Exchange.valueflow)
#         Exchange.centsflow = sty.overlaid_number(
#             " Cents 1", Exchange.centsflow, "%.2f", True)
#     with cEv4:
#         # st.write(findComiss(Exchange.valueflow))
#         Exchange.percentflow = float(findComiss(Exchange.valueflow))
#         if Exchange.valueflow > 0.00 and Exchange.valueflow <= 200:
#             Exchange.valuepercentflow = Exchange.percentflow
#             Exchange.percentflow = sty.overlaid_number(
#                 " pComis", 0.00, "%.2f", edit_disable
#             )
#         else:
#             Exchange.percentflow = sty.overlaid_number(
#                 " pComis", Exchange.percentflow, "%.2f", edit_disable)
#     with cEv5:
#         if Exchange.percentflow > 0.00:
#             Exchange.valuepercentflow = abs(round(
#                 Exchange.valueflow - (Exchange.valueflow * (1.00 + Exchange.percentflow / 100)), 2))

#         Exchange.valuepercentflow = sty.overlaid_number(
#             " %Value", Exchange.valuepercentflow, "%.2f", True)

#     with cEv6:
#         Exchange.cents2flow = (
#             Exchange.valueflow - Exchange.centsflow) - Exchange.valuepercentflow
#         Exchange.cents2flow = round(
#             Exchange.cents2flow - int(Exchange.cents2flow), 2)
#         Exchange.cents2flow = sty.overlaid_number(
#             " Cents2", Exchange.cents2flow, "%.2f", True)
#     with cEv7:
#         Exchange.valuewire = sty.overlaid_number(
#             " Wire", Exchange.valuewire, "%.2f", edit_disable)
#     with cEv8:
#         Exchange.totalflow = round(
#             Exchange.centsflow + Exchange.cents2flow + Exchange.valuepercentflow, 2)
#         Exchange.totalflow = sty.overlaid_number(
#             " Recieve", Exchange.totalflow, "%.2f", True)
#     with cEv9:
#         Exchange.totaltopay = Exchange.valueflow - Exchange.totalflow
#         Exchange.totaltopay = sty.overlaid_number(
#             " Pay", Exchange.totaltopay, "%.2f", True)
#     with cEv10:
#         Exchange.cashflowok = st.checkbox("Ok")
        
                
#         # st.error("Do you really, really, wanna do this?")
#         # subtmit_button = st.form_submit_button(label="Yes, I'm ready to delete",disabled=edit_disable)
#         # if subtmit_button:
#         #     st.success("Deleted!")
   
def delExchange(sel_row):

    # st.divider()
    cDel1, cDel2, cDel3, cDel4 = st.columns([4,2,2,9])
    
    with cDel1:
        st.error('Id: ' + str(sel_row[0]['Id']) + ' / ' + sel_row[0]
                ["Date"] + ' / ' + sel_row[0]["Time"] + ' / ' + sel_row[0]["Value"])
        
    with cDel2:
        st.write('')
        dLog = sty.overlaid_input('log:', '', False)
        dvLogin = loginC.verify_login(dLog)
        loginOk = False
        if (dvLogin==None and dLog != ''):
            st.sidebar.error('User does not exist!')
            
    with cDel3:
        st.write('')
        dPsw = sty.overlaid_psw('psw:', 'password')
        
    with cDel4:
        if dPsw:
           loginOk = loginC.check_password(dPsw, dvLogin[1])
           if loginOk:
              st.write('')
              bDel = st.button('Del')
              exchangeC.delete_exchange(sel_row[0]['Id'])
        