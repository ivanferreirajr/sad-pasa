import streamlit as st
import pandas as pd
from os.path import join, dirname
# import numpy as np
# import matplotlib.pylab as plt 

# setup
uri_salas1 = join(dirname(__file__), '..', 'data','cenario1-salas.csv' )
uri_turmas1 = join(dirname(__file__), '..', 'data','cenario1-turmas.csv' )
uri_salas2 = join(dirname(__file__), '..', 'data','cenario2-salas.csv' )
uri_turmas2 = join(dirname(__file__), '..', 'data','cenario2-turmas.csv' )

data_salas1 = pd.read_csv(uri_salas1)
data_turmas1 = pd.read_csv(uri_turmas1)

data_salas2 = pd.read_csv(uri_salas2)
data_turmas2 = pd.read_csv(uri_turmas2)

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

