import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Gestão de Alimentos", page_icon="🍔", layout="wide")

# --- LÓGICA DOS TOASTS (Requisito 4) ---
# Fica no topo para disparar assim que a tela recarregar
if "toast_sucesso" in st.session_state:
    st.toast(st.session_state.toast_sucesso, icon="✅")
    del st.session_state.toast_sucesso
if "toast_erro" in st.session_state:
    st.toast(st.session_state.toast_erro, icon="🔴")
    del st.session_state.toast_erro

st.title("🍔 Gestão do Cardápio Base")

API_COMIDAS = "http://127.0.0.1:8000/comidas"

aba_listar, aba_cadastrar, aba_editar, aba_deletar = st.tabs(["📋 Listar", "➕ Cadastrar", "✏️ Editar", "❌ Deletar"])

with aba_listar:
    termo_busca = st.text_input("🔍 Buscar alimento por nome (ex: feijao)...").lower()
    
    if "page_comidas" not in st.session_state:
        st.session_state.page_comidas = 1
    
    limit = 10
    
    try:
        params = {"nome": termo_busca, "page": st.session_state.page_comidas, "limit": limit}
        resp = requests.get(API_COMIDAS, params=params)
        
        if resp.status_code == 200:
            resultado = resp.json()
            comidas = resultado["data"]
            total_items = resultado["total"]
            total_pages = resultado["pages"]
            
            if comidas:
                df = pd.DataFrame(comidas)
                df_mostrar = df[["id", "nome", "categoria", "custo_unitario"]].copy()
                df_mostrar.columns = ["ID", "Nome do Alimento", "Categoria", "Custo (R$)"]
                
                # Formata os números e converte TUDO para texto para alinhar à esquerda
                df_mostrar["Custo (R$)"] = df_mostrar["Custo (R$)"].apply(lambda x: f"{float(x):.2f}")
                df_mostrar = df_mostrar.astype(str)
                
                def aplicar_zebra(row):
                    cor = '#f0f5fa' if int(row.name) % 2 == 0 else '#ffffff'
                    return [f'background-color: {cor}'] * len(row)
                
                st.dataframe(
                    df_mostrar.style.apply(aplicar_zebra, axis=1), 
                    use_container_width=True, 
                    hide_index=True
                )
                
                st.markdown("---")
                col_voltar, col_info, col_avancar = st.columns([1, 4, 1])
                
                with col_voltar:
                    if st.button("⬅️ Voltar", disabled=st.session_state.page_comidas <= 1, use_container_width=True):
                        st.session_state.page_comidas -= 1
                        st.rerun()
                
                with col_info:
                    st.markdown(f"""
                        <div style='text-align: center; border: 1px solid #e6e9ef; border-radius: 8px; padding: 7px; background-color: #f8f9fb;'>
                            <span style='color: #6d7a8a; font-size: 14px;'>Página <strong style='font-size: 16px; color: #123258;'>{st.session_state.page_comidas}</strong> de {total_pages}</span>
                            <span style='color: #bdc3c7; margin: 0 10px;'>|</span>
                            <span style='color: #6d7a8a; font-size: 13px;'>Total de {total_items} itens</span>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col_avancar:
                    if st.button("Avançar ➡️", disabled=st.session_state.page_comidas >= total_pages, use_container_width=True):
                        st.session_state.page_comidas += 1
                        st.rerun()
            else:
                st.info("Nenhum alimento encontrado na busca.")
        else:
            st.info("Nenhum alimento cadastrado ainda.")
    except requests.exceptions.RequestException:
        st.toast("Erro ao conectar com o servidor.", icon="🔴")


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
                headers = {}
                if "token" in st.session_state:
                    headers["Authorization"] = f"Bearer {st.session_state.token}"
                    
                resp = requests.post(API_COMIDAS, json=payload, headers=headers)
                if resp.status_code in [200, 201]:
                    st.session_state.toast_sucesso = f"{nome} cadastrado com sucesso!"
                    st.rerun()  
                else:
                    st.toast("Erro ao cadastrar na API.", icon="🔴")
            except requests.exceptions.RequestException:
                st.toast("Backend offline.", icon="🔴")


with aba_editar:
    st.subheader("Modificar um item existente")
    try:
        resp = requests.get(API_COMIDAS, params={"limit": 1000})
        if resp.status_code == 200:
            resultado_edit = resp.json()
            comidas_edit = resultado_edit["data"]
            if comidas_edit:
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
                                headers = {}
                                if "token" in st.session_state:
                                    headers["Authorization"] = f"Bearer {st.session_state.token}"
                                res_up = requests.patch(f"{API_COMIDAS}/{dados_atuais['id']}", json=payload_up, headers=headers)
                                if res_up.status_code == 200:
                                    st.session_state.toast_sucesso = "Atualizado com sucesso!"
                                    st.rerun()
                                else:
                                    st.toast("Falha ao atualizar.", icon="🔴")
                            except requests.exceptions.RequestException:
                                st.toast("Erro de conexão.", icon="🔴")
            else:
                st.info("Cadastre um alimento primeiro.")
        else:
            st.toast("Erro ao buscar dados.", icon="🔴")
    except requests.exceptions.RequestException:
        st.toast("Erro ao conectar com o servidor.", icon="🔴")


with aba_deletar:
    st.subheader("❌ Remover Alimento do Sistema")
    try:
        resp = requests.get(API_COMIDAS, params={"limit": 1000})
        if resp.status_code == 200:
            resultado_del = resp.json()
            comidas_del = resultado_del["data"]
            if comidas_del:
                opcoes_del = {f"ID {c['id']} - {c['nome']}": c for c in comidas_del}
                
                col_sel, col_btn = st.columns([3, 1])
                with col_sel:
                    item_del = st.selectbox("Selecione o alimento que deseja deletar:", list(opcoes_del.keys()), key="del_comida_select")
                
                @st.dialog("Confirmar Exclusão de Alimento")
                def modal_confirmar_deletar_comida(comida_dados):
                    st.warning(f"⚠️ Atenção! Você está prestes a excluir permanentemente um item.")
                    st.write(f"Deseja realmente deletar o alimento **{comida_dados['nome']}** (Categoria: {comida_dados['categoria']})?")
                    
                    col_modal_cancel, col_modal_conf = st.columns(2)
                    with col_modal_cancel:
                        if st.button("Cancelar", use_container_width=True):
                            st.rerun() # Fecha o modal sem executar nada
                    with col_modal_conf:
                        if st.button("Confirmar Exclusão", type="primary", use_container_width=True):
                            try:
                                headers = {}
                                if "token" in st.session_state:
                                    headers["Authorization"] = f"Bearer {st.session_state.token}"
                                
                                res_del = requests.delete(f"{API_COMIDAS}/{comida_dados['id']}", headers=headers)
                                
                                if res_del.status_code == 204:
                                    st.session_state.toast_sucesso = f"{comida_dados['nome']} deletado com sucesso do sistema!"
                                    st.rerun() 
                                elif res_del.status_code == 401:
                                    st.toast("Erro de Autenticação: Usuário não autorizado.", icon="🔴")
                                else:
                                    st.toast("Erro ao deletar. O alimento pode estar vinculado a um desperdício.", icon="🔴")
                            except requests.exceptions.RequestException:
                                st.toast("Erro de conexão.", icon="🔴")

                with col_btn:
                    st.write("") 
                    st.write("")
                    if st.button("Deletar Selecionado", use_container_width=True, type="primary"):
                        comida_selecionada = opcoes_del[item_del]
                        modal_confirmar_deletar_comida(comida_selecionada)
            else:
                st.info("Nenhum alimento cadastrado para deletar.")
        else:
            st.toast("Erro ao buscar dados.", icon="🔴")
    except requests.exceptions.RequestException:
        st.toast("Erro ao conectar com o servidor.", icon="🔴")