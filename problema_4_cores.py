# dicionários com os municípios do estado de Roraima e seus municípios fronteiriços
Roraima = {
    'Uiramuta': ['Pacaraima', 'Normandia'],
    'Pacaraima': ['Uiramuta', 'Normandia', 'Boa Vista', 'Amajari'],
    'Normandia': ['Uiramuta', 'Bonfim', 'Boa Vista', 'Pacaraima'],
    'Boa Vista': ['Pacaraima', 'Normandia', 'Bonfim', 'Canta', 
                  'Mucajai', 'Alto Alegre', 'Amajari'],
    'Bonfim': ['Caracarai', 'Canta', 'Boa Vista', 'Normandia'],
    'Canta': ['Bonfim', 'Caracarai', 'Iracema', 'Mucajai', 'Boa Vista'],
    'Amajari': ['Pacaraima', 'Boa Vista', 'Alto Alegre'],
    'Alto Alegre': ['Amajari', 'Boa Vista', 'Mucajai', 'Iracema'],
    'Mucajai': ['Alto Alegre', 'Boa Vista', 'Canta', 'Iracema'],
    'Iracema': ['Alto Alegre', 'Mucajai', 'Canta', 'Caracarai'],
    'Caracarai': ['Iracema', 'Canta', 'Bonfim', 'Caroebe', 'Sao Joao da Baliza', 
                  'Sao Luiz do Anaua', 'Rorainopolis'],
    'Caroebe': ['Sao Joao da Baliza', 'Caracarai'],
    'Sao Joao da Baliza': ['Rorainopolis', 'Sao Luiz do Anaua', 'Caracarai', 'Caroebe'],
    'Rorainopolis': ['Caracarai', 'Sao Luiz do Anaua', 'Sao Joao da Baliza'],
    'Sao Luiz do Anaua': ['Caracarai', 'Sao Joao da Baliza', 'Rorainopolis'],
}

class Problema:
    def __init__(self, bordas, cores):
        # bordas é um dicionário onde cada chave é uma região
        # e seu valor é uma lista de suas regiões fronteiriças
        self.bordas = bordas

        # mapa é um dicionário com todas as regiões e suas cores
        # começa em branco
        # representa o estado inicial do sistema
        self.mapa = {}
        for regiao in bordas:
            self.mapa[regiao] = None

        # cores é uma lista com as 4 cores a serem usadas na coloração
        self.cores = cores

class No:
    def __init__(self, mapa, regiao, cor):
        # mapa é uma lista de dicionarios
        # cada chave é uma região, seu valor é sua cor atual
        # representa diferentes estados do sistema
        self.mapa = mapa

        # ao criar um novo nó, passando uma região e uma cor,
        # o nó é criado com a coloração atualizada
        mapa[regiao] = cor

    def __str__(self):
        string = ''
        for regiao in self.mapa:
            string = string + f'\n{regiao}: {self.mapa[regiao]}'
        return string

    def __repr__(self):
        return self.__str__()
    
    def filhos(self, cores, proxima_regiao):
        filhos = []
        for c in cores:
            print(c)
            filhos.append(No(self.mapa, proxima_regiao, c))
        return filhos

'''
A busca funcionará assim:
Começando com todas as regiões em branco, uma a uma, na ordem em que elas aparecem na lista,
será adicionado à fronteira 4 nós, um para cada opção de cores para aquela região.
Depois, para a próxima região, serão novamente acrescentados 4 nós, e assim por diante.
Serão podados os nós que tenham regiões vizinhas com a mesma cor.

Dessa forma, o tipo de busca mais interessante é a em profundidade, pois ela colorirá
todos os nós em menos iterações
'''

class Coloracao:
    def __init__(self, problema):
        self.problema = problema
        self.fronteira = []
        self.status = 'Coloração iniciando'

    def passo():
        pass