import streamlit as st
import pandas as pd
import hashlib
from datetime import datetime

st.set_page_config(page_title="Controle Financeiro", page_icon="🏠")

USUARIOS = {
    "43623202886": "Bruno",
    "42899462830": "Ingrid"
}

def hash_senha(s):
    return hashlib.sha256(s.encode()).hexdigest()

# =====================
# CRIA DATAFRAME DO ZERO SEM ARQUIVO
# =====================
if "users" not in st.session_state:
    st.session_state.users = pd.DataFrame(columns=["cpf", "senha"])

if "dados" not in st.session_state:
    st.session_state.dados = pd.DataFrame(columns=["cpf","data","tipo","descricao","valor"])

if "cpf" not in st.session_state:
    st.session_state.cpf = None

# =====================
# LOGIN
# =====================
if st.session_state.cpf is None:

    st.title("🔐 Acesso")

    cpf = st.text_input("CPF")

    if cpf not in USUARIOS:
        st.warning("CPF não autorizado")
        st.stop()

    st.success(f"Olá {USUARIOS[cpf]}")

    senha = st.text_input("Senha", type="password")

    if st.button("Entrar / Criar"):

        users = st.session_state.users

        if cpf in users["cpf"].values:

            senha_salva = users.loc[users["cpf"] == cpf, "senha"].values[0]

            if hash_senha(senha) == senha_salva:
                st.session_state.cpf = cpf
                st.rerun()
            else:
                st.error("Senha errada")

        else:
            st.session_state.users = pd.concat([
                users,
                pd.DataFrame([[cpf, hash_senha(senha)]], columns=["cpf","senha"])
            ], ignore_index=True)

            st.session_state.cpf = cpf
            st.rerun()

    st.stop()

# =====================
# APP
# =====================
nome = USUARIOS[st.session_state.cpf]

st.title(f"🏠 Olá {nome}")

st.subheader("➕ Lançar")

tipo = st.selectbox("Tipo", ["💰 Salário","💸 Gasto","🏠 Reserva Casa"])
desc = st.text_input("Descrição")
valor = st.number_input("Valor", min_value=0.0)

if st.button("Adicionar"):

    novo = pd.DataFrame([[
        st.session_state.cpf,
        datetime.now().strftime("%Y-%m-%d"),
        tipo,
        desc,
        valor
    ]], columns=["cpf","data","tipo","descricao","valor"])

    st.session_state.dados = pd.concat([st.session_state.dados, novo], ignore_index=True)

    st.success("Salvo!")

df = st.session_state.dados
df = df[df["cpf"] == st.session_state.cpf]

st.divider()
st.subheader("📊 Resumo")

if len(df) > 0:
    st.write(df.tail(10))
else:
    st.info("Sem dados ainda")
