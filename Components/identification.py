import streamlit as st
import pandas as pd
import Controllers.idController as idC
import Models.identification as Identification

def adicionar_item():

    item_name = st.text_input("Identification:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Add"):
            if item_name:
                Identification.idcity = 0
                Identification.name_city = item_name
                idC.insert_identification(item_name)
                st.success("Added!")
                items = idC.get_all_ids(0)
            else:
                st.warning("Fill the filed identification.")
    with col2:
        if st.button("Update"):
            items = idC.get_all_ids(0)
            st.success("Updated!")


def mainIdentification():
    
    pCol1, pCol2  = st.columns(2)
    with pCol1:
        # Carregar todos os itens da tabela
        items = idC.get_all_ids(0)
        selected_item_id = st.selectbox("Select Identification:", items, format_func=lambda x: x[1])
        if selected_item_id: item_id = selected_item_id[0]
        
        if item_id > 0 :
            item_details = idC.get_det_identification(item_id)
            item_name = item_details[1]
            new_name = st.text_input("Identification:", item_name)
            Identification.ididentification = item_id
            Identification.nameidentification = new_name
            
            # Botão para salvar as alterações ou adicionar um novo item
            col1, col2, col3, col4 = st.columns([1.2,1.2,1.2,.5])
            with col1:
                if st.button("Save", key="sId"):
                    idC.update_identification(Identification)
                    items = idC.get_all_ids(0)
                    st.success("Saved!")
            with col2:
                # Botão para excluir o item
                if st.button("Delete", key="dId"):
                    idC.delete_identification(item_id)
                    st.success("Deleted!")
            with col3:
                if st.button("Update", key="uId"):
                    items = idC.get_all_ids(0)
                    st.success("Updated!")
            with col4:
                if st.button("New", key="nId"):
                    items = idC.get_all_ids(0)
                    selected_item_id = None
                    
        else:
            # Adicionar um novo item
            adicionar_item()

    with pCol2:
        rows = idC.get_all_ids(0)
        df = pd.DataFrame(rows, columns=['Id', 'Identification'])
                        
        config = {
            'ididentification': st.column_config.NumberColumn('Id'),
            'name_id': st.column_config.TextColumn('Identification'),
            }
        
        left_aligned_df = df.style.set_properties(**{'text-align': 'center'})

        # Get dataframe row-selections from user with st.data_editor
        edited_df = st.data_editor(left_aligned_df,
                                    column_config=config, 
                                    hide_index=True,
                                    disabled=df.columns,
                                    width=400,
                                    height=500)