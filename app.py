import streamlit as st
import pandas as pd
import os
import hashlib

st.set_page_config(page_title="Controle Financeiro", page_icon="🏠")

# =====================
# USUÁRIOS PERMITIDOS
# =====================
USUARIOS = {
    "43623202886": "Bruno",
    "42899462830": "Ingrid"
}

ARQ_USERS = "users.csv"

# =====================
# HASH
# =====================
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

if "modo" not in st.session_state:
    st.session_state.modo = "cpf"

# =====================
# LOGOUT AUTOMÁTICO SIMPLES (reset)
# =====================
def reset():
    st.session_state.cpf_logado = None
    st.session_state.modo = "cpf"

# =====================
# TELA DE LOGIN / CADASTRO
# =====================
if st.session_state.cpf_logado is None:

    st.title("🔐 Sistema de Acesso")

    cpf = st.text_input("Digite seu CPF")

    if cpf not in USUARIOS:
        st.warning("CPF não autorizado")
        st.stop()

    nome = USUARIOS[cpf]
    st.success(f"Olá {nome}")

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
                st.error("As senhas não coincidem")
                st.stop()

            novo = pd.DataFrame([[cpf, hash_senha(senha1)]],
                                columns=["cpf", "senha"])

            users = pd.concat([users, novo], ignore_index=True)
            users.to_csv(ARQ_USERS, index=False)

            st.success("Conta criada! Agora faça login.")
            st.stop()

    st.stop()

# =====================
# APP LOGADO
# =====================
nome = USUARIOS[st.session_state.cpf_logado]

st.title(f"🏠 Bem-vindo {nome}")

st.success("Login realizado com sucesso ✔")

if st.button("Sair"):
    reset()
    st.rerun()
