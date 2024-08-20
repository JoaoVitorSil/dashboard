import streamlit as st
import plotly.express as px
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier



data = pd.read_csv("injury_data.csv")

st.sidebar.header("Opções de Modelo")
modelo = st.sidebar.selectbox(
    "Escolha o modelo:",
    ("K-NN", "K-Means")
)

def knn():
    k = st.sidebar.slider('K vizinhos', min_value=1,max_value=20) 
    
    X = data.drop('Likelihood_of_Injury', axis=1)
    y = data['Likelihood_of_Injury']
    
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    
    scaler = StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)
    
    i_range = range(1,k+1)
    scores = []
    for i in i_range:
        knn = KNeighborsClassifier(n_neighbors=i, metric='euclidean')
        knn.fit(x_train, y_train)
        y_pred = knn.predict(x_test)
        scores.append(accuracy_score(y_test,y_pred)) 
        
    df = {'x': i_range, 'y': scores}
    fig = px.line(df, x='x', y='y',markers=True, labels={
        'x': 'Número de Vizinhos',
        'y': 'Acurácia',
    })
    tab1, tab2 = st.tabs(["# :material/bar_chart: Gráfico", ":material/monitoring: Estatísticas"])
    tab1.markdown("<h2 style='text-align: center;'>Gráfico do K-NN</h2>", unsafe_allow_html=True)
    tab1.plotly_chart(fig)
    df = pd.DataFrame(df)
    tab2.markdown("<h2 style='text-align: center;'>Estatísticas</h2>", unsafe_allow_html=True)
    tab2.markdown('')  
    left,center,right = tab2.columns(3,gap="large")
    with left:
        st.info("Média:")
        st.metric(label="",value=f"{df["y"].describe()[1]:,.3f}",label_visibility="collapsed")
        st.info("Valor mínimo:")
        st.metric(label="",value=f"{df["y"].describe()[3]:,.3f}",label_visibility="collapsed")

    with center:
        st.info("Desvio Padrão:")
        if k == 1: 
            st.metric(label="",value=f"{0:,.3f}",label_visibility="collapsed")
        else:
            st.metric(label="",value=f"{df["y"].describe()[2]:,.3f}",label_visibility="collapsed")
        st.info("Valor máximo:")
        st.metric(label="",value=f"{df["y"].describe()[7]:,.3f}",label_visibility="collapsed")
    with right:
        st.info("Mediana:")
        st.metric(label="",value=f"{df["y"].describe()[5]:,.3f}",label_visibility="collapsed")
def kmeans():
    k = st.sidebar.slider('K clusters',min_value=2, max_value=10)
    
    x = data
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x)    
    pca = PCA(n_components=2)
    x_pca = pca.fit_transform(x_scaled)
    
    kmeans = KMeans(n_clusters=k, n_init="auto")
    kmeans.fit(x_pca)
    data['Cluster'] = kmeans.labels_
    
    fig = px.scatter(x_pca, x=0, y=1, color=data["Cluster"],labels={
        '0': 'Componente 1',
        '1': 'Componete 2',
        'color': 'Clusters'
    })
    st.markdown("<h2 style='text-align: center;'>Gráfico do K-Means</h2>", unsafe_allow_html=True)
    st.plotly_chart(fig)
if modelo == "K-NN":
    knn()
else:
    kmeans()