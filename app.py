import streamlit as st
import pandas as pd
import os
import hashlib
from datetime import datetime
import time

st.set_page_config(page_title="Controle Financeiro", page_icon="🏠")

# =====================
# CONFIG
# =====================
USERS_FIXOS = {
    "43623202886": {"nome": "Bruno"},
    "42899462830": {"nome": "Ingrid"}
}

META_CASA = 500000

ARQ_USERS = "users.csv"
ARQ_DATA = "dados.csv"

# =====================
# HASH
# =====================
def hash_senha(s):
    return hashlib.sha256(s.encode()).hexdigest()

# =====================
# ARQUIVOS
# =====================
if not os.path.exists(ARQ_USERS):
    pd.DataFrame(columns=["cpf", "senha"]).to_csv(ARQ_USERS, index=False)

if not os.path.exists(ARQ_DATA):
    pd.DataFrame(columns=["cpf","data","tipo","descricao","valor"]).to_csv(ARQ_DATA, index=False)

users = pd.read_csv(ARQ_USERS)
df = pd.read_csv(ARQ_DATA)

# =====================
# SESSION STATE
# =====================
if "cpf" not in st.session_state:
    st.session_state.cpf = None

if "last_action" not in st.session_state:
    st.session_state.last_action = time.time()

# =====================
# TIMEOUT 10 MIN
# =====================
def check_timeout():
    if st.session_state.cpf is not None:
        if time.time() - st.session_state.last_action > 600:  # 10 min
            st.session_state.cpf = None
            st.warning("⏳ Sessão expirada por inatividade")
            st.rerun()

check_timeout()

# =====================
# LOGIN
# =====================
if st.session_state.cpf is None:

    st.title("🔐 Acesso ao Sistema")

    cpf = st.text_input("CPF")

    if cpf not in USERS_FIXOS:
        st.warning("CPF não autorizado")
        st.stop()

    st.success(f"Olá {USERS_FIXOS[cpf]['nome']}, seja bem-vindo!")

    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):

        st.session_state.last_action = time.time()

        if cpf in users["cpf"].values:

            senha_salva = users[users["cpf"] == cpf]["senha"].values[0]

            if hash_senha(senha) == senha_salva:
                st.session_state.cpf = cpf
                st.rerun()
            else:
                st.error("Senha incorreta")

        else:
            nova = pd.DataFrame([[cpf, hash_senha(senha)]],
                                columns=users.columns)

            users = pd.concat([users, nova], ignore_index=True)
            users.to_csv(ARQ_USERS, index=False)

            st.session_state.cpf = cpf
            st.success("Conta criada!")
            st.rerun()

    st.stop()

# =====================
# APP LOGADO
# =====================
st.session_state.last_action = time.time()

nome = USERS_FIXOS[st.session_state.cpf]["nome"]

st.title(f"🏠 Controle Financeiro de {nome}")

# =====================
# LANÇAR
# =====================
st.subheader("➕ Lançar")

tipo = st.selectbox(
    "Tipo",
    ["💰 Salário","🏠 Reserva Casa","💸 Gasto","💡 Luz","🚿 Água","💳 Cartão","🛒 Compras"]
)

descricao = st.text_input("Descrição")
valor = st.number_input("Valor", min_value=0.0)

if st.button("Adicionar"):

    st.session_state.last_action = time.time()

    data = datetime.now().strftime("%Y-%m-%d")

    novo = pd.DataFrame([[st.session_state.cpf,data,tipo,descricao,valor]],
                        columns=df.columns)

    df = pd.concat([df, novo], ignore_index=True)
    df.to_csv(ARQ_DATA, index=False)

    st.success("✔ Lançado!")

st.divider()

# =====================
# FILTRO USER
# =====================
df_user = df[df["cpf"] == st.session_state.cpf]

if len(df_user) == 0:
    st.info("Sem dados ainda")
    st.stop()

# =====================
# RESUMO
# =====================
salario = df_user[df_user["tipo"] == "💰 Salário"]["valor"].sum()
reserva = df_user[df_user["tipo"] == "🏠 Reserva Casa"]["valor"].sum()
gastos = df_user[df_user["tipo"] != "💰 Salário"]["valor"].sum()

saldo = salario - gastos
falta = META_CASA - reserva
progresso = reserva / META_CASA

st.subheader("📊 Resumo")

st.metric("💰 Salário", f"R$ {salario:.2f}")
st.metric("💸 Gastos", f"R$ {gastos:.2f}")
st.metric("💰 Saldo", f"R$ {saldo:.2f}")

st.divider()

st.subheader("🏠 Casa")

st.write(f"Reservado: R$ {reserva:.2f}")
st.write(f"Falta: R$ {falta:.2f}")

st.progress(min(progresso,1.0))
