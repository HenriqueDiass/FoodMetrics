import streamlit as st
import requests

st.set_page_config(page_title="Registrar Desperdício", page_icon="⚖️")

st.title("⚖️ Registrar Desperdício")
st.write("Preencha os dados abaixo para registrar uma nova perda de insumo.")

# Criando um formulário organizado
with st.form("form_registro"):
    col1, col2 = st.columns(2)
    
    with col1:
        produto = st.text_input("Nome do Produto", placeholder="Ex: Arroz, Feijão, Carne...")
        peso = st.number_input("Peso desperdiçado (kg)", min_value=0.0, step=0.1)
        
    with col2:
        setor = st.selectbox("Setor de Origem", ["Cozinha Quente", "Cozinha Fria", "Estoque", "Salão"])
        motivo = st.selectbox("Motivo do Descarte", ["Sobras de produção", "Passou da validade", "Erro de preparo", "Outros"])
        
    observacao = st.text_area("Observações Adicionais (Opcional)")
    
    # Botão de salvar
    submit = st.form_submit_button("Salvar Registro", type="primary")
    
    if submit:
        # Tratamento de erros do frontend (Regra do Professor)
        try:
            # Tenta mandar pro backend fantasma
            resposta = requests.post("http://localhost:8000/api", timeout=1)
        except requests.exceptions.RequestException:
            st.error("🚨 Falha ao salvar: O servidor backend não está respondendo.")