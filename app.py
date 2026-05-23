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

if "cpf_logado" not in st.session_state:
    st.session_state.cpf_logado = None

if "cpf_temp" not in st.session_state:
    st.session_state.cpf_temp = ""

if "modo" not in st.session_state:
    st.session_state.modo = "cpf"  # cpf / login / cadastro

# =====================
# TELA CPF
# =====================
st.title("🔐 Acesso ao Sistema")

cpf = st.text_input("CPF", value=st.session_state.cpf_temp)
st.session_state.cpf_temp = cpf

if cpf == "":
    st.stop()

if cpf not in USUARIOS:
    st.warning("CPF não autorizado")
    st.stop()

st.success(f"Olá {USUARIOS[cpf]}")

# =====================
# SE USUÁRIO JÁ EXISTE → LOGIN
# =====================
if cpf in users["cpf"].values:

    st.subheader("🔑 Login")

    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):

        senha_salva = users.loc[users["cpf"] == cpf, "senha"].values[0]

        if hash_senha(senha) == senha_salva:
            st.session_state.cpf_logado = cpf
            st.rerun()
        else:
            st.error("Senha incorreta")

# =====================
# SE NÃO EXISTE → CADASTRO
# =====================
else:

    st.subheader("🆕 Criar conta")

    senha1 = st.text_input("Criar senha", type="password")
    senha2 = st.text_input("Confirmar senha", type="password")

    if st.button("Cadastrar"):

        if senha1 == "" or senha2 == "":
            st.warning("Preencha todos os campos")
            st.stop()

        if senha1 != senha2:
            st.error("Senhas não coincidem")
            st.stop()

        users = pd.concat([
            users,
            pd.DataFrame([[cpf, hash_senha(senha1)]], columns=["cpf","senha"])
        ], ignore_index=True)

        users.to_csv(ARQ_USERS, index=False)

        st.success("Conta criada! Agora faça login.")
        st.rerun()

# =====================
# APP (SÓ ENTRA SE LOGADO)
# =====================
if st.session_state.cpf_logado is not None:

    st.title(f"🏠 Bem-vindo {USUARIOS[st.session_state.cpf_logado]}")

    st.success("Login realizado com sucesso ✔")

    if st.button("Sair"):
        st.session_state.cpf_logado = None
        st.rerun()
