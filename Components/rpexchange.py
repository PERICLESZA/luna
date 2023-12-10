import streamlit as st
import pandas as pd
import Styles as sty
import Controllers.exchangeController as exchangeC
import Controllers.customerController as customerC
import Controllers.statusController as statusC
import Controllers.storeController as storeC
from datetime import datetime, timedelta
from st_aggrid import AgGrid, GridUpdateMode, JsCode, ColumnsAutoSizeMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from datetime import date, datetime

# Função principal do Streamlit
def mainRpExchange():
    dtIni = datetime.now().date()
    dtFim = dtIni + timedelta(days=30)

    cRl1, cRl2, cRl3, cRl4, cRl5, cRl6, cRl7 = st.columns(
        [1, 1, 2.5, 2, 2, 1, 1])
    with cRl1:
        dtIni = sty.overlaid_date("Start date:", dtIni)
    with cRl2:
        dtFim = sty.overlaid_date("End date", dtFim)
    with cRl3:
        i_customer = customerC.get_all_customers(1, 0)
        x = format_func = lambda x: x[1]
        selected_i_id = sty.overlaid_selectbox(
            "Phone No./Name:", i_customer, 0, x)
        if selected_i_id:
            customer_id = selected_i_id[0]
    with cRl4:
        i_status = statusC.get_all_status(1)
        x = format_func = lambda x: x[1]
        selected_item_id = sty.overlaid_selectbox(
            "Select Status:", i_status, 0, x)
        if selected_item_id:
            status_id = selected_item_id[0]
    with cRl5:
        i_store = storeC.get_all_store(1)
        x = format_func = lambda x: x[1]
        selected_item_id = sty.overlaid_selectbox(
            "Select Store:", i_store, 0, x)
        if selected_item_id:
            store_id = selected_item_id[0]
    
    submit_button = st.button(label='Print')
    if submit_button:
        # Chama a função para gerar e exibir o relatório
        exchange_Report(dtIni, dtFim, customer_id, status_id, store_id)

def exchange_Report(start_date, end_date, customer_code, status_filter, store_filter):

    cashflow_data = exchangeC.get_cashflow_rp(start_date, end_date, customer_code, status_filter, store_filter)

    columns = ['Id', 'Date', 'Time', 'Name', 'Check', 'Value', 'Cents1', 'pComiss', 'Comiss', 'Cents2',
        'Wire', 'Reciev', 'Pay', 'Ok', 'Status']

    df = pd.DataFrame(cashflow_data, columns=columns)

    total_row = pd.DataFrame({
        'Check':   ['Total'],
        'Value':   [format(df['Value'].sum(), ",.2f")],
        'Cents1':  [format(df['Cents1'].sum(), ",.2f")],
        'pComiss': [format(0.00, ",.2f")],
        'Comiss':  [format(df['Comiss'].sum(),",.2f")],
        'Cents2':  [format(df['Cents2'].sum(),",.2f")],
        'Wire':    [format(df['Wire'].sum(),",.2f")],
        'Reciev':  [format(df['Reciev'].sum(),",.2f")],
        'Pay':     [format(df['Pay'].sum(),",.2f")],
    })
    
    df['Value']   = df['Value'].apply(lambda x: format(round(x, 2), ".2f"))
    df['Cents1']  = df['Cents1'].apply(lambda x: format(round(x, 2), ".2f"))
    df['pComiss'] = df['pComiss'].apply(lambda x: format(round(x, 2), ".2f"))
    df['Comiss']  = df['Comiss'].apply(lambda x: format(round(x, 2), ".2f"))
    df['Cents2']  = df['Cents2'].apply(lambda x: format(round(x, 2), ".2f"))
    df['Wire']    = df['Wire'].apply(lambda x: format(round(x, 2), ".2f"))
    df['Reciev']  = df['Reciev'].apply(lambda x: format(round(x, 2), ".2f"))
    df['Pay']     = df['Pay'].apply(lambda x: format(round(x, 2), ".2f"))

    # df = pd.concat([df, total_row])

    gd = GridOptionsBuilder.from_dataframe(df)
    # gd.configure_selection(selection_mode="single")
    # gd.configure_default_column(editable=edit_disable)
    
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
            
    gd.configure_columns(df, cellStyle=cellstyle_jscode)
    
    gridoptions = gd.build()

    grid_table = AgGrid(
                        df, gridOptions=gridoptions,
                        enable_enterprise_modules=True,
                        fit_columns_on_grid_load=True,
                        height=450,
                        width='50%',
                        # GridUpdateMode=GridUpdateMode.SELECTION_CHANGED,
                        # reload_data=True,
                        allow_unsafe_jscode=True,
                        )


    st.write(total_row)

    # sel_row = grid_table["selected_rows"]
    # Adicionar botão de download CSV
    
    csv_file = df.to_csv(index=False, sep=";").encode('utf-8')
    st.download_button('Download CSV', csv_file, 'data.csv', 'text/csv')

if __name__ == "__main__":
    mainRpExchange()
