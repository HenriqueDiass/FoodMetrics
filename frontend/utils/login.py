import streamlit as st
import os
import base64
import requests

def get_logo_base64():
    diretorio_atual = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    caminho_logo = os.path.join(diretorio_atual, "data", "logo.png")
    try:
        with open(caminho_logo, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        return ""

def tela_login():
    # --- Lógica de Toasts na Tela de Login ---
    if "toast_sucesso" in st.session_state:
        st.toast(st.session_state.toast_sucesso, icon="✅")
        del st.session_state.toast_sucesso
    if "toast_erro" in st.session_state:
        st.toast(st.session_state.toast_erro, icon="🔴")
        del st.session_state.toast_erro

    if st.session_state.get("autenticado", False):
        return
        
    if "tela_auth" not in st.session_state:
        st.session_state.tela_auth = "login"

    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background: linear-gradient(135deg, #123258 10%, #53a458 90%) !important; }
    header { visibility: hidden; }
    
    div[data-testid="stForm"] {
        background-color: #ffffff;
        padding: 2.5rem 2rem;
        border-radius: 0 0 24px 24px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        border: none;
        margin-top: -15px;
    }
    
    div[data-testid="stFormSubmitButton"] button { border-radius: 8px !important; font-weight: 600 !important; }
    div[data-testid="stFormSubmitButton"] button[kind="primary"] { background-color: #53a458 !important; color: white !important; border: none !important; }
    div[data-testid="stFormSubmitButton"] button[kind="primary"]:hover { background-color: #418245 !important; transform: translateY(-2px) !important; }
    div[data-testid="stFormSubmitButton"] button[kind="secondary"] { background-color: transparent !important; color: #123258 !important; border: 2px solid #123258 !important; }
    div[data-testid="stFormSubmitButton"] button[kind="secondary"]:hover { background-color: #f0f5fa !important; transform: translateY(-2px) !important; }
    </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1.5, 2.0, 1.5])
        with col2:
            st.write("") 
            logo_b64 = get_logo_base64()
            
            top_card_html = "<div style='background: linear-gradient(135deg, #53a458 0%, #123258 100%); padding: 3rem 2rem 1rem 2rem; border-radius: 12px 12px 0 0; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.3); position: relative; z-index: 2;'>"
            if logo_b64:
                top_card_html += f"<div style='background-color: white; padding: 12px 24px; border-radius: 16px; display: inline-block; margin-bottom: 1rem;'><img src='data:image/png;base64,{logo_b64}' style='width: 250px;'></div>"
            top_card_html += "<div style='color: #ffffff; font-size: 1.5rem; font-weight: bold;'>FOODMETRICS</div></div>"
            st.markdown(top_card_html, unsafe_allow_html=True)
            
            # ======== TELA DE LOGIN ========
            if st.session_state.tela_auth == "login":
                with st.form("form_login"):
                    st.markdown("<h4 style='text-align: center; color: #123258; margin-bottom: 1rem;'>Entrar</h4>", unsafe_allow_html=True)
                    usuario = st.text_input("Email", placeholder="Seu email cadastrado")
                    senha = st.text_input("Senha", type="password", placeholder="Sua senha")
                    
                    st.write("") 
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        submitted_login = st.form_submit_button("Entrar", type="primary", use_container_width=True)
                    with col_btn2:
                        ir_cadastro = st.form_submit_button("Criar Conta", type="secondary", use_container_width=True)
                    
                    if submitted_login:
                        if not usuario or not senha:
                            st.warning("Preencha e-mail e senha.")
                        else:
                            try:
                                response = requests.post("http://127.0.0.1:8000/token", data={"username": usuario, "password": senha})
                                if response.status_code == 200:
                                    st.session_state.autenticado = True
                                    st.session_state.token = response.json()["access_token"]
                                    # GUARDA O TOAST NA MEMÓRIA PARA A PRÓXIMA TELA
                                    st.session_state.toast_sucesso = "Login realizado com sucesso! Bem-vindo(a)."
                                    st.rerun()
                                else:
                                    st.error("E-mail ou senha incorretos.")
                            except requests.exceptions.ConnectionError:
                                st.error("Não foi possível conectar ao servidor.")
                    
                    if ir_cadastro:
                        st.session_state.tela_auth = "cadastro"
                        st.rerun()

            # ======== TELA DE CADASTRO ========
            else:
                with st.form("form_cadastro"):
                    st.markdown("<h4 style='text-align: center; color: #123258; margin-bottom: 1rem;'>Nova Conta</h4>", unsafe_allow_html=True)
                    nome = st.text_input("Nome Completo")
                    email = st.text_input("Email")
                    senha = st.text_input("Senha", type="password")
                    confirma_senha = st.text_input("Confirmar Senha", type="password")
                    
                    st.write("") 
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        submitted_cadastro = st.form_submit_button("Cadastrar", type="primary", use_container_width=True)
                    with col_btn2:
                        ir_login = st.form_submit_button("Voltar", type="secondary", use_container_width=True)
                    
                    if submitted_cadastro:
                        if not nome or not email or not senha:
                            st.warning("Preencha todos os campos.")
                        elif senha != confirma_senha: 
                            st.error("As senhas não coincidem!")
                        else:
                            dados = {"nome": nome, "email": email, "senha": senha}
                            try:
                                resp = requests.post("http://127.0.0.1:8000/usuarios", json=dados)
                                if resp.status_code == 201:
                                    # GUARDA O TOAST E VOLTA PRA TELA DE LOGIN SOZINHO
                                    st.session_state.toast_sucesso = "Conta criada com sucesso! Verifique seu e-mail."
                                    st.session_state.tela_auth = "login"
                                    st.rerun()
                                elif resp.status_code == 400:
                                    st.toast('Erro: Email já existe.', icon='🔴')
                                    st.error("Este email já está cadastrado no sistema.")
                            except requests.exceptions.ConnectionError:
                                st.error("Não foi possível conectar ao servidor.")
                    
                    if ir_login:
                        st.session_state.tela_auth = "login"
                        st.rerun()