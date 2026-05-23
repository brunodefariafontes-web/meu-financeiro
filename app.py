import streamlit as st

st.set_page_config(
    page_title="Controle Financeiro",
    page_icon="🏠"
)

# =====================
# CPFs AUTORIZADOS
# =====================
USUARIOS = {
    "43623202886": "Bruno",
    "42899462830": "Ingrid"
}

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

    cpf = st.text_input("Digite seu CPF")

    if st.button("Entrar"):

        if cpf in USUARIOS:

            st.session_state.logado = True
            st.session_state.usuario = USUARIOS[cpf]

            st.rerun()

        else:
            st.error("CPF não autorizado")

    st.stop()

# =====================
# APP
# =====================
st.title(f"🏠 Bem-vindo {st.session_state.usuario}")

st.success("Acesso realizado com sucesso ✔")

st.write("Seu aplicativo financeiro está funcionando.")

# =====================
# SAIR
# =====================
if st.button("Sair"):

    st.session_state.logado = False
    st.session_state.usuario = ""

    st.rerun()
