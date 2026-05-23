import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Controle Financeiro Inteligente", layout="centered")

st.title("🏠 Controle Financeiro Inteligente")

META_CASA = 500000
ARQUIVO = "dados.csv"

# =====================
# CRIAR ARQUIVO
# =====================
if not os.path.exists(ARQUIVO):
    df = pd.DataFrame(columns=["data", "tipo", "categoria", "descricao", "valor"])
    df.to_csv(ARQUIVO, index=False)

df = pd.read_csv(ARQUIVO)

# =====================
# CATEGORIAS COMPLETAS
# =====================
categorias = [
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

# =====================
# INPUT
# =====================
st.subheader("➕ Novo lançamento")

tipo = st.selectbox("Tipo", categorias)
descricao = st.text_input("Descrição (opcional)")
valor = st.number_input("Valor (R$)", min_value=0.0)

if st.button("Adicionar"):

    data = datetime.now().strftime("%Y-%m-%d")

    novo = pd.DataFrame([[data, tipo, tipo, descricao, valor]],
                        columns=df.columns)

    df = pd.concat([df, novo], ignore_index=True)
    df.to_csv(ARQUIVO, index=False)

    st.success("✔ Registrado!")

st.divider()

# =====================
# CÁLCULOS
# =====================
salario = df[df["tipo"] == "💰 Salário"]["valor"].sum()
reserva = df[df["tipo"] == "🏠 Reserva Casa"]["valor"].sum()

gastos = df[df["tipo"] != "💰 Salário"]["valor"].sum()

saldo = salario - gastos

falta = META_CASA - reserva
progresso = reserva / META_CASA if META_CASA > 0 else 0

# gastos por grupo
fixos = df[df["tipo"].isin(["💡 Luz","🚿 Água","📶 Internet","💳 Cartão","🏠 Aluguel"])]["valor"].sum()
variaveis = df[df["tipo"].isin(["🛒 Comprinhas","🍔 Lazer","🛍 Mercado","💸 Outros"])]["valor"].sum()

# =====================
# PAINEL
# =====================
st.subheader("📊 Visão geral")

col1, col2, col3 = st.columns(3)

col1.metric("💰 Salário", f"R$ {salario:,.2f}")
col2.metric("💸 Gastos", f"R$ {gastos:,.2f}")
col3.metric("💰 Saldo", f"R$ {saldo:,.2f}")

st.divider()

# =====================
# META CASA
# =====================
st.subheader("🏠 Meta da Casa (R$ 500.000)")

st.write(f"💵 Reservado: **R$ {reserva:,.2f}**")
st.write(f"🏠 Falta: **R$ {falta:,.2f}**")

st.progress(min(progresso, 1.0))
st.write(f"📊 Progresso: **{progresso*100:.2f}%**")

# =====================
# ANÁLISE INTELIGENTE
# =====================
st.subheader("🧠 Análise financeira")

if salario > 0:
    gasto_pct = (gastos / salario) * 100

    if gasto_pct > 85:
        st.error("🔴 Você está gastando demais! Isso prejudica MUITO a compra da casa.")
        st.write("👉 Corte principalmente: Comprinhas e Cartão.")
    elif gasto_pct > 70:
        st.warning("🟡 Atenção: seus gastos estão altos.")
        st.write("👉 Tente reduzir gastos variáveis para acelerar a casa.")
    else:
        st.success("🟢 Você está no caminho certo da casa!")

# =====================
# ALERTA POR TIPO
# =====================
st.divider()

st.subheader("📌 Onde ajustar")

if variaveis > fixos:
    st.warning("⚠️ Seus gastos variáveis estão maiores que os fixos.")
    st.write("👉 Diminua: comprinhas, lazer e mercado não essencial.")
else:
    st.success("✔ Gastos estão bem controlados.")

if variaveis > salario * 0.3:
    st.error("🔴 Gastos supérfluos muito altos!")
    st.write("👉 Para acelerar a casa: reduza agora.")
else:
    st.info("💡 Gastos variáveis dentro do aceitável.")

# =====================
# HISTÓRICO
# =====================
st.divider()

st.subheader("📋 Últimos registros")
st.dataframe(df.tail(10), use_container_width=True)
