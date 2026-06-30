import streamlit as st
import os
import base64


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
    

def tela_login():
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
        padding: 2.5rem 2rem;
        border-radius: 0 0 24px 24px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        border: none;
        margin-top: -5px;
        position: relative;
        z-index: 0;
    }
    
    /* Botão verde do FoodMetrics */
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
            
            # Top card gradient (Azul claro para Azul Escuro)
            top_card_html = "<div style='background: linear-gradient(135deg, #53a458 0%, #123258 100%); padding: 3rem 2rem 2rem 2rem; border-radius: 12px 12px 0 0; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.3); position: relative; z-index: 1;'>"
            
            if logo_b64:
                top_card_html += f"<div style='background-color: white; padding: 12x 24px; border-radius: 16px; display: inline-block; margin-bottom: 2rem;'><img src='data:image/png;base64,{logo_b64}' style='width: 350px;'></div>"
            else:
                top_card_html += "<div style='color: white; margin-bottom: 2rem; font-size: 1.5rem; font-weight: bold;'>FOODMETRICS</div>"
                
            top_card_html += "<div style='color: #ffffff; font-size: 1.8rem; font-weight: bold; margin-top: 0; margin-bottom: 0.5rem;'>FOODMETRICS</div>"
            top_card_html += "<div style='color: #E2E8F0; font-size: 1.1rem; font-weight: normal; margin-top: 0; line-height: 1.4;'>Gestão Inteligente de Desperdício</div>"
            top_card_html += "<p style='font-size: 0.85rem; color: #CBD5E1; margin-top: 2rem; margin-bottom: 0;'>Transformando sobras em economia</p>"
            top_card_html += "</div>"
            
            st.markdown(top_card_html, unsafe_allow_html=True)
            
            with st.form("login_form"):
                usuario = st.text_input("E-mail", placeholder="usuario@gmail.com")
                senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")
                
                submitted = st.form_submit_button("Entrar no sistema", use_container_width=True)

                col_vazia, col_link = st.columns([2.1, 1.8])
                with col_link:
                    btn_login = st.form_submit_button("Não tem uma conta? Cadastre-se")

                if submitted:
                    import requests
                    
                    if not usuario or not senha:
                        st.warning("Por favor, preencha e-mail e senha.")
                    else:
                        try:
                            # Chama a API de login
                            # NOTA: Mesmo sendo o e-mail do usuário, a chave AQUI precisa 
                            # continuar como "username" para o FastAPI aceitar.
                            response = requests.post(
                                "http://127.0.0.1:8000/token",
                                data={"username": usuario, "password": senha}
                            )
                            
                            if response.status_code == 200:
                                dados = response.json()
                                st.session_state.autenticado = True
                                # Salva o token na sessão para usar nas próximas requisições protegidas
                                st.session_state.token = dados["access_token"]
                                st.success("Login aprovado!")
                                st.rerun()
                            else:
                                st.error("E-mail ou senha incorretos.")
                        except requests.exceptions.ConnectionError:
                            st.error("Não foi possível conectar ao servidor. O backend está rodando?")
                            
            # Esta verificação precisa ficar fora do 'if submitted' mas dentro do 'with col2:'
            if btn_login:
                st.session_state.tela_auth = "cadastro"
                st.rerun()

    
    st.write("")