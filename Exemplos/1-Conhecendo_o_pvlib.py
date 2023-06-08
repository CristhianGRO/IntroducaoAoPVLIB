#INTRODUÇÃO AO PVLIB - Exemplo 1: Conhecendo o PVLib.
#==========================================================================================
#Autor: Cristhian Gabriel da Rosa de Oliveira | Departamento de Engenharia Elétrica, UFMT
#Jun. 2023
#==========================================================================================

#Importando as bibliotecas e módulos necessários para a execução do código.
import pvlib 
from pvlib.modelchain import ModelChain
from pvlib.location import Location
from pvlib.pvsystem import PVSystem
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS

import pandas as pd 
import matplotlib.pyplot as plt

#Criando um objeto do tipo location, com as informações de coordenada geográfica, fuso horário, altitude e nome, que serão utilizadas pelo ModelChain. As coordenadas se referem ao endereço da FAET UFMT.
location = Location(latitude=-15.608259564142905, 
                    longitude=-56.06485209329807,
                    tz='America/Fortaleza',
                    altitude=190,
                    name='FAET UFMT')

#Escolhendo as bases de dados de módulos e inversores a serem utilizados.
sandia_models = pvlib.pvsystem.retrieve_sam('SandiaMod')
cec_inverters = pvlib.pvsystem.retrieve_sam('CECInverter')
#Selecionando o modelo do módulo e inversor a ser utilizado.
module = sandia_models['Canadian_Solar_CS5P_220M___2009_']
inverter = cec_inverters['ABB__MICRO_0_25_I_OUTD_US_208__208V_']

#Definindo o modelo de desempenho de acordo com a temperatura de costa de célula.
temperature_parameters = TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_glass']

#Definindo o sistema PV, com as informaçães de ângulo, ajuste de temperatura, modelo de módulo e de inversor, bem como definindo a quantidade de módulos utilizados por string e a quantidade d strings adotadas.
system = PVSystem(surface_tilt=45,surface_azimuth=180,
                  module_parameters = module, 
                  inverter_parameters = inverter,
                  temperature_model_parameters=temperature_parameters,
                  modules_per_string=1,
                  strings_per_inverter=1)

#Criação de um ModelChain com base nos dados do sistema PV e localização definidos.
modelChain = ModelChain(system,location)

#Criação de um Pandas Dataframe com os horários de início e fim da simulação, para uma dada granularidade de dados e fuso horário.
times = pd.date_range(start="2019-01-01",end="2019-01-02",
                    freq="1h",
                    tz=location.tz)
#Coletando as informações de temperatura, umidade relativa e vento, para os horários definidos, considerando condições atmosféricas de céu limpo.
clear_sky = location.get_clearsky(times)

#Execução do modelo de simulação, considerando condiçães atmosféricas de céu limpo e plotagem da potência CA gerada.
modelChain.run_model(clear_sky)
modelChain.results.ac.plot(figsize=(16,9))
plt.show()


