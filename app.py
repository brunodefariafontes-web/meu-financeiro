import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Controle Financeiro", layout="centered")

st.title("💰 Controle Financeiro Inteligente")

ARQUIVO = "dados.csv"
CONFIG = "config.csv"

# =====================
# CRIAR ARQUIVOS SE NÃO EXISTIREM
# =====================
if not os.path.exists(ARQUIVO):
    df = pd.DataFrame(columns=["data", "tipo", "descricao", "valor"])
    df.to_csv(ARQUIVO, index=False)

if not os.path.exists(CONFIG):
    cfg = pd.DataFrame([[0.0]], columns=["saldo_inicial"])
    cfg.to_csv(CONFIG, index=False)

df = pd.read_csv(ARQUIVO)
cfg = pd.read_csv(CONFIG)

saldo_inicial = float(cfg.loc[0, "saldo_inicial"])

menu = st.sidebar.radio("Menu", ["⚙ Configuração", "➕ Lançamentos", "📊 Resumo"])

# =====================
# CONFIGURAÇÃO
# =====================
if menu == "⚙ Configuração":

    st.subheader("Definir saldo inicial")

    novo_saldo = st.number_input(
        "Quanto você tem hoje? (R$)",
        min_value=0.0,
        value=saldo_inicial,
        format="%.2f"
    )

    if st.button("Salvar saldo inicial"):
        cfg.loc[0, "saldo_inicial"] = novo_saldo
        cfg.to_csv(CONFIG, index=False)
        st.success("Saldo atualizado!")

# =====================
# LANÇAMENTOS
# =====================
elif menu == "➕ Lançamentos":

    tipo = st.selectbox(
        "Tipo",
        ["💰 Salário", "🛒 Compra", "💸 Gasto", "🧾 Conta"]
    )

    descricao = st.text_input("Descrição")
    valor = st.number_input("Valor (R$)", min_value=0.0)

    if st.button("Adicionar"):

        data = datetime.now().strftime("%Y-%m-%d")

        novo = pd.DataFrame([[data, tipo, descricao, valor]],
                            columns=df.columns)

        df = pd.concat([df, novo], ignore_index=True)
        df.to_csv(ARQUIVO, index=False)

        st.success("Lançado com sucesso!")

# =====================
# RESUMO
# =====================
elif menu == "📊 Resumo":

    if len(df) == 0:
        st.warning("Sem dados ainda.")
        st.stop()

    salarios = df[df["tipo"] == "💰 Salário"]["valor"].sum()
    gastos = df[df["tipo"] != "💰 Salário"]["valor"].sum()

    saldo_atual = saldo_inicial + salarios - gastos

    st.subheader("💰 Seu dinheiro")

    st.metric("Saldo inicial", f"R$ {saldo_inicial:.2f}")
    st.metric("Salários recebidos", f"R$ {salarios:.2f}")
    st.metric("Gastos totais", f"R$ {gastos:.2f}")
    st.metric("💰 Saldo atual", f"R$ {saldo_atual:.2f}")

    st.divider()

    # ALERTA INTELIGENTE
    if saldo_atual < saldo_inicial * 0.2:
        st.error("🔴 Atenção: seu saldo está muito baixo!")
    elif saldo_atual < saldo_inicial * 0.5:
        st.warning("🟡 Cuidado com os gastos.")
    else:
        st.success("🟢 Situação financeira saudável.")

    st.divider()

    st.subheader("📋 Últimos lançamentos")
    st.dataframe(df.tail(10), use_container_width=True)
