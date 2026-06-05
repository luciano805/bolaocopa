import streamlit as st

# --- LÓGICA DO SISTEMA ---
class BolaoCopa2026:
    def __init__(self):
        self.participantes = {}

    def cadastrar_participante(self, nome):
        if nome not in self.participantes:
            self.participantes[nome] = {'pontuacao': 0}
            return True
        return False

# --- INTERFACE WEB COM STREAMLIT ---

# 1. Título do site
st.title("🏆 Bolão da Copa 2026 - HarmonizaPRO")

# 2. 'Memória' do site (para não perder os dados quando a página atualizar)
if 'bolao' not in st.session_state:
    st.session_state.bolao = BolaoCopa2026()

st.write("Bem-vindo ao software de gestão do bolão! Vamos começar cadastrando o pessoal.")

# 3. Área de Cadastro
st.header("1. Fazer cadastro")
nome_novo = st.text_input("Digite seu nome:")

# Botão de cadastro
if st.button("Cadastrar"):
    if nome_novo:
        sucesso = st.session_state.bolao.cadastrar_participante(nome_novo)
        if sucesso:
            st.success(f"Boa! {nome_novo} foi cadastrado com sucesso!")
        else:
            st.warning("Atenção: Esse nome já está cadastrado.")
    else:
        st.error("Por favor, digite um nome antes de clicar.")

# 4. Lista de Participantes
st.header("2. Quem já está no jogo?")
if st.session_state.bolao.participantes:
    for nome in st.session_state.bolao.participantes.keys():
        st.write(f"👤 {nome}")
else:
    st.info("Nenhum participante cadastrado ainda. Seja o primeiro!")

st.divider()
st.caption("Fase 2 do App (Em breve): Adicionar os seletores para escolher as 24 seleções classificadas e os 8 terceiros colocados!")
