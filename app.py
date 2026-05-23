import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(
    page_title="Controle Financeiro",
    page_icon="🏠",
    layout="wide"
)

# =====================
# CONFIG
# =====================
META_CASA = 500000
ARQUIVO = "dados_financeiros.csv"

USUARIOS = {
    "43623202886": "Bruno",
    "42899462830": "Ingrid"
}

# =====================
# CRIAR CSV
# =====================
if not os.path.exists(ARQUIVO):

    df_inicial = pd.DataFrame(
        columns=[
            "Usuario",
            "Tipo",
            "Descricao",
            "Valor",
            "Data"
        ]
    )

    df_inicial.to_csv(ARQUIVO, index=False)

# =====================
# LER CSV
# =====================
try:
    df = pd.read_csv(ARQUIVO)
except:
    df = pd.DataFrame(
        columns=[
            "Usuario",
            "Tipo",
            "Descricao",
            "Valor",
            "Data"
        ]
    )

# =====================
# SESSION
# =====================
if "logado" not in st.session_state:
    st.session_state.logado = False

if "usuario" not in st.session_state:
    st.session_state.usuario = ""

# =====================
# LOGIN
# =====================
if not st.session_state.logado:

    st.title("🔐 Acesso ao Sistema")

    st.subheader("🏠 Controle Financeiro")

    cpf = st.text_input(
        "Digite seu CPF",
        max_chars=11
    ).strip()

    cpf = ''.join(filter(str.isdigit, cpf))

    if st.button("Entrar"):

        if str(cpf) in USUARIOS:

            st.session_state.logado = True
            st.session_state.usuario = USUARIOS[str(cpf)]

            st.rerun()

        else:
            st.error("CPF não autorizado")

    st.stop()

# =====================
# USUÁRIO
# =====================
usuario = st.session_state.usuario

# =====================
# DADOS GERAIS
# =====================
df_user = df

# =====================
# RESUMOS
# =====================
salario = df_user[
    df_user["Tipo"] == "💰 Salário"
]["Valor"].sum()

reserva_casa = df_user[
    df_user["Tipo"] == "🏠 Reserva Casa"
]["Valor"].sum()

gastos = df_user[
    (df_user["Tipo"] != "💰 Salário") &
    (df_user["Tipo"] != "🏠 Reserva Casa")
]["Valor"].sum()

saldo = salario - gastos - reserva_casa

falta_casa = META_CASA - reserva_casa

if falta_casa < 0:
    falta_casa = 0

progresso = reserva_casa / META_CASA

if progresso > 1:
    progresso = 1.0

# =====================
# APP
# =====================
st.title(f"🏠 Controle Financeiro - {usuario}")

st.success("Acesso realizado com sucesso ✔")

# =====================
# RESUMO FIXO
# =====================
st.divider()

st.subheader("🏠 Objetivo da Casa")

st.info(
    "Toda compra impacta sua meta. "
    "Pense na casa antes de gastar."
)

# =====================
# CARDS
# =====================
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Salário",
    f"R$ {salario:,.2f}"
)

col2.metric(
    "💸 Gastos",
    f"R$ {gastos:,.2f}"
)

col3.metric(
    "🏠 Casa",
    f"R$ {reserva_casa:,.2f}"
)

col4.metric(
    "💵 Saldo",
    f"R$ {saldo:,.2f}"
)

# =====================
# PROGRESSO CASA
# =====================
st.divider()

st.subheader("📈 Progresso da Casa")

st.write(f"🎯 Meta: R$ {META_CASA:,.2f}")
st.write(f"💵 Reservado: R$ {reserva_casa:,.2f}")
st.write(f"📉 Falta: R$ {falta_casa:,.2f}")

st.progress(progresso)

st.write(f"📊 Progresso: {progresso * 100:.2f}%")

# =====================
# ANÁLISE
# =====================
st.divider()

st.subheader("🧠 Análise Financeira")

if salario == 0:

    st.warning(
        "Cadastre um salário para iniciar a análise financeira."
    )

else:

    percentual = (gastos / salario) * 100

    if percentual > 80:

        st.error(
            "⚠ Seus gastos estão muito altos. "
            "Isso pode atrasar bastante a compra da casa."
        )

    elif percentual > 60:

        st.warning(
            "⚠ Seus gastos estão moderados. "
            "Tente reduzir compras não essenciais."
        )

    else:

        st.success(
            "✅ Seu controle financeiro está saudável."
        )

# =====================
# NOVO LANÇAMENTO
# =====================
st.divider()

st.subheader("➕ Novo Lançamento")

with st.form("form_lancamento", clear_on_submit=True):

    col_a, col_b = st.columns(2)

    with col_a:

        tipo = st.selectbox(
            "Tipo",
            [
                "💰 Salário",
                "🏠 Reserva Casa",
                "💳 Cartão",
                "💡 Luz",
                "🚿 Água",
                "🛒 Compras",
                "🍔 Alimentação",
                "🚗 Transporte",
                "📱 Internet",
                "🏥 Saúde",
                "🎮 Lazer",
                "📦 Outros"
            ]
        )

    with col_b:

        valor = st.number_input(
            "Valor",
            min_value=0.0,
            step=1.0
        )

    descricao = st.text_input("Descrição")

    # =====================
    # ALERTA ANTES DO GASTO
    # =====================
    if tipo != "💰 Salário":

        if valor > 1000:

            st.error(
                "⚠ Valor alto detectado. "
                "Pense na casa antes de concluir esse gasto."
            )

        elif valor > 300:

            st.warning(
                "⚠ Esse gasto pode atrasar sua meta da casa."
            )

        elif valor > 0:

            st.info(
                "🏠 Pequenos gastos recorrentes também impactam sua meta."
            )

    salvar = st.form_submit_button("Salvar Lançamento")

    if salvar:

        novo = pd.DataFrame([
            {
                "Usuario": usuario,
                "Tipo": tipo,
                "Descricao": descricao,
                "Valor": valor,
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M")
            }
        ])

        df = pd.concat([df, novo], ignore_index=True)

        df.to_csv(ARQUIVO, index=False)

        st.success("Lançamento salvo com sucesso ✔")

        st.rerun()

# =====================
# LANÇAMENTOS
# =====================
st.divider()

st.subheader("📋 Lançamentos")

if len(df_user) > 0:

    df_exibir = df_user.sort_index(
        ascending=False
    ).reset_index()

    for i, row in df_exibir.iterrows():

        with st.container():

            col1, col2, col3, col4, col5 = st.columns(
                [2, 3, 2, 2, 1]
            )

            col1.write(row["Tipo"])

            col2.write(row["Descricao"])

            col3.write(f'R$ {row["Valor"]:,.2f}')

            col4.write(row["Data"])

            # =====================
            # APAGAR
            # =====================
            if col5.button(
                "🗑",
                key=f"delete_{row['index']}"
            ):

                df = df.drop(row["index"])

                df.to_csv(ARQUIVO, index=False)

                st.success("Lançamento apagado ✔")

                st.rerun()

            st.divider()

else:

    st.info("Nenhum lançamento encontrado.")

# =====================
# EXPORTAR CSV
# =====================
st.divider()

st.subheader("📤 Exportar Dados")

csv = df_user.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Baixar CSV",
    data=csv,
    file_name="controle_financeiro.csv",
    mime="text/csv"
)

# =====================
# ZERAR DADOS
# =====================
st.divider()

st.subheader("🗑 Reiniciar Controle")

st.warning(
    "Essa ação apagará todos os lançamentos."
)

if st.button("Zerar Todos os Dados"):

    df = pd.DataFrame(
        columns=[
            "Usuario",
            "Tipo",
            "Descricao",
            "Valor",
            "Data"
        ]
    )

    df.to_csv(ARQUIVO, index=False)

    st.success("Todos os dados foram apagados ✔")

    st.rerun()

# =====================
# SAIR
# =====================
st.divider()

if st.button("Sair"):

    st.session_state.logado = False
    st.session_state.usuario = ""

    st.rerun()
