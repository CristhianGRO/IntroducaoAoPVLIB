#INTRODUÇÃO AO PVLIB - Exemplo 2: Geração anual e comparação entre hemisférios.
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

#Criando um objeto do tipo location, para cada hemisfério, com as informações de coordenada geográfica, fuso horário, altitude e nome, que serão utilizadas pelo ModelChain. 

#A localização no hemisfério sul se refere ao endereço da FAET/UFMT.
location_sul = Location(latitude=-15.608259564142905, 
                        longitude=-56.06485209329807,
                        tz='America/Fortaleza',
                        altitude=190,
                        name='FAET UFMT')

#A localização se refere ao endereço da Universidade de New Castle, no Reino Unido.
location_norte = Location(latitude=  54.978, 
                          longitude= -1.615,
                          tz='US/Eastern',
                          altitude=190,
                          name='Hemisferio norte')

#Considera-se os mesmos módulos e inversores para ambos os cenários de avaliação
#Escolhendo as bases de dados de módulos e inversores a serem utilizados.
sandia_models = pvlib.pvsystem.retrieve_sam('SandiaMod')
cec_inverters = pvlib.pvsystem.retrieve_sam('CECInverter')
#Selecionando o modelo do módulo e inversor a ser utilizado.
module = sandia_models['Canadian_Solar_CS5P_220M___2009_']
inverter = cec_inverters['ABB__MICRO_0_25_I_OUTD_US_208__208V_']

#Definindo o modelo de desempenho de acordo com a temperatura de costa de célula.
temperature_parameters = TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_glass']

#Definindo o sistema PV, com as informaçães de ângulo, ajuste de temperatura, modelo de módulo e de inversor, bem como definindo a quantidade de módulos utilizados por string e a quantidade de strings adotadas.
system_sul = PVSystem(surface_tilt=45,surface_azimuth=180,
                      module_parameters = module, 
                      inverter_parameters = inverter,
                      temperature_model_parameters=temperature_parameters,
                      modules_per_string=1,
                      strings_per_inverter=1)

system_norte = PVSystem(surface_tilt=45,surface_azimuth=30,
                        module_parameters = module, 
                        inverter_parameters = inverter,
                        temperature_model_parameters=temperature_parameters,
                        modules_per_string=1,
                        strings_per_inverter=1)

#Criação dos ModelChain, com as informações de localização e sistema PV.
modelChain_sul = ModelChain(system_sul,location_sul)
modelChain_norte = ModelChain(system_norte,location_norte)

#Criação de um Pandas Dataframe com os horários de início e fim da simulação, para uma dada granularidade de dados e fuso horário.
#Seleciona-se o período relativo ao ano de 2019.
times = pd.date_range(start="2019-01-01",end="2020-01-01",
                    freq="1h",
                    tz=location_norte.tz)
#Coletando as informações de temperatura, umidade relativa e vento, para os horários definidos, considerando condições atmosféricas de céu limpo.
clear_sky_sul   = location_sul.get_clearsky(times)
clear_sky_norte = location_norte.get_clearsky(times)

#Execução do modelo de simulação, considerando condiçães atmosféricas de céu limpo e plotagem da potência CA gerada.
modelChain_sul.run_model(clear_sky_sul)
modelChain_norte.run_model(clear_sky_norte)

#Mudando o estilo de cores dos gráficos
plt.style.use('bmh')
#Criando um subplot para o gráfico relativo a geração anual no hemisfério sul
plt.subplot(2,1,1)
plt.plot(modelChain_sul.results.ac,label='Hemisferio sul')
plt.title('Potencia AC gerada em um ano para o Hemisfério Sul')
plt.xlabel('Horas')
plt.ylabel('Potencia AC [W]')
plt.ylim(0,200)
plt.legend()
#Criando um subplot para o gráfico relativo a geração anual no hemisfério norte
plt.subplot(2,1,2)
plt.plot(modelChain_norte.results.ac,label='Hemisferio norte')
plt.title('Potencia AC gerada em um ano para o Hemisfério Norte')
plt.xlabel('Horas')
plt.ylabel('Potencia AC [W]')
plt.ylim(0,200)
plt.legend()

plt.show()