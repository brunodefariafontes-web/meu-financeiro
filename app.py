import streamlit as st
import pandas as pd
import os
from datetime import datetime

# =====================
# CONFIGURAÇÃO DA PÁGINA
# =====================
st.set_page_config(
    page_title="Financeiro Pessoal",
    page_icon="💰",
    layout="centered"
)

# =====================
# TÍTULO BONITO
# =====================
st.markdown("""
    <h1 style='text-align: center; color: #00B4D8;'>💰 Meu Controle Financeiro</h1>
    <p style='text-align: center;'>Organize seu dinheiro de forma simples</p>
""", unsafe_allow_html=True)

ARQUIVO = "dados.csv"

# =====================
# CRIAR ARQUIVO SE NÃO EXISTIR
# =====================
if not os.path.exists(ARQUIVO):
    df = pd.DataFrame(columns=["data", "tipo", "categoria", "valor"])
    df.to_csv(ARQUIVO, index=False)

df = pd.read_csv(ARQUIVO)

# =====================
# MENU
# =====================
menu = st.sidebar.radio(
    "📌 Menu",
    ["➕ Adicionar", "📊 Resumo"]
)

# =====================
# ADICIONAR
# =====================
if menu == "➕ Adicionar":

    st.subheader("Adicionar novo registro")

    tipo = st.selectbox("Tipo", ["💸 Gasto", "💰 Receita"])
    categoria = st.text_input("Categoria (ex: mercado, salário)")
    valor = st.number_input("Valor (R$)", min_value=0.0, format="%.2f")

    if st.button("Salvar"):
        data = datetime.now().strftime("%Y-%m-%d")

        novo = pd.DataFrame([[data, tipo, categoria, valor]],
                            columns=df.columns)

        df = pd.concat([df, novo], ignore_index=True)
        df.to_csv(ARQUIVO, index=False)

        st.success("✔ Salvo com sucesso!")

# =====================
# RESUMO BONITO
# =====================
elif menu == "📊 Resumo":

    st.subheader("Resumo financeiro")

    if len(df) == 0:
        st.warning("Nenhum dado registrado ainda.")
    else:

        receitas = df[df["tipo"] == "💰 Receita"]["valor"].sum()
        gastos = df[df["tipo"] == "💸 Gasto"]["valor"].sum()
        saldo = receitas - gastos

        # CARDS BONITOS
        col1, col2, col3 = st.columns(3)

        col1.metric("💰 Receita", f"R$ {receitas:.2f}")
        col2.metric("💸 Gasto", f"R$ {gastos:.2f}")
        col3.metric("📊 Saldo", f"R$ {saldo:.2f}")

        st.divider()

        st.subheader("📋 Últimos registros")
        st.dataframe(df.tail(10), use_container_width=True)
