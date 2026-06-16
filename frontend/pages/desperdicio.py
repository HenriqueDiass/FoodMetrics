import streamlit as st
import requests
import pandas as pd
from utils import bloqueio_api_offline, exibir_status_sidebar

st.set_page_config(page_title="Registrar Desperdício", page_icon="🗑️", layout="wide")
exibir_status_sidebar()
bloqueio_api_offline()

st.title("🗑️ Gestão de Desperdícios")

API_COMIDAS = "http://127.0.0.1:8000/comidas"
API_DESPERDICIOS = "http://127.0.0.1:8000/desperdicios"

# Carregar comidas (para selectboxes, pegamos uma lista maior)
resp_comidas = requests.get(API_COMIDAS, params={"limit": 1000})
lista_comidas = resp_comidas.json()["data"] if resp_comidas.status_code == 200 else []

if not lista_comidas:
    st.warning("⚠️ Cadastre Alimentos na aba 'Comidas' antes de gerenciar os desperdícios!")
else:
    opcoes_comidas = {item["nome"]: item["id"] for item in lista_comidas}
    opcoes_comidas_inverso = {item["id"]: item["nome"] for item in lista_comidas}

  
    aba_listar, aba_cadastrar, aba_editar, aba_deletar = st.tabs(["📋 Listar", "➕ Cadastrar", "✏️ Editar", "❌ Deletar"])

    
    with aba_listar:
        termo_busca = st.text_input("🔍 Buscar desperdício por Setor (ex: Cozinha Quente)...").lower()
        
        # Gerenciar estado da página
        if "page_desperdicio" not in st.session_state:
            st.session_state.page_desperdicio = 1
        
        limit = 10
        
        try:
            params = {"setor": termo_busca, "page": st.session_state.page_desperdicio, "limit": limit}
            resp_desp = requests.get(API_DESPERDICIOS, params=params)
            
            if resp_desp.status_code == 200:
                resultado = resp_desp.json()
                desperdicios = resultado["data"]
                total_items = resultado["total"]
                total_pages = resultado["pages"]
                
                if desperdicios:
                    df = pd.DataFrame(desperdicios)
                    
                    df["Nome do Alimento"] = df["comida_id"].map(opcoes_comidas_inverso)
                    
                    df_mostrar = df[["id", "Nome do Alimento", "setor", "quantidade", "motivo"]].copy()
                    df_mostrar.columns = ["ID", "Alimento", "Setor", "Quantidade (kg)", "Motivo"]
                    
                    def aplicar_zebra(row):
                        cor = '#f0f5fa' if row.name % 2 == 0 else '#ffffff'
                        return [f'background-color: {cor}'] * len(row)
                        
                    
                    st.dataframe(
                        df_mostrar.style.apply(aplicar_zebra, axis=1).format({"Quantidade (kg)": "{:.2f}"}), 
                        use_container_width=True, 
                        hide_index=True
                    )

                    # Melhoria Visual da Paginação
                    st.markdown("---")
                    col_voltar, col_info, col_avancar = st.columns([2, 3, 2])
                    
                    with col_voltar:
                        if st.button("⬅️ Voltar", disabled=st.session_state.page_desperdicio <= 1, use_container_width=True, key="btn_ant_desp"):
                            st.session_state.page_desperdicio -= 1
                            st.rerun()
                    
                    with col_info:
                        # Estilização do contador de páginas (mesmo estilo de comidas.py)
                        st.markdown(f"""
                            <div style='text-align: center; border: 1px solid #e6e9ef; border-radius: 10px; padding: 5px; background-color: #f8f9fb;'>
                                <small style='color: #6d7a8a; font-size: 12px;'>PÁGINA</small><br>
                                <strong style='font-size: 20px; color: #123258;'>{st.session_state.page_desperdicio} <span style='color: #bdc3c7; font-weight: normal;'>/</span> {total_pages}</strong><br>
                                <small style='color: #6d7a8a; font-size: 11px;'>Total de {total_items} registros</small>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    with col_avancar:
                        if st.button("Avançar ➡️", disabled=st.session_state.page_desperdicio >= total_pages, use_container_width=True, key="btn_prox_desp"):
                            st.session_state.page_desperdicio += 1
                            st.rerun()
                else:
                    st.info("Nenhum desperdício encontrado.")
            else:
                st.info("Nenhum registro de desperdício cadastrado ainda.")
        except requests.exceptions.RequestException:
            st.error("🚨 Erro ao conectar com o servidor.")

    
    with aba_cadastrar:
        st.subheader("Registrar nova perda de alimento")
        with st.form("form_desperdicio", clear_on_submit=True):
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
                try:
                    headers = {}
                    if "token" in st.session_state:
                        headers["Authorization"] = f"Bearer {st.session_state.token}"
                    res = requests.post(API_DESPERDICIOS, json=payload, headers=headers)
                    if res.status_code in [200, 201]:
                        st.success("✅ Desperdício registrado com sucesso!")
                        st.rerun()
                    else:
                        st.error("Erro ao registrar no backend.")
                except requests.exceptions.RequestException:
                    st.error("🚨 Backend offline.")

    
    with aba_editar:
        st.subheader("Modificar um item existente")
        try:
            resp_desp = requests.get(API_DESPERDICIOS, params={"limit": 1000})
            if resp_desp.status_code == 200:
                resultado_edit = resp_desp.json()
                desperdicios_edit = resultado_edit["data"]
                
                if desperdicios_edit:
                    opcoes_desp = {}
                    for d in desperdicios_edit:
                        nome_alim = opcoes_comidas_inverso.get(d["comida_id"], "Desconhecido")
                        label = f"ID: {d['id']} - {nome_alim} ({d['quantidade']}kg no {d['setor']})"
                        opcoes_desp[label] = d

                    desp_selecionado = st.selectbox("Selecione o registro para editar:", list(opcoes_desp.keys()))
                    
                    if desp_selecionado:
                        dados_atuais = opcoes_desp[desp_selecionado]
                        with st.form("form_editar_desperdicio"):
                            nome_atual_alimento = opcoes_comidas_inverso.get(dados_atuais['comida_id'])
                            idx_alim = list(opcoes_comidas.keys()).index(nome_atual_alimento) if nome_atual_alimento in opcoes_comidas else 0
                            novo_nome_sel = st.selectbox("Alimento", list(opcoes_comidas.keys()), index=idx_alim)
                            nova_qtd = st.number_input("Peso (kg)", min_value=0.1, step=0.1, value=float(dados_atuais['quantidade']))
                            
                            lista_setores = ["Cozinha Quente", "Cozinha Fria", "Salão", "Estoque"]
                            idx_setor = lista_setores.index(dados_atuais['setor']) if dados_atuais['setor'] in lista_setores else 0
                            novo_setor = st.selectbox("Setor de Origem", lista_setores, index=idx_setor)
                            
                            lista_motivos = ["Sobras de produção", "Passou da validade", "Erro de preparo", "Sobras de cliente"]
                            idx_motivo = lista_motivos.index(dados_atuais['motivo']) if dados_atuais['motivo'] in lista_motivos else 0
                            novo_motivo = st.selectbox("Motivo", lista_motivos, index=idx_motivo)
                            nova_obs = st.text_input("Observações", value=dados_atuais.get('observacao') or '')
                            submit_update = st.form_submit_button("Atualizar Registro", type="primary")

                            if submit_update:
                                payload_up = {
                                    "comida_id": opcoes_comidas[novo_nome_sel],
                                    "quantidade": nova_qtd,
                                    "setor": novo_setor,
                                    "motivo": novo_motivo,
                                    "observacao": nova_obs if nova_obs else None
                                }
                                try:
                                    headers = {}
                                    if "token" in st.session_state:
                                        headers["Authorization"] = f"Bearer {st.session_state.token}"
                                    res_up = requests.put(f"{API_DESPERDICIOS}/{dados_atuais['id']}", json=payload_up, headers=headers)
                                    if res_up.status_code == 405:
                                        res_up = requests.patch(f"{API_DESPERDICIOS}/{dados_atuais['id']}", json=payload_up, headers=headers)
                                    
                                    if res_up.status_code in [200, 204]:
                                        st.success("✅ Registro atualizado com sucesso!")
                                        st.rerun()
                                    else:
                                        st.error("Falha ao atualizar.")
                                except requests.exceptions.RequestException:
                                    st.error("🚨 Erro de conexão.")
                else:
                    st.info("Cadastre um desperdício primeiro.")
            else:
                st.error("Erro ao buscar dados.")
        except requests.exceptions.RequestException:
            st.error("🚨 Erro ao buscar os dados para edição.")

    
    with aba_deletar:
        st.subheader("❌ Remover Desperdício do Histórico")
        try:
            resp_desp = requests.get(API_DESPERDICIOS, params={"limit": 1000})
            if resp_desp.status_code == 200:
                resultado_del = resp_desp.json()
                desperdicios_del = resultado_del["data"]
                
                if desperdicios_del:
                    # Monta os nomes bonitinhos para selecionar no formato: "ID - Alimento (Xkg no Setor Y)"
                    opcoes_del = {}
                    for d in desperdicios_del:
                        nome_alim = opcoes_comidas_inverso.get(d["comida_id"], "Desconhecido")
                        label = f"ID: {d['id']} - {nome_alim} ({d['quantidade']}kg no {d['setor']})"
                        opcoes_del[label] = d['id']
                    
                    col_sel, col_btn = st.columns([3, 1])
                    with col_sel:
                        item_del = st.selectbox("Selecione o registro que deseja deletar:", list(opcoes_del.keys()), key="del_desp_select")
                    with col_btn:
                        st.write("")
                        st.write("")
                        if st.button("Deletar Selecionado", use_container_width=True, type="primary"):
                            try:
                                headers = {}
                                if "token" in st.session_state:
                                    headers["Authorization"] = f"Bearer {st.session_state.token}"
                                res_del = requests.delete(f"{API_DESPERDICIOS}/{opcoes_del[item_del]}", headers=headers)
                                if res_del.status_code in [200, 204]:
                                    st.success("Deletado com sucesso!")
                                    st.rerun()
                                else:
                                    st.error("Erro ao deletar no banco.")
                            except requests.exceptions.RequestException:
                                st.error("🚨 Erro de conexão.")
                else:
                    st.info("Nenhum registro de desperdício para deletar.")
            else:
                st.error("Erro ao buscar dados.")
        except requests.exceptions.RequestException:
            st.error("🚨 Erro ao conectar com o servidor.")
