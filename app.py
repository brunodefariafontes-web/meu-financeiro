import streamlit as st
import pandas as pd
import os

st.title("💰 Controle Financeiro")

ARQUIVO = "dados.csv"

if not os.path.exists(ARQUIVO):
    df = pd.DataFrame(columns=["data", "tipo", "categoria", "valor"])
    df.to_csv(ARQUIVO, index=False)

df = pd.read_csv(ARQUIVO)

st.write(df)
