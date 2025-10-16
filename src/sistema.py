import sqlite3
from .evento import Evento
from datetime import datetime

class Sistema_Evento:
    def __init__(self, db_nome='dados/eventos.db'):
        self.conn = sqlite3.connect(db_nome)
        self.cursor = self.conn.cursor() #Estabelencendo conexao com banco de dados.

        #chama o metodo para criar as tabelas
        self._criar_tabelas()       
              
    def _criar_tabelas(self): #tabela eventos
        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS eventos ( 
            id INTEGER PRIMARY KEY, 
            nome TEXT NOT NULL, 
            data TEXT,
            local TEXT, 
            categoria TEXT, 
            capacidade INTEGER, 
            preco REAL
        ) 
        ''') 
        #tabela participantes.
        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS participantes ( 
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL, 
            email TEXT UNIQUE NOT NULL, 
            checkin INTEGER DEFAULT 0 -- 0 para False, 1 para True
            )
     ''')
        
        #tabela para associar Participantes e Eventos (inscrição).
        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS inscricoes (
            participante_id INTEGER,
            evento_id INTEGER,
            PRIMARY KEY (participante_id, evento_id),
            FOREIGN KEY (participante_id) REFERENCES participantes (id),
            FOREIGN KEY (evento_id) REFERENCES eventos (id)
            ) 
        ''')
        self.conn.commit() #Salva as mudanças(criação de tabelas)

    def fechar_conexao(self):
        self.conn.close()#metodo para fechar a concexao quando finalizar o sistema.


    def cadastrar_evento(self, evento): ## -> metodo para cadastrar evento dentro da lista de eventos
        try:
            self.cursor.execute(''' 
                INSERT INTO eventos (nome, data, local,  categoria, capacidade, preco) VALUES (?,?,?,?,?,?) ''', (evento.get_nome(), evento.get_data(), evento.get_local(), evento.get_categoria(), evento.get_capacidade_max(), evento.get_preco() ) )
            self.conn.commit()
            print(f'Evento {evento.get_nome()}, cadastrado com sucesso do BD.')
        except sqlite3.Error as e:
            print(f'Erro ao cadastrar evento: {e}')
        
    def cadastrar_participante(self,participante): # -> metodo para adicionar participante a lista de participantes
        try:
            self.cursor.execute(''' INSERT INTO participantes (nome, email) VALUES (?, ?) ''', (participante.get_nome(), participante.get_email()) )
            self.conn.commit()
            print(f'Participante {participante.get_nome()} Cadastrado com sucesso. ')
        except sqlite3.IntegrityError: #Ativar erro se o email ja existir.
            print(f'Erro: Participante com email {participante.get_email()} já cadastrado')
        except sqlite3.Error as e:
            print(f'Erro ao cadastrar participantes: {e}')
        
    def listar_eventos(self):
       self.cursor.execute(''' SELECT nome, data, local, categoria, capacidade, preco FROM eventos ''')
       eventos = self.cursor.fetchall() #pega todos os resultados.
       if not eventos:
           print('Nenhum evento Cadastrado.')
           return
       
       print('--LISTA DE TODOS OS EVENTOS--')
       for nome, data, local, categoria, capacidade, preco in eventos:
        try:
            data_obj = datetime.strptime(data, '%Y-%m-%d %H:%M:%S') #O formato de entrada que esta no DB.
            data_formatada = data_obj.strftime('%d/%m/%Y')
        except ValueError: #caso a data não esteja no formato esperado, use a string original.
            data_formatada = data

        print(f'Nome: {nome}')
        print(f'Data: {data_formatada}')
        print(f'Local: {local}')
        print(f'Capacidade: {capacidade}')
        print(f'Categoria: {categoria}')
        print(f'Preço: {preco:.2f}')
        print('-'*20)

    def inscrever_participante(self, email_participante, nome_evento):
        self.cursor.execute("SELECT id FROM participantes WHERE email = ?" , (email_participante,) )
        part_result = self.cursor.fetchone() #busca o id do participante pelo email.
        if not part_result:
            print(f'Erro: Participante com email {email_participante} não foi encontrado!')
            return
        
        participante_id = part_result[0]
        
        self.cursor.execute("SELECT id FROM eventos WHERE nome = ?", (nome_evento,))
        event_result = self.cursor.fetchone() #Busca o id do evento pelo nome.
        if not event_result:
            print(f'Erro: Evento {nome_evento} não encontrado.')
            return
        
        evento_id = event_result[0]

        try:
            self.cursor.execute(''' INSERT INTO inscricoes (participante_id, evento_id) VALUES (?,?) ''', (participante_id, evento_id))
            self.conn.commit() #Inseri a tabela de isncrição.
            print(f'participante {email_participante} inscrito com sucesso no evento {nome_evento}')
        except sqlite3.IntegrityError:
            print(f'Participante {email_participante} já esta inscrito no evento {nome_evento}.')
        except sqlite3.Error as e:
            print(f'Erro ao realizar inscrição: {e}')



    def buscar_por_categoria(self,categoria): ## busca a categoria do evento onde foi criada  na base da classe  evento
        self.cursor.execute(''' SELECT nome, data, local, capacidade, preco FROM eventos WHERE categoria = ?''', (categoria,))
        event_result = self.cursor.fetchall() #buscando informacoes da tabela pela categoria informada.
        if not event_result:
            print(f'Nenhum evento encontrado na categoria: {categoria}')
            return 
        
        print(f"--- EVENTOS NA CATEGORIA: {categoria} ---")
        for nome, data, local, capacidade, preco in event_result:
            obj_data = datetime.strptime(data, '%Y-%m-%d %H:%M:%S' ) #Transfoma a data banco para o formato de data br.
            data_formatada = obj_data.strftime('%d/%m/%Y')

            print(f'Nome: {nome}, Data {data_formatada}, Local: {local}, Capacidade: {capacidade}, Preço: {preco}')
            print("-" * 20)
                
    def buscar_por_data(self,data_busca): ## metodo para buscar evento pela data 
        data_obj = datetime.strptime(data_busca, '%d/%m/%Y') #convertendo a data recebida de br para formato do banco de dados.
        data_busca_db = data_obj.strftime('%Y-%m-%d')
        paramentro_like = f'{data_busca_db}%'

        self.cursor.execute(''' SELECT nome, data, local, capacidade, preco FROM eventos WHERE data LIKE ? ''', (paramentro_like,))
        data_result = self.cursor.fetchall()

        if not data_result:
            print(f"Nunhum resultado encontrado na data: {data_busca}")
            return 
        
        print(f'--- EVENTOS ENCONTRADOS NA DATA: {data_busca} ---')
        for nome, data, local, capacidade, preco in data_result:
            obj_data = datetime.strptime(data, '%Y-%m-%d %H:%M:%S') #converetendo novamente agora para o formato de saida br.
            data_formatada = obj_data.strftime('%d/%m/%Y')
            print(f'Nome: {nome}, Data: {data_formatada}, Local: {local}, Capacidade: {capacidade}, Preço: {preco} ')
            print('-' * 20)
                
    def cancelar_inscricao(self,email_participante, nome_evento): # metoodo para cancelar a inscrição
        self.cursor.execute("SELECT id FROM participantes WHERE email = ?" , (email_participante,) )
        part_result = self.cursor.fetchone() #obtendo o emial do participante para realizar o cancelamento.
        
        self.cursor.execute("SELECT id FROM eventos WHERE nome = ?", (nome_evento,))
        event_result = self.cursor.fetchone()
        
        if not part_result or not event_result:
            print("Erro: Participante ou Evento não encontrado.")
            return

        participante_id = part_result[0]
        evento_id = event_result[0]
        
        # 2. Deletar a Inscrição
        try:
            self.cursor.execute(''' 
                DELETE FROM inscricoes WHERE participante_id = ? AND evento_id = ? 
            ''', (participante_id, evento_id))
            
            if self.cursor.rowcount > 0: # Verifica se alguma linha foi deletada
                self.conn.commit()
                print(f"Inscrição do participante {email_participante} no evento {nome_evento} cancelada com sucesso.")
            else:
                print(f"Inscrição não encontrada para {email_participante} no evento {nome_evento}.")
                
        except sqlite3.Error as e:
            print(f"Erro ao cancelar inscrição: {e}")

    def listar_participantes_por_evento(self, nome_evento):
        """
        Busca o evento pelo nome e lista todos os participantes inscritos, 
        incluindo o status de check-in.
        """
        
        # 1. Obter o ID do Evento
        self.cursor.execute("SELECT id FROM eventos WHERE nome = ?", (nome_evento,))
        event_result = self.cursor.fetchone()
        
        if not event_result:
            print(f"Erro: Evento '{nome_evento}' não encontrado.")
            return
            
        evento_id = event_result[0]
        
        # 2. Consultar as três tabelas (JOIN)
        # Seleciona nome, email e status de check-in (checkin=1 significa True)
        self.cursor.execute('''
            SELECT 
                p.nome, 
                p.email, 
                p.checkin
            FROM 
                participantes p
            JOIN 
                inscricoes i ON p.id = i.participante_id
            WHERE 
                i.evento_id = ?
            ORDER BY 
                p.nome
        ''', (evento_id,))
        
        participantes = self.cursor.fetchall()
        
        # 3. Exibir os resultados
        
        if not participantes:
            print(f"O evento '{nome_evento}' não possui participantes inscritos.")
            return

        print(f"\n--- LISTA DE PARTICIPANTES INSCRITOS NO EVENTO: '{nome_evento}' ---")
        
        total_inscritos = len(participantes)
        total_checkin = 0
        
        for nome, email, checkin in participantes:
            status_checkin = "SIM" if checkin == 1 else "NÃO"
            
            if checkin == 1:
                total_checkin += 1
                
            print(f"  Nome: {nome}")
            print(f"  E-mail: {email}")
            print(f"  Check-in: {status_checkin}")
            print("-" * 15)

        print(f"\nResumo do Evento:")
        print(f"Total de Inscritos: {total_inscritos}")
        print(f"Total de Check-ins realizados: {total_checkin}")
        print("-" * 40)

    def realizar_chekin(self,email):
        try:
            # 1. Atualizar o campo checkin na tabela participantes
            self.cursor.execute(''' 
                UPDATE participantes SET checkin = 1 WHERE email = ? AND checkin = 0 
            ''', (email,))
            
            if self.cursor.rowcount > 0:
                self.conn.commit()
                print(f"Check-in realizado com sucesso para o participante com email {email}!")
            else:
                # Pode não ter atualizado se já estava em check-in ou se o email não existe
                self.cursor.execute("SELECT id FROM participantes WHERE email = ?" , (email,) )
                if self.cursor.fetchone():
                    print(f"O participante com email {email} já havia realizado o check-in.")
                else:
                    print(f"Erro: Participante com email {email} não encontrado.")                    
        except sqlite3.Error as e:
            print(f"Erro ao realizar check-in: {e}")

    def gerar_relatorio(self): #Gera um relatorio com o nome do evento e numero de participantes inscritos.
       self.cursor.execute(''' SELECT e.nome, COUNT(i.participante_id) as inscritos FROM eventos e LEFT JOIN inscricoes i ON e.id = i.evento_id GROUP BY e.id ''')
       relatorio = self.cursor.fetchall()
       
       print(" \--- RELATORIO DE INSCRIÇÕES POR EVENTO ---")
       for nome_evento, inscritos in relatorio:
           print(f'Nome de Evento: {nome_evento} | Numero de Inscritos: {inscritos}')
           print('-'*40)

    def listar_eventos_com_vaga(self):
        self.cursor.execute('''
        SELECT 
            e.nome, 
            e.data, 
            e.local, 
            e.capacidade, 
            e.preco,
            COUNT(i.participante_id) as inscritos
        FROM eventos e
        LEFT JOIN inscricoes i ON e.id = i.evento_id
        GROUP BY e.id
    ''')
        eventos = self.cursor.fetchall()

        print("-- EVENTOS COM VAGAS DISPONÍVEIS --")
        for nome, data, local, capacidade, preco, inscritos in eventos:
            if inscritos < capacidade:
                data_formatada = datetime.strptime(data, '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y')
                print(f"Nome: {nome} | Data: {data_formatada} | Local: {local} | Vagas Restantes: {capacidade - inscritos} | Preço: R${preco:.2f}")
            else:
                print(f"Evento '{nome}' está lotado.")
        print("-" * 40)
                
    def calcular_receita_evento(self,nome_evento):
        self.cursor.execute('''
        SELECT 
            e.id, 
            e.preco
        FROM eventos e
        WHERE e.nome = ?
         ''', (nome_evento,))
        evento = self.cursor.fetchone()

        if not evento:
            print(f"Erro: Evento '{nome_evento}' não encontrado.")
            return 0

        evento_id, preco = evento

        self.cursor.execute('''
            SELECT COUNT(*) FROM inscricoes WHERE evento_id = ?
        ''', (evento_id,))
        inscritos = self.cursor.fetchone()[0]

        receita = inscritos * preco

        print(f"A receita do evento '{nome_evento}' é de R${receita:.2f}.")
        return receita
         
