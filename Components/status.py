import streamlit as st
import pandas as pd
import Controllers.statusController as statusC
import Models.status as Status

def adicionar_item():
    item_name = st.text_input("Status:")
    item_emphasis = st.checkbox("Emphasis:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Add"):
            if item_name:
                Status.idstatus = 0
                Status.description = item_name
                Status.emphasis = item_emphasis
                statusC.insert_status(Status)
                st.success("Added!")
                items = statusC.get_all_status(1)
            else:
                st.warning("Fill the filed Status.")
    with col2:
        if st.button("Update"):
            items = statusC.get_all_status(0)
            st.success("Updated!")

def mainStatus():
    pCol1, pCol2  = st.columns(2)
    with pCol1:
        # Carregar todos os itens da tabela
        item_id=0
        items = statusC.get_all_status(0)
        # x =  
        selected_item_id = st.selectbox("Select Status:", items, format_func=lambda x: x[1])
        if selected_item_id: item_id = selected_item_id[0]
        
        if item_id > 0 :
            item_details = statusC.get_det_status(item_id)
            item_description = item_details[1]
            item_emphasis = item_details[2]
            new_description = st.text_input("Status:", item_description)
            new_emphasis = st.checkbox("Emphasis:", False , item_emphasis)
            
            # Customer.active = st.checkbox("Active", False, key="bActive")
            Status.idstatus = item_id
            Status.description = new_description
            Status.emphasis = new_emphasis
            
            # Botão para salvar as alterações ou adicionar um novo item
            col1, col2, col3, col4 = st.columns([1.2,1.2,1.2,.5])
            with col1:
                if st.button("Save", key="sStatus"):
                    statusC.update_status(Status)
                    st.success("Saved!")
            with col2:
                # Botão para excluir o item
                if st.button("Delete", key="dStatus"):
                    statusC.delete_status(item_id)
                    st.success("Deleted!")
            with col3:
                if st.button("Update", key="uStatus"):
                    items = statusC.get_all_status(0)
                    st.success("Updated!")
            with col4:
                if st.button("New", key="nStatus"):
                    items = statusC.get_all_status(0)
                    selected_item_id = None
                    
        else:
            # Adicionar um novo item
            adicionar_item()

    with pCol2:
        rows = statusC.get_all_status(0)
        df = pd.DataFrame(rows, columns=['Id', 'Status', 'Emphasis'])
        df['Emphasis'] = df['Emphasis'].astype(bool)
        
        config = {
            'idstatus': st.column_config.NumberColumn('Id'),
            'description': st.column_config.TextColumn('Status'),
            'emphasis': st.column_config.CheckboxColumn('Emphasis'),
            }
        
        left_aligned_df = df.style.set_properties(**{'text-align': 'center'})

        # Get dataframe row-selections from user with st.data_editor
        edited_df = st.data_editor(left_aligned_df,
                                    column_config=config, 
                                    hide_index=True,
                                    disabled=df.columns,
                                    width=400,
                                    height=500)