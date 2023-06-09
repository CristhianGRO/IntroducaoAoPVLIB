#INTRODUÇÃO AO PVLIB - Exemplo 8 - Pré-Processamento dos dados fornecidos pelo PVGIS.
#==========================================================================================
#Autor: Cristhian Gabriel da Rosa de Oliveira | Departamento de Engenharia Elétrica, UFMT
#Jun. 2023
#==========================================================================================
#Importando as bibliotecas e módulos necessários para a execução do código.
from pvlib.location import Location
import pandas as pd
import matplotlib.pyplot as plt

#Lendo as colunas referentes a tempo, temperatura do ar, irradiância e velocidade do vento do arquivo .csv
#Pulam-se as 16 primeiras linhas, por conterem informações que não são relevantes para o cálculo.
tmy = pd.read_csv("IntroducaoAoPVLIB\Exemplos\TMY_FAET_UFMT.csv",skiprows=16,nrows=8760,
                usecols=["time(UTC)","T2m","G(h)","Gb(n)","Gd(h)","WS10m"],
                index_col=0)

#Selecionando os dados TMY referentes a um período desejado, nesse caso, o ano de 2017.
tmy.index=pd.date_range(start="2017-01-01 00:00", end="2017-12-31 23:00",freq="h")

#Alterando o nome das colunas para o formato que o pvlib irá interpretar.
tmy.columns = ["temp_air","ghi","dni","dhi","wind_speed"]

#Salvando os dados TMY para leitura do PVLIB
tmy.to_csv("IntroducaoAoPVLIB\Exemplos\PVLIB_TMY.csv")

#Plotando os dados meteorologicos obtidos
plt.style.use('bmh')
tmy.plot(figsize=(16,9))

#Obtenção dos dados de céu limpo, para fins de comparação
location = Location(latitude=-15.608259564142905, 
                    longitude=-56.06485209329807,
                    tz='America/Fortaleza',
                    altitude=190,
                    name='FAET UFMT')

#Criação de um Pandas Dataframe com os horários de início e fim da simulação, para uma dada granularidade de dados e fuso horário.
times = pd.date_range(start="2017-01-01 00:00", end="2017-12-31 23:00",
                    freq="1h",
                    tz=location.tz)

#Coletando as informações de temperatura, umidade relativa e vento, para os horários definidos, considerando condições atmosféricas de céu limpo.
clear_sky = location.get_clearsky(times)

#Plotando os dados meteorologicos obtidos
clear_sky.plot(figsize=(16,9))
plt.show()