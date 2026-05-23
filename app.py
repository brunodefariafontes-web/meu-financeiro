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
ARQ_DATA = "dados.csv"

# =====================
# HASH SENHA
# =====================
def hash_senha(s):
    return hashlib.sha256(s.encode()).hexdigest()

# =====================
# CRIAR ARQUIVOS SE NÃO EXISTIREM
# =====================
if not os.path.exists(ARQ_USERS):
    pd.DataFrame(columns=["cpf", "senha"]).to_csv(ARQ_USERS, index=False)

if not os.path.exists(ARQ_DATA):
    pd.DataFrame(columns=["cpf","data","tipo","descricao","valor"]).to_csv(ARQ_DATA, index=False)

# =====================
# LER DADOS
# =====================
users = pd.read_csv(ARQ_USERS)
df = pd.read_csv(ARQ_DATA)

# garante colunas corretas (evita erro que você teve)
if "cpf" not in users.columns:
    users = pd.DataFrame(columns=["cpf", "senha"])

# =====================
# SESSION
# =====================
if "cpf" not in st.session_state:
    st.session_state.cpf = None

# =====================
# LOGIN / PRIMEIRO ACESSO
# =====================
if st.session_state.cpf is None:

    st.title("🔐 Acesso ao Sistema")

    cpf = st.text_input("CPF")

    if cpf not in USUARIOS:
        st.warning("CPF não autorizado")
        st.stop()

    st.success(f"Olá {USUARIOS[cpf]}, seja bem-vindo!")

    senha = st.text_input("Senha", type="password")

    if st.button("Entrar / Criar conta"):

        # =====================
        # PRIMEIRO ACESSO
        # =====================
        if cpf not in users["cpf"].values:

            if senha == "":
                st.warning("Crie uma senha para continuar")
                st.stop()

            novo = pd.DataFrame([[cpf, hash_senha(senha)]],
                                columns=["cpf", "senha"])

            users = pd.concat([users, novo], ignore_index=True)
            users.to_csv(ARQ_USERS, index=False)

            st.session_state.cpf = cpf
            st.success("Conta criada com sucesso!")
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
# APP PRINCIPAL
# =====================
nome = USUARIOS[st.session_state.cpf]

st.title(f"🏠 Controle Financeiro - {nome}")

st.divider()

# =====================
# LANÇAR DADOS
# =====================
st.subheader("➕ Lançar")

tipo = st.selectbox(
    "Tipo",
    ["💰 Salário","🏠 Reserva Casa","💸 Gasto","💡 Luz","🚿 Água","💳 Cartão","🛒 Compras"]
)

descricao = st.text_input("Descrição")
valor = st.number_input("Valor", min_value=0.0)

if st.button("Adicionar"):

    novo = pd.DataFrame([[
        st.session_state.cpf,
        datetime.now().strftime("%Y-%m-%d"),
        tipo,
        descricao,
        valor
    ]], columns=df.columns)

    df = pd.concat([df, novo], ignore_index=True)
    df.to_csv(ARQ_DATA, index=False)

    st.success("✔ Salvo!")

st.divider()

# =====================
# FILTRAR USUÁRIO
# =====================
df_user = df[df["cpf"] == st.session_state.cpf]

if len(df_user) > 0:

    salario = df_user[df_user["tipo"] == "💰 Salário"]["valor"].sum()
    reserva = df_user[df_user["tipo"] == "🏠 Reserva Casa"]["valor"].sum()
    gastos = df_user[df_user["tipo"] != "💰 Salário"]["valor"].sum()

    META_CASA = 500000

    saldo = salario - gastos
    falta = META_CASA - reserva
    progresso = reserva / META_CASA if META_CASA > 0 else 0

    st.subheader("📊 Resumo")

    st.metric("💰 Salário", f"R$ {salario:.2f}")
    st.metric("💸 Gastos", f"R$ {gastos:.2f}")
    st.metric("💰 Saldo", f"R$ {saldo:.2f}")

    st.divider()

    st.subheader("🏠 Casa")

    st.write(f"Meta: R$ {META_CASA:,.2f}")
    st.write(f"Reservado: R$ {reserva:,.2f}")
    st.write(f"Falta: R$ {falta:,.2f}")

    st.progress(min(progresso, 1.0))

else:
    st.info("Sem lançamentos ainda")
