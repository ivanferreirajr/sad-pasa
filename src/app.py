import streamlit as st
import pandas as pd
import database as db
from modeling import allocation
# import numpy as np
# import matplotlib.pylab as plt 

# setup & connection with database
connection = db.Connection()

connection.execute("SELECT * FROM cenario1_salas")
data_salas1 = connection.fetchall()
data_salas1 = pd.DataFrame(data_salas1, columns=['id_sala','numero_cadeiras','acessivel','qualidade'] )

connection.execute("SELECT * FROM cenario1_turmas")
data_turmas1 = connection.fetchall()
data_turmas1 = pd.DataFrame(data_turmas1, columns=['disciplina','professor','dias_horario','numero_alunos','curso','período','acessibilidade','qualidade'] )

connection.execute("SELECT * FROM cenario2_salas")
data_salas2 = connection.fetchall()
data_salas2 = pd.DataFrame(data_salas2, columns=['id_sala','numero_cadeiras','acessivel','qualidade'] )

connection.execute("SELECT * FROM cenario2_turmas")
data_turmas2 = connection.fetchall()
data_turmas2 = pd.DataFrame(data_turmas2, columns=['disciplina','professor','dias_horario','numero_alunos','curso','período','acessibilidade','qualidade'] )

# header
st.title("PASA")

# st.subheader("DSS for PASA")

### sidebar
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
    elif cenario  == "cenário 2":
        df = allocation(data_salas2, data_turmas2)
    st.write(df)

    #otimization = 75
    #st.markdown(f"Taxa média de Ocupação: {otimization}%")
    st.markdown("### Trocar turma")

    input1, input2 = st.beta_columns([1, 1])
    with input1:
        st.text_input("Turma/Horario 1")
    with input2: 
        st.text_input("Turma/Horario 2")
    if st.button('Trocar'):
        st.write(input1)

