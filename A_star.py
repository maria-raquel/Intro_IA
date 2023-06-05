import heapq as hp

def acao(destino, custo):
    return { 'destino': destino, 'custo': custo}

# A primeira adaptação será adicionar uma chave nos dicionários 
# que guarde a distância da cidade a Bucareste em linha reta
estados_romenia = [
    { 'estado': 'Arad',
      'acoes': [acao('Zerind', 75), acao('Sibiu', 140), acao('Timisoara', 118)], 
      'distancia': 366 },

    { 'estado': 'Zerind',
      'acoes': [acao('Arad', 75), acao('Oradea', 71)],
       'distancia': 374 },

    { 'estado': 'Timisoara',
      'acoes': [acao('Arad', 118), acao('Lugoj', 111)], 
      'distancia': 329 },

    { 'estado': 'Sibiu',
      'acoes': [acao('Arad', 140), acao('Oradea', 151), acao('Fagaras', 99),
                acao('Rimnicu Vilcea', 80)], 
      'distancia': 253 },

    { 'estado': 'Oradea',
      'acoes': [acao('Zerind', 71), acao('Sibiu', 151)], 
      'distancia': 380 },

    { 'estado': 'Lugoj',
      'acoes': [acao('Timisoara', 111), acao('Mehadia', 70)], 
      'distancia': 244 },

    { 'estado': 'Mehadia',
      'acoes': [acao('Lugoj', 70), acao('Drobeta', 75)], 
      'distancia': 241 },

    { 'estado': 'Drobeta',
      'acoes': [acao('Mehadia', 75), acao('Craiova', 120)], 
      'distancia': 242 },

    { 'estado': 'Craiova',
      'acoes': [acao('Drobeta', 120), acao('Rimnicu Vilcea', 146),
                acao('Pitesti', 138)], 
      'distancia': 160 },

    { 'estado': 'Rimnicu Vilcea',
      'acoes': [acao('Sibiu', 80), acao('Craiova', 146), acao('Pitesti', 97)], 
      'distancia': 193 },

    { 'estado': 'Fagaras',
      'acoes': [acao('Sibiu', 99), acao('Bucharest', 211)], 
      'distancia': 176 },

    { 'estado': 'Pitesti',
      'acoes': [acao('Rimnicu Vilcea', 97), acao('Craiova', 138), acao('Bucharest', 101)],
       'distancia': 100 },

    { 'estado': 'Giurgiu',
      'acoes': [acao('Bucharest', 90)],
      'distancia': 77 },

    { 'estado': 'Bucharest',
      'acoes': [acao('Fagaras', 211), acao('Pitesti', 101), acao('Giurgiu', 90),
                acao('Urziceni', 85)], 
      'distancia': 0 },

    { 'estado': 'Urziceni',
      'acoes': [acao('Bucharest', 85), acao('Vaslui', 142), acao('Hirsova', 98)], 
      'distancia': 80 },

    { 'estado': 'Hirsova',
      'acoes': [acao('Urziceni', 98), acao('Eforie', 86)], 
      'distancia': 151 },

    { 'estado': 'Eforie',
      'acoes': [acao('Hirsova', 86)], 
      'distancia': 161 },

    { 'estado': 'Vaslui',
      'acoes': [acao('Urziceni', 142), acao('Iasi', 92)], 
      'distancia': 199 },

    { 'estado': 'Iasi',
      'acoes': [acao('Vaslui', 92), acao('Neamt', 87)], 
      'distancia': 226 },

    { 'estado': 'Neamt',
      'acoes': [acao('Iasi', 87)], 
      'distancia': 234 }
]

class No:
    def __init__(self, estado, custo, pai, acao):
        self.estado = estado
        self.custo = custo
        self.pai = pai
        self.acao = acao

        # Adicionamos um campo no nó que guardará seu valor para a função de avaliação
        # A função é a soma da disttância e o custo do nó
        distancia = next(e for e in estados_romenia if e['estado'] == estado)['distancia']
        self.funcao_avaliacao = custo + distancia

    def __str__(self):
        return f'({self.estado}, c = {self.custo})'

    def __repr__(self):
        return self.__str__()
    
    # Precisamos definir o operador de comparação para a fila de prioridade
    def __lt__(self, other):
        return self.funcao_avaliacao < other.funcao_avaliacao

    def filhos(self, problema):
        espaco_acoes = next(e for e in problema.espaco_estados if e['estado'] == self.estado)

        resultado = []
        for acao in espaco_acoes['acoes']:
            filho = No(acao['destino'], acao['custo'],
                       self, acao['destino'])
            resultado.append(filho)

        return resultado

    def constroi_solucao(self):
        no_atual = self
        solucao = [no_atual]
        while no_atual.pai != None:
            no_atual = no_atual.pai
            solucao.insert(0, no_atual)

        return solucao

class Problema:
    def __init__(self, espaco_estados, inicial, objetivo):
        self.espaco_estados = espaco_estados
        self.inicial = inicial
        self.objetivo = objetivo

BUSCA_INICIANDO = 0
BUSCA_FALHOU = 1
BUSCA_SUCESSO = 2
BUSCA_EM_CURSO = 3

class A_Star:
    def __init__(self, problema):
        self.problema = problema
        self.visitados = [problema.inicial.estado]

        # A fronteira passa a ser uma fila com prioridade
        self.fronteira = []
        hp.heappush(self.fronteira, problema.inicial)

        self.solucao = []
        self.situacao = BUSCA_INICIANDO

    def executar(self):
        while self.situacao != BUSCA_FALHOU and self.situacao != BUSCA_SUCESSO:
            self.passo_busca()

        if self.situacao == BUSCA_FALHOU:
            print("Busca falhou")
        elif self.situacao == BUSCA_SUCESSO:
            print("Busca teve sucesso")
            print(f"Solucao: {self.solucao}")

        return

    def passo_busca(self):
        if (self.situacao == BUSCA_FALHOU):
            print("Busca falhou")
            return

        if (self.situacao == BUSCA_SUCESSO):
            print("Busca chegou ao objetivo com sucesso")
            return

        try:
            # Removemos o elemento da fila que tem a menor função de avaliação
            no = hp.heappop(self.fronteira)
        except IndexError:
            self.situacao = BUSCA_FALHOU
            return

        if self.problema.objetivo(no):
            self.situacao = BUSCA_SUCESSO
            self.solucao = no.constroi_solucao()
            return

        for filho in no.filhos(self.problema):
            if not (filho in self.fronteira) and not (filho.estado in self.visitados):
                # Adicionamos os filhos na lista com prioridade
                hp.heappush(self.fronteira, filho)
                self.visitados.append(filho.estado)

        return