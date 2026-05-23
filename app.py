import streamlit as st
import pandas as pd
import os
import hashlib

st.set_page_config(page_title="Controle Financeiro", page_icon="🏠")

USUARIOS = {
    "43623202886": "Bruno",
    "42899462830": "Ingrid"
}

ARQ_USERS = "users.csv"

def hash_senha(s):
    return hashlib.sha256(s.encode()).hexdigest()

# =====================
# ARQUIVO
# =====================
if not os.path.exists(ARQ_USERS):
    pd.DataFrame(columns=["cpf", "senha"]).to_csv(ARQ_USERS, index=False)

users = pd.read_csv(ARQ_USERS)

# =====================
# SESSION STATE
# =====================
if "cpf" not in st.session_state:
    st.session_state.cpf = ""

if "logado" not in st.session_state:
    st.session_state.logado = False

# =====================
# LOGIN / CADASTRO
# =====================
if not st.session_state.logado:

    st.title("🔐 Sistema de Acesso")

    cpf = st.text_input("CPF", value=st.session_state.cpf)
    st.session_state.cpf = cpf

    if cpf == "":
        st.stop()

    if cpf not in USUARIOS:
        st.warning("CPF não autorizado")
        st.stop()

    st.success(f"Olá {USUARIOS[cpf]}")

    # =====================
    # SE JÁ EXISTE → LOGIN
    # =====================
    if cpf in users["cpf"].values:

        st.subheader("🔑 Login")

        senha = st.text_input("Senha", type="password")

        if st.button("Entrar"):

            senha_salva = users.loc[users["cpf"] == cpf, "senha"].values[0]

            if hash_senha(senha) == senha_salva:
                st.session_state.logado = True
                st.rerun()
            else:
                st.error("Senha incorreta")

    # =====================
    # PRIMEIRO ACESSO → CADASTRO
    # =====================
    else:

        st.subheader("🆕 Criar conta")

        senha1 = st.text_input("Criar senha", type="password")
        senha2 = st.text_input("Confirmar senha", type="password")

        if st.button("Cadastrar"):

            if senha1 == "" or senha2 == "":
                st.warning("Preencha os campos")
                st.stop()

            if senha1 != senha2:
                st.error("Senhas não coincidem")
                st.stop()

            novo = pd.DataFrame([[cpf, hash_senha(senha1)]],
                                columns=["cpf","senha"])

            users = pd.concat([users, novo], ignore_index=True)
            users.to_csv(ARQ_USERS, index=False)

            st.session_state.logado = True
            st.rerun()

    st.stop()

# =====================
# APP LOGADO
# =====================
st.title(f"🏠 Bem-vindo {USUARIOS[st.session_state.cpf]}")

st.success("Login realizado com sucesso ✔")

if st.button("Sair"):
    st.session_state.logado = False
    st.session_state.cpf = ""
    st.rerun()
