import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Gestão de Alimentos", page_icon="🍔", layout="wide")
st.title("🍔 Gestão do Cardápio Base")

API_COMIDAS = "http://127.0.0.1:8000/comidas"

# Organizando a tela em abas nativas
aba_listar, aba_cadastrar, aba_editar = st.tabs(["📋 Listar & Deletar", "➕ Novo Alimento", "✏️ Editar Alimento"])


with aba_listar:
    try:
        resp = requests.get(API_COMIDAS)
        if resp.status_code == 200 and resp.json():
            comidas = resp.json()
            df = pd.DataFrame(comidas)
            
            st.write("Alimentos cadastrados no sistema:")
            
            for index, row in df.iterrows():
                col1, col2, col3, col4, col5 = st.columns([1, 3, 2, 2, 2])
                col1.write(f"**ID:** {row['id']}")
                col2.write(f"{row['nome']}")
                col3.write(f"{row['categoria']}")
                col4.write(f"R$ {row['custo_unitario']:.2f}/kg")
                
                # Botão de deletar por ID
                if col5.button("❌ Deletar", key=f"del_{row['id']}"):
                    try:
                        res_del = requests.delete(f"{API_COMIDAS}/{row['id']}")
                        if res_del.status_code == 204:
                            st.success("Deletado com sucesso!")
                            st.rerun()  # Atualiza a lista sem deslogar o usuário
                        else:
                            st.error("Erro ao deletar. Pode estar vinculado a um desperdício.")
                    except requests.exceptions.RequestException:
                        st.error("🚨 Erro de conexão ao tentar deletar.")
            st.divider()
        else:
            st.info("Nenhum alimento cadastrado ainda.")
    except requests.exceptions.RequestException:
        st.error("🚨 Erro ao conectar com o servidor para listar os alimentos.")


with aba_cadastrar:
    st.subheader("Adicionar novo item ao estoque")
    with st.form("form_comida_nova", clear_on_submit=True):
        nome = st.text_input("Nome do Alimento", placeholder="Ex: Arroz Branco")
        categoria = st.selectbox("Categoria", ["Cozinha Quente", "Cozinha Fria", "Bebidas", "Hortifruti", "Outros"])
        custo = st.number_input("Custo Unitário por Kg (R$)", min_value=0.1, step=0.5)
        
        submit_create = st.form_submit_button("Salvar no Cardápio", type="primary")

        if submit_create:
            payload = {"nome": nome, "categoria": categoria, "custo_unitario": custo}
            try:
                resp = requests.post(API_COMIDAS, json=payload)
                if resp.status_code in [200, 201]:
                    st.success(f"✅ {nome} cadastrado com sucesso!")
                    st.rerun()  # Faz a Aba 1 atualizar instantaneamente
                else:
                    st.warning("Erro ao cadastrar na API.")
            except requests.exceptions.RequestException:
                st.error("🚨 Backend offline. O servidor FastAPI está desligado.")


with aba_editar:
    st.subheader("Modificar um item existente")
    try:
        resp = requests.get(API_COMIDAS)
        if resp.status_code == 200 and resp.json():
            comidas_edit = resp.json()
            
            # Mapeia Nome para os dados completos do item
            opcoes_comidas = {f"{c['id']} - {c['nome']}": c for c in comidas_edit}
            comida_selecionada = st.selectbox("Selecione o alimento para editar:", list(opcoes_comidas.keys()))
            
            if comida_selecionada:
                dados_atuais = opcoes_comidas[comida_selecionada]
                
                with st.form("form_editar_comida"):
                    novo_nome = st.text_input("Novo Nome", value=dados_atuais['nome'])
                    
                    lista_categorias = ["Cozinha Quente", "Cozinha Fria", "Bebidas", "Hortifruti", "Outros"]
                    idx_cat = lista_categorias.index(dados_atuais['categoria']) if dados_atuais['categoria'] in lista_categorias else 0
                    
                    nova_cat = st.selectbox("Nova Categoria", lista_categorias, index=idx_cat)
                    novo_custo = st.number_input("Novo Custo (R$)", min_value=0.1, step=0.5, value=float(dados_atuais['custo_unitario']))
                    
                    # Botão devidamente embutido dentro do bloco do form
                    submit_update = st.form_submit_button("Atualizar Alimento", type="primary")
                    
                    if submit_update:
                        payload_up = {"nome": novo_nome, "categoria": nova_cat, "custo_unitario": novo_custo}
                        try:
                            res_up = requests.patch(f"{API_COMIDAS}/{dados_atuais['id']}", json=payload_up)
                            if res_up.status_code == 200:
                                st.success("✅ Alimento atualizado com sucesso!")
                                st.rerun()
                            else:
                                st.error("Falha ao atualizar os dados.")
                        except requests.exceptions.RequestException:
                            st.error("🚨 Erro de conexão ao tentar atualizar.")
        else:
            st.info("Cadastre um alimento primeiro para liberar a edição.")
    except requests.exceptions.RequestException:
        st.error("🚨 Erro ao buscar os dados para o formulário de edição.")
