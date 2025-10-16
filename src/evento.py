from datetime import datetime

class Evento:
    def __init__(self, nome, data, local, categoria, capacidade_max, preco):
        self.__nome = nome
        self.__data = data
        self.__local = local
        self.__categoria = categoria
        self.__capacidade_max = capacidade_max
        self.__preco = preco
        
        # Validações
        if capacidade_max <= 0:
            raise ValueError("Capacidade máxima deve ser um número positivo")
        if preco < 0:
            raise ValueError("Preço não pode ser negativo")
        
        # Validação de data (opcional - verifica se a data não é passada)
        try:
            data_obj = datetime.strptime(data, '%Y-%m-%d %H:%M:%S')
            if data_obj < datetime.now():
                print("Aviso: A data do evento é anterior à data atual.")
        except ValueError:
            pass  # Se a data não estiver no formato esperado, ignora a validação

    def get_nome(self):
        return self.__nome
    def get_data(self):
        return self.__data
    def get_local(self):
        return self.__local
    def get_capacidade_max(self):
        return self.__capacidade_max
    def get_categoria(self):
        return self.__categoria
    def get_preco(self):
        return self.__preco
    def detalhes(self):
        return f"Evento: {self.__nome}, Data: {self.__data.strftime('%d-%m-%Y')}, Local: {self.__local}"
    def vagas_disponiveis(self):
        return self.__capacidade_max - len(self.__participantes)
    
    def inscrever_participante(self, participante):
        if self.vagas_disponiveis() <= 0:
            raise Exception("Evento está lotado")
        for p in self.__participantes:
            if p.get_email() == participante.get_email():
                raise Exception("E-mail já cadastrado neste evento")
        self.__participantes.append(participante)
    
    def cancelar_inscricao(self, email):
        for p in self.__participantes:
            if p.get_email() == email:
                self.__participantes.remove(p)
                return
        raise Exception("Participante não encontrado")
    def total_inscritos(self):
        return len(self.__participantes)
    def receita_total(self):
        return self.__preco * len(self.__participantes)
    def get_participantes(self):
        return self.__participantes
    
    def get_data_formatada(self):
        """
        Retorna a data formatada no padrão brasileiro (DD/MM/YYYY).
        """
        try:
            data_obj = datetime.strptime(self.__data, '%Y-%m-%d %H:%M:%S')
            return data_obj.strftime('%d/%m/%Y')
        except ValueError:
            return self.__data

class Workshop(Evento):
    def __init__(self, nome, data, local, capacidade_max, categoria, preco, material_necessario):
        super().__init__(nome, data, local, capacidade_max, categoria, preco)
        self.__material_necessario = material_necessario
    def detalhes(self):
        return super().detalhes() + f", Material necessário: {self.__material_necessario}"

class Palestra(Evento):
    def __init__(self, nome, data, local, capacidade_max, categoria, preco, palestrante):
        super().__init__(nome, data, local, capacidade_max, categoria, preco)
        self.__palestrante = palestrante
    def detalhes(self):
        return super().detalhes() + f", Palestrante: {self.__palestrante}"

class Participante:
    def __init__(self, nome, email):
        self.__nome = nome
        self.__email = email
        self.__check_in = False
    def get_nome(self):
        return self.__nome
    def get_email(self):
        return self.__email
    def realizar_check_in(self):
        self.__check_in = True
    def check_in_realizado(self):
        return self.__check_in
