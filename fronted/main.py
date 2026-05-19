import streamlit as st
import pandas as pd


st.set_page_config(page_title="FoodMetrics - Painel", page_icon="📊", layout="wide")

st.title("📊 Painel do Restaurante")
st.write("Resumo diário do controle de desperdício.")


col1, col2, col3 = st.columns(3)
col1.metric("Total Desperdiçado Hoje", "12.5 kg", "-1.2 kg")
col2.metric("Prejuízo Estimado", "R$ 150,00", "-R$ 20,00")
col3.metric("Setor Crítico", "Cozinha Quente", None)

st.divider()

st.subheader("📋 Últimos Registros")


dados_mock = pd.DataFrame({
    "Data": ["19/05/2026", "19/05/2026", "18/05/2026"],
    "Produto": ["Arroz Branco", "Carne Bovina", "Salada"],
    "Peso (kg)": [2.5, 1.2, 0.8],
    "Motivo": ["Sobras da rampa", "Queima", "Vencimento"]
})


st.dataframe(dados_mock, use_container_width=True, hide_index=True)


st.error("🚨 Erro de Conexão: Backend offline. Exibindo dados locais.")
