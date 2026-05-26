import streamlit as st
import pandas as pd
import requests
import plotly.express as px  # <-- A mágica visual entra aqui

st.set_page_config(page_title="Dashboard - FoodMetrics", page_icon="📊", layout="wide")
st.title("📊 Dashboard do Restaurante")

API_DESPERDICIOS = "http://127.0.0.1:8000/desperdicios"

try:
    resposta = requests.get(API_DESPERDICIOS)
    
    if resposta.status_code == 200:
        dados = resposta.json()
        
        if dados:
            df = pd.DataFrame(dados)
            
            # Puxa o nome da comida
            df['Produto'] = df['comida'].apply(lambda x: x['nome'] if isinstance(x, dict) else 'Desconhecido')
            
            total_kg = df["quantidade"].sum()
            prejuizo = df["custo_estimado"].sum()
            
            # 1. CARDS
            col1, col2, col3 = st.columns(3)
            col1.metric("Prejuízo Total Estimado", f"R$ {prejuizo:.2f}")
            col2.metric("Comida Jogada Fora", f"{total_kg:.1f} kg")
            col3.metric("Total de Lançamentos", len(df))
            
            st.divider()
            
            # 2. GRÁFICOS PREMIUM COM PLOTLY
            col_grafico1, col_grafico2, col_grafico3 = st.columns(3)
            
            with col_grafico1:
                st.subheader("📉 Prejuízo por Produto")
                grafico_produtos = df.groupby("Produto")["custo_estimado"].sum().reset_index()
                
                fig1 = px.bar(grafico_produtos, x="Produto", y="custo_estimado", 
                              color_discrete_sequence=["#deff9a"], template="plotly_dark")
                
                # O segredo da elegância: limitando a largura da barra (width=0.3)
                fig1.update_traces(width=0.3, marker_line_color="#deff9a", marker_line_width=2, opacity=0.8)
                fig1.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", 
                                   xaxis_title=None, yaxis_title="R$")
                
                st.plotly_chart(fig1, use_container_width=True)
                
            with col_grafico2:
                st.subheader("🗑️ Desperdício (Setor)")
                grafico_setor = df.groupby("setor")["quantidade"].sum().reset_index()
                
                fig2 = px.bar(grafico_setor, x="setor", y="quantidade", 
                              color_discrete_sequence=["#ff4b4b"], template="plotly_dark")
                
                fig2.update_traces(width=0.3, marker_line_color="#ff4b4b", marker_line_width=2, opacity=0.8)
                fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                                   xaxis_title=None, yaxis_title="Kg")
                
                st.plotly_chart(fig2, use_container_width=True)

            with col_grafico3:
                st.subheader("🍩 Motivos de Descarte")
                
                # Criando o gráfico de Donut (Pizza com furo)
                fig3 = px.pie(df, names="motivo", values="quantidade", hole=0.6, 
                              template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Pastel)
                
                fig3.update_traces(textposition='inside', textinfo='percent')
                fig3.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", 
                                   margin=dict(t=0, b=0, l=0, r=0))
                
                st.plotly_chart(fig3, use_container_width=True)
            
            # 3. TABELA REAL
            st.subheader("📋 Histórico Completo")
            df_mostrar = df[["id", "Produto", "quantidade", "setor", "motivo", "custo_estimado"]]
            df_mostrar.columns = ["ID", "Produto", "Peso (Kg)", "Setor", "Motivo", "Custo (R$)"]
            st.dataframe(df_mostrar, use_container_width=True, hide_index=True)
            
        else:
            st.info("Nenhum desperdício registrado no banco de dados. O painel será atualizado automaticamente quando houver registros!")
    else:
        st.warning("Erro ao buscar dados da API. Verifique a conexão.")

except requests.exceptions.RequestException:
    st.error("🚨 O Backend está offline. Lembre-se de rodar o FastAPI em outro terminal!")