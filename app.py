import streamlit as st
import pandas as pd

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

TODAS_SELECOES = [time for times in GRUPOS.values() for time in times]

# --- LÓGICA DE DADOS E PONTUAÇÃO ---
class BolaoCopa2026:
    def __init__(self):
        self.participantes = {}
        # Gabarito oficial que o Administrador vai preencher
        self.gabarito = {
            '1_lugar': [], '2_lugar': [], '3_lugar': [],
            'avos16': [], 'oitavas': [], 'quartas': [], 'semis': [], 'campeao': []
        }

    def salvar_palpite(self, nome, palpites):
        self.participantes[nome] = palpites
        self.calcular_todas_pontuacoes() # Recalcula sempre que alguém salva

    def atualizar_gabarito(self, nova_fase, times):
        self.gabarito[nova_fase] = times
        self.calcular_todas_pontuacoes() # Recalcula quando sai resultado real

    def calcular_todas_pontuacoes(self):
        # Todos os times que passaram de fase nos grupos (independente da posição)
        classificados_grupos_gabarito = self.gabarito['1_lugar'] + self.gabarito['2_lugar'] + self.gabarito['3_lugar']

        for nome, dados in self.participantes.items():
            pontos = 0
            
            # --- PONTUAÇÃO DOS GRUPOS ---
            # 1º LUGAR
            for time in dados.get('1_lugar', []):
                if time in self.gabarito['1_lugar']: pontos += 2
                elif time in classificados_grupos_gabarito: pontos += 1
            
            # 2º LUGAR
            for time in dados.get('2_lugar', []):
                if time in self.gabarito['2_lugar']: pontos += 2
                elif time in classificados_grupos_gabarito: pontos += 1
                
            # 3º LUGAR
            for time in dados.get('3_lugar', []):
                if time in self.gabarito['3_lugar']: pontos += 2
                elif time in classificados_grupos_gabarito: pontos += 1

            # --- PONTUAÇÃO DO MATA-MATA (3 Pontos cada) ---
            fases_mata_mata = ['avos16', 'oitavas', 'quartas', 'semis']
            for fase in fases_mata_mata:
                for time in dados.get(fase, []):
                    if time in self.gabarito[fase]:
                        pontos += 3

            # --- PONTUAÇÃO CAMPEÃO (10 Pontos) ---
            if dados.get('campeao') and dados['campeao'] in self.gabarito['campeao']:
                pontos += 10
                
            self.participantes[nome]['pontuacao'] = pontos

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Bolão Copa 2026", page_icon="🏆", layout="wide")

if 'bolao' not in st.session_state:
    st.session_state.bolao = BolaoCopa2026()

st.title("🏆 Bolão da Copa - HarmonizaPRO")

# --- CRIANDO AS ABAS ---
aba_palpites, aba_ranking, aba_admin = st.tabs(["📝 Fazer Palpites", "📊 Ranking e Pontuações", "⚙️ Área do Administrador"])

# ==========================================
# ABA 1: FAZER PALPITES
# ==========================================
with aba_palpites:
    st.write("Preencha todas as fases! Se quiser alterar depois, basta digitar seu nome exatamente igual e salvar novamente por cima.")
    nome_participante = st.text_input("👤 **Digite seu nome:**", placeholder="Ex: João da Silva")

    if nome_participante:
        meus_palpites = {
            '1_lugar': [], '2_lugar': [], '3_lugar': [],
            'avos16': [], 'oitavas': [], 'quartas': [], 'semis': [], 'campeao': []
        }
        times_restantes = []
        grupos_incompletos = False
        
        st.header("1️⃣ Fase de Grupos")
        col1, col2, col3 = st.columns(3)
        colunas = [col1, col2, col3]
        
        i = 0
        for nome_grupo, times in GRUPOS.items():
            with colunas[i % 3]:
                with st.container(border=True):
                    st.markdown(f"**{nome_grupo}**")
                    opcoes = ["Selecione..."] + times
                    
                    primeiro = st.selectbox("🥇 1º", opcoes, key=f"p1_{nome_grupo}")
                    segundo = st.selectbox("🥈 2º", opcoes, key=f"p2_{nome_grupo}")
                    
                    if primeiro != "Selecione..." and segundo != "Selecione...":
                        if primeiro == segundo:
                            st.error("⚠️ Times diferentes!")
                            grupos_incompletos = True
                        else:
                            meus_palpites['1_lugar'].append(primeiro)
                            meus_palpites['2_lugar'].append(segundo)
                            for t in times:
                                if t not in [primeiro, segundo]:
                                    times_restantes.append(t)
                    else:
                        grupos_incompletos = True
            i += 1

        if not grupos_incompletos:
            st.markdown("### Melhores Terceiros Colocados")
            meus_palpites['3_lugar'] = st.multiselect("Selecione 8 seleções que sobram:", times_restantes, max_selections=8)

            if len(meus_palpites['3_lugar']) == 8:
                st.divider()
                st.header("2️⃣ Mata-Mata")
                st.write("Agora, baseando-se nas seleções que você acha que vão passar, defina o resto do campeonato!")
                
                # Lista das 32 seleções que o usuário disse que iam passar para facilitar a escolha dele
                times_classificados_usuario = meus_palpites['1_lugar'] + meus_palpites['2_lugar'] + meus_palpites['3_lugar']
                
                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    meus_palpites['avos16'] = st.multiselect("⚽ Quem passa pros **16-Avos**? (Escolha 16)", times_classificados_usuario, max_selections=16)
                    meus_palpites['quartas'] = st.multiselect("⚽ Quem passa para as **Quartas**? (Escolha 4)", meus_palpites['avos16'] if meus_palpites['avos16'] else TODAS_SELECOES, max_selections=4)
                
                with col_m2:
                    meus_palpites['oitavas'] = st.multiselect("⚽ Quem passa pras **Oitavas**? (Escolha 8)", meus_palpites['avos16'] if meus_palpites['avos16'] else TODAS_SELECOES, max_selections=8)
                    meus_palpites['semis'] = st.multiselect("⚽ Quem passa para as **Semis**? (Escolha 2)", meus_palpites['quartas'] if meus_palpites['quartas'] else TODAS_SELECOES, max_selections=2)
                
                st.markdown("### 🏆 Grande Campeão")
                opcoes_campeao = ["Selecione..."] + (meus_palpites['semis'] if meus_palpites['semis'] else TODAS_SELECOES)
                escolha_campeao = st.selectbox("Quem levanta a taça?", opcoes_campeao)
                if escolha_campeao != "Selecione...":
                    meus_palpites['campeao'] = [escolha_campeao]

                st.divider()
                if st.button("💾 Salvar Todos os Meus Palpites", type="primary", use_container_width=True):
                    st.session_state.bolao.salvar_palpite(nome_participante, meus_palpites)
                    st.success(f"🎉 Excelente! Palpites de **{nome_participante}** registrados com sucesso.")
                    st.balloons()
            else:
                st.warning("⚠️ Selecione exatamente 8 terceiros colocados para liberar o Mata-Mata.")
        else:
            st.info("⚠️ Preencha todos os 1º e 2º lugares dos grupos.")

# ==========================================
# ABA 2: RANKING E PONTUAÇÕES
# ==========================================
with aba_ranking:
    st.header("🏆 Classificação Geral")
    
    # Regras visíveis para a galera
    with st.expander("📖 Regras de Pontuação"):
        st.write("""
        * **Fase de Grupos:** Acertou que o time passou, mas errou a posição = **1 Ponto**. Acertou a posição exata (1º, 2º ou 3º) = **2 Pontos**.
        * **Mata-Mata:** Acertar quem avança em cada fase (16-avos, oitavas, quartas e semis) = **3 Pontos**.
        * **Campeão:** Acertar o vencedor da Copa = **10 Pontos**.
        """)

    if st.session_state.bolao.participantes:
        dados_tabela = []
        for nome, dados in st.session_state.bolao.participantes.items():
            dados_tabela.append({"Participante": nome, "Pontos": dados.get('pontuacao', 0)})
        
        df_ranking = pd.DataFrame(dados_tabela).sort_values(by="Pontos", ascending=False)
        df_ranking.index = range(1, len(df_ranking) + 1)
        st.dataframe(df_ranking, use_container_width=True)
    else:
        st.warning("Nenhum palpite registrado ainda.")

# ==========================================
# ABA 3: ÁREA DO ADMINISTRADOR (Você controla os resultados aqui)
# ==========================================
# ==========================================
# ABA 3: ÁREA DO ADMINISTRADOR (Protegida por Senha)
# ==========================================
with aba_admin:
    st.header("⚙️ Painel de Resultados Oficiais")
    st.write("Área restrita. Digite a senha para lançar os resultados.")
    
    # Campo de senha (o type="password" esconde o que está sendo digitado)
    senha_digitada = st.text_input("🔑 Senha do Administrador:", type="password")
    
    # Defina a sua senha aqui
    SENHA_CORRETA = "admin123"
    
    if senha_digitada == SENHA_CORRETA:
        st.success("Acesso liberado!")
        
        st.markdown("### 📋 Resultados da Fase de Grupos")
        gab_1 = st.multiselect("✅ Passaram em **1º Lugar** (Oficial)", TODAS_SELECOES, default=st.session_state.bolao.gabarito['1_lugar'])
        gab_2 = st.multiselect("✅ Passaram em **2º Lugar** (Oficial)", TODAS_SELECOES, default=st.session_state.bolao.gabarito['2_lugar'])
        gab_3 = st.multiselect("✅ Passaram em **3º Lugar** (Oficial)", TODAS_SELECOES, default=st.session_state.bolao.gabarito['3_lugar'])
        
        st.markdown("### ⚔️ Resultados do Mata-Mata")
        gab_16 = st.multiselect("✅ Passaram para os **16-Avos**", TODAS_SELECOES, default=st.session_state.bolao.gabarito['avos16'])
        gab_8 = st.multiselect("✅ Passaram para as **Oitavas**", TODAS_SELECOES, default=st.session_state.bolao.gabarito['oitavas'])
        gab_4 = st.multiselect("✅ Passaram para as **Quartas**", TODAS_SELECOES, default=st.session_state.bolao.gabarito['quartas'])
        gab_2_semi = st.multiselect("✅ Passaram para as **Semis**", TODAS_SELECOES, default=st.session_state.bolao.gabarito['semis'])
        gab_camp = st.multiselect("🏆 **Campeão da Copa**", TODAS_SELECOES, default=st.session_state.bolao.gabarito['campeao'])

        if st.button("🔄 Atualizar Gabarito e Recalcular Ranking", type="primary"):
            st.session_state.bolao.atualizar_gabarito('1_lugar', gab_1)
            st.session_state.bolao.atualizar_gabarito('2_lugar', gab_2)
            st.session_state.bolao.atualizar_gabarito('3_lugar', gab_3)
            st.session_state.bolao.atualizar_gabarito('avos16', gab_16)
            st.session_state.bolao.atualizar_gabarito('oitavas', gab_8)
            st.session_state.bolao.atualizar_gabarito('quartas', gab_4)
            st.session_state.bolao.atualizar_gabarito('semis', gab_2_semi)
            st.session_state.bolao.atualizar_gabarito('campeao', gab_camp)
            st.success("Gabarito atualizado com sucesso! Olhe a aba de Ranking para ver as mudanças.")
    
    elif senha_digitada != "":
        st.error("Senha incorreta!")
