import streamlit as st
import pandas as pd
import database as db
import numpy as np
from modeling import allocation

# setup & connection with database
connection = db.Connection()

data_salas1 = connection.query("SELECT * FROM cenario1_salas")
data_salas1 = pd.DataFrame(data_salas1, columns=['id_sala','numero_cadeiras','acessivel','qualidade'] )

data_turmas1 = connection.query("SELECT * FROM cenario1_turmas")
data_turmas1 = pd.DataFrame(data_turmas1, columns=['disciplina','professor','dias_horario','numero_alunos','curso','período','acessibilidade','qualidade'] )

data_salas2 = connection.query("SELECT * FROM cenario2_salas")
data_salas2 = pd.DataFrame(data_salas2, columns=['id_sala','numero_cadeiras','acessivel','qualidade'] )

data_turmas2 = connection.query("SELECT * FROM cenario2_turmas")
data_turmas2 = pd.DataFrame(data_turmas2, columns=['disciplina','professor','dias_horario','numero_alunos','curso','período','acessibilidade','qualidade'] )

# functions
@st.cache
def replace_class(turma_1, turma_2):
    print("calma")

@st.cache
def occupancy_rate(data):
    rate = data['numero_alunos'] * 100 / data['numero_cadeiras']
    return np.mean(rate)

@st.cache
def allocation_table(data, table_name):
    connection.cursor.copy_from(data, table_name, null='', sep=',')
    connection.commit()

# header
st.title("PASA")
st.subheader("Um sistema de apoio à decisão para o problema da alocação de salas de aula")
st.markdown("Escolha um cenário na barra lateral e comece a análise")

# sidebar
st.sidebar.markdown("## Configurações")

cenario = st.sidebar.selectbox(
    "Selecione o cenário",
    ("cenário 1", "cenário 2")
)

if st.sidebar.checkbox("Mostrar dados dos cenário"):
    if cenario  == "cenário 1":
        st.markdown("### Dados Salas")
        st.write(data_salas1)
        st.markdown("### Dados Turmas")
        st.write(data_turmas1)
    else:
        st.markdown("### Dados Salas")
        st.write(data_salas2)
        st.markdown("### Dados Turmas")
        st.write(data_turmas2)

# main screen
if st.button('Alocar salas'):
    if cenario  == "cenário 1":
        df = allocation(data_salas1, data_turmas1)
        #db.insert_values(connection, df, 'turmas_alocadas_cenario1')
    elif cenario  == "cenário 2":
        df = allocation(data_salas2, data_turmas2)
        #db.insert_values(connection, df, 'turmas_alocadas_cenario2')
    st.write(df)

    st.markdown(f"Taxa ocupação média: {round(occupancy_rate(df), 2)}%")
    
    st.markdown("### Trocar turma")
    input1, input2 = st.beta_columns([1, 1])
    with input1:
        st.text_input("Horario/Sala - 1", 'ex: 35')
    with input2:
        st.text_input("Horario/Sala - 2", 'ex: 25')
    if st.button('Trocar'):
        st.write(input1)
        #df = replace_class(input1, input2)
    
    # dataviz
    st.markdown("### Gráficos")
    st.write("Quantidade de turmas por horário")
    st.bar_chart(df['horario'].value_counts())
