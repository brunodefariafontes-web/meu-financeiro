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

# =====================
# HASH
# =====================
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# =====================
# CRIA CSV
# =====================
if not os.path.exists(ARQ_USERS):
    df = pd.DataFrame(columns=["cpf", "senha"])
    df.to_csv(ARQ_USERS, index=False)

# =====================
# LÊ CSV
# =====================
users = pd.read_csv(ARQ_USERS)

# =====================
# SESSION
# =====================
if "logado" not in st.session_state:
    st.session_state.logado = False

if "cpf_logado" not in st.session_state:
    st.session_state.cpf_logado = ""

# =====================
# APP LOGADO
# =====================
if st.session_state.logado:

    st.title(f"🏠 Bem-vindo {USUARIOS[st.session_state.cpf_logado]}")
    st.success("Login realizado com sucesso ✔")

    if st.button("Sair"):
        st.session_state.logado = False
        st.session_state.cpf_logado = ""
        st.rerun()

    st.stop()

# =====================
# LOGIN / CADASTRO
# =====================
st.title("🔐 Acesso ao Sistema")

cpf = st.text_input("CPF")

if cpf == "":
    st.stop()

if cpf not in USUARIOS:
    st.warning("CPF não autorizado")
    st.stop()

st.success(f"Olá {USUARIOS[cpf]}")

# =====================
# LOGIN
# =====================
if cpf in users["cpf"].values:

    st.subheader("🔑 Login")

    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):

        senha_salva = users.loc[
            users["cpf"] == cpf,
            "senha"
        ].values[0]

        if hash_senha(senha) == senha_salva:

            st.session_state.logado = True
            st.session_state.cpf_logado = cpf

            st.rerun()

        else:
            st.error("Senha incorreta")

# =====================
# CADASTRO
# =====================
else:

    st.subheader("🆕 Criar Conta")

    senha1 = st.text_input("Criar senha", type="password")
    senha2 = st.text_input("Confirmar senha", type="password")

    if st.button("Cadastrar"):

        if senha1 == "" or senha2 == "":
            st.warning("Preencha todos os campos")
            st.stop()

        if senha1 != senha2:
            st.error("As senhas não coincidem")
            st.stop()

        novo = pd.DataFrame([
            [cpf, hash_senha(senha1)]
        ], columns=["cpf", "senha"])

        users = pd.concat([users, novo], ignore_index=True)

        # 🔥 SALVA DE VERDADE
        users.to_csv(ARQ_USERS, index=False)

        st.success("Conta criada com sucesso!")

        st.info("Agora faça login com sua senha.")
