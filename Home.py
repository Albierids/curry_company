import streamlit as st
from PIL import Image

# ------------------
# Ajusta a largura da página de apresentação
# ------------------
st.set_page_config(
    page_title="Home",
    layout="wide",
    initial_sidebar_state="expanded"
)
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

st.write('# Curry Company Growth Dashboard')

# Texto de introdução
st.markdown(
    """
    Growth Dashboard foi construído para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.

    ### Como utilizar esse Growth Dashboard?
    - Visão Empresa:
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Tática: Indicadores semanais de crescimento.
        - Visão Geográfica: Insights de geolocalização.
    - Visão Entregador:
        - Acompanhamento dos indicadores semanais de crescimento.
    - Visão Restaurantes:
        - Indicadores semanais de crescimento dos restaurantes.



    ### Sugestões e Ajuda
    - Time de Data Science no Discord: @meigarom
    """
)