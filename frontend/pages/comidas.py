import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Gestão de Alimentos", page_icon="🍔", layout="wide")
st.title("🍔 Gestão do Cardápio Base")

API_COMIDAS = "http://127.0.0.1:8000/comidas"


aba_listar, aba_cadastrar, aba_editar, aba_deletar = st.tabs(["📋 Listar", "➕ Cadastrar", "✏️ Editar", "❌ Deletar"])


with aba_listar:
    termo_busca = st.text_input("🔍 Buscar alimento por nome (ex: feijao)...").lower()
    
    try:
        resp = requests.get(API_COMIDAS)
        if resp.status_code == 200 and resp.json():
            comidas = resp.json()
            df = pd.DataFrame(comidas)
            
            if termo_busca:
                df = df[df["nome"].str.lower().str.contains(termo_busca)]
            
            if not df.empty:
                df_mostrar = df[["id", "nome", "categoria", "custo_unitario"]].copy()
                df_mostrar.columns = ["ID", "Nome do Alimento", "Categoria", "Custo (R$)"]
                
                def aplicar_zebra(row):
                    cor = '#f0f5fa' if row.name % 2 == 0 else '#ffffff'
                    return [f'background-color: {cor}'] * len(row)
                
                st.dataframe(
                    df_mostrar.style.apply(aplicar_zebra, axis=1).format({"Custo (R$)": "{:.2f}"}), 
                    use_container_width=True, 
                    hide_index=True
                )
            else:
                st.info("Nenhum alimento encontrado na busca.")
        else:
            st.info("Nenhum alimento cadastrado ainda.")
    except requests.exceptions.RequestException:
        st.error("🚨 Erro ao conectar com o servidor.")


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
                    st.rerun()  
                else:
                    st.warning("Erro ao cadastrar na API.")
            except requests.exceptions.RequestException:
                st.error("🚨 Backend offline.")


with aba_editar:
    st.subheader("Modificar um item existente")
    try:
        resp = requests.get(API_COMIDAS)
        if resp.status_code == 200 and resp.json():
            comidas_edit = resp.json()
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
                    submit_update = st.form_submit_button("Atualizar Alimento", type="primary")
                    
                    if submit_update:
                        payload_up = {"nome": novo_nome, "categoria": nova_cat, "custo_unitario": novo_custo}
                        try:
                            res_up = requests.patch(f"{API_COMIDAS}/{dados_atuais['id']}", json=payload_up)
                            if res_up.status_code == 200:
                                st.success("✅ Atualizado com sucesso!")
                                st.rerun()
                            else:
                                st.error("Falha ao atualizar.")
                        except requests.exceptions.RequestException:
                            st.error("🚨 Erro de conexão.")
        else:
            st.info("Cadastre um alimento primeiro.")
    except requests.exceptions.RequestException:
        st.error("🚨 Erro ao buscar dados.")


with aba_deletar:
    st.subheader("❌ Remover Alimento do Sistema")
    try:
        resp = requests.get(API_COMIDAS)
        if resp.status_code == 200 and resp.json():
            comidas_del = resp.json()
            opcoes_del = {f"ID {c['id']} - {c['nome']}": c['id'] for c in comidas_del}
            
            col_sel, col_btn = st.columns([3, 1])
            with col_sel:
                item_del = st.selectbox("Selecione o alimento que deseja deletar:", list(opcoes_del.keys()), key="del_comida_select")
            with col_btn:
                st.write("") 
                st.write("")
                if st.button("Deletar Selecionado", use_container_width=True, type="primary"):
                    try:
                        res_del = requests.delete(f"{API_COMIDAS}/{opcoes_del[item_del]}")
                        if res_del.status_code == 204:
                            st.success("Deletado com sucesso!")
                            st.rerun()  
                        else:
                            st.error("Erro ao deletar. O alimento pode estar vinculado a um registro de desperdício.")
                    except requests.exceptions.RequestException:
                        st.error("🚨 Erro de conexão.")
        else:
            st.info("Nenhum alimento cadastrado para deletar.")
    except requests.exceptions.RequestException:
        st.error("🚨 Erro ao conectar com o servidor.")