import streamlit as st
import pandas as pd
import Controllers.cityController as cityC
import Models.city as City

def adicionar_item():

    item_name = st.text_input("City:")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Add"):
            if item_name:
                City.idcity = 0
                City.name_city = item_name
                cityC.add_or_update_item(City)
                st.success("Added!")
                items = cityC.get_items(0)
            else:
                st.warning("Fill the filed City.")
    with col2:
        if st.button("Update"):
            items = cityC.get_items(0)
            st.success("Updated!")

def mainCity():
    
    pCol1, pCol2  = st.columns(2)
    with pCol1:

        # Carregar todos os itens da tabela
        items = cityC.get_items(0)
        selected_item_id = st.selectbox("Select City:", items, format_func=lambda x: x[1])
        if selected_item_id: item_id = selected_item_id[0]
          
        if item_id > 0 :
            item_details = cityC.get_item_details(item_id)
            item_name = item_details[1]

            new_name = st.text_input("Nome:", item_name)
            City.idcity = item_details[0]
            City.name_city = new_name

            # Botão para salvar as alterações ou adicionar um novo item
            col1, col2, col3, col4 = st.columns([1.2,1.2,1.2,.5])
            with col1:
                if st.button("Save", key="sCity"):
                    cityC.add_or_update_item(City)
                    items = cityC.get_items(0)
                    st.success("Saved!")
            with col2:
                # Botão para excluir o item
                if st.button("Delete", key="dCity"):
                    cityC.delete_item(item_id)
                    st.success("Deleted!")
            with col3:
                if st.button("Update", key="uCity"):
                    items = cityC.get_items(0)
                    st.success("Updated!")
            with col4:
                if st.button("New", key="nCity"):
                    selected_item_id = None
                    
        else:
            # Adicionar um novo item
            adicionar_item()
    # st.write(City)        
    with pCol2:
        rows = cityC.get_items(0)
        df = pd.DataFrame(rows, columns=['IdCity', 'City'])
                        
        config = {
            'idcity': st.column_config.NumberColumn('IdCity'),
            'name_city': st.column_config.TextColumn('City'),
            }
        
        left_aligned_df = df.style.set_properties(**{'text-align': 'center'})

        # Get dataframe row-selections from user with st.data_editor
        edited_df = st.data_editor(left_aligned_df,
                                    column_config=config, 
                                    hide_index=True,
                                    disabled=df.columns,
                                    width=400,
                                    height=500)