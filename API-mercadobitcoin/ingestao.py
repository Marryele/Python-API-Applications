#%%
from abc import ABC, abstractmethod#classe base abstrata 
import json
import os 
from typing import List, Union
import requests
import logging
import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class mercadobitcoinapi():

    def __init__(self, coin:str) -> None:
        self.coin = coin
        self.base_endpoint = "https://www.mercadobitcoin.net/api"

    @abstractmethod #quando adiciono isso forço o desenvolvedor a criar outro endpoint
    def _get_endpoint(self, **kwargs) -> str:  #o **kwargs indica que pode receber inumeras variaveis chave-valor
        pass

    def get_data(self,**kwargs) -> dict:
        endpoint = self._get_endpoint(**kwargs)
        logger.info(f"Getting data from endpoint: {endpoint}")
        response = requests.get(endpoint)
        response.raise_for_status() #metodo da biblioteca pra retornar se der erro
        return response.json()
        

class daysummaryapi(mercadobitcoinapi):

    type = 'day-summary'

    def _get_endpoint(self, date: datetime) -> str:
        return f"{self.base_endpoint}/{self.coin}/{self.type}/{date.year}/{date.month}/{date.day}"


print(daysummaryapi(coin="BTC").get_data(date = datetime.date(2021,6,21)))


#------------------------------CRIANDO UMA OUTRA EXTENSÃO
class tradesapi(mercadobitcoinapi):
    type = "trades"

    def _get_unix_date (self, date:datetime) -> int: #criei essa classe para que a outra não tenha 
                                                    #responsabilidade de conversão e não fira o principio
        return int(date.timestamp())

    def _get_endpoint(self, date_from: datetime.datetime = None, date_to:datetime.datetime = None) -> str:  
                                                                                    # = None é valor default
        if date_from and not date_to:
            unix_date_from = self._get_unix_date(date_from)
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}/{unix_date_from}"
        elif date_from and date_to:
            unix_date_from = self._get_unix_date(date_from)
            unix_date_to = self._get_unix_date(date_to)
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}/{unix_date_from}/{unix_date_to}"
        else:
            endpoint = f"{self.base_endpoint}/{self.coin}/{self.type}"
        return endpoint


#sem passar data cai no else
print(tradesapi("BTC").get_data())

# com datefrom
print(tradesapi("BTC").get_data(date_from = datetime.datetime(2022,8,1)))

# com datefrom e dateto
print(tradesapi("BTC").get_data(date_from = datetime.datetime(2022,8,1), date_to = datetime.datetime(2022,8,2)))


#---CLASSE DE EXCECÇÃO CUSTOMIZADA

class DataTypeNotSupportedForIngestionException(Exception):
    def __init__(self,data) -> None:
        self.data = data
        self.message = f"Data type {type(data)} is not supported for ingestion"
        super().__init__(self.message)
# %%
#--------------- DATA WRITER

class datawriter:
    
    def __init__(self, coin: str, api: str) -> None:
        self.api = api
        self.coin = coin
        #tive que criar esse now para remover os espaços pois o arquvio json não estava sendo criado com espaço de pontos
        self.now = str(datetime.datetime.now()).replace(" ","_").replace(":",'').replace(".",'')
        self.filename = f"{self.api}/{self.coin}/{self.now}.json"

    def _write_row(self, row: str) -> None:

        os.makedirs(os.path.dirname(self.filename),exist_ok= True)
        print(f"nome arquivo: {self.filename}")
        #C:\Users\Marry\aws_engenharia_dados\API\day-summary\BTC
        with open(self.filename,"a") as f:  # a é o método append para não apagar os dados do arquivo
            f.write(row)

    def write(self, data: Union[List, dict]):
        if isinstance(data, dict):
            self._write_row(json.dumps(data) + "\n")
        elif isinstance(data, List):
            for element in data:
                self.write(element) #aqui em vez de escrever ele vai chamar a propria função e entrar no primeiro dict
        else:
            #não é dict nem lista
            #vai levantar uma exceção customizada
            raise DataTypeNotSupportedForIngestionException(data)

#%%
data = daysummaryapi("BTC").get_data(date =datetime.date(2021,6,23))

writer = datawriter('day_summary.json') #criei um arquivo da classe e chamei de writer
writer.write(data)   #chamei o metodo write passando os dados
# %%
data = tradesapi("BTC").get_data()
writer = datawriter('trades_summary.json') #criei um arquivo da classe e chamei de writer
writer.write(data)   #chamei o metodo write passando os dados
# %%


#-----CRIANDO UM INGESTOR

class dataingestor(ABC):

    def __init__(self,writer:datawriter,coins: List[str], default_start_date: datetime.date) -> None:
        self.coins = coins
        self.default_start_date= default_start_date
        self.writer = writer

    @abstractmethod
    def ingest(self) -> None:
        pass

class daysummaryingestor(dataingestor):

    def ingest(self) -> None:
        date = self.default_start_date
       
        if date< datetime.date.today():
            
            for coin in self.coins:
                api = daysummaryapi(coin=coin)
                data = api.get_data(date=date)
                self.writer(coin=coin,api=api.type).write(data)


#%%
ingestor = daysummaryingestor(writer=datawriter,coins=['BTC', 'ETH','LTC'],default_start_date=datetime.date(2022,8,2))

ingestor.ingest()
# %%
