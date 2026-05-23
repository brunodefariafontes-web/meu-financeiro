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

META_CASA = 500000

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
# RESUMO
# =====================
if len(st.session_state.dados) > 0:

    df = pd.DataFrame(st.session_state.dados)

    st.divider()

    st.subheader("📊 Resumo Financeiro")

    salario = df[df["Tipo"] == "💰 Salário"]["Valor"].sum()

    reserva_casa = df[df["Tipo"] == "🏠 Reserva Casa"]["Valor"].sum()

    gastos = df[
        df["Tipo"] != "💰 Salário"
    ]["Valor"].sum()

    saldo = salario - gastos

    falta_casa = META_CASA - reserva_casa

    progresso = reserva_casa / META_CASA

    # =====================
    # CARDS
    # =====================
    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Salário", f"R$ {salario:,.2f}")

    col2.metric("💸 Gastos", f"R$ {gastos:,.2f}")

    col3.metric("💵 Saldo", f"R$ {saldo:,.2f}")

    st.divider()

    # =====================
    # CASA
    # =====================
    st.subheader("🏠 Meta da Casa")

    st.write(f"🎯 Meta: R$ {META_CASA:,.2f}")

    st.write(f"💵 Reservado: R$ {reserva_casa:,.2f}")

    st.write(f"📉 Falta: R$ {falta_casa:,.2f}")

    porcentagem = progresso * 100

    st.progress(min(progresso, 1.0))

    st.write(f"📊 Progresso: {porcentagem:.2f}%")

    # =====================
    # ALERTAS
    # =====================
    st.divider()

    st.subheader("🧠 Análise Financeira")

    if salario == 0:
        st.warning("Cadastre seu salário para análise financeira.")

    else:

        percentual_gasto = (gastos / salario) * 100

        if percentual_gasto > 80:
            st.error(
                "⚠ Seus gastos estão muito altos. "
                "Diminua despesas para acelerar a compra da casa."
            )

        elif percentual_gasto > 60:
            st.warning(
                "⚠ Seus gastos estão moderados. "
                "Tente economizar mais."
            )

        else:
            st.success(
                "✅ Seu controle financeiro está saudável."
            )

    # =====================
    # TABELA
    # =====================
    st.divider()

    st.subheader("📋 Lançamentos")

    st.dataframe(df, use_container_width=True)

# =====================
# SAIR
# =====================
st.divider()

if st.button("Sair"):

    st.session_state.logado = False
    st.session_state.usuario = ""

    st.rerun()
