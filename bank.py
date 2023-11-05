import streamlit as st
import pandas as pd
import Controllers.bankController as bankC
import Models.bank as Bank

def adicionar_item():

    item_name = st.text_input("Bank:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Add"):
            if item_name:
                Bank.id = 0
                Bank.name = item_name
                bankC.insert_bank(item_name)
                st.success("Added!")
                items = bankC.get_all_bank(1)
            else:
                st.warning("Fill the filed Bank.")
    with col2:
        if st.button("Update"):
            items = bankC.get_all_cities(0)
            st.success("Updated!")


def mainBank():
    pCol1, pCol2  = st.columns(2)
    with pCol1:
        # Carregar todos os itens da tabela
        item_id=0
        items = bankC.get_all_bank(1)
        x =  format_func=lambda x: x[1]
        selected_item_id = st.selectbox("Select Bank:", items,x)
        if selected_item_id: item_id = selected_item_id[0]
        
        if item_id > 0 :
            item_details = bankC.get_det_bank(item_id)
            item_name = item_details[1]
            new_name = st.text_input("Nome:", item_name)
            Bank.id = item_id
            Bank.name = new_name
            
            # Botão para salvar as alterações ou adicionar um novo item
            col1, col2, col3, col4 = st.columns([1.2,1.2,1.2,.5])
            with col1:
                if st.button("Save", key="sCity"):
                    bankC.update_bank(Bank)
                    st.success("Saved!")
            with col2:
                # Botão para excluir o item
                if st.button("Delete", key="dBank"):
                    bankC.delete_bank(item_id)
                    st.success("Deleted!")
            with col3:
                if st.button("Update", key="uBank"):
                    items = bankC.get_all_cities(0)
                    st.success("Updated!")
            with col4:
                if st.button("New", key="nBank"):
                    items = bankC.get_all_bank(0)
                    selected_item_id = None
                    
        else:
            # Adicionar um novo item
            adicionar_item()

    with pCol2:
        rows = bankC.get_all_bank(0)
        df = pd.DataFrame(rows, columns=['Id', 'Bank'])
                        
        config = {
            'id': st.column_config.NumberColumn('Id'),
            'name': st.column_config.TextColumn('Bank'),
            }
        
        left_aligned_df = df.style.set_properties(**{'text-align': 'center'})

        # Get dataframe row-selections from user with st.data_editor
        edited_df = st.data_editor(left_aligned_df,
                                    column_config=config, 
                                    hide_index=True,
                                    disabled=df.columns,
                                    width=400,
                                    height=500)