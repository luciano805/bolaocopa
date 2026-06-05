import streamlit as st

# --- DADOS DA COPA DO MUNDO 2026 ---
# Grupos limpos e organizados
GRUPOS = {
    "Grupo A": ["🇲🇽 México", "🇿🇦 África do Sul", "🇰🇷 Coreia do Sul", "🇨🇿 República Tcheca"],
    "Grupo B": ["🇨🇦 Canadá", "🇧🇦 Bósnia e Herzegovina", "🇶🇦 Catar", "🇨🇭 Suíça"],
    "Grupo C": ["🇧🇷 Brasil", "🇲🇦 Marrocos", "🇭🇹 Haiti", "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Escócia"],
    "Grupo D": ["🇺🇸 Estados Unidos", "🇵🇾 Paraguai", "🇦🇺 Austrália", "🇹🇷 Turquia"],
    "Grupo E": ["🇩🇪 Alemanha", "🇨🇼 Curaçao", "🇨🇮 Costa do Marfim", "🇪🇨 Equador"],
    "Grupo F": ["🇳🇱 Holanda", "🇯🇵 Japão", "🇸🇪 Suécia", "🇹🇳 Tunísia"],
    "Grupo G": ["🇧🇪 Bélgica", "🇪🇬 Egito", "🇮🇷 Irã", "🇳🇿 Nova Zelândia"],
    "Grupo H": ["🇪🇸 Espanha", "🇨🇻 Cabo Verde", "🇸🇦 Arábia Saudita", "🇺🇾 Uruguai"],
    "Grupo I": ["🇫🇷 França", "🇸🇳 Senegal", "🇮🇶 Iraque", "🇳🇴 Noruega"],
    "Grupo J": ["🇦🇷 Argentina", "🇩🇿 Argélia", "🇦🇹 Áustria", "🇯🇴 Jordânia"],
    "Grupo K": ["🇵🇹 Portugal", "🇨🇩 RD Congo", "🇺🇿 Uzbequistão", "🇨🇴 Colômbia"],
    "Grupo L": ["🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra", "🇭🇷 Croácia", "🇬🇭 Gana", "🇵🇦 Panamá"]
}

# --- LÓGICA DE DADOS ---
class BolaoCopa2026:
    def __init__(self):
        self.participantes = {}

    def salvar_palpite(self, nome, diretos, terceiros):
        self.participantes[nome] = {
            'diretos': diretos,
            'terceiros': terceiros,
            'pontuacao': 0
        }

# --- CONFIGURAÇÃO DA PÁGINA STREAMLIT ---
st.set_page_config(page_title="Bolão Copa 2026", page_icon="🏆", layout="wide")

if 'bolao' not in st.session_state:
    st.session_state.bolao = BolaoCopa2026()

st.title("🏆 Bolão da Copa do Mundo 2026")
st.write("Insira seu nome e faça seus palpites para a fase de grupos!")

st.divider()

# --- ÁREA DE PALPITES ---
nome_participante = st.text_input("👤 **Digite seu nome para registrar o palpite:**", placeholder="Ex: João da Silva")

if nome_participante:
    st.header("1️⃣ Classificados Diretos (1º e 2º de cada grupo)")
    st.write("Selecione exatamente **2 seleções** em cada grupo abaixo.")
    
    palpites_diretos = []
    times_restantes = [] # Vai guardar quem não foi escolhido para a repescagem dos 3ºs
    
    # Cria 3 colunas para o layout não ficar gigante para baixo
    col1, col2, col3 = st.columns(3)
    colunas = [col1, col2, col3]
    
    i = 0
    for nome_grupo, times in GRUPOS.items():
        with colunas[i % 3]:
            # Multiselect limitando a 2 escolhas
            escolhidos = st.multiselect(
                f"**{nome_grupo}**", 
                times, 
                max_selections=2,
                key=f"diretos_{nome_grupo}"
            )
            palpites_diretos.extend(escolhidos)
            
            # Adiciona os times não escolhidos na lista de restantes
            for time in times:
                if time not in escolhidos:
                    times_restantes.append(time)
        i += 1

    st.divider()
    
    # --- ÁREA DOS TERCEIROS COLOCADOS ---
    st.header("2️⃣ Melhores Terceiros Colocados")
    st.write("Das seleções que sobraram, selecione as **8** que avançarão como os melhores terceiros.")
    
    palpites_terceiros = st.multiselect(
        "Selecione as 8 seleções:", 
        times_restantes,
        max_selections=8
    )

    st.divider()

    # --- BOTÃO DE SALVAR ---
    # Só libera o botão se o cara escolheu tudo certinho (24 diretos e 8 terceiros)
    if len(palpites_diretos) == 24 and len(palpites_terceiros) == 8:
        if st.button("💾 Salvar Meus Palpites", type="primary", use_container_width=True):
            st.session_state.bolao.salvar_palpite(nome_participante, palpites_diretos, palpites_terceiros)
            st.success(f"🎉 Sensacional! Os palpites de **{nome_participante}** foram salvos com sucesso!")
            st.balloons()
    else:
        st.warning(f"⚠️ Para salvar, você precisa selecionar **24** classificados diretos (você selecionou {len(palpites_diretos)}) e **8** terceiros colocados (você selecionou {len(palpites_terceiros)}).")

# --- ÁREA PARA VER QUEM JÁ PALPITOU ---
st.divider()
with st.expander("👀 Ver quem já registrou palpites"):
    if st.session_state.bolao.participantes:
        for nome, dados in st.session_state.bolao.participantes.items():
            st.write(f"✅ {nome}")
    else:
        st.write("Ninguém palpitou ainda.")
