import streamlit as st
import pandas as pd
import Controllers.countryController as countryC
import Models.country as Country

def adicionar_item():
    item_name = st.text_input("Country:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Add"):
            if item_name:
                Country.idcountry = 0
                Country.namecountry = item_name
                countryC.insert_country(Country)
                st.success("Added!")
                items = countryC.get_all_country(1)
            else:
                st.warning("Fill the filed Country.")
    with col2:
        if st.button("Update"):
            items = countryC.get_all_country(0)
            st.success("Updated!")

def mainCountry():
    pCol1, pCol2  = st.columns(2)
    with pCol1:
        # Carregar todos os itens da tabela
        item_id=0
        items = countryC.get_all_country(0)
        # x =  
        selected_item_id = st.selectbox("Select Country:", items, format_func=lambda x: x[1])
        if selected_item_id: item_id = selected_item_id[0]
        
        if item_id > 0 :
            item_details = countryC.get_det_country(item_id)
            item_description = item_details[1]
            new_description = st.text_input("Country:", item_description)
            
            Country.idcountry = item_id
            Country.namecountry = new_description
            
            # Botão para salvar as alterações ou adicionar um novo item
            col1, col2, col3, col4 = st.columns([1.2,1.2,1.2,.5])
            with col1:
                if st.button("Save", key="sStatus"):
                    countryC.update_country(Country)
                    st.success("Saved!")
            with col2:
                # Botão para excluir o item
                if st.button("Delete", key="dStatus"):
                    countryC.delete_country(item_id)
                    st.success("Deleted!")
            with col3:
                if st.button("Update", key="uStatus"):
                    items = countryC.get_all_country(0)
                    st.success("Updated!")
            with col4:
                if st.button("New", key="nStatus"):
                    items = countryC.get_all_country(0)
                    selected_item_id = None
                    
        else:
            # Adicionar um novo item
            adicionar_item()

    with pCol2:
        rows = countryC.get_all_country(0)
        df = pd.DataFrame(rows, columns=['Id', 'Country'])
        
        config = {
            'idcountry': st.column_config.NumberColumn('Id'),
            'namecountry': st.column_config.TextColumn('Country'),
            }
        
        left_aligned_df = df.style.set_properties(**{'text-align': 'center'})

        # Get dataframe row-selections from user with st.data_editor
        edited_df = st.data_editor(left_aligned_df,
                                    column_config=config, 
                                    hide_index=True,
                                    disabled=df.columns,
                                    width=400,
                                    height=500)