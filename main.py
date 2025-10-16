from src.evento import Evento, Participante, Palestra, Workshop
from src.sistema import Sistema_Evento

def exibir_menu():
    """ Exibe as opções principais do sistema. """
    print('\n--- MENU PRINCIPAL ---')
    print('1. Gerenciar Eventos (Cadastrar, Lsitar)')
    print('2. Gerenciar Participantes (inscrever, Cancelar, Check-in)')
    print('3. Relatorios e Análises')
    print('4. Sair')
    return input('Escolha uma opção: ')

def Menu_evento(Sistema):
    """ Sub-menu para gerenciar eventos """
    while True:
        print('\n--- MENU EVENTOS ---')
        print('1. Cadastrar Novo Evento')
        print('2. Listar todos os Eventos')
        print('3. Buscar Eventos por Data')
        print('4. Voltar ao Menu Principal')
        escolha = input('Escolha uma opção: ')

        if escolha == '1':
            cadastrar_evento(Sistema)
        elif escolha == '2':
            print(sistema.listar_eventos())

ev1 = Evento('TEC-RECIFE', '15/12/2025', 'Olinda', 10, 'Livre', 100)
ev2 = Palestra('Palestra Direitos','30/12/2025', 'Recife', 30, 'Estudantes', 75, 'Dr. Antonio de Goes')
p1 = Participante('Ana', 'anateste@gmail.com')
p2 = Participante('Matheus', 'matheusteste@gmail.com')

sis = Sistema_Evento()

#sis.cadastrar_evento(ev1)
#sis.cadastrar_evento(ev2)
#sis.cadastrar_participante(p2)
#sis.listar_eventos()
#sis.inscrever_participante('matheusteste@gmail.com','TEC-RECIFE')
#sis.inscrever_participante('anateste@gmail.com','TEC-RECIFE')
#sis.buscar_por_categoria('Estudantes')
#sis.buscar_por_data('15/12/2025')
sis.listar_participantes_por_evento('TEC-RECIFE')
#sis.realizar_chekin('anateste@gmail.com')