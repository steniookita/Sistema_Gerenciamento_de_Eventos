from src.evento import Workshop, Palestra, Evento

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
        print('2. Lsitar todos os Eventos')
        print('3. Buscar Eventos por Data')
        print('4. Voltar ao Menu Principal')
        escolha = input('Escolha uma opção: ')

        if escolha == '1':
            cadastrar_evento(Sistema)
        elif escolha == '2':
            print(sistema.listar_eventos())