import streamlit as st
import pandas as pd
import os
import hashlib
from datetime import datetime

st.set_page_config(page_title="Controle Financeiro", page_icon="🏠")

# =====================
# USUÁRIOS AUTORIZADOS
# =====================
USUARIOS = {
    "43623202886": "Bruno",
    "42899462830": "Ingrid"
}

ARQ_USERS = "users.csv"

# =====================
# HASH SENHA
# =====================
def hash_senha(s):
    return hashlib.sha256(s.encode()).hexdigest()

# =====================
# CRIAR ARQUIVO SE NÃO EXISTIR
# =====================
if not os.path.exists(ARQ_USERS):
    pd.DataFrame(columns=["cpf", "senha"]).to_csv(ARQ_USERS, index=False)

users = pd.read_csv(ARQ_USERS)

# garantir colunas corretas
if "cpf" not in users.columns or "senha" not in users.columns:
    users = pd.DataFrame(columns=["cpf", "senha"])

# =====================
# SESSION
# =====================
if "cpf" not in st.session_state:
    st.session_state.cpf = None

# =====================
# LOGIN
# =====================
if st.session_state.cpf is None:

    st.title("🔐 Acesso ao Sistema")

    cpf = st.text_input("CPF")

    if cpf not in USUARIOS:
        st.warning("CPF não autorizado")
        st.stop()

    st.success(f"Olá {USUARIOS[cpf]}, seja bem-vindo!")

    senha = st.text_input("Senha", type="password")

    if st.button("Entrar / Criar senha"):

        # =====================
        # PRIMEIRO ACESSO
        # =====================
        if cpf not in users["cpf"].values:

            if senha == "":
                st.warning("Digite uma senha para criar conta")
                st.stop()

            novo = pd.DataFrame([[cpf, hash_senha(senha)]],
                                columns=["cpf", "senha"])

            users = pd.concat([users, novo], ignore_index=True)
            users.to_csv(ARQ_USERS, index=False)

            st.session_state.cpf = cpf
            st.success("Senha criada com sucesso!")
            st.rerun()

        # =====================
        # LOGIN NORMAL
        # =====================
        else:

            senha_salva = users.loc[users["cpf"] == cpf, "senha"].values[0]

            if hash_senha(senha) == senha_salva:
                st.session_state.cpf = cpf
                st.rerun()
            else:
                st.error("Senha incorreta")

    st.stop()

# =====================
# APP PRINCIPAL (SIMPLES)
# =====================
nome = USUARIOS[st.session_state.cpf]

st.title(f"🏠 Olá {nome}")

st.success("Login realizado com sucesso ✔")
