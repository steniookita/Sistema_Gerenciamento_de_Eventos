from src.sistema import Sistema_Evento
from src.evento import Evento, Participante
from datetime import datetime

def limpar_tela():
    """Função auxiliar para limpar a tela (multiplataforma)"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    """Pausa a execução até o usuário pressionar Enter"""
    input("\nPressione ENTER para continuar...")

def exibir_menu_principal():
    """Exibe o menu principal do sistema"""
    print("\n" + "="*50)
    print("   SISTEMA DE GERENCIAMENTO DE EVENTOS")
    print("="*50)
    print("\n[1] Gerenciar Eventos")
    print("[2] Gerenciar Participantes")
    print("[3] Gerenciar Inscrições")
    print("[4] Relatórios e Consultas")
    print("[0] Sair do Sistema")
    print("-"*50)

def menu_eventos():
    """Exibe o submenu de eventos"""
    print("\n" + "="*50)
    print("   GERENCIAR EVENTOS")
    print("="*50)
    print("\n[1] Cadastrar Novo Evento")
    print("[2] Listar Todos os Eventos")
    print("[3] Buscar Eventos por Categoria")
    print("[4] Buscar Eventos por Data")
    print("[5] Listar Eventos com Vagas Disponíveis")
    print("[0] Voltar ao Menu Principal")
    print("-"*50)

def menu_participantes():
    """Exibe o submenu de participantes"""
    print("\n" + "="*50)
    print("   GERENCIAR PARTICIPANTES")
    print("="*50)
    print("\n[1] Cadastrar Novo Participante")
    print("[2] Realizar Check-in")
    print("[3] Listar Participantes de um Evento")
    print("[0] Voltar ao Menu Principal")
    print("-"*50)

def menu_inscricoes():
    """Exibe o submenu de inscrições"""
    print("\n" + "="*50)
    print("   GERENCIAR INSCRIÇÕES")
    print("="*50)
    print("\n[1] Inscrever Participante em Evento")
    print("[2] Cancelar Inscrição")
    print("[0] Voltar ao Menu Principal")
    print("-"*50)

def menu_relatorios():
    """Exibe o submenu de relatórios"""
    print("\n" + "="*50)
    print("   RELATÓRIOS E CONSULTAS")
    print("="*50)
    print("\n[1] Relatório Geral de Inscrições")
    print("[2] Calcular Receita de um Evento")
    print("[0] Voltar ao Menu Principal")
    print("-"*50)

def cadastrar_evento(sistema):
    """Função para cadastrar um novo evento"""
    print("\n--- CADASTRAR NOVO EVENTO ---")
    
    try:
        nome = input("Nome do evento: ").strip()
        if not nome:
            print("Erro: Nome não pode estar vazio!")
            return
        
        # Data no formato brasileiro
        data_str = input("Data do evento (DD/MM/YYYY): ").strip()
        data_obj = datetime.strptime(data_str, '%d/%m/%Y')
        data_formatada = data_obj.strftime('%Y-%m-%d %H:%M:%S')
        
        local = input("Local do evento: ").strip()
        
        print("\nCategorias disponíveis: Show, Palestra, Workshop, Conferência, Festa, Outro")
        categoria = input("Categoria: ").strip()
        
        capacidade = int(input("Capacidade máxima: "))
        if capacidade <= 0:
            print("Erro: Capacidade deve ser maior que zero!")
            return
        
        preco = float(input("Preço do ingresso (R$): "))
        if preco < 0:
            print("Erro: Preço não pode ser negativo!")
            return
        
        # Criar objeto Evento (assumindo que a classe existe)
        evento = Evento(nome, data_formatada, local, categoria, capacidade, preco)
        sistema.cadastrar_evento(evento)
        
    except ValueError as e:
        print(f"Erro: Entrada inválida! {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

def cadastrar_participante(sistema):
    """Função para cadastrar um novo participante"""
    print("\n--- CADASTRAR NOVO PARTICIPANTE ---")
    
    try:
        nome = input("Nome completo: ").strip()
        if not nome:
            print("Erro: Nome não pode estar vazio!")
            return
        
        email = input("E-mail: ").strip().lower()
        if not email or '@' not in email:
            print("Erro: E-mail inválido!")
            return
        
        # Criar objeto Participante (assumindo que a classe existe)
        participante = Participante(nome, email)
        sistema.cadastrar_participante(participante)
        
    except Exception as e:
        print(f"Erro inesperado: {e}")

def inscrever_participante_menu(sistema):
    """Função para inscrever participante em evento"""
    print("\n--- INSCREVER PARTICIPANTE EM EVENTO ---")
    
    email = input("E-mail do participante: ").strip().lower()
    nome_evento = input("Nome do evento: ").strip()
    
    if email and nome_evento:
        sistema.inscrever_participante(email, nome_evento)
    else:
        print("Erro: E-mail e nome do evento são obrigatórios!")

def cancelar_inscricao_menu(sistema):
    """Função para cancelar inscrição"""
    print("\n--- CANCELAR INSCRIÇÃO ---")
    
    email = input("E-mail do participante: ").strip().lower()
    nome_evento = input("Nome do evento: ").strip()
    
    if email and nome_evento:
        sistema.cancelar_inscricao(email, nome_evento)
    else:
        print("Erro: E-mail e nome do evento são obrigatórios!")

def realizar_checkin_menu(sistema):
    """Função para realizar check-in"""
    print("\n--- REALIZAR CHECK-IN ---")
    
    email = input("E-mail do participante: ").strip().lower()
    
    if email:
        sistema.realizar_chekin(email)
    else:
        print("Erro: E-mail é obrigatório!")

def buscar_categoria_menu(sistema):
    """Função para buscar eventos por categoria"""
    print("\n--- BUSCAR EVENTOS POR CATEGORIA ---")
    print("Categorias: Show, Palestra, Workshop, Conferência, Festa, Outro")
    
    categoria = input("Digite a categoria: ").strip()
    
    if categoria:
        sistema.buscar_por_categoria(categoria)
    else:
        print("Erro: Categoria não pode estar vazia!")

def buscar_data_menu(sistema):
    """Função para buscar eventos por data"""
    print("\n--- BUSCAR EVENTOS POR DATA ---")
    
    data = input("Digite a data (DD/MM/YYYY): ").strip()
    
    try:
        # Validar formato
        datetime.strptime(data, '%d/%m/%Y')
        sistema.buscar_por_data(data)
    except ValueError:
        print("Erro: Formato de data inválido! Use DD/MM/YYYY")

def calcular_receita_menu(sistema):
    """Função para calcular receita de um evento"""
    print("\n--- CALCULAR RECEITA DO EVENTO ---")
    
    nome_evento = input("Nome do evento: ").strip()
    
    if nome_evento:
        sistema.calcular_receita_evento(nome_evento)
    else:
        print("Erro: Nome do evento não pode estar vazio!")

def listar_participantes_menu(sistema):
    """Função para listar participantes de um evento"""
    print("\n--- LISTAR PARTICIPANTES DO EVENTO ---")
    
    nome_evento = input("Nome do evento: ").strip()
    
    if nome_evento:
        sistema.listar_participantes_por_evento(nome_evento)
    else:
        print("Erro: Nome do evento não pode estar vazio!")

def processar_menu_eventos(sistema):
    """Processa as opções do menu de eventos"""
    while True:
        limpar_tela()
        menu_eventos()
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == '1':
            cadastrar_evento(sistema)
            pausar()
        elif opcao == '2':
            print()
            sistema.listar_eventos()
            pausar()
        elif opcao == '3':
            buscar_categoria_menu(sistema)
            pausar()
        elif opcao == '4':
            buscar_data_menu(sistema)
            pausar()
        elif opcao == '5':
            print()
            sistema.listar_eventos_com_vaga()
            pausar()
        elif opcao == '0':
            break
        else:
            print("Opção inválida! Tente novamente.")
            pausar()

def processar_menu_participantes(sistema):
    """Processa as opções do menu de participantes"""
    while True:
        limpar_tela()
        menu_participantes()
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == '1':
            cadastrar_participante(sistema)
            pausar()
        elif opcao == '2':
            realizar_checkin_menu(sistema)
            pausar()
        elif opcao == '3':
            listar_participantes_menu(sistema)
            pausar()
        elif opcao == '0':
            break
        else:
            print("Opção inválida! Tente novamente.")
            pausar()

def processar_menu_inscricoes(sistema):
    """Processa as opções do menu de inscrições"""
    while True:
        limpar_tela()
        menu_inscricoes()
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == '1':
            inscrever_participante_menu(sistema)
            pausar()
        elif opcao == '2':
            cancelar_inscricao_menu(sistema)
            pausar()
        elif opcao == '0':
            break
        else:
            print("Opção inválida! Tente novamente.")
            pausar()

def processar_menu_relatorios(sistema):
    """Processa as opções do menu de relatórios"""
    while True:
        limpar_tela()
        menu_relatorios()
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == '1':
            print()
            sistema.gerar_relatorio()
            pausar()
        elif opcao == '2':
            calcular_receita_menu(sistema)
            pausar()
        elif opcao == '0':
            break
        else:
            print("Opção inválida! Tente novamente.")
            pausar()

def main():
    """Função principal do programa"""
    # Criar pasta para o banco de dados se não existir
    import os
    if not os.path.exists('dados'):
        os.makedirs('dados')
    
    # Inicializar o sistema
    sistema = Sistema_Evento()
    
    print("\n" + "="*50)
    print("   BEM-VINDO AO SISTEMA DE EVENTOS!")
    print("="*50)
    pausar()
    
    try:
        while True:
            limpar_tela()
            exibir_menu_principal()
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == '1':
                processar_menu_eventos(sistema)
            elif opcao == '2':
                processar_menu_participantes(sistema)
            elif opcao == '3':
                processar_menu_inscricoes(sistema)
            elif opcao == '4':
                processar_menu_relatorios(sistema)
            elif opcao == '0':
                print("\n" + "="*50)
                print("   Encerrando o sistema...")
                print("   Obrigado por usar nosso sistema!")
                print("="*50 + "\n")
                break
            else:
                print("\nOpção inválida! Tente novamente.")
                pausar()
    
    except KeyboardInterrupt:
        print("\n\nPrograma interrompido pelo usuário.")
    
    except Exception as e:
        print(f"\nErro crítico: {e}")
    
    finally:
        # Fechar conexão com o banco de dados
        sistema.fechar_conexao()
        print("Conexão com banco de dados encerrada.")

if __name__ == "__main__":
    main()