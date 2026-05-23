import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Controle Financeiro", layout="centered")

st.title("🏠 Controle Financeiro + Meta da Casa")

# =====================
# CONFIGURAÇÕES FIXAS
# =====================
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
# INPUT PRINCIPAL (1 PÁGINA)
# =====================
st.subheader("➕ Lançar movimento")

tipo = st.selectbox(
    "Tipo",
    [
        "💰 Salário",
        "💸 Gasto",
        "🏠 Reserva Casa"
    ]
)

descricao = st.text_input("Descrição (opcional)")
valor = st.number_input("Valor (R$)", min_value=0.0)

if st.button("Adicionar"):

    data = datetime.now().strftime("%Y-%m-%d")

    novo = pd.DataFrame([[data, tipo, descricao, valor]],
                        columns=df.columns)

    df = pd.concat([df, novo], ignore_index=True)
    df.to_csv(ARQUIVO, index=False)

    st.success("✔ Lançado com sucesso!")

st.divider()

# =====================
# CÁLCULOS
# =====================
salario = df[df["tipo"] == "💰 Salário"]["valor"].sum()
gastos = df[df["tipo"] == "💸 Gasto"]["valor"].sum()
reserva = df[df["tipo"] == "🏠 Reserva Casa"]["valor"].sum()

saldo = salario - gastos

falta_casa = META_CASA - reserva
progresso = reserva / META_CASA if META_CASA > 0 else 0

# =====================
# PAINEL PRINCIPAL
# =====================
st.subheader("📊 Visão geral")

col1, col2, col3 = st.columns(3)

col1.metric("💰 Salário total", f"R$ {salario:,.2f}")
col2.metric("💸 Gastos", f"R$ {gastos:,.2f}")
col3.metric("💰 Saldo atual", f"R$ {saldo:,.2f}")

st.divider()

# =====================
# META DA CASA
# =====================
st.subheader("🏠 Meta da Casa (R$ 500.000)")

st.write(f"💵 Já reservado: **R$ {reserva:,.2f}**")
st.write(f"🏠 Falta: **R$ {falta_casa:,.2f}**")

st.progress(min(progresso, 1.0))

st.write(f"📊 Progresso: **{progresso * 100:.2f}%**")

# ALERTA INTELIGENTE CASA
if progresso >= 1:
    st.success("🏠 META ALCANÇADA! Você já pode comprar a casa 🎉")
elif progresso >= 0.7:
    st.warning("🟡 Você já está perto da meta, continue firme!")
else:
    st.info("🔵 Construindo patrimônio... continue reservando!")

st.divider()

# =====================
# HISTÓRICO
# =====================
st.subheader("📋 Últimos registros")
st.dataframe(df.tail(10), use_container_width=True)
