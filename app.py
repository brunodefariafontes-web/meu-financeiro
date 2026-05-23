import streamlit as st
import pandas as pd
import os
import hashlib

st.set_page_config(page_title="Controle Financeiro", page_icon="🏠")

USERS_FILE = "users.csv"
ARQ = "dados.csv"

# =====================
# USUÁRIOS FIXOS AUTORIZADOS
# =====================
USERS_FIXOS = {
    "43623202886": {
        "nome": "Bruno",
        "msg": "Olá Bruno, seja bem-vindo!"
    },
    "42899462830": {
        "nome": "Ingrid",
        "msg": "Olá Ingrid, seja bem-vinda!"
    }
}

# =====================
# HASH SENHA
# =====================
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# =====================
# ARQUIVOS
# =====================
if not os.path.exists(USERS_FILE):
    pd.DataFrame(columns=["cpf", "senha", "biometria"]).to_csv(USERS_FILE, index=False)

if not os.path.exists(ARQ):
    pd.DataFrame(columns=["cpf", "data", "tipo", "descricao", "valor"]).to_csv(ARQ, index=False)

users = pd.read_csv(USERS_FILE)

# =====================
# ESTADO
# =====================
if "cpf_logado" not in st.session_state:
    st.session_state.cpf_logado = None

# =====================
# LOGIN CPF
# =====================
if st.session_state.cpf_logado is None:

    st.title("🔐 Acesso ao Sistema")

    cpf = st.text_input("Digite seu CPF")

    if cpf not in USERS_FIXOS:
        st.error("❌ CPF não autorizado")
        st.stop()

    user_info = USERS_FIXOS[cpf]

    st.success(user_info["msg"])

    st.write("📌 Crie sua senha e confirme o acesso")

    senha = st.text_input("Senha", type="password")

    biometria = st.checkbox("✔ Confirmo cadastro de biometria (simulado)")

    if st.button("Entrar / Cadastrar"):

        if not biometria:
            st.warning("Você precisa confirmar a biometria (simulado)")
            st.stop()

        # verifica se já existe
        if cpf in users["cpf"].values:

            senha_salva = users[users["cpf"] == cpf]["senha"].values[0]

            if hash_senha(senha) == senha_salva:
                st.session_state.cpf_logado = cpf
                st.rerun()
            else:
                st.error("Senha incorreta")

        else:
            # primeiro acesso -> cria conta
            nova = pd.DataFrame([[cpf, hash_senha(senha), True]],
                                columns=users.columns)

            users = pd.concat([users, nova], ignore_index=True)
            users.to_csv(USERS_FILE, index=False)

            st.session_state.cpf_logado = cpf
            st.success("Conta criada com sucesso!")
            st.rerun()

    st.stop()

# =====================
# USUÁRIO LOGADO
# =====================
nome = USERS_FIXOS[st.session_state.cpf_logado]["nome"]

st.title(f"🏠 Olá {nome}, bem-vindo ao seu controle financeiro")
