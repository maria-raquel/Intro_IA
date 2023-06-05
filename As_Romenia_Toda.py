import heapq as hp
from geopy.geocoders import Nominatim
from haversine import haversine
from busca_largura import estados_romenia

BUSCA_INICIANDO = 0
BUSCA_FALHOU = 1
BUSCA_SUCESSO = 2
BUSCA_EM_CURSO = 3

# Recebe o nome de uma cidade e retorna suas coordenadas geográficas
def coordenadas(cidade):
    geolocator = Nominatim(user_agent="my-app")
    location = geolocator.geocode(cidade)
    if location is None:
        return None
    else:
        return location.latitude, location.longitude

# Para cada cidade na lista estados_romenia, adicionamos suas coordenadas geográficas
for estado in estados_romenia:
    estado['coordenadas'] = coordenadas(estado['estado'])

def distancia(estado_atual, estado_objetivo):
    estado1 = next(e for e in estados_romenia if e['estado'] == estado_atual)
    estado2 = next(e for e in estados_romenia if e['estado'] == estado_objetivo)
    distancia = haversine(estado1['coordenadas'], estado2['coordenadas'])
    return distancia

def acao(destino, custo):
    return { 'destino': destino, 'custo': custo}

# Para cada cidade, adicionamos suas coordenadas geográficas
for estado in estados_romenia:
    estado['coordenadas'] = coordenadas(estado['estado'])

class No:
    # O nó passa a receber o estado objetivo como parâmetro
    def __init__(self, estado, custo, pai, acao, objetivo):
        self.estado = estado
        self.custo = custo
        self.pai = pai
        self.acao = acao
        self.objetivo = objetivo

        # A função de avaliação agora calcula a distancia
        # em linha reta do estado atual ao objetivo
        # usando as coordenadas geográficas
        self.funcao_avaliacao = custo + distancia(estado, objetivo)

    def __str__(self):
        return f'({self.estado}, f = {self.custo})'

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
                       self, acao['destino'], self.objetivo)
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
    
class A_Star:
    def __init__(self, problema):
        self.problema = problema
        self.visitados = [problema.inicial.estado]
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
                hp.heappush(self.fronteira, filho)
                self.visitados.append(filho.estado)

        return