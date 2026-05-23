import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.title("💰 Controle Financeiro")

ARQUIVO = "dados.csv"

# -----------------------------
# CRIA ARQUIVO SE NÃO EXISTIR
# -----------------------------
if not os.path.exists(ARQUIVO):
    df = pd.DataFrame(columns=["data", "tipo", "categoria", "valor"])
    df.to_csv(ARQUIVO, index=False)

df = pd.read_csv(ARQUIVO)

menu = st.sidebar.selectbox("Menu", ["Adicionar", "Ver dados"])

# -----------------------------
# ADICIONAR
# -----------------------------
if menu == "Adicionar":

    tipo = st.selectbox("Tipo", ["Gasto", "Receita"])
    categoria = st.text_input("Categoria")
    valor = st.number_input("Valor", min_value=0.0)
    data = datetime.now().strftime("%Y-%m-%d")

    if st.button("Salvar"):
        novo = pd.DataFrame([[data, tipo, categoria, valor]],
                            columns=df.columns)

        df = pd.concat([df, novo], ignore_index=True)
        df.to_csv(ARQUIVO, index=False)

        st.success("Salvo com sucesso!")

# -----------------------------
# VER DADOS
# -----------------------------
elif menu == "Ver dados":
    st.write(df)

    st.metric("Total de registros", len(df))
