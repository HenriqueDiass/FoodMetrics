import streamlit as st
import requests
from utils import bloqueio_api_offline, exibir_status_sidebar

st.set_page_config(page_title="Registrar Desperdício", page_icon="🗑️")
exibir_status_sidebar()
bloqueio_api_offline()

st.title("🗑️ Registrar Desperdício")

API_COMIDAS = "http://127.0.0.1:8000/comidas"
API_DESPERDICIOS = "http://127.0.0.1:8000/desperdicios"

resp_comidas = requests.get(API_COMIDAS)
lista_comidas = resp_comidas.json() if resp_comidas.status_code == 200 else []

if not lista_comidas:
    st.warning("⚠️ Cadastre Alimentos na aba 'Comidas' antes de registrar o desperdício!")
else:
    
    opcoes_comidas = {item["nome"]: item["id"] for item in lista_comidas}

    with st.form("form_desperdicio"):
        nome_selecionado = st.selectbox("Qual alimento sobrou?", options=list(opcoes_comidas.keys()))
        quantidade = st.number_input("Peso desperdiçado (kg)", min_value=0.1, step=0.1)
        setor = st.selectbox("Setor de Origem", ["Cozinha Quente", "Cozinha Fria", "Salão", "Estoque"])
        motivo = st.selectbox("Motivo do Descarte", ["Sobras de produção", "Passou da validade", "Erro de preparo", "Sobras de cliente"])
        obs = st.text_input("Observações Adicionais (Opcional)")

        submit = st.form_submit_button("Registrar Perda", type="primary")

        if submit:
            payload = {
                "comida_id": opcoes_comidas[nome_selecionado],
                "quantidade": quantidade,
                "setor": setor,
                "motivo": motivo,
                "observacao": obs if obs else None
            }
            res = requests.post(API_DESPERDICIOS, json=payload)
            if res.status_code in [200, 201]:
                st.success("✅ Desperdício registrado com sucesso no banco!")
            else:
                st.error("Erro ao registrar.")
