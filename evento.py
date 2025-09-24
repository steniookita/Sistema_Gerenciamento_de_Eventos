class Evento():
    def __init__(self, nome, data, local, capacidade_maxima, categoria, preco):
        self.__nome = nome
        self.__data = data
        self.__local = local
        self.__capacidade_maxima = capacidade_maxima
        self.__categoria = categoria
        self.__preco = preco
        self.__inscritos = []