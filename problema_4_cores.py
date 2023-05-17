from copy import deepcopy

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

        # cores é uma lista com as 4 cores a serem usadas na coloração
        self.cores = cores

class No:
    def __init__(self, mapa, regiao, cor):
        # mapa é um dicionario
        # cada chave é uma região, seu valor é sua cor atual
        # representa diferentes estados do sistema
        self.mapa = deepcopy(mapa)

        # ao criar um novo nó, passando uma região e uma cor,
        # o nó é criado com a coloração atualizada
        self.mapa[regiao] = cor

    def __str__(self):
        string = ''
        for regiao in self.mapa:
            if self.mapa[regiao] != '':
                string = string + f'{regiao}: {self.mapa[regiao]}\n'
        return string

    def __repr__(self):
        return self.__str__()
    
    def filhos(self, cores, proxima_regiao):
        filhos = []
        for cor in cores:
            filho = No(self.mapa, proxima_regiao, cor)
            filhos.append(filho)
        return filhos

class Coloracao:
    def __init__(self, problema):
        self.problema = problema
        self.fronteira = []
        self.status = 'Coloração iniciando'
        # status possíveis: 'Coloração iniciando', 'Coloração em andamento', 'Coloração finalizada'

        self.indice = 0
        # o indice guardará a posição da próxima região a ser colorida na busca

        # mapa é um dicionário com todas as regiões e suas cores
        # começa em branco
        # representa o estado inicial do sistema
        self.mapa = {}
        for regiao in self.problema.bordas:
            self.mapa[regiao] = ''

    def passo(self):
        if self.status == 'Coloração finalizada':
            print('Coloração finalizada')
            return
        
        try:
            no = self.fronteira.pop(-1)
        except IndexError:
            self.situacao = 'Coloração finalizada'
            return

        for filho in no.filhos(self.problema.cores, self.problema.bordas[self.problema.mapa]):
            self.fronteira.append(filho)
            pass