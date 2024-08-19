import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go


st.sidebar.header("Opções do Dataset")

data = pd.read_csv("injury_data.csv")

if st.sidebar.checkbox('Show dataframe',value=True):
    st.title("Dataset:")
    st.write("O dataset escolhido foi encontrado na plataforma Kaggle e ele refere-se a um conjunto de dados projetado especificamente para a previsão de lesões em jogadores de futebol a partir de alguns atributos que serão mostrados neste trabralho.")
    with st.expander("Tabela", expanded=True, icon=":material/table:"):
        showData = st.multiselect('Filtro: ',data.columns, default=data.columns.tolist())
        st.write(data[showData])
    st.markdown("----------")

st.sidebar.header("Opções de Estastísticas")
atributo_stats = st.sidebar.selectbox(
    "Escolha o tipo de gráfico:",
    ("Idade", "Altura", "Peso", "Intensidade")
)
df = pd.DataFrame()
df["Idade"] = data["Player_Age"]
df["Altura"] = data["Player_Height"]
df["Peso"] = data["Player_Weight"]
df["Intensidade"] = data["Training_Intensity"]

st.title("Estatíticas: "+atributo_stats)
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
st.markdown("----------")
st.sidebar.header("Opções de Gráficos")
tipo_grafico = st.sidebar.selectbox(
    "Escolha o tipo de gráfico:",
    ("Histograma", "Boxplot", "Pizza")
)

histograms = {
    'Idade': go.Histogram(
        x=data['Player_Age'], name='Idade do Jogador', nbinsx=20,
        marker=dict(line=dict(width=2, color='black'))
    ),
    'Peso': go.Histogram(
        x=data['Player_Weight'], name='Peso do Jogador', nbinsx=20,
        marker=dict(line=dict(width=2, color='black'))
    ),
    'Altura': go.Histogram(
        x=data['Player_Height'], name='Altura do Jogador', nbinsx=20,
        marker=dict(line=dict(width=2, color='black'))
    ),
    'Intensidade': go.Histogram(
        x=data['Training_Intensity'], name='Intensidade de Treinamento', nbinsx=20,
        marker=dict(line=dict(width=2, color='black'))
    )
    
}

boxplots = {
    'Idade': go.Box(
        y=data['Player_Age']
    ),
    'Peso': go.Box(
        y=data['Player_Weight']
    ),
    'Altura': go.Box(
        y=data['Player_Height']
    ),
    'Intensidade': go.Box(
        y=data['Training_Intensity']
    )
}

count = pd.DataFrame(0, index=range(2), columns=range(1))
for i in range(2):
  count[0][i] = len(data[data['Previous_Injuries'] == i])
  
counts = pd.DataFrame(0, index=range(6), columns=range(1))
for i in range(6):
  counts[0][i] = len(data[data['Recovery_Time'] == i + 1])
  
count1 = pd.DataFrame(0, index=range(2), columns=range(1))
for i in range(2):
  count1[0][i] = len(data[data['Likelihood_of_Injury'] == i])

pies = {
    'Lesões anteriores': go.Pie(labels=["Sem lesões anterioes", "Com lesões anterioes"], values=count[0]),
    'Tempo': go.Pie(labels=["1 dia","2 dias","3 dias","4 dias","5 dias","6 dias"], values=counts[0]),
    'Lesões': go.Pie(labels=["Sem lesões", "Com lesões"], values=count1[0])
}

def gerar_grafico(tipo):
    if tipo == "Histograma":
        fig = go.Figure(data=[histograms['Idade']])

        for histogram in list(histograms.values())[1:]:
            fig.add_trace(histogram.update(visible=False))

        fig.update_layout(
            title={
            'text': 'Distribuição de Idade dos Jogadores',
            'x': 0.5, 
            'xanchor': 'center' 
            },
            xaxis_title_text='Idade',
            yaxis_title_text='Frequência',
            updatemenus=[
                dict(
                    x = 0.11,
                    y = 1.2,
                    active=0,
                    buttons=[
                        dict(label="Idade",
                            method="update",
                            args=[{"visible": [True, False, False, False]},
                                {"title": "Distribuição da Idade do Jogador",
                                    "xaxis": {"title": "Idade"},
                                    "yaxis": {"title": "Frequência"}}]),
                        dict(label="Peso",
                            method="update",
                            args=[{"visible": [False, True, False, False]},
                                {"title": "Distribuição do Peso do Jogador",
                                    "xaxis": {"title": "Peso (kg)"},
                                    "yaxis": {"title": "Frequência"}}]),
                        dict(label="Altura",
                            method="update",
                            args=[{"visible": [False, False, True, False]},
                                {"title": "Distribuição da Altura do Jogador",
                                    "xaxis": {"title": "Altura (cm)"},
                                    "yaxis": {"title": "Frequência"}}]),
                        dict(label="Intensidade",
                            method="update",
                            args=[{"visible": [False, False, False, True]},
                                {"title": "Distribuição da Intensidade de Treinamento",
                                    "xaxis": {"title": "Intensidade de Treinamento"},
                                    "yaxis": {"title": "Frequência"}}])
                    ]
                )
            ]
        )
    elif tipo == "Boxplot":
        fig = go.Figure(data=[boxplots['Idade']])
        
        for boxplot in list(boxplots.values())[1:]:
            fig.add_trace(boxplot.update(visible=False))

        fig.update_layout(
            title={
            'text': 'Distribuição de Idade dos Jogadores',
            'x': 0.5,
            'xanchor': 'center' 
            },
            xaxis_title_text='Idade',
            yaxis_title_text='Frequência',
            updatemenus=[
                dict(
                    x = 0.11,
                    y = 1.2,
                    active=0,
                    buttons=[
                        dict(label="Idade",
                            method="update",
                            args=[{"visible": [True, False, False, False]},
                                {"title": "Distribuição da Idade do Jogador",
                                    "xaxis": {"title": "Idade"},
                                    "yaxis": {"title": "Frequência"}}]),
                        dict(label="Peso",
                            method="update",
                            args=[{"visible": [False, True, False, False]},
                                {"title": "Distribuição do Peso do Jogador",
                                    "xaxis": {"title": "Peso (kg)"},
                                    "yaxis": {"title": "Frequência"}}]),
                        dict(label="Altura",
                            method="update",
                            args=[{"visible": [False, False, True, False]},
                                {"title": "Distribuição da Altura do Jogador",
                                    "xaxis": {"title": "Altura (cm)"},
                                    "yaxis": {"title": "Frequência"}}]),
                        dict(label="Intensidade",
                            method="update",
                            args=[{"visible": [False, False, False, True]},
                                {"title": "Distribuição da Intensidade de Treinamento",
                                    "xaxis": {"title": "Intensidade de Treinamento"},
                                    "yaxis": {"title": "Frequência"}}])
                    ]
                )
            ]
        )
    elif tipo == "Pizza":
        fig = go.Figure(data=[pies['Lesões anteriores']])
        
        for pie in list(pies.values())[1:]:
            fig.add_trace(pie.update(visible=False))

        fig.update_layout(
            title={
            'text': 'Lesões anteriores dos Jogadores',
            'x': 0.5,
            'xanchor': 'center' 
            },
            updatemenus=[
                dict(
                    x = 0.11,
                    y = 1.2,
                    active=0,
                    buttons=[
                        dict(label="Lesões anteriores",
                            method="update",
                            args=[{"visible": [True, False, False]},
                                {"title": "Distribuição ds lesões anteriores dos Jogadores"}]),
                        dict(label="Tempo",
                            method="update",
                            args=[{"visible": [False, True, False]},
                                  {"title": "Distribuição do tempo de resuperação dos Jogadores"}]),
                        dict(label="Lesões",
                            method="update",
                            args=[{"visible": [False, False, True]},
                                  {"title": "Distribuição das lesões dos Jogadores"}]),
                    ]
                )
            ]
        )
    return fig

grafico = gerar_grafico(tipo_grafico)

st.title("Gráficos:")

st.plotly_chart(grafico)