import streamlit as st
import pandas as pd
import Controllers.percentcheckController as percentcheckC
import Models.percentcheck as Percentcheck

def adicionar_item():
    item_formula = st.text_input("Formula:")
    item_valuereturn = st.text_input("Return:")
    item_valuereturntype = st.text_input("Return type:")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Add"):
            if item_formula:
                Percentcheck.idpercentcheck = 0
                Percentcheck.formula = item_formula
                Percentcheck.valuereturn = item_valuereturn
                Percentcheck.valuereturntype = item_valuereturntype
                percentcheckC.insert_percentcheck(Percentcheck)
                st.success("Added!")
                items = percentcheckC.get_all_percentcheck(1)
            else:
                st.warning("Fill the filed Percentcheck.")
    with col2:
        if st.button("Update"):
            items = percentcheckC.get_all_percentcheck(0)
            st.success("Updated!")


def mainPercentcheck():
    pCol1, pCol2  = st.columns(2)
    with pCol1:
        # Carregar todos os itens da tabela
        item_id=0
        items = percentcheckC.get_all_percentcheck(0)
        # x =  
        selected_item_id = st.selectbox("Select Percentcheck:", items, format_func=lambda x: x[1])
        if selected_item_id: item_id = selected_item_id[0]
        
        if item_id > 0 :
            item_details = percentcheckC.get_det_percentcheck(item_id)
            item_formula = item_details[1]
            item_valuereturn = item_details[2]
            item_valuereturntype = item_details[3]
            
            new_formula = st.text_input("Formula:", item_formula)
            new_valuereturn = st.number_input("Return:", item_valuereturn)
            new_valuereturntype = st.text_input(
                "Return type:", item_valuereturntype)
            
            Percentcheck.idpercentcheck = item_id
            Percentcheck.formula = new_formula
            Percentcheck.valuereturn = new_valuereturn
            Percentcheck.valuereturntype = new_valuereturntype
            
            # Botão para salvar as alterações ou adicionar um novo item
            col1, col2, col3, col4 = st.columns([1.2,1.2,1.2,.5])
            with col1:
                if st.button("Save", key="spercentcheck"):
                    percentcheckC.update_percentcheck(Percentcheck)
                    st.success("Saved!")
            with col2:
                # Botão para excluir o item
                if st.button("Delete", key="dpercentcheck"):
                    percentcheckC.delete_percentcheck(item_id)
                    st.success("Deleted!")
            with col3:
                if st.button("Update", key="upercentcheck"):
                    items = percentcheckC.get_all_percentcheck(0)
                    st.success("Updated!")
            with col4:
                if st.button("New", key="npercentcheck"):
                    items = percentcheckC.get_all_percentcheck(0)
                    selected_item_id = None
                    
        else:
            # Adicionar um novo item
            adicionar_item()

    with pCol2:
        rows = percentcheckC.get_all_percentcheck(0)
        df = pd.DataFrame(rows, columns=['Id', 'Formula', 'Return', 'Type'])
        
        config = {
            'idpercentcheck': st.column_config.NumberColumn('Id'),
            'Formula': st.column_config.TextColumn('Formula'),
            'Return': st.column_config.TextColumn('Return'),
            'Type': st.column_config.TextColumn('Type'),
            }
        
        left_aligned_df = df.style.set_properties(**{'text-align': 'center'})

        # Get dataframe row-selections from user with st.data_editor
        edited_df = st.data_editor(left_aligned_df,
                                    column_config=config, 
                                    hide_index=True,
                                    disabled=df.columns,
                                    width=400,
                                    height=500)