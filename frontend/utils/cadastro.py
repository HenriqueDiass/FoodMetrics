import streamlit as st
import os
import base64
import requests

def get_logo_base64():
    """Lê a logo local e converte para base64 para uso no HTML/CSS."""
    diretorio_atual = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    caminho_logo = os.path.join(diretorio_atual, "data", "logo.png")
    
    try:
        with open(caminho_logo, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return encoded_string
    except FileNotFoundError:
        return ""

def tela_cadastro():
    if st.session_state.get("autenticado", False):
        return
        
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #123258 10%, #53a458 90%) !important;
    }
    
    header { visibility: hidden; }
    
    div[data-testid="column"] > div > div > div > div.element-container {
        margin-bottom: 0 !important;
    }

    div[data-testid="stForm"] {
        background-color: #ffffff;
        padding: 2.5rem 2rem 3rem 2rem;
        border-radius: 0 0 24px 24px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        border: none;
        margin-top: -5px;
        position: relative;
        z-index: 0;
    }
    
    /* 1. SEU BOTÃO VERDE ORIGINAL (Mantido exatamente como você fez) */
    div[data-testid="stFormSubmitButton"] button {
        background-color: #53a458 !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.5rem !important;
        margin-top: 1rem !important;
        border: none !important;
        transition: 0.2s !important;
    }
    div[data-testid="stFormSubmitButton"] button:hover {
        background-color: #418245 !important;
        transform: translateY(-2px) !important;
    }

    /* 2. O BOTÃO DE TEXTO (Isolado no CSS por estar dentro de uma coluna interna do form) */
    div[data-testid="column"] div[data-testid="column"] div[data-testid="stFormSubmitButton"] {
        display: flex;
        justify-content: flex-end;
    }
    
    div[data-testid="column"] div[data-testid="column"] div[data-testid="stFormSubmitButton"] button {
        background-color: transparent !important;
        color: #64748b !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin-top: 0.5rem !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
    }
    
    div[data-testid="column"] div[data-testid="column"] div[data-testid="stFormSubmitButton"] button:hover {
        background-color: transparent !important;
        color: #123258 !important;
        text-decoration: underline !important;
        transform: none !important;
    }

    div[data-testid="InputInstructions"] {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1.5, 2.0, 1.5])
        with col2:
            st.write("")
            st.write("")
            
            logo_b64 = get_logo_base64()
            
            # Top card gradient
            top_card_html = "<div style='background: linear-gradient(135deg, #53a458 0%, #123258 100%); padding: 3rem 2rem 2rem 2rem; border-radius: 12px 12px 0 0; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.3); position: relative; z-index: 1;'>"
            
            if logo_b64:
                top_card_html += f"<div style='background-color: white; padding: 12px 24px; border-radius: 16px; display: inline-block; margin-bottom: 2rem;'><img src='data:image/png;base64,{logo_b64}' style='width: 350px;'></div>"
            else:
                top_card_html += "<div style='color: white; margin-bottom: 2rem; font-size: 1.5rem; font-weight: bold;'>FOODMETRICS</div>"
                
            top_card_html += "<div style='color: #ffffff; font-size: 1.8rem; font-weight: bold; margin-top: 0; margin-bottom: 0.5rem;'>CRIAR CONTA</div>"
            top_card_html += "<div style='color: #E2E8F0; font-size: 1.1rem; font-weight: normal; margin-top: 0; line-height: 1.4;'>Junte-se ao FoodMetrics</div>"
            top_card_html += "</div>"
            
            st.markdown(top_card_html, unsafe_allow_html=True)
            
            with st.form("cadastro_form"):
                nome = st.text_input("Nome Completo", placeholder="Seu nome")
                email = st.text_input("E-mail", placeholder="seu@email.com")
                senha = st.text_input("Senha", type="password", placeholder="Crie uma senha")
                confirma_senha = st.text_input("Confirmação de Senha", type="password", placeholder="Repita a senha")
                
                submitted = st.form_submit_button("Cadastrar", use_container_width=True)
                
                col_vazia, col_link = st.columns([2.5, 1.8])
                with col_link:
                    btn_login = st.form_submit_button("Já tem uma conta? Faça login")
                
                if submitted:
                    if not nome or not email or not senha or not confirma_senha:
                        st.warning("Por favor, preencha todos os campos.")
                    elif senha != confirma_senha:
                        st.error("As senhas não coincidem. Tente novamente.")
                    else:
                        try:
                            # 1. Definir a URL da sua API
                            api_url = "http://127.0.0.1:8000/usuarios"
                            
                            # 2. Montar o payload (corpo da requisição) igual ao esperado pelo FastAPI
                            payload = {
                                "nome": nome,
                                "email": email,
                                "senha": senha
                            }
                            
                            # 3. Fazer a requisição POST
                            resposta = requests.post(api_url, json=payload)
                            
                            # 4. Verificar o status da resposta
                            if resposta.status_code in [200, 201]:
                                st.success("Conta criada com sucesso! Redirecionando para o login...")
                                # Opcional: Redireciona automaticamente para a tela de login
                                st.session_state.tela_auth = "login"
                                st.rerun()
                            else:
                                # Tenta pegar a mensagem de erro que o FastAPI retorna (ex: Email já cadastrado)
                                try:
                                    erro_detalhe = resposta.json().get("detail", "Erro desconhecido ao cadastrar.")
                                except:
                                    erro_detalhe = resposta.text
                                st.error(f"Erro ao criar conta: {erro_detalhe}")
                                
                        except requests.exceptions.ConnectionError:
                            st.error("Não foi possível conectar ao servidor.")
                # Ação do botão que parece um texto
                if btn_login:
                    st.session_state.tela_auth = "login"
                    st.rerun()
                
    st.write("")