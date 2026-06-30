import streamlit as st
from utils.login import tela_login
from utils.cadastro import tela_cadastro 

st.set_page_config(page_title="FoodMetrics", page_icon="🍔", layout="wide")

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if "tela_auth" not in st.session_state:
    st.session_state.tela_auth = "login"

# 2. Lógica de Roteamento (Navegação)
if not st.session_state.autenticado:
    # Alterna entre Login e Cadastro dependendo do estado atual
    if st.session_state.tela_auth == "login":
        auth_page = st.Page(tela_login, title="Login", icon="🔐")
    else:
        auth_page = st.Page(tela_cadastro, title="Cadastro", icon="📝")
    
    pg = st.navigation([auth_page])

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
            st.session_state.tela_auth = "login" 
            st.rerun()

# 3. Executa a navegação configurada
pg.run()