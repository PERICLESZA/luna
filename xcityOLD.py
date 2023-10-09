import streamlit as st
# import Controllers.cityController as cityController
import Controllers.cityController as cityController
import Models.city as city
import pandas as pd

st.title("Add City")
col1, col2 = st.columns(2)

with col1:
    with st.form(key="include_city"):
        input_nameCity = st.text_input(label="City Name")
        input_button_submit = st.form_submit_button("Add")

    if input_button_submit:
        city.name_city = input_nameCity
        cityController.Incluir(city)

with col2:

    rows = cityController.selecionar()
    df = pd.DataFrame(rows, columns=['idcity', 'name_city'])
    config = {
        'idcity': st.column_config.NumberColumn('Id '),
        'name_city': st.column_config.TextColumn('City'),
    }

    # result = st.data_editor(
    #     df, column_config=config, num_rows='dynamic', disabled=False
    #     )
        
    def dataframe_with_selections(df):
        df_with_selections = df.copy()
        df_with_selections.insert(0, "Select", False)

        # Get dataframe row-selections from user with st.data_editor
        edited_df = st.data_editor(
            df_with_selections,
            hide_index=True,
            column_config={"Select": st.column_config.CheckboxColumn(required=True)},
            disabled=df.columns,
        )

        # Filter the dataframe using the temporary column, then drop the column
        selected_rows = edited_df[edited_df.Select]
        return selected_rows.drop('Select', axis=1)


