from abc import ABC, abstractmethod


class Pessoa(ABC):

    @property
    @abstractmethod
    def nome(self):
        pass

    @property
    @abstractmethod
    def salario(self):
        pass

    @property
    @abstractmethod
    def cpf(self):
        pass

    @property
    @abstractmethod
    def atividade(self):
        pass

class Professor(Pessoa):
    def __init__(self,nome, salario, cpf, disciplina):
        self._nome = nome
        self._salario = salario
        self._cpf = cpf
        self.disciplina = disciplina

    @property
    def nome(self):
        return self._nome

    @property
    def salario(self):
        return self._salario

    @property
    def cpf(self):
        return self._cpf

    def atividade(self):
        return f"Professo {self.nome} com o cpf {self.cpf} , com o salario {self.salario} , ministra a materia {self.disciplina}"


class Medico(Pessoa):
    def __init__(self,nome, salario, cpf, especialidade):
        self._nome = nome
        self._salario = salario
        self._cpf = cpf
        self.especialidade = especialidade

    @property
    def nome(self):
        return self._nome

    @property
    def salario(self):
        return self._salario

    @property
    def cpf(self):
        return self._cpf

    def atividade(self):
        return f"O medico {self.nome} com o cpf {self.cpf} , com o salario {self.salario} , tem como especialidade {self.especialidade}"

bd = []

def cadastrar(pessoa):
    if isinstance(pessoa , Pessoa):
        bd.append(pessoa)
        print(f"{pessoa.nome} cadastrado com sucesso")
    else: 
        print(f"Deu erro")

p1 = Professor("Yan",1,1,"polydance")
p2 = Medico("jaime",2,2,"cardiologia")

cadastrar(p1)
cadastrar(p2)

for pessoa in bd:
    print(pessoa.atividade())