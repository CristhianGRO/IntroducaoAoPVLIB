#INTRODUÇÃO AO PVLIB - Exemplo 9: Dados TMY no PVLib.
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

#Definindo o sistema PV, com as informaçães de ângulo, ajuste de temperatura, modelo de módulo e de inversor, bem como definindo a quantidade de módulos utilizados por string e a quantidade de strings adotadas.
system = PVSystem(surface_tilt=45,surface_azimuth=180,
                  module_parameters = module, 
                  inverter_parameters = inverter,
                  temperature_model_parameters=temperature_parameters,
                  modules_per_string=1,
                  strings_per_inverter=1)

#Criação de um ModelChain com base nos dados do sistema PV e localização definidos.
modelChain = ModelChain(system,location)

#Lendo o arquivo .CSV com dados TMY processados.
tmy = pd.read_csv("IntroducaoAoPVLIB\Exemplos\PVLIB_TMY.csv", index_col=0)
tmy.index = pd.to_datetime(tmy.index)

#Execução do modelo de simulação, considerando condições atmosféricas obtidas a partir de dados TMY e plotagem da potência CA gerada.
modelChain.run_model(tmy)
plt.style.use('bmh')
plt.subplot(2,1,1)
modelChain.results.ac.plot(figsize=(16,9))
plt.title("Potência CA gerada ao longo de um ano")
plt.ylabel("Potência (W)")

#Plotando a soma da energia CA gerada, por mês.                      
plt.subplot(2,1,2)
modelChain.results.ac.resample("M").sum().plot(figsize=(16,9))
plt.title("Soma da potência CA gerada por mês")
plt.xlabel("Mês")
plt.ylabel("Potência (W)")

plt.show()

