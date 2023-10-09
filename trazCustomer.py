import streamlit as st
import Services.database as db

# Função para obter dados da tabela MySQL com base no ID e retornar como um dicionário
def obter_dados_por_id(id):

    try:
        # Crie um cursor para executar consultas SQL
        cur = db.cnxn.cursor(dictionary=True)  # Use dictionary=True para obter resultados como dicionários

        # Consulta SQL para obter os nomes dos campos da tabela
        cur.execute(f"SELECT * FROM customer WHERE idcustomer = %s", (id,))

        # Obtenha o registro selecionado como um dicionário
        registro = cur.fetchone()

        # Feche o cursor e a conexão
        cur.close()

        # Retorne o registro
        return registro

    except Exception as e:
        st.error(f"Erro ao obter dados: {str(e)}")
        return {}

# Interface do Streamlit
st.title("Obter Dados do MySQL por ID")

# Formulário para inserir o ID do registro
id = st.number_input("ID do Registro:", min_value=1, step=1)

# Botão para obter dados por ID
if st.button("Obter Dados por ID"):
    if id:
        registro_encontrado = obter_dados_por_id(id)
        if registro_encontrado:
            st.write("Dados Encontrados:")
            st.write(registro_encontrado)
        else:
            st.warning("Nenhum registro encontrado com o ID especificado.")
    else:
        st.warning("Por favor, insira um ID válido.")

# Observação: Lembre-se de ajustar o nome da tabela e as informações de conexão com o banco de dados no código.
