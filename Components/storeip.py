import streamlit as st
import pandas as pd
import Controllers.storeipController as storeipC
import Models.storeip as Storeip
import Controllers.storeController as storeC
import Models.store as Store
import Styles as sty

def mainStoreip():
    pCol1, pCol2 = st.columns(2)
    with pCol1:
        # Carregar todos os itens da tabela
        item_id = 0
        items = storeipC.get_all_storeip(0)
        selected_item_id = st.selectbox(
            "Select IP", items, format_func=lambda x: x[0])
        if selected_item_id:
            item_id = selected_item_id[0]

        if item_id != '<<New>>':
            
            item_details = storeipC.get_det_storeip(item_id)
            item_name = item_details[0]
            new_name = st.text_input("IP:", item_name)
            ipOrigin = item_name 
             
            items = storeC.get_all_store(1)
            x = format_func = lambda x: x[1]
            if (selected_item_id[1] is not None) and (selected_item_id[1] > 0):
                indice = next((i for i, item in enumerate(items)
                              if item[0] == selected_item_id[1]), None)
                i_id = st.selectbox("Store:", items, indice, x)

            # i_idstore = st.selectbox("Store:", items, format_func=lambda x: x[1])
            # if selected_item_id: new_id = selected_item_id[0]

            Storeip.idstore = i_id[0]
            Storeip.ipstore = new_name

            # Botão para salvar as alterações ou adicionar um novo item
            col1, col2, col3, col4 = st.columns([1.2, 1.2, 1.2, .5])
            with col1:
                if st.button("Save", key="sStoreIP"):
                    storeipC.update_storeip(Storeip, ipOrigin)
                    # items = cityC.get_all_cities(0)
                    st.success("Saved!")
            with col2:
                # Botão para excluir o item
                if st.button("Delete", key="dStoreIP"):
                    storeipC.delete_storeip(item_id)
                    st.success("Deleted!")
            with col3:
                if st.button("Update", key="uStoreIP"):
                    items = storeipC.get_all_storeip(0)
                    st.success("Updated!")
            with col4:
                if st.button("New", key="nStoreIP"):
                    items = storeipC.get_all_storeip(0)
                    selected_item_id = None

        else:
            # Adicionar um novo item
            adicionar_item()

    with pCol2:

        rows = storeipC.get_all_storeip(4)

        df = pd.DataFrame(rows, columns=['IP', 'Store'])

        left_aligned_df = df.style.set_properties(**{'text-align': 'center'})

        # Get dataframe row-selections from user with st.data_editor
        edited_df = st.data_editor(left_aligned_df,
                                   hide_index=True,
                                   disabled=df.columns,
                                   width=400,
                                   height=500)

def adicionar_item():

    i_ipstore = st.text_input("IP:")
    items = storeC.get_all_store(3)
    i_idstore = st.selectbox("Store:", items, format_func=lambda x: x[1])
    if i_idstore: i_idstore = i_idstore[0]
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Add"):
            if i_ipstore:
                Storeip.ipstore = i_ipstore
                Storeip.idstore = i_idstore
                storeipC.insert_storeip(Storeip)
                st.success("Added!")
                items = storeipC.get_all_storeip(0)
            else:
                st.warning("Fill the filed StoreIP.")
    with col2:
        if st.button("Update"):
            items = storeipC.get_all_storeip(0)
            st.success("Updated!")


