import streamlit as st
from utils.login import tela_login

st.set_page_config(page_title="FoodMetrics", page_icon="🍔", layout="wide")

# 1. Inicializa a "memória" de login
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

# 2. Lógica de Roteamento (Navegação)
if not st.session_state.autenticado:
    # Se NÃO estiver logado, a única página que o sistema enxerga é a tela de login
    login_page = st.Page(tela_login, title="Login", icon="🔐")
    pg = st.navigation([login_page])

else:
    # Se ESTIVER logado, mapeamos os arquivos da pasta "pages"
    pg_inicio = st.Page("pages/inicio.py", title="Início", icon="🏠")
    pg_dash = st.Page("pages/dashboards.py", title="Dashboards", icon="📊")
    pg_comidas = st.Page("pages/comidas.py", title="Comidas", icon="🍔")
    pg_desp = st.Page("pages/desperdicio.py", title="Desperdício", icon="🗑️")
    
    # Organiza o menu que aparecerá na barra lateral
    pg = st.navigation([pg_inicio, pg_dash, pg_comidas, pg_desp])
    
    # Adiciona um botão de Sair na barra lateral
    with st.sidebar:
        st.divider()
        if st.button("Sair do Sistema", use_container_width=True):
            st.session_state.autenticado = False
            st.rerun()

# 3. Executa a navegação configurada
pg.run()
