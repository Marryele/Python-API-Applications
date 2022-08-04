#%%
## Aula How bootcamps turma 2021

import datetime
import math


class Pessoa:
    def __init__(            # o __init__ método especial da classe vai ser executado sempre que inicializar a classe
            self,
            nome: str,
            sobrenome: str,
            data_de_nascimento: datetime.date) -> None:
        self.data_de_nascimento = data_de_nascimento
        self.sobrenome = sobrenome
        self.nome = nome

    @property
    def idade(self) -> int:
        return math.floor((datetime.date.today() - self.data_de_nascimento).days / 365.2425) 
        #365.2425 para considerar anos bisextos

    def __str__(self) -> str:
        return f"{self.nome} {self.sobrenome} tem {self.idade} anos"

class Curriculo:
    def __init__(self, pessoa: Pessoa, experiencia: list):
        self.experiencia = experiencia
        self.pessoa = pessoa

    @property
    def quat_exper(self) -> int:
        return len(self.experiencia)

    @property
    def empresa_atual(self) -> str:
        return self.experiencia[-1]

    def addiciona_experiencia(self,experiencia:str) -> None:
        self.experiencia.append(experiencia)

    def __str__(self):
        return f"{self.pessoa.nome} {self.pessoa.sobrenome} tem {self.pessoa.idade} anos e já " \
               f"trabalhou em {self.quat_exper} empresas e atualmente trabalha na empresa {self.empresa_atual}"


#%%
andre = Pessoa(nome = 'Andre', sobrenome='Sionek', data_de_nascimento=datetime.date(1991,1,9))

print(andre)
print(andre.nome)


curriculo_andre = Curriculo(pessoa= andre, experiencia=['HBSC','OLIST', 'EmCasa','Gousto'])

print(curriculo_andre.pessoa.idade)
print(curriculo_andre)
curriculo_andre.addiciona_experiencia("How Education")
print(curriculo_andre)


class Vivente:
    def __init__(self, nome: str, data_de_nascimento: datetime.date) -> None:
        self.nome = nome
        self.data_de_nascimento = data_de_nascimento

    @property
    def idade(self) -> int:
        return math.floor((datetime.date.today() - self.data_de_nascimento).days / 365.2425)

    def emite_ruido(self, ruido: str):
        print(f"{self.nome} fez ruido: {ruido}")

#criando uma classe que recebe herança de outra
class PessoaHeranca(Vivente):
    def __str__(self) -> str:
        return f"{self.nome} tem {self.idade} anos"

    def fala(self, frase):
        return self.emite_ruido(frase)


class Cachorro(Vivente):
    def __init__(self, nome: str, data_de_nascimento: datetime.date, raca: str):
        super().__init__(nome, data_de_nascimento) #o super pega os dados da Vivente
        #assim não fere o principio de modificação da classe principal e adiciona Raça pro cachorro extentendo ela
        self.raca = raca

    def __str__(self):
        return f"{self.nome} é da raça {self.raca} e tem {self.idade} anos"

    def late(self):
        return self.emite_ruido("Au! Au!")



andre2 = PessoaHeranca(nome='Andre', data_de_nascimento=datetime.date(1991, 1, 9))

print(andre2)

belisco = Cachorro(nome='Belisco', data_de_nascimento=datetime.date(2019, 4, 15), raca='Lhasa Apso')

print(belisco)

belisco.late()
belisco.late()
belisco.late()
andre2.fala("Cala a boca Belisco!")
belisco.late()
# %%
