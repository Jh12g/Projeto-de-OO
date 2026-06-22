from abc import ABC, abstractmethod


class Pessoa(ABC):

    @property
    @abstractmethod
    def nome(self):
        pass

    @property
    @abstractmethod
    def cpf(self):
        pass

    @abstractmethod
    def atividade(self):
        pass

class Professor(Pessoa):
    def __init__(self,nome,cpf,disciplina):
            self._nome = nome
            self._cpf = cpf
            self.disciplina = disciplina

    @property
    def nome(self):
        return self._nome
    
    @property
    def cpf(self):
        return self._cpf

    def atividade(self):
        return f"Professo {self.nome}, com o cpf{self._cpf} , ministra a materia {self.disciplina}"
p1 = Professor("yan",123456,"viado")
print(p1.atividade())


class Person(ABC):
    
    def __init__(self,nome,cpf):
        self._nome = nome
        self._cpf = cpf

    @property
    def nome(self):
        return self._nome   
    
    @property 
    def cpf(self):
        return self._cpf

    @abstractmethod
    def atividade(self):
        pass

class Medico(Person):
    def __init__(self, nome,cpf,especialidade):
        super().__init__(nome,cpf)
        self.especialidade = especialidade

    def atividade(self):
        return f"Medico {self.nome}, com o cpf {self._cpf},  especialidade em {self.especialidade}"

medico1 = Medico("fernandin",123123123,"cardiologia")
print(medico1.atividade())
