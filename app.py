import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Controle Financeiro",
    page_icon="🏠",
    layout="wide"
)

# =====================
# USUÁRIOS
# =====================
USUARIOS = {
    "43623202886": "Bruno",
    "42899462830": "Ingrid"
}

# =====================
# SESSION
# =====================
if "logado" not in st.session_state:
    st.session_state.logado = False

if "usuario" not in st.session_state:
    st.session_state.usuario = ""

if "dados" not in st.session_state:
    st.session_state.dados = []

# =====================
# LOGIN
# =====================
if not st.session_state.logado:

    st.title("🔐 Acesso ao Sistema")

    cpf = st.text_input("Digite seu CPF")

    if st.button("Entrar"):

        if cpf in USUARIOS:

            st.session_state.logado = True
            st.session_state.usuario = USUARIOS[cpf]

            st.rerun()

        else:
            st.error("CPF não autorizado")

    st.stop()

# =====================
# APP
# =====================
st.title(f"🏠 Controle Financeiro - {st.session_state.usuario}")

st.success("Acesso realizado com sucesso ✔")

st.divider()

# =====================
# LANÇAMENTOS
# =====================
st.subheader("➕ Novo Lançamento")

tipo = st.selectbox(
    "Tipo",
    [
        "💰 Salário",
        "🏠 Reserva Casa",
        "💳 Cartão",
        "💡 Luz",
        "🚿 Água",
        "🛒 Compras",
        "🍔 Alimentação",
        "🚗 Transporte",
        "📦 Outros"
    ]
)

descricao = st.text_input("Descrição")

valor = st.number_input(
    "Valor",
    min_value=0.0,
    step=1.0
)

if st.button("Salvar"):

    st.session_state.dados.append({
        "Tipo": tipo,
        "Descrição": descricao,
        "Valor": valor
    })

    st.success("Lançamento salvo!")

# =====================
# TABELA
# =====================
if len(st.session_state.dados) > 0:

    df = pd.DataFrame(st.session_state.dados)

    st.divider()

    st.subheader("📊 Resumo")

    st.dataframe(df, use_container_width=True)

    total = df["Valor"].sum()

    st.metric("💵 Total", f"R$ {total:,.2f}")

# =====================
# SAIR
# =====================
st.divider()

if st.button("Sair"):

    st.session_state.logado = False
    st.session_state.usuario = ""
    st.rerun()
