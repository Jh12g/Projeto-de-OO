from abc import ABC, abstractmethod
from datetime import datetime, date, time
import json
import os

class Pessoa(ABC):
    def __init__(self, nome, cpf, idade):
        self._nome = nome
        self._cpf = cpf
        self._idade = idade

    @property
    def nome(self):
        return self._nome

    @property
    def cpf(self):
        return self._cpf
        
    @property
    def idade(self):
        return self._idade

    @abstractmethod
    def detalhar_perfil(self):
        pass

class Funcionario(Pessoa):
    def __init__(self, nome, cpf, idade, salario, escala):
        super().__init__(nome, cpf, idade)
        self.__salario = salario
        self.__escala = escala

    @property
    def salario(self):
        return self.__salario

    @property
    def escala(self):
        return self.__escala

    @salario.setter
    def salario(self, novo_salario):
        if novo_salario > 0:
            self.__salario = novo_salario
        else:
            raise ValueError("O salário não pode ser negativo ou zero.")

    def detalhar_perfil(self):
        return f"[Funcionário] {self.nome} - Escala: {self.__escala}"

class Medico(Funcionario):
    def __init__(self, nome, cpf, idade, salario, escala, crm, especialidade, custo_consulta):
        super().__init__(nome, cpf, idade, salario, escala)
        self.__crm = crm
        self.__especialidade = especialidade
        self.__custo_consulta = custo_consulta

    @property
    def crm(self):
        return self.__crm

    @property
    def especialidade(self):
        return self.__especialidade

    @property
    def custo_consulta(self):
        return self.__custo_consulta

    @custo_consulta.setter
    def custo_consulta(self, novo_custo):
        self.__custo_consulta = novo_custo

    def detalhar_perfil(self):
        return f"[Médico] Dr(a). {self.nome} - {self.especialidade} (CRM: {self.__crm})"


#  PRONTUÁRIO E PACIENTES 

class ProntuarioMedico:
    def __init__(self, id_prontuario):
        self.__id = id_prontuario
        self.__anotacoes = []

    def adicionar_nota(self, nota):
        agora = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.__anotacoes.append(f"[{agora}] {nota}")

    @property
    def id_prontuario(self):
        return self.__id

    @property
    def historico(self):
        return self.__anotacoes
        
    @historico.setter
    def historico(self, lista_notas):
        self.__anotacoes = lista_notas

class Paciente(Pessoa):
    def __init__(self, nome, cpf, idade, doenca_cronica):
        super().__init__(nome, cpf, idade)
        self.__doenca_cronica = doenca_cronica
        # Composição
        self.__prontuario = ProntuarioMedico(id_prontuario=cpf)

    @property
    def doenca_cronica(self):
        return self.__doenca_cronica

    @doenca_cronica.setter
    def doenca_cronica(self, nova_doenca):
        self.__doenca_cronica = nova_doenca

    @property
    def prontuario(self):
        return self.__prontuario

    def detalhar_perfil(self):
        return f"[Paciente] {self.nome} - Tratamento para: {self.doenca_cronica}"

class PacienteEspecial(Paciente):
    def __init__(self, nome, cpf, idade, doenca_cronica, plano_saude):
        super().__init__(nome, cpf, idade, doenca_cronica)
        self.__plano_saude = plano_saude

    @property
    def plano_saude(self):
        return self.__plano_saude

    def detalhar_perfil(self):
        return f"[Paciente Especial] {self.nome} - Tratamento: {self.doenca_cronica} | Plano: {self.__plano_saude}"


# GESTÃO DA CLÍNICA, AGENDAMENTO E FATURA

class Agendamento:
    def __init__(self, id_agendamento, data_ag, hora_ag, medico, paciente, status="Pendente"):
        self.__id = id_agendamento
        self.__data = data_ag  # Espera objeto datetime.date
        self.__hora = hora_ag  # Espera objeto datetime.time
        self.__medico = medico  # Instância de Medico
        self.__paciente = paciente  # Instância de Paciente ou PacienteEspecial
        self.__status = status

    @property
    def id_agendamento(self):
        return self.__id

    @property
    def medico(self):
        return self.__medico

    @property
    def paciente(self):
        return self.__paciente

    @property
    def data(self):
        return self.__data

    @property
    def hora(self):
        return self.__hora

    @property
    def status(self):
        return self.__status

    def confirmar_atendimento(self):
        self.__status = "Concluida"

class Fatura:
    def __init__(self, id_fatura, valor_total, status_pagamento="Aberta"):
        self.__id = id_fatura
        self.__valor_total = valor_total
        self.__status_pagamento = status_pagamento

    @property
    def id_fatura(self):
        return self.__id

    @property
    def valor_total(self):
        return self.__valor_total

    @property
    def status_pagamento(self):
        return self.__status_pagamento

    def registrar_pagamento(self):
        self.__status_pagamento = "Paga"

class SetorFaturamento:
    def gerar_fatura(self, agendamento, id_custom=101):
        if agendamento.status == "Concluida":
            valor = agendamento.medico.custo_consulta
            if isinstance(agendamento.paciente, PacienteEspecial):
                print(f" Consulta coberta pelo plano de saúde: {agendamento.paciente.plano_saude}.")
                valor = 0.0
            return Fatura(id_fatura=id_custom, valor_total=valor)
        return None

class Clinica:
    def __init__(self):
        self.__medicos = []
        self.__pacientes = []
        self.__funcionarios = []
        self.__agendamentos = []
        self.__contador_id = 1
        self.ARQUIVO_DB = "banco_clinica.json"

    def cadastrar_medico(self, medico):
        self.__medicos.append(medico)

    def cadastrar_paciente(self, paciente):
        self.__pacientes.append(paciente)
        
    def cadastrar_funcionario(self, funcionario):
        self.__funcionarios.append(funcionario)

    def realizar_agendamento(self, data_ag, hora_ag, medico, paciente, id_custom=None, status="Pendente"):
        id_atual = id_custom if id_custom is not None else self.__contador_id
        agendamento = Agendamento(id_atual, data_ag, hora_ag, medico, paciente, status)
        self.__agendamentos.append(agendamento)
        if id_custom is None:
            self.__contador_id += 1
        return agendamento
    
    def buscar_agendamentos_pendentes(self):
        return [ag for ag in self.__agendamentos if ag.status == "Pendente"]

    @property
    def medicos(self):
        return self.__medicos

    @property
    def pacientes(self):
        return self.__pacientes

    @property
    def funcionarios(self):
        return self.__funcionarios

    @property
    def agendamentos(self):
        return self.__agendamentos

    # === SISTEMA DE PERSISTÊNCIA JSON ===

    def salvar_dados(self, faturas):
        """Converte todas as listas de objetos em dicionários e salva no arquivo JSON."""
        dados = {
            "contador_id": self.__contador_id,
            "funcionarios": [],
            "medicos": [],
            "pacientes": [],
            "agendamentos": [],
            "faturas": []
        }

        # 1. Funcionários
        for f in self.__funcionarios:
            # Evita duplicar médicos que também são funcionários na lista base
            dados["funcionarios"].append({
                "nome": f.nome, "cpf": f.cpf, "idade": f.idade,
                "salario": f.salario, "escala": f.escala
            })

        # 2. Médicos
        for m in self.__medicos:
            dados["medicos"].append({
                "nome": m.nome, "cpf": m.cpf, "idade": m.idade,
                "salario": m.salario, "escala": m.escala, "crm": m.crm,
                "especialidade": m.especialidade, "custo_consulta": m.custo_consulta
            })

        # 3. Pacientes
        for p in self.__pacientes:
            p_dict = {
                "nome": p.nome, "cpf": p.cpf, "idade": p.idade,
                "doenca_cronica": p.doenca_cronica,
                "prontuario": p.prontuario.historico,
                "tipo": "Especial" if isinstance(p, PacienteEspecial) else "Comum"
            }
            if isinstance(p, PacienteEspecial):
                p_dict["plano_saude"] = p.plano_saude
            dados["pacientes"].append(p_dict)

        # 4. Agendamentos (Salvamos os CPFs em vez dos objetos completos)
        for ag in self.__agendamentos:
            dados["agendamentos"].append({
                "id": ag.id_agendamento,
                "data": ag.data.strftime("%d/%m/%Y"),
                "hora": ag.hora.strftime("%H:%M"),
                "medico_cpf": ag.medico.cpf,
                "paciente_cpf": ag.paciente.cpf,
                "status": ag.status
            })

        # 5. Faturas
        for fat in faturas:
            dados["faturas"].append({
                "id": fat.id_fatura,
                "valor_total": fat.valor_total,
                "status_pagamento": fat.status_pagamento
            })

        with open(self.ARQUIVO_DB, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        print("\n Dados salvos com sucesso!")

    def carregar_dados(self):
        """Lê o arquivo JSON e reconstrói os objetos em memória."""
        if not os.path.exists(self.ARQUIVO_DB):
            return [] # Retorna uma lista de faturas vazia se o arquivo não existir

        with open(self.ARQUIVO_DB, "r", encoding="utf-8") as f:
            try:
                dados = json.load(f)
            except json.JSONDecodeError:
                return []

        self.__contador_id = dados.get("contador_id", 1)

        # 1. Recriar Funcionários
        for f in dados.get("funcionarios", []):
            self.cadastrar_funcionario(Funcionario(f["nome"], f["cpf"], f["idade"], f["salario"], f["escala"]))

        # 2. Recriar Médicos
        for m in dados.get("medicos", []):
            self.cadastrar_medico(Medico(m["nome"], m["cpf"], m["idade"], m["salario"], m["escala"], m["crm"], m["especialidade"], m["custo_consulta"]))

        # 3. Recriar Pacientes e seus Prontuários
        for p in dados.get("pacientes", []):
            if p["tipo"] == "Especial":
                novo_p = PacienteEspecial(p["nome"], p["cpf"], p["idade"], p["doenca_cronica"], p["plano_saude"])
            else:
                novo_p = Paciente(p["nome"], p["cpf"], p["idade"], p["doenca_cronica"])
            novo_p.prontuario.historico = p["prontuario"]
            self.cadastrar_paciente(novo_p)

        # Helper para buscar objetos por CPF durante a reconstrução das relações
        dict_medicos = {m.cpf: m for m in self.__medicos}
        dict_pacientes = {p.cpf: p for p in self.__pacientes}

        # 4. Recriar Agendamentos vinculando os objetos corretos através do CPF
        for ag in dados.get("agendamentos", []):
            medico_obj = dict_medicos.get(ag["medico_cpf"])
            paciente_obj = dict_pacientes.get(ag["paciente_cpf"])
            
            if medico_obj and paciente_obj:
                data_obj = datetime.strptime(ag["data"], "%d/%m/%Y").date()
                hora_obj = datetime.strptime(ag["hora"], "%H:%M").time()
                self.realizar_agendamento(data_obj, hora_obj, medico_obj, paciente_obj, id_custom=ag["id"], status=ag["status"])

        # 5. Recriar Faturas (precisa ser retornado para o escopo do menu)
        lista_faturas = []
        for fat in dados.get("faturas", []):
            lista_faturas.append(Fatura(fat["id"], fat["valor_total"], fat["status_pagamento"]))
            
        print("\n Banco de dados carregado com sucesso!")
        return lista_faturas


#  MENU 

def iniciar_sistema():
    clinica = Clinica()
    financeiro = SetorFaturamento()
    
    # Tenta carregar dados existentes, se não houver, inicia vazio ou com os padrões
    faturas_abertas = clinica.carregar_dados()

    # Caso o arquivo não exista (primeira execução), cadastra os dados padrão
    if not os.path.exists(clinica.ARQUIVO_DB):
        print("Criando banco de dados inicial com registros padrão...")
        paciente_comum = Paciente("Gabriel", "111.222.333-44", 25, "Nenhuma")
        paciente_esp = PacienteEspecial("Mariana", "555.666.777-88", 30, "Asma", "Unimed")
        dr_house = Medico("Gregory House", "999.888-77", 50, 15000, "Integral", "CRM/SP 123", "Infectologia", 800.00)

        clinica.cadastrar_paciente(paciente_comum)
        clinica.cadastrar_paciente(paciente_esp)
        clinica.cadastrar_medico(dr_house)
        clinica.salvar_dados(faturas_abertas)

    while True:
        print("\n" + "="*45)
        print(" GESTÃO DE CLÍNICA ")
        print("="*45)
        print("1. Cadastrar Médico")
        print("2. Cadastrar Paciente (Comum ou Especial)")
        print("3. Cadastrar Funcionário")
        print("4. Agendar Consulta")
        print("5. Realizar Atendimento (Médico)")
        print("6. Visualizar Prontuário de Paciente")
        print("7. Efetuar Pagamento de Fatura")
        print("8. Sair do programa")
        print("="*45)
        
        opcao = input("Escolha uma opção: ")

        try:
            if opcao == "1":
                print("\n--- NOVO MÉDICO ---")
                nome = input("Nome: ")
                cpf = input("CPF: ")
                idade = int(input("Idade: "))
                salario = float(input("Salário: "))
                escala = input("Escala (ex: Manhã, Integral): ")
                crm = input("CRM: ")
                especialidade = input("Especialidade: ")
                custo = float(input("Custo da consulta (R$): "))
                
                novo_medico = Medico(nome, cpf, idade, salario, escala, crm, especialidade, custo)
                clinica.cadastrar_medico(novo_medico)
                clinica.salvar_dados(faturas_abertas) # Salva as alterações
                print(" Médico cadastrado com sucesso!")

            elif opcao == "2":
                print("\n--- NOVO PACIENTE ---")
                tipo = input("É paciente com plano de saúde? (s/n): ").strip().lower()
                nome = input("Nome: ")
                cpf = input("CPF: ")
                idade = int(input("Idade: "))
                doenca = input("Tratamento crônico/Doença (ou 'Nenhuma'): ")
                
                if tipo == 's':
                    plano = input("Nome do Plano de Saúde: ")
                    novo_paciente = PacienteEspecial(nome, cpf, idade, doenca, plano)
                else:
                    novo_paciente = Paciente(nome, cpf, idade, doenca)
                    
                clinica.cadastrar_paciente(novo_paciente)
                clinica.salvar_dados(faturas_abertas) # Salva as alterações
                print(f" {novo_paciente.detalhar_perfil()} cadastrado com sucesso!")

            elif opcao == "3":
                print("\n--- NOVO FUNCIONÁRIO ---")
                nome = input("Nome: ")
                cpf = input("CPF: ")
                idade = int(input("Idade: "))
                salario = float(input("Salário: "))
                escala = input("Escala (ex: Noturno, Tarde): ")
                
                novo_func = Funcionario(nome, cpf, idade, salario, escala)
                clinica.cadastrar_funcionario(novo_func)
                clinica.salvar_dados(faturas_abertas) # Salva as alterações
                print(" Funcionário cadastrado com sucesso!")

            elif opcao == "4":
                if not clinica.medicos or not clinica.pacientes:
                    print(" É necessário ter ao menos um médico e um paciente cadastrados.")
                    continue

                print("\n--- PACIENTES ---")
                for i, p in enumerate(clinica.pacientes):
                    print(f"{i + 1}. {p.nome}")
                escolha_pac = int(input("Selecione o paciente: ")) - 1
                pac_escolhido = clinica.pacientes[escolha_pac]

                print("\n--- MÉDICOS ---")
                for i, m in enumerate(clinica.medicos):
                    print(f"{i + 1}. Dr(a). {m.nome} - {m.especialidade} (R${m.custo_consulta:.2f})")
                escolha_med = int(input("Selecione o médico: ")) - 1
                med_escolhido = clinica.medicos[escolha_med]

                data_str = input("Data da consulta (DD/MM/AAAA): ")
                hora_str = input("Horário (HH:MM): ")
                
                data_agendamento = datetime.strptime(data_str, "%d/%m/%Y").date()
                hora_agendamento = datetime.strptime(hora_str, "%H:%M").time()

                agendamento = clinica.realizar_agendamento(
                    data_agendamento, hora_agendamento, med_escolhido, pac_escolhido
                )
                clinica.salvar_dados(faturas_abertas) # Salva as alterações
                print(f" Consulta marcada para {data_agendamento.strftime('%d/%m/%Y')} às {hora_agendamento.strftime('%H:%M')}!")

            elif opcao == "5":
                pendentes = clinica.buscar_agendamentos_pendentes()
                if not pendentes:
                    print(" Não há consultas pendentes.")
                    continue
                
                print("\n--- CONSULTAS PENDENTES ---")
                for i, ag in enumerate(pendentes):
                    print(f"{i + 1}. Paciente: {ag.paciente.nome} | Médico: {ag.medico.nome} | Data: {ag.data.strftime('%d/%m/%Y')} {ag.hora.strftime('%H:%M')}")
                
                escolha_ag = int(input("Selecione a consulta para atender: ")) - 1
                consulta_atual = pendentes[escolha_ag]

                print(f"\n👨‍⚕️ Atendendo paciente: {consulta_atual.paciente.nome}")
                sintomas = input("Digite o parecer clínico/anotações: ")
                
                consulta_atual.paciente.prontuario.adicionar_nota(sintomas)
                consulta_atual.confirmar_atendimento()
                
                # Gera fatura com um ID baseado no tamanho atual da lista para não fixar em 101 sempre
                id_fatura_gerada = 100 + len(faturas_abertas) + 1
                nova_fatura = financeiro.gerar_fatura(consulta_atual, id_custom=id_fatura_gerada)
                if nova_fatura:
                    faturas_abertas.append(nova_fatura)
                
                clinica.salvar_dados(faturas_abertas) # Salva prontuário, status e faturas novas
                print(" Consulta finalizada e prontuário atualizado!")

            elif opcao == "6":
                print("\n--- VISUALIZAR PRONTUÁRIO ---")
                for i, p in enumerate(clinica.pacientes):
                    print(f"{i + 1}. {p.nome}")
                escolha_pac = int(input("Selecione o paciente: ")) - 1
                paciente = clinica.pacientes[escolha_pac]
                
                print(f"\n Prontuário de {paciente.nome} (CPF: {paciente.cpf}):")
                historico = paciente.prontuario.historico
                if not historico:
                    print("Nenhum registro encontrado.")
                else:
                    for nota in historico:
                        print(f"- {nota}")

            elif opcao == "7":
                faturas_pendentes = [f for f in faturas_abertas if f.status_pagamento == "Aberta"]
                
                if not faturas_pendentes:
                    print(" Não há faturas em aberto no momento.")
                    continue

                print(f"\n--- PAGAMENTO DE FATURAS ---")
                for i, fat in enumerate(faturas_pendentes):
                    print(f"{i + 1}. Fatura ID {fat.id_fatura} | Valor: R${fat.valor_total:.2f}")
                
                escolha_fat = int(input("Selecione a fatura para pagar: ")) - 1
                fatura_atual = faturas_pendentes[escolha_fat]

                if fatura_atual.valor_total == 0:
                    print(" Esta fatura tem valor R$0.00 (Coberta por Plano de Saúde). Baixando automaticamente.")
                    fatura_atual.registrar_pagamento()
                else:
                    print("1. Cartão de Crédito | 2. PIX | 3. Dinheiro")
                    forma_pgto = input("Escolha a forma de pagamento: ")
                    if forma_pgto in ["1", "2", "3"]:
                        fatura_atual.registrar_pagamento()
                        print(" Pagamento confirmado!")
                    else:
                        print(" Opção inválida.")
                
                clinica.salvar_dados(faturas_abertas) # Salva alteração de status da fatura

            elif opcao == "8":
                print("Encerrando o sistema... Até logo!")
                break

            else:
                print(" Opção inválida! Escolha um número do menu.")

        except (ValueError, IndexError) as e:
            print(f"\n Erro: Entrada inválida. Certifique-se de digitar opções válidas. ({e})")

if __name__ == "__main__":
    iniciar_sistema()