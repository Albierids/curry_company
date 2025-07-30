# ===================================================================
# Comunidade Data Scienc - ComunidadeDS - https://comunidadeds.com/

# Curso Analista de Dados
# Ciclo 06 - Aula 46 - Criando a Página - Visão Restaurante
# Professor: Meigarom Lopes
# Aluno: Alfredo Junior Albieri
# Ano letivo: 2025
# ===================================================================
# ===================================================================

# ===================
# Libraries
# ===================
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
# from streamlit.cli import main
from datetime import datetime
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static

# ===================================================================
# Ajusta a largura da página de aapresentação
# ===================================================================
st.set_page_config(
    page_title="Visão Restaurante",
    page_icon="🍽",
    layout="wide",          # valores: "centered" ou "wide"
    initial_sidebar_state="expanded"  # ou "collapsed"
)

# ===================
# Bibliotecas
# ===================
import pandas as pd 
import numpy as np
import folium
import streamlit as st

# ================
# Import Dataset
# ================
df = pd.read_csv("dataset/train.csv")

# ---------------------------------------------------------------------
# Funções
# ---------------------------------------------------------------------
def avg_std_time_on_traffic( df1 ):
    cols = ['City', 'Time_taken(min)', 'Road_traffic_density']
    df_aux = ( df1.loc[:, ['City', 'Time_taken(min)', 'Road_traffic_density']]
                  .groupby( ['City', 'Road_traffic_density'] )
                  .agg( {'Time_taken(min)': ['mean', 'std']}) )
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    
    fig = px.sunburst(df_aux, path=['City', 'Road_traffic_density'], values='avg_time',
                    color='std_time', color_continuous_scale='RdBu',
                    color_continuous_midpoint=np.average(df_aux['std_time']))
    return fig

def avg_std_time_graph( df1 ):            
    st.markdown('### Tempo médio e Desvio Padrão por Entregas por cidade')
    df_aux = ( df1.loc[:, ['City', 'Time_taken(min)']]
                .groupby('City')
                .agg( {'Time_taken(min)': ['mean', 'std']}) )
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Control', x=df_aux['City'], y=df_aux['avg_time'], error_y=dict(type='data', array=df_aux['std_time'])))
    fig.update_layout(barmode='group')

    return fig

def avg_std_time_delivery( df1, festival, op ):  
    """
    Esta função calcula o tempo médio e o desvio padrão do tempo de entrega.
    Parâmetros:
        Input:
            - df1: Dataframe com os dados necessários para o cálculo
            - op: Tipo de operação que precisa ser calculado
                'avg_time': Calcula o tempo médio
                'std_time': Calcula o desvio padrão do tempo
        Output:
            - df: Dataframe com 2 colunas e 1 linha
    """
    df_aux = ( df1.loc[:, ['Time_taken(min)', 'Festival']]
                  .groupby( 'Festival' )
                  .agg( {'Time_taken(min)': ['mean', 'std']}) )

    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    df_aux = np.round(df_aux.loc[df_aux['Festival'] == festival, op], 2)

    return df_aux

def distance( df1, fig ):
    if fig == False:
        cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude' ]
        df1['distance(km)'] = df1[cols].apply(lambda x:
                                              haversine((x['Restaurant_latitude'], x['Restaurant_longitude']),
                                                        (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1 )
    
        avg_distance = np.round(df1['distance(km)'].mean(), 2)        
        return avg_distance
    else:
        cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude' ]
        df1['distance(km)'] = df1[cols].apply(lambda x:
                                              haversine((x['Restaurant_latitude'], x['Restaurant_longitude']),
                                                        (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1 )
    
        avg_distance = df1.loc[:, [ 'City', 'distance(km)']].groupby('City').mean().reset_index()
        fig = go.Figure( data=[ go.Pie( labels=avg_distance['City'], values=avg_distance['distance(km)'], pull=[0, 0.1, 0])])
        return fig

# ===================================
# Limpeza nos dados
# ===================================
df1 = df.copy()

# 1. convertendo a coluna Delivery_person_Age de texto para número
# Remove espaços e padroniza como string
linhas_selecionadas = (df1['Delivery_person_Age'] != 'NaN ' )
df1 = df1.loc[linhas_selecionadas, :].copy()

linhas_selecionadas = (df1['Road_traffic_density'] != 'NaN ' )
df1 = df1.loc[linhas_selecionadas, :].copy()

linhas_selecionadas = (df1['City'] != 'NaN ' )
df1 = df1.loc[linhas_selecionadas, :].copy()

linhas_selecionadas = (df1['Festival'] != 'NaN ' )
df1 = df1.loc[linhas_selecionadas, :].copy()

df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)

# 2. convertendo a coluna Delivery_person_Ratings de texto para numero decinal (float)
df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)

# 3. convertendo a coluna Order_Date de texto para data
df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')

# 4. convertendo a coluna multiple_deliveries de testo para numero inteiro (int)
linhas_selecionadas = (df1['multiple_deliveries'] != 'NaN ' )
df1 = df1.loc[linhas_selecionadas, :].copy()

## 5. Removendo os espaços dentro de strings/texto/object
#df1 = df1.reset_index(drop=True)
#for i in range(len(df1)):
#    df1.loc[i, 'ID'] = df1.loc[i, 'ID'].strip()

# 6. Removendo os espaços dentro de strings/texto/object
df1.loc[:, 'ID'] = df1.loc[:,'ID'].str.strip()
df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()

# Limpando a colunas Time_taken
df1['Time_taken(min)'] = df1['Time_taken(min)'].apply( lambda x: x.split( '(min)')[1] )
df1['Time_taken(min)'] = df1['Time_taken(min)'].astype( int )

# ====================================================================
# Barra Lateral
# Ver documentos e escolher o que quer usar https://docs.streamlit.io
# ====================================================================

st.sidebar.markdown(
    """
    ### 🔗 Acesso Rápido às Páginas
    - [📊 Home](./Home.py)
    - [📊 Visão da Empresa](./pages/1_visao_empresa.py)
    - [🛵 Visão dos Entregadores](./pages/2_visao_entregadores.py)
    - [🍽️ Visão dos Restaurantes](./pages/3_visao_restaurantes.py)
    """)


st.header("Marketplace - Visão Restaurantes")

image_path = 'image/Curry_companhy.jpg'
image = Image.open(image_path)
st.sidebar.image(image, width=60)

st.sidebar.markdown('# Curry Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.sidebar.markdown('## Selecione a data limite')

date_slider = st.sidebar.slider(
    'Até qual valor?',
    value=datetime(2022, 4, 6),          # precisa estar entre min e max
    min_value=datetime(2022, 2, 11),
    max_value=datetime(2022, 4, 13),
    format='DD-MM-YYYY'
)

# st.header(date_slider.strftime('%d-%m-%Y'))
st.sidebar.markdown("""---""")

traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito?',
    ['Low', 'Midium', 'High', 'Jam'],
    default=['Low', 'Midium', 'High', 'Jam'])

st.sidebar.markdown("""---""")
st.sidebar.markdown('#### Powerred by Comunidade DS')

# Filtros de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de trâsito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

# =====================================================================
# layout no Streamlit
# Ver documentos e escolher o que quer usar https://docs.streamlit.io
# =====================================================================

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '_', '_'])

with tab1:
    with st.container():
        st.markdown("### Overal Metrics")

        col1, col2, col3, col4, col5, col6 = st.columns(6)

        with col1:
            delivery_unique = len(df1.loc[:, 'Delivery_person_ID'].unique())
            col1.metric('Entregadores únicos', delivery_unique)

        with col2:
            avg_distance = distance( df1, fig = False )
            col2.metric('Distância Média Entregas', avg_distance)
  
        with col3:
            df_aux = avg_std_time_delivery( df1, 'Yes', 'avg_time' )
            col3.metric('Tempo Médio Entregas c/ Festival', df_aux)    
        
        with col4:
            df_aux = avg_std_time_delivery( df1, 'Yes', 'std_time' )
            col4.metric('STD Médio c/ Festival', df_aux)
          
        with col5:
            df_aux = avg_std_time_delivery( df1, 'No', 'avg_time' )
            col5.metric('Tempo Médio Entregas s/ Festival', df_aux)
          
        with col6:
            df_aux = avg_std_time_delivery( df1, 'No', 'std_time' )
            col6.metric('Desvio Padrão das Entregas s/ Festival', df_aux)  
            
    with st.container():
        st.markdown("""---""")        
        col1, col2 = st.columns(2)
        with col1:
            fig = avg_std_time_graph( df1 )
            st.plotly_chart( fig )

        with col2:
            st.markdown("### Tempo médio e Desvio Padrão por Entrega por Pedido")
            df_aux = ( df1.loc[:, ['City', 'Time_taken(min)', 'Type_of_order']]
                          .groupby( ['City', 'Type_of_order'] )
                          .agg( {'Time_taken(min)': ['mean', 'std']}) )
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
            st.dataframe( df_aux )
                
    with st.container():
        st.markdown("""---""")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Distribuição do tempo Entregas por cidade")
            fig = distance( df1, fig = True )
            st.plotly_chart( fig )

        with col2:
            st.markdown("### Distribuição do tempo Entregas por Cidade e por Tráfego")
            fig = avg_std_time_on_traffic( df1 )
            st.plotly_chart( fig )

