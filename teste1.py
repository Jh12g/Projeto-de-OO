from abc import ABC, abstractmethod
from datetime import date, time

# CLASSES BASES E HERANÇA

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

    # O Contrato: Toda classe herdeira deve implementar este método
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
    def especialidade(self):
        return self.__especialidade

    @property
    def custo_consulta(self):
        return self.__custo_consulta

    @custo_consulta.setter
    def custo_consulta(self, novo_custo):
        self.__custo_consulta = novo_custo

    # Polimorfismo: Sobrescrevendo o método abstrato
    def detalhar_perfil(self):
        return f"[Médico] Dr(a). {self.nome} - {self.especialidade} (CRM: {self.__crm})"


# PRONTUÁRIO E PACIENTE (COMPOSIÇÃO)

class ProntuarioMedico:
    def __init__(self, id_prontuario):
        self.__id = id_prontuario
        self.__anotacoes = []

    def adicionar_nota(self, nota):
        self.__anotacoes.append(nota)

    @property
    def historico(self):
        return self.__anotacoes

class Paciente(Pessoa):
    def __init__(self, nome, cpf, idade, doenca_cronica):
        super().__init__(nome, cpf, idade)
        self.__doenca_cronica = doenca_cronica
        # Composição: Prontuário nasce e morre com o Paciente
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


# GESTÃO DA CLÍNICA, AGENDAMENTO E FATURAMENTO


class Agendamento:
    def __init__(self, id_agendamento, data_ag, hora_ag, medico, paciente):
        self.__id = id_agendamento
        self.__data = data_ag
        self.__hora = hora_ag
        self.__medico = medico
        self.__paciente = paciente
        self.__status = "Pendente"

    @property
    def medico(self):
        return self.__medico

    @property
    def paciente(self):
        return self.__paciente

    @property
    def status(self):
        return self.__status

    def confirmar_atendimento(self):
        self.__status = "Concluida"

class Fatura:
    def __init__(self, id_fatura, valor_total):
        self.__id = id_fatura
        self.__valor_total = valor_total
        self.__status_pagamento = "Aberta"

    @property
    def valor_total(self):
        return self.__valor_total

    @property
    def status_pagamento(self):
        return self.__status_pagamento

    def registrar_pagamento(self):
        self.__status_pagamento = "Paga"

class SetorFaturamento:
    def gerar_fatura(self, agendamento):
        # Acessando as propriedades de forma limpa (sem os parênteses do antigo get_status())
        if agendamento.status == "Concluida":
            valor = agendamento.medico.custo_consulta
            return Fatura(id_fatura=101, valor_total=valor)
        return None

class Clinica:
    def __init__(self):
        self.__medicos = []
        self.__pacientes = []
        self.__agendamentos = []
        self.__contador_id = 1

    def cadastrar_medico(self, medico):
        self.__medicos.append(medico)

    def cadastrar_paciente(self, paciente):
        self.__pacientes.append(paciente)

    def realizar_agendamento(self, data_ag, hora_ag, medico, paciente):
        agendamento = Agendamento(self.__contador_id, data_ag, hora_ag, medico, paciente)
        self.__agendamentos.append(agendamento)
        self.__contador_id += 1
        return agendamento


# SIMULAÇÃO PRÁTICA 


print("--- INICIANDO SISTEMA DA CLÍNICA ---\n")
clinica = Clinica()
financeiro = SetorFaturamento()

# Cadastros
gabriel = Paciente("Gabriel", "111.222.333-44", 25, "Ligma")
dr_house = Medico("Gregory House", "999.888-77", 50, 15000, "Integral", "CRM/SP 123", "Infectologia", 800.00)

clinica.cadastrar_paciente(gabriel)
clinica.cadastrar_medico(dr_house)

# Polimorfismo na prática:
print(gabriel.detalhar_perfil())
print(dr_house.detalhar_perfil())
print("-" * 30)

# Agendamento
consulta = clinica.realizar_agendamento(date.today(), time(14, 30), dr_house, gabriel)
print(f"Consulta marcada. Status atual: {consulta.status}")

# Atendimento (O Médico acessa o prontuário do Paciente via Associação do Agendamento)
consulta.medico  # Apenas demonstrando que o objeto está ligado
consulta.paciente.prontuario.adicionar_nota("Paciente apresentou sintomas graves de Ligma. Recomendado repouso.")

consulta.confirmar_atendimento()
print(f"Consulta finalizada. Status atual: {consulta.status}")
print(f"Prontuário atualizado: {gabriel.prontuario.historico}")
print("-" * 30)

# Faturamento
fatura = financeiro.gerar_fatura(consulta)
if fatura:
    print(f"Fatura gerada! Valor: R${fatura.valor_total:.2f} | Status: {fatura.status_pagamento}")
    fatura.registrar_pagamento()
    print(f"Pagamento recebido. Novo status: {fatura.status_pagamento}")


# Apenas um comentario pra dizer q é complicado da commit ave maria
