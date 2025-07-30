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
# Ajusta a largura da página de apresentação
# ------------------
st.set_page_config(
    page_title="Visão Entregadores",
    page_icon="🚚",
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
def top_delivers( df1, top_asc ):                
    df2 = ( df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']]
               .groupby( ['City', 'Delivery_person_ID'] )
               .max().sort_values(['City', 'Time_taken(min)'], ascending=top_asc)
               .reset_index() )

    df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
    df_aux02 = df2.loc[df2['City'] == 'Urban', :].head(10)
    df_aux03 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)

    df3 = pd.concat( [df_aux01, df_aux02, df_aux03] ).reset_index( drop=True)

    return df3

# ------------------ Início da estrutura lógica do código ---------------------
# ------------------
# Import Dataset
# ------------------
df = pd.read_csv("dataset/train.csv")

# ------------------
# limpando os dados
# ------------------
df1 = clean_code( df )

# ------------------
# Barra Lateral
# ------------------

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

# ------------------
# layout no Streamlit
# Ver documentos e escolher o que quer usar https://docs.streamlit.io
# ------------------
st.header("Marketplace - Visão Entregadores")

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '_', '_'])

with tab1:
    with st.container():
        st.title('Overall Metrics')

        col1, col2, col3, col4 = st.columns(4, gap='large')
        with col1:
            # A maior idade dos entregadores
            #st.subheader('Maior de idade')
            maior_idade = df1.loc[:, 'Delivery_person_Age'].max()
            col1.metric('Maior idade', maior_idade)

        with col2:
            # A menor idade dos entregadores
            #st.subheader('Menor de idade')        
            menor_idade = df1.loc[:, 'Delivery_person_Age'].min()
            col2.metric('Menor idade', menor_idade)

        with col3:
            # A melhor condição de veículo            
            #st.subheader('Melhor condição de veículo')
            melhor_condicao = df1.loc[:, 'Vehicle_condition'].max()
            col3.metric('Melhor condição de veículo', melhor_condicao)

        with col4:
            # A pior condição de veículo            
            #st.subheader('Pior condição de veículo')
            pior_condicao = df1.loc[:, 'Vehicle_condition'].min()
            col4.metric('Pior condição de veículo', pior_condicao)
    
    with st.container():
        st.markdown("""---""")
        st.title('Avaliações')

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('##### Avaliações média por entregador')
            df_avg_ratings_per_deliver = ( df1.loc[:, ['Delivery_person_Ratings', 'Delivery_person_ID']]
                                              .groupby('Delivery_person_ID')
                                              .mean()
                                              .reset_index() )
            st.dataframe(df_avg_ratings_per_deliver)

        with col2:
            st.markdown('##### Avaliação média por transito') 
            # Com a função agregação (agg)
            df_avg_std_rating_by_traffic = ( df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density' ]]
                                                .groupby('Road_traffic_density')
                                                .agg( {'Delivery_person_Ratings': ['mean', 'std']} ))

            # Mudança de nome das colunas
            df_avg_std_rating_by_traffic.columns = ['delivery_mean','delivery_std']

            # Reset do index
            df_avg_std_rating_by_traffic = df_avg_std_rating_by_traffic.reset_index()

            st.dataframe(df_avg_std_rating_by_traffic)

            
            st.markdown('##### Avaliação média por clima')
            # Com a função agregação (agg)
            df_avg_std_rating_by_Weatherconditions = ( df1.loc[:, ['Delivery_person_Ratings', 'Weatherconditions' ]]
                                                          .groupby('Weatherconditions')
                                                          .agg( {'Delivery_person_Ratings': ['mean', 'std']} ))

            # Mudança de nome das colunas
            df_avg_std_rating_by_Weatherconditions.columns = ['delivery_mean','delivery_std']

            # Reset do index
            df_avg_std_rating_by_Weatherconditions = df_avg_std_rating_by_Weatherconditions.reset_index()

            st.dataframe(df_avg_std_rating_by_Weatherconditions)



    with st.container():
        st.markdown("""---""")
        st.title('Velocidade de entrega')

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('##### Top entregadores mais rápidos')
            df3 = top_delivers( df1, top_asc=True )
            st.dataframe(df3)
          
        with col2:
            st.markdown('##### Top entregadores mais lentos')
            df3 = top_delivers( df1, top_asc=False )
            st.dataframe(df3)
