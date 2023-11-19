import streamlit as st
import pandas as pd
import Controllers.classController as classC
import Models.classcustomer as ClassC

def adicionar_item():

    item_name = st.text_input("Class:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Add"):
            if item_name:
                ClassC.idclasscustomer = 0
                ClassC.description = item_name
                classC.insert_class(item_name)
                st.success("Added!")
                items = classC.get_all_classes(0)
            else:
                st.warning("Fill the filed class.")
    with col2:
        if st.button("Update"):
            items = classC.get_all_classes(0)
            st.success("Updated!")


def mainClass():
    
    pCol1, pCol2  = st.columns(2)
    with pCol1:
        # Carregar todos os itens da tabela
        items = classC.get_all_classes(0)
        selected_item_id = st.selectbox("Select class:", items, format_func=lambda x: x[1])
        if selected_item_id: item_id = selected_item_id[0]
        
        if item_id > 0 :
            item_details = classC.get_det_class(item_id)
            item_name = item_details[1]
            new_name = st.text_input("Class:", item_name)
            ClassC.idclasscustomer = item_id
            ClassC.description = new_name
            
            # Botão para salvar as alterações ou adicionar um novo item
            col1, col2, col3, col4 = st.columns([1.2,1.2,1.2,.5])
            with col1:
                if st.button("Save", key="sClass"):
                    classC.update_class(ClassC)
                    # items = classC.get_all_class(0)
                    st.success("Saved!")
            with col2:
                # Botão para excluir o item
                if st.button("Delete", key="dClass"):
                    classC.delete_class(item_id)
                    st.success("Deleted!")
            with col3:
                if st.button("Update", key="uClass"):
                    items = classC.get_all_classes(0)
                    st.success("Updated!")
            with col4:
                if st.button("New", key="nClass"):
                    items = classC.get_all_classes(0)
                    selected_item_id = None
                    
        else:
            # Adicionar um novo item
            adicionar_item()

    with pCol2:
        rows = classC.get_all_classes(0)
        df = pd.DataFrame(rows, columns=['IdClass', 'ClassC'])
                        
        config = {
            'idclasscustomer': st.column_config.NumberColumn('IdClass'),
            'description': st.column_config.TextColumn('ClassC'),
            }
        
        left_aligned_df = df.style.set_properties(**{'text-align': 'center'})

        # Get dataframe row-selections from user with st.data_editor
        edited_df = st.data_editor(left_aligned_df,
                                    column_config=config, 
                                    hide_index=True,
                                    disabled=df.columns,
                                    width=400,
                                    height=500)