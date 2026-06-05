import streamlit as st

# --- DADOS DA COPA DO MUNDO 2026 ---
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
            'diretos': diretos, # Agora guarda exatamente quem foi 1º e 2º
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
    st.header("1️⃣ Classificados Diretos")
    st.write("Selecione o **1º e 2º colocado** de cada grupo.")
    
    palpites_diretos = {} # Vamos guardar organizadinho por grupo
    times_restantes = []  # Para a repescagem
    grupos_incompletos = False # Trava de segurança
    
    col1, col2, col3 = st.columns(3)
    colunas = [col1, col2, col3]
    
    i = 0
    for nome_grupo, times in GRUPOS.items():
        with colunas[i % 3]:
            # Criamos um container visual para cada grupo ficar bem separadinho
            with st.container(border=True):
                st.markdown(f"#### {nome_grupo}")
                opcoes = ["Selecione..."] + times
                
                # Caixas individuais para 1º e 2º lugar
                primeiro = st.selectbox("🥇 1º Lugar", opcoes, key=f"1_{nome_grupo}")
                segundo = st.selectbox("🥈 2º Lugar", opcoes, key=f"2_{nome_grupo}")
                
                # Validações do grupo
                if primeiro != "Selecione..." and segundo != "Selecione...":
                    if primeiro == segundo:
                        st.error("⚠️ Escolha times diferentes!")
                        grupos_incompletos = True
                    else:
                        palpites_diretos[nome_grupo] = {'1º': primeiro, '2º': segundo}
                        # Guarda os que não passaram para a lista de terceiros
                        for t in times:
                            if t not in [primeiro, segundo]:
                                times_restantes.append(t)
                else:
                    grupos_incompletos = True
        i += 1

    st.divider()
    
    # --- ÁREA DOS TERCEIROS COLOCADOS (Só aparece se finalizar os diretos) ---
    if not grupos_incompletos:
        st.header("2️⃣ Melhores Terceiros Colocados")
        st.write("Das seleções que sobraram, selecione as **8** que avançarão para o mata-mata.")
        
        palpites_terceiros = st.multiselect(
            "Selecione exatamente 8 seleções:", 
            times_restantes,
            max_selections=8
        )

        st.divider()

        # --- BOTÃO DE SALVAR ---
        if len(palpites_diretos) == 12 and len(palpites_terceiros) == 8:
            if st.button("💾 Salvar Meus Palpites", type="primary", use_container_width=True):
                st.session_state.bolao.salvar_palpite(nome_participante, palpites_diretos, palpites_terceiros)
                st.success(f"🎉 Sensacional! Os palpites de **{nome_participante}** foram salvos com sucesso!")
                st.balloons()
        else:
            st.warning(f"⚠️ Você precisa selecionar **8** terceiros colocados para salvar (você selecionou {len(palpites_terceiros)}).")
    else:
        st.info("⚠️ Preencha corretamente o 1º e 2º lugar de **todos os 12 grupos** acima para liberar a escolha dos terceiros colocados.")

# --- ÁREA PARA VER QUEM JÁ PALPITOU ---
st.divider()
with st.expander("👀 Ver quem já registrou palpites"):
    if st.session_state.bolao.participantes:
        for nome, dados in st.session_state.bolao.participantes.items():
            st.write(f"✅ {nome}")
    else:
        st.write("Ninguém palpitou ainda.")
