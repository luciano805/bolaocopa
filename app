class BolaoCopa2026:
    def __init__(self):
        # Armazena os palpites dos colaboradores
        self.participantes = {}
        # Armazena os resultados reais da Copa
        self.gabarito_grupos = {'diretos': [], 'terceiros': []}
        self.gabarito_mata_mata = {
            'oitavas': [], 'quartas': [], 'semis': [], 'final': [], 'campeao': ''
        }

    def cadastrar_participante(self, nome):
        """Cria um perfil vazio para o colaborador."""
        if nome not in self.participantes:
            self.participantes[nome] = {
                'grupos_diretos': [], # Os 24 times que passam em 1º e 2º
                'grupos_terceiros': [], # Os 8 melhores 3ºs
                'mata_mata': {
                    'oitavas': [], 'quartas': [], 'semis': [], 'final': [], 'campeao': ''
                },
                'pontuacao': 0
            }
            print(f"Colaborador '{nome}' cadastrado com sucesso!")
        else:
            print(f"O colaborador '{nome}' já existe.")

    def registrar_palpite_grupos(self, nome, diretos, terceiros):
        """Registra os 24 classificados diretos e os 8 melhores terceiros."""
        if nome in self.participantes:
            if len(diretos) == 24 and len(terceiros) == 8:
                self.participantes[nome]['grupos_diretos'] = diretos
                self.participantes[nome]['grupos_terceiros'] = terceiros
                print(f"Palpites da fase de grupos registrados para {nome}.")
            else:
                print("Erro: Você deve informar exatamente 24 classificados diretos e 8 terceiros.")

    def registrar_palpite_mata_mata(self, nome, fase, times):
        """Registra os times que o colaborador acha que vão avançar em cada fase."""
        if nome in self.participantes and fase in self.participantes[nome]['mata_mata']:
            self.participantes[nome]['mata_mata'][fase] = times
            print(f"Palpite da fase '{fase}' registrado para {nome}.")

    def definir_gabarito_grupos(self, diretos, terceiros):
        """Define os resultados reais da fase de grupos."""
        self.gabarito_grupos['diretos'] = diretos
        self.gabarito_grupos['terceiros'] = terceiros
        print("Gabarito da fase de grupos atualizado!")

    def calcular_ranking(self):
        """Calcula os pontos de todos e exibe o ranking."""
        print("\n--- CALCULANDO PONTUAÇÕES ---")
        
        # Sistema de Pontuação (pode ser ajustado)
        PTS_DIRETO = 3     # Acertou quem passou em 1º ou 2º
        PTS_TERCEIRO = 2   # Acertou quem passou em 3º
        # Pontos do mata-mata poderiam ser adicionados aqui
        
        for nome, dados in self.participantes.items():
            pontos = 0
            
            # Checar acertos dos classificados diretos
            acertos_diretos = set(dados['grupos_diretos']).intersection(self.gabarito_grupos['diretos'])
            pontos += len(acertos_diretos) * PTS_DIRETO
            
            # Checar acertos dos terceiros colocados
            acertos_terceiros = set(dados['grupos_terceiros']).intersection(self.gabarito_grupos['terceiros'])
            pontos += len(acertos_terceiros) * PTS_TERCEIRO
            
            self.participantes[nome]['pontuacao'] = pontos

        # Gerar ranking ordenado
        ranking = sorted(self.participantes.items(), key=lambda x: x[1]['pontuacao'], reverse=True)
        
        print("\n🏆 RANKING DO BOLÃO DA EMPRESA 🏆")
        for posicao, (nome, dados) in enumerate(ranking, start=1):
            print(f"{posicao}º Lugar: {nome} - {dados['pontuacao']} pontos")

# ==========================================
# EXEMPLO DE USO DO SOFTWARE NA PRÁTICA
# ==========================================

# 1. Iniciar o Bolão
meu_bolao = BolaoCopa2026()

# 2. Cadastrar Colaboradores
meu_bolao.cadastrar_participante("João Silva")
meu_bolao.cadastrar_participante("Maria Souza")

# 3. Inserir Palpites (Exemplo simplificado com apenas alguns times para demonstração)
# Na prática, a lista 'diretos' deve ter 24 times e 'terceiros' deve ter 8 times.
palpite_joao_diretos = ["Brasil", "França", "Argentina", "Espanha", "Inglaterra", "Portugal"] + ["TimeX"] * 18
palpite_joao_terceiros = ["Croácia", "Uruguai", "Japão", "Senegal", "EUA", "México", "Marrocos", "Coreia"]

meu_bolao.registrar_palpite_grupos("João Silva", palpite_joao_diretos, palpite_joao_terceiros)

# 4. Inserir o Gabarito Real (Após os jogos da Copa)
gabarito_real_diretos = ["Brasil", "Alemanha", "Argentina", "Espanha", "Itália", "Portugal"] + ["TimeX"] * 18
gabarito_real_terceiros = ["Croácia", "Uruguai", "Japão", "Senegal", "EUA", "Camarões", "Holanda", "Gana"]

meu_bolao.definir_gabarito_grupos(gabarito_real_diretos, gabarito_real_terceiros)

# 5. Ver o Resultado
meu_bolao.calcular_ranking()
