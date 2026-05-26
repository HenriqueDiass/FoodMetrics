import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from utils import bloqueio_api_offline, exibir_status_sidebar

st.set_page_config(page_title="Dashboard - FoodMetrics", page_icon="📊", layout="wide")
exibir_status_sidebar()
bloqueio_api_offline()

st.title("📊 Dashboard do Restaurante")

PALETA = ["#123258", "#2a91d3", "#53a458", "#50626e"]
API_DESPERDICIOS = "http://127.0.0.1:8000/desperdicios"

resposta = requests.get(API_DESPERDICIOS)

if resposta.status_code == 200:
    dados = resposta.json()
    
    if dados:
        df = pd.DataFrame(dados)
        
       
        df['Produto'] = df['comida'].apply(lambda x: x['nome'] if isinstance(x, dict) else 'Desconhecido')
        total_kg = df["quantidade"].sum()
        prejuizo = df["custo_estimado"].sum()
        
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Prejuízo Total Estimado", f"R$ {prejuizo:.2f}")
        col2.metric("Comida Jogada Fora", f"{total_kg:.1f} kg")
        col3.metric("Total de Lançamentos", len(df))
        
        st.divider()
        
        
        col_grafico1, col_grafico2, col_grafico3 = st.columns(3)
        
        with col_grafico1:
            st.subheader("📉 Prejuízo por Produto")
            grafico_produtos = df.groupby("Produto")["custo_estimado"].sum().reset_index()
            
            fig1 = px.bar(grafico_produtos, x="Produto", y="custo_estimado", 
                            color_discrete_sequence=[PALETA[0]]) 
            
            fig1.update_traces(width=0.3, marker_line_color=PALETA[0], marker_line_width=2, opacity=0.8)
            fig1.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", 
                                xaxis_title=None, yaxis_title="R$")
            
            st.plotly_chart(fig1, use_container_width=True)
            
        with col_grafico2:
            st.subheader("🗑️ Desperdício (Setor)")
            grafico_setor = df.groupby("setor")["quantidade"].sum().reset_index()
            
            fig2 = px.bar(grafico_setor, x="setor", y="quantidade", 
                            color_discrete_sequence=[PALETA[1]]) 
            
            fig2.update_traces(width=0.3, marker_line_color=PALETA[1], marker_line_width=2, opacity=0.8)
            fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                                xaxis_title=None, yaxis_title="Kg")
            
            st.plotly_chart(fig2, use_container_width=True)

        with col_grafico3:
            st.subheader("🍩 Motivos de Descarte")
            
          
            fig3 = px.pie(df, names="motivo", values="quantidade", hole=0.6, 
                            color_discrete_sequence=PALETA)
            
            fig3.update_traces(textposition='inside', textinfo='percent')
            fig3.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", 
                                margin=dict(t=0, b=0, l=0, r=0))
            
            st.plotly_chart(fig3, use_container_width=True)
        
        st.divider()
        st.subheader("📋 Histórico Completo")
        df_mostrar = df[["id", "Produto", "quantidade", "setor", "motivo", "custo_estimado"]]
        df_mostrar.columns = ["ID", "Produto", "Peso (Kg)", "Setor", "Motivo", "Custo (R$)"]
        st.dataframe(df_mostrar, use_container_width=True, hide_index=True)
        
    else:
        st.info("Nenhum desperdício registrado no banco de dados. O painel será atualizado automaticamente quando houver registros!")
else:
    st.warning("Erro ao buscar dados da API. Verifique a conexão.")
