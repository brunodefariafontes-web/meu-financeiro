import streamlit as st
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt

# =====================
# CONFIG
# =====================
st.set_page_config(
    page_title="Controle Financeiro",
    page_icon="🏠",
    layout="centered"
)

st.title("🏠💰 Controle Financeiro Inteligente")

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
# SIDEBAR
# =====================
modo = st.sidebar.selectbox("Menu", ["📊 Dashboard", "➕ Lançar"])

# =====================
# INPUT
# =====================
if modo == "➕ Lançar":

    st.subheader("Adicionar lançamento")

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

    if st.button("Salvar"):

        data = datetime.now().strftime("%Y-%m-%d")

        novo = pd.DataFrame([[data, tipo, descricao, valor]],
                            columns=df.columns)

        df = pd.concat([df, novo], ignore_index=True)
        df.to_csv(ARQUIVO, index=False)

        st.success("✔ Salvo!")

# =====================
# DASHBOARD
# =====================
else:

    if len(df) == 0:
        st.warning("Sem dados ainda.")
        st.stop()

    # =====================
    # FILTRO MES
    # =====================
    df["data"] = pd.to_datetime(df["data"])
    df["mes"] = df["data"].dt.month

    mes_atual = datetime.now().month
    df_mes = df[df["mes"] == mes_atual]

    # =====================
    # CÁLCULOS
    # =====================
    salario = df["valor"][df["tipo"] == "💰 Salário"].sum()
    reserva = df["valor"][df["tipo"] == "🏠 Reserva Casa"].sum()
    gastos = df["valor"][df["tipo"] != "💰 Salário"].sum()

    saldo = salario - gastos

    progresso = reserva / META_CASA
    falta = META_CASA - reserva

    # =====================
    # CARDS
    # =====================
    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Salário", f"R$ {salario:,.2f}")
    col2.metric("💸 Gastos", f"R$ {gastos:,.2f}")
    col3.metric("💰 Saldo", f"R$ {saldo:,.2f}")

    st.divider()

    # =====================
    # META CASA
    # =====================
    st.subheader("🏠 Meta da Casa")

    st.write(f"💵 Reservado: R$ {reserva:,.2f}")
    st.write(f"🏠 Falta: R$ {falta:,.2f}")

    st.progress(min(progresso, 1.0))

    if progresso >= 1:
        st.success("🎉 CASA ALCANÇADA!")
    elif progresso >= 0.7:
        st.warning("🟡 Você está perto da casa!")
    else:
        st.info("🔵 Continue economizando")

    # =====================
    # ALERTA ECONOMIA
    # =====================
    if salario > 0:

        uso = (gastos / salario) * 100

        st.subheader("🧠 Modo economia")

        if uso > 85:
            st.error("🔴 Você está gastando demais! corte agora se quer a casa.")
        elif uso > 70:
            st.warning("🟡 Atenção: reduza gastos desnecessários.")
        else:
            st.success("🟢 Controle saudável")

    # =====================
    # PREVISÃO CASA
    # =====================
    if saldo > 0:
        meses = falta / saldo if saldo > 0 else 0

        st.subheader("⏳ Previsão")

        if meses > 0:
            st.info(f"Se continuar assim, você compra a casa em ~{meses:.1f} meses")

    # =====================
    # GRÁFICO
    # =====================
    st.subheader("📊 Gastos por categoria")

    gastos_cat = df[df["tipo"] != "💰 Salário"].groupby("tipo")["valor"].sum()

    fig, ax = plt.subplots()
    gastos_cat.plot(kind="bar", ax=ax)

    st.pyplot(fig)

    # =====================
    # HISTÓRICO
    # =====================
    st.subheader("📋 Últimos lançamentos")
    st.dataframe(df.tail(10), use_container_width=True)
