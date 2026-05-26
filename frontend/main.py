import streamlit as st
import os
from utils import exibir_status_sidebar


st.set_page_config(
    page_title="FoodMetrics - Início",
    layout="wide"
)

api_online = exibir_status_sidebar()

PALETA_FOODMETRICS = ["#123258", "#2a91d3", "#53a458", "#50626e"]
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_logo = os.path.join(diretorio_atual, "data", "logo.png")



col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.image(caminho_logo, use_container_width=True)

st.markdown("<h1 style='text-align: center;'>Gestão Inteligente de Desperdício</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2rem;'>Transformando sobras em economia e sustentabilidade.</p>", unsafe_allow_html=True)
st.divider()


col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown("### 🍔 Comida")
    st.markdown("Gerencie o cadastro de produtos e seus custos.")
    if st.button("Acessar Cardápio", use_container_width=True):
        st.switch_page("pages/comidas.py")

with col_b:
    st.markdown("### 🗑️ Registro")
    st.markdown("Lance os desperdícios ocorridos em tempo real.")
    if st.button("Registrar Perda", use_container_width=True):
        st.switch_page("pages/desperdicio.py")

with col_c:
    st.markdown("### 📊 Dashboards")
    st.markdown("Visualize o impacto financeiro e operacional.")
    if st.button("Ver Relatórios", use_container_width=True):
        st.switch_page("pages/dashboards.py")
