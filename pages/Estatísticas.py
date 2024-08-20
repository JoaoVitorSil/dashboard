import streamlit as st
import pandas as pd

data = pd.read_csv("injury_data.csv")

st.sidebar.header("Opções de Estastísticas")
atributo_stats = st.sidebar.selectbox(
    "Escolha o atributo:",
    ("Idade", "Altura", "Peso", "Intensidade")
)
df = pd.DataFrame()
df["Idade"] = data["Player_Age"]
df["Altura"] = data["Player_Height"]
df["Peso"] = data["Player_Weight"]
df["Intensidade"] = data["Training_Intensity"]

st.title(":material/monitoring: Estatíticas: ")      
st.markdown('')
left,center,right = st.columns(3,gap="large")
with left:
    st.info("Média:")
    st.metric(label="",value=f"{df[atributo_stats].describe()[1]:,.3f}",label_visibility="collapsed")
    st.info("Valor mínimo:")
    st.metric(label="",value=f"{df[atributo_stats].describe()[3]:,.3f}",label_visibility="collapsed")

with center:
    st.info("Desvio Padrão:")
    st.metric(label="",value=f"{df[atributo_stats].describe()[2]:,.3f}",label_visibility="collapsed")
    st.info("Valor máximo:")
    st.metric(label="",value=f"{df[atributo_stats].describe()[7]:,.3f}",label_visibility="collapsed")
with right:
    st.info("Mediana:")
    st.metric(label="",value=f"{df[atributo_stats].describe()[5]:,.3f}",label_visibility="collapsed")