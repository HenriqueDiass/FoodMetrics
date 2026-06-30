# 🥗 FoodMetrics

O **FoodMetrics** é um sistema de gestão e controle de desperdício de alimentos, projetado para ajudar restaurantes a monitorar perdas e reduzir prejuízos financeiros.

## 🧠 Lógica de Negócio

O sistema opera sobre três pilares principais:

1.  **Gestão de Insumos:** Cadastro de produtos com seus respectivos custos unitários e categorias (Hortifruti, Carnes, etc).
2.  **Registro de Perdas:** Registro detalhado de cada desperdício, informando a quantidade, o setor de origem (Cozinha, Estoque, Salão) e o motivo (Validade, Erro de preparo, Sobras).
3.  **Cálculo de Impacto:** O sistema calcula automaticamente o prejuízo financeiro de cada descarte multiplicando a quantidade perdida pelo custo unitário do insumo no momento do registro.

## 🛠️ Tecnologias

-   **Backend:** FastAPI (Python) + SQLAlchemy (ORM)
-   **Banco de Dados:** SQLite
-   **Frontend:** Streamlit

## 🚀 Como Executar

1.  **Backend:**
    ```bash
    uvicorn backend.main:app --reload
    ```
2.  **Frontend:**
    ```bash
    streamlit run frontend/main.py
    ```

---
*FoodMetrics - Transformando desperdício em dados para uma cozinha mais eficiente.*


URL FRONT: https://foodmetrics.streamlit.app/
URL BACK: https://foodmetrics-production.up.railway.app/docs