# ===================================================================
# Comunidade Data Scienc - ComunidadeDS - https://comunidadeds.com/

# Curso Analista de Dados
# Ciclo 07 - Modularizando o código, criando funções
# Professor: Meigarom Lopes
# Aluno: Alfredo Junior Albieri
# Ano letivo: 2025
# ===================================================================

# ===================
# Libraries
# ===================
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go

# ===================
# Bibliotecas
# ===================
import folium
import haversine
import pandas as pd 
import numpy as np
from datetime import datetime
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static

# ------------------
# Ajusta a largura da página de aapresentação
# ------------------
st.set_page_config(
    page_title="Visão Empresa",
    layout="wide",          # valores: "centered" ou "wide"
    initial_sidebar_state="expanded"  # ou "collapsed"
)

# ===================================
# Funções
# ===================================
# Limpeza dos dados
def clean_code( df1 ):
    """ Esta função tem a responsabilidade de limpar o dataframe

        Tipos de limpeza:
        1. Remoção dos NaN
        2. Mudança do tipo da coluna de dados
        3. Remoção dos espaços das variáveis de texto
        4. Formatação da coluna de datas
        5. Limpeza da coluna de tempo (remoção do texto da variável numérica)

        Input: Dataframe
        Output: Dataframe
    """
    # 1. convertendo a coluna Age de texto para número
    linhas_selecionadas = (df1['Delivery_person_Age'] != 'NaN ' )
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    linhas_selecionadas = (df1['Road_traffic_density'] != 'NaN ' )
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    linhas_selecionadas = (df1['City'] != 'NaN ' )
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    linhas_selecionadas = (df1['Festival'] != 'NaN ' )
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)
    
    # 2. convertendo a coluna Ratings de texto para numero decinal (float)
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)
    
    # 3. convertendo a coluna Order_Date de texto para data
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')
    
    # 4. convertendo a coluna multiple_deliveries de texto para numero inteiro (int)
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

    return df1

# Funções das Metricas do negócio ---------------------------------------
def order_metric( df1 ):
    columns = ['ID', 'Order_Date']
    # seleção de linhas
    df_aux = ( df1.loc[:, columns]
                  .groupby('Order_Date')
                  .count()
                  .reset_index() )
    # Desenhar gráfico de linhas
    fig = px.bar(df_aux, x='Order_Date', y='ID')
    return fig

def traffic_order_share( df1 ):
    df_aux = ( df1.loc[:,['ID', 'Road_traffic_density']]
                  .groupby('Road_traffic_density')
                  .count()
                  .reset_index() )
    # Calcula o percentual
    df_aux['entregas_perc'] = df_aux['ID'] / df_aux['ID'].sum()    
    # Criar o gráfico de pizza
    fig = px.pie(df_aux, values= 'entregas_perc', names='Road_traffic_density')
    return fig
                            
def traffic_order_city ( df1 ):
    df_aux = ( df1.loc[:, ['ID', 'City', 'Road_traffic_density']]
                  .groupby(['City', 'Road_traffic_density'])
                  .count()
                  .reset_index() )    
    # criar o gráfico de bolhas
    fig = px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID', color='City')
    return fig

def order_by_week( df1 ):
    # criar a coluna de semana
    df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U')  
    df_aux = ( df1.loc[:, ['ID', 'week_of_year']]
                  .groupby('week_of_year')
                  .count()
                  .reset_index() )
    # criar o gráfico de linhas
    fig = px.line(df_aux, x='week_of_year', y='ID')
    return fig

def order_share_by_week( df1 ):
    df_aux01 = df1.loc[:, ['ID', 'week_of_year',]].groupby('week_of_year').count().reset_index()
    df_aux02 = ( df1.loc[:, ['Delivery_person_ID', 'week_of_year',]]
                    .groupby('week_of_year')
                    .nunique()
                    .reset_index() )    
    # juntar 2 dataframe
    df_aux = pd.merge(df_aux01, df_aux02, how='inner')
    # Cálculo
    df_aux['order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']    
    # criar o gráfico
    fig = px.line(df_aux, x='week_of_year', y='order_by_deliver')
    return fig

def country_maps( df1 ):
    df_aux = ( df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']]
                  .groupby(['City', 'Road_traffic_density'])
                  .median()
                  .reset_index() )

    map = folium.Map()        
    # desenhar mapa e colocar ponto no mapa
    for index, location_info in df_aux.iterrows():
        folium.Marker([location_info['Delivery_location_latitude'], 
                      location_info['Delivery_location_longitude']],
                      popup=location_info[['City', 'Road_traffic_density']] ).add_to(map)

    folium_static(map, width=1024, height=600)

# ------------------ Início da estrutura lógica do código ---------------------
# ------------------
# Import Dataset
# ------------------
df = pd.read_csv("dataset/train.csv")

# ------------------
# limpando os dados
# ------------------
df1 = clean_code( df )

# ====================================================================
# Barra Lateral
# ====================================================================

st.sidebar.markdown(
    """
    ### 🔗 Acesso Rápido às Páginas
    - [📊 Home](./Home.py)
    - [📊 Visão da Empresa](./pages/1_visao_empresa.py)
    - [🛵 Visão dos Entregadores](./pages/2_visao_entregadores.py)
    - [🍽️ Visão dos Restaurantes](./pages/3_visao_restaurantes.py)
    """)

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

# Filtro de trânsito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

# =====================================================================
# layout com Streamlit
# =====================================================================
st.header("Marketplace - Visão Cliente")

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
    with st.container():
        # Order Metric   
        st.markdown('# Orders by Day')
        fig = order_metric( df1 )
        st.plotly_chart(fig, use_container_width=True)
    
    with st.container():
        col1, col2 = st.columns(2)
        with col1:            
            st.markdown('## Traffic Order Share')
            fig = traffic_order_share( df1 )
            st.plotly_chart(fig, use_container_width=True)
          
        with col2:
            st.markdown('## Traffic Order City')
            fig = traffic_order_city( df1 )            
            st.plotly_chart(fig, use_container_width=True)             

with tab2:
    with st.container():
        st.markdown('## Order by Week')
        fig = order_by_week( df1 )
        st.plotly_chart(fig, use_container_width=True) 

    with st.container():
        st.markdown('## Order Share by Week')
        fig = order_share_by_week( df1 )
        st.plotly_chart(fig, use_container_width=True)       

with tab3:
    st.markdown('## Country Maps')
    country_maps( df1 )

#print('===> Estou aqui <===')