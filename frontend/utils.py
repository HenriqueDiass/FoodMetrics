import requests
import streamlit as st

API_BASE_URL = "http://127.0.0.1:8000"

def verificar_status_api():
    try:
        response = requests.get(f"{API_BASE_URL}/comidas", timeout=2)
        if response.status_code == 200:
            return True
    except:
        pass
    return False

def exibir_status_sidebar():
    online = verificar_status_api()
    if online:
        st.sidebar.success("● API Online")
    else:
        st.sidebar.error("● API Offline")
    return online

def bloqueio_api_offline():
    if not verificar_status_api():
        st.error("### 🚨 O sistema está temporariamente indisponível")
        st.info("Não conseguimos conectar ao servidor do FoodMetrics. Isso pode acontecer se o backend estiver desligado ou em manutenção.")
        st.markdown("""
        **Como resolver:**
        1. Abra o terminal na pasta do projeto.
        2. Execute o comando: `uvicorn backend.main:app --reload`
        3. Atualize esta página.
        """)
        st.stop() 
