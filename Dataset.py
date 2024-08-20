import os
os.system('pip install plotly')
import streamlit as st
import pandas as pd

data = pd.read_csv("injury_data.csv")

description = """
<div style="text-align: justify;">
    O dataset escolhido foi encontrado na 
    plataforma Kaggle e ele refere-se a um conjunto
    de dados projetado especificamente 
    para a previsão de lesões em jogadores de 
    futebol a partir de alguns atributos que 
    serão mostrados neste trabralho.
</div>
"""

st.title(":material/database: Dataset:")
if st.sidebar.checkbox('Mostrar descrição',value=True):
        st.markdown(description, unsafe_allow_html=True)
        st.markdown(' ')

with st.expander("Tabela", expanded=False, icon=":material/table:"):
    showData = st.multiselect('Filtro: ',data.columns, default=data.columns.tolist())
    st.write(data[showData])

st.sidebar.header("Download")
st.sidebar.download_button(
    label="Baixar o dataset em CSV",
    data=data.to_csv(index=False),
    file_name="injury_data.csv",
    mime="text/csv"
)

