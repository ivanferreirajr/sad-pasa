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
def change_class(conn, table_name, id_turma1, id_turma2):
    query = f"SELECT horario, id_sala FROM {table_name} WHERE id_sala = %s;"
    horario1, id_sala1 = conn.query(query, id_turma1)
    horario2, id_sala2 = conn.query(query, id_turma2)

    sql = f"UPDATE {table_name} SET id_sala = %s, horario = %s WHERE id_sala = %s;"
    conn.execute(sql, (id_sala1, horario1, id_sala2))
    conn.execute(sql, (id_sala2, horario2, id_sala1))

    select = f"SELECT * FROM {table_name}"
    df = connection.query(select)
    df = pd.DataFrame(df, columns=['horario','id_sala','disciplina','professor', 'numero_cadeiras', 'numero_alunos'] )

    return df

@st.cache
def replace_class(df, id_turma1, id_turma2):
    id_sala1 = df[df['id'] == id_turma1]['id_sala']
    id_sala2 = df[df['id'] == id_turma2]['id_sala']
    cadeiras1 = df[df['id'] == id_turma1]['numero_cadeiras']
    cadeiras2 = df[df['id'] == id_turma2]['numero_cadeiras']
    df[df['id'] == id_turma1].replace({ 'id_sala': id_sala1, 'numero_cadeiras': cadeiras1 }, inplace=True)
    df[df['id'] == id_turma2].replace({ 'id_sala': id_sala2, 'numero_cadeiras': cadeiras2 }, inplace=True)
    
@st.cache
def occupancy_rate(data):
    rate = data['numero_alunos'] * 100 / data['numero_cadeiras']
    return np.mean(rate)

def allocation_table(data, table_name):
    connection.copy_from(data, table_name)

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
        table = 'turmas_alocadas_cenario1'
    elif cenario  == "cenário 2":
        df = allocation(data_salas2, data_turmas2)
        table = 'turmas_alocadas_cenario2'
    st.write(df)

    st.markdown(f"Taxa ocupação média: {round(occupancy_rate(df), 2)}%")

    #allocation_table(df, table)
    #connection.insert_values(df, table)

    # dataviz
    st.markdown("### Gráficos")
    st.write("Quantidade de turmas por horário")
    st.bar_chart(df['horario'].value_counts())

    st.markdown("### Trocar turma")

    #input_troca = st.text_input("Horario/Sala", "25-23")
    #input1 = input_troca.split('-')[0]
    #input2 = input_troca.split('-')[1]
    #replace_class(df, input1, input2 )
    #st.write(df)
    #st.markdown(f"Taxa ocupação média: {round(occupancy_rate(df), 2)}%")
 
    input1, input2 = st.beta_columns([1, 1])
    with input1:
        st.text_input("Horario/Sala - 1", 'ex: 35')
    with input2:
        st.text_input("Horario/Sala - 2", 'ex: 25')
    if st.button('Trocar'):
        replace_class(df, input1, input2)
            #df = replace_class(connection, table, input1, input2)
        st.write(df)
        st.markdown(f"Taxa ocupação média: {round(occupancy_rate(df), 2)}%")
 