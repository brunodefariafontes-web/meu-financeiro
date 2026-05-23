import streamlit as st
import pandas as pd
import os
from datetime import datetime

# =====================
# CONFIG
# =====================
st.set_page_config(
    page_title="Controle Financeiro",
    page_icon="🏠",
    layout="centered"
)

st.title("🏠 Controle Financeiro Inteligente")

META_CASA = 500000
ARQUIVO = "dados.csv"

# =====================
# CRIAR ARQUIVO
# =====================
if not os.path.exists(ARQUIVO):
    df = pd.DataFrame(columns=["data", "tipo", "descricao", "valor"])
    df.to_csv(ARQUIVO, index=False)

df = pd.read_csv(ARQUIVO)

# =====================
# MENU
# =====================
menu = st.sidebar.radio("Menu", ["📊 Resumo", "➕ Lançar"])

# =====================
# LANÇAR
# =====================
if menu == "➕ Lançar":

    st.subheader("Novo lançamento")

    tipo = st.selectbox(
        "Tipo",
        [
            "💰 Salário",
            "🏠 Reserva Casa",
            "💡 Luz",
            "🚿 Água",
            "📶 Internet",
            "💳 Cartão",
            "🏠 Aluguel",
            "🛒 Comprinhas",
            "🍔 Lazer",
            "🛍 Mercado",
            "💸 Outros"
        ]
    )

    descricao = st.text_input("Descrição")
    valor = st.number_input("Valor (R$)", min_value=0.0)

    if st.button("Adicionar"):

        data = datetime.now().strftime("%Y-%m-%d")

        novo = pd.DataFrame([[data, tipo, descricao, valor]],
                            columns=df.columns)

        df = pd.concat([df, novo], ignore_index=True)
        df.to_csv(ARQUIVO, index=False)

        st.success("✔ Salvo com sucesso!")

# =====================
# RESUMO
# =====================
else:

    if len(df) == 0:
        st.warning("Sem dados ainda.")
        st.stop()

    salario = df[df["tipo"] == "💰 Salário"]["valor"].sum()
    reserva = df[df["tipo"] == "🏠 Reserva Casa"]["valor"].sum()
    gastos = df[df["tipo"] != "💰 Salário"]["valor"].sum()

    saldo = salario - gastos

    falta = META_CASA - reserva
    progresso = reserva / META_CASA if META_CASA > 0 else 0

    # =====================
    # PAINEL
    # =====================
    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Salário", f"R$ {salario:,.2f}")
    col2.metric("💸 Gastos", f"R$ {gastos:,.2f}")
    col3.metric("💰 Saldo", f"R$ {saldo:,.2f}")

    st.divider()

    # =====================
    # CASA
    # =====================
    st.subheader("🏠 Meta da Casa (R$ 500.000)")

    st.write(f"💵 Reservado: R$ {reserva:,.2f}")
    st.write(f"🏠 Falta: R$ {falta:,.2f}")

    st.progress(min(progresso, 1.0))

    if progresso >= 1:
        st.success("🎉 Você já atingiu a meta da casa!")
    elif progresso >= 0.7:
        st.warning("🟡 Quase lá! Continue economizando.")
    else:
        st.info("🔵 Foco na economia para atingir a casa.")

    st.divider()

    # =====================
    # ALERTA SIMPLES
    # =====================
    if salario > 0:
        porcentagem = (gastos / salario) * 100

        if porcentagem > 85:
            st.error("🔴 Você está gastando demais!")
        elif porcentagem > 70:
            st.warning("🟡 Atenção com seus gastos.")
        else:
            st.success("🟢 Você está no controle.")

    # =====================
    # HISTÓRICO
    # =====================
    st.subheader("📋 Últimos registros")
    st.dataframe(df.tail(10), use_container_width=True)
