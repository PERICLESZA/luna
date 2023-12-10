import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode, JsCode, ColumnsAutoSizeMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode, ColumnsAutoSizeMode

# Dados de exemplo
dados = {'Código': [1, 2, 3, 4],
         'Nome': ['João', 'Maria', 'José', 'Ana']}

df = pd.DataFrame(dados)

# Mapeamento de códigos para nomes
codigo_para_nome = {1: 'João', 2: 'Maria', 3: 'José', 4: 'Ana'}

# Construa as opções para o selectbox
nomes = df['Nome'].tolist()
codigos = df['Código'].tolist()
codigo_nome_options = dict(zip(codigos, nomes))

# Função para renderizar o seletor na célula da tabela
def render_selectbox(value, _):
    return f'<select style="width: 100%"><option value="{value}" selected>{codigo_para_nome[value]}</option></select>'

# Adiciona uma nova coluna usando a função de renderização personalizada
df['Nome (Selectbox)'] = df['Código']

# Ag-Grid
grid_options = {
    'enableRangeSelection': True,
    'enableSorting': True,
    'enableFilter': True,
    'domLayout': 'autoHeight',
}

column_defs = [
    {'headerName': 'Código', 'field': 'Código', 'editable': False},
    {'headerName': 'Nome', 'field': 'Nome'},
    {'headerName': 'Nome (Selectbox)', 'field': 'Nome (Selectbox)', 'editable': True,
     'cellRenderer': 'render_selectbox'}
]

ag_grid = AgGrid(df, gridOptions=grid_options, columnDefs=column_defs,
                 update_mode=GridUpdateMode.SELECTION_CHANGED,
                 enable_enterprise_modules=False,  # Desabilita os módulos da versão Enterprise
                 allow_unsafe_jscode=True)  # Permite código JS personalizado

# Ajuste os dados selecionados na Ag-Grid
# selected_rows = ag_grid['selected_rows']

# Exiba as informações correspondentes aos dados selecionados
# if selected_rows:
#     selected_codigo = selected_rows[0]['Código']
#     selected_nome = codigo_para_nome[selected_codigo]
#     st.write(f'Dados selecionados na tabela Ag-Grid: Código={selected_codigo}, Nome={selected_nome}')
