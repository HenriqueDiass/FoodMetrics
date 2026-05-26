import streamlit as st
import requests
import pandas as pd
from utils import bloqueio_api_offline, exibir_status_sidebar

st.set_page_config(page_title="Comidas", page_icon="🍔")
exibir_status_sidebar()
bloqueio_api_offline()

st.title("🍔 Cadastrar Comida Base")

API_COMIDAS = "http://127.0.0.1:8000/comidas"

with st.form("form_comida"):
    nome = st.text_input("Nome do Alimento", placeholder="Ex: Arroz Branco")
    categoria = st.selectbox("Categoria", ["Cozinha Quente", "Cozinha Fria", "Bebidas", "Hortifruti", "Outros"])
    custo = st.number_input("Custo Unitário por Kg (R$)", min_value=0.1, step=0.5)
    submit = st.form_submit_button("Salvar no Cardápio", type="primary")

    if submit:
        payload = {"nome": nome, "categoria": categoria, "custo_unitario": custo}
        resp = requests.post(API_COMIDAS, json=payload)
        if resp.status_code in [200, 201]:
            st.success(f"✅ {nome} cadastrado com sucesso!")
        else:
            st.warning("Erro ao cadastrar.")

st.divider()

st.subheader("Cardápio Atual")
resp = requests.get(API_COMIDAS)
if resp.status_code == 200 and resp.json():
    df = pd.DataFrame(resp.json())
    st.dataframe(df[["id", "nome", "categoria", "custo_unitario"]], hide_index=True)
else:
    st.info("Nenhum alimento cadastrado ainda.")
