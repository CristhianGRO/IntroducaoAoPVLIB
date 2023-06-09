#INTRODUÇÃO AO PVLIB - Exemplo 7: Simulando o efeito de um Tracker de Eixo duplo.
#==========================================================================================
#Autor: Cristhian Gabriel da Rosa de Oliveira | Departamento de Engenharia Elétrica, UFMT
#Jun. 2023
#==========================================================================================

#Importando as bibliotecas e módulos necessários para a execução do código.
#Em especial, no módulo pvsystem, importamos o método SingleAxisTrackerMount, que permite definir um tracker de eixo Único.
import pvlib 
from pvlib.modelchain import ModelChain
from pvlib.location import Location
from pvlib.pvsystem import PVSystem, Array, SingleAxisTrackerMount, AbstractMount
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

#Criação de um Pandas Dataframe com os horários de início e fim da simulação, para uma dada granularidade de dados e fuso horário.
times = pd.date_range(start="2019-01-01",end="2019-01-02",
                    freq="1h",
                    tz=location.tz)
#Coletando as informações de temperatura, umidade relativa e vento, para os horários definidos, considerando condições atmosféricas de céu limpo.
clear_sky = location.get_clearsky(times)

#Definindo os parâmetros do Tracker de Eixo Único.
tracker = SingleAxisTrackerMount(axis_tilt = 45,
                                axis_azimuth=180,
                                max_angle = 90,
                                backtrack = False)

#Coletando a posição do sol que será usada para orientar o sistema de Tracker.
posicao_sol = location.get_solarposition(times)
#Definindo os valores de ângulo do Tracker de Eixo Único, conforme a posição do sol.
orientacao = tracker.get_orientation(solar_zenith=posicao_sol['apparent_zenith'],
                                     solar_azimuth=posicao_sol['azimuth'])

#Definindo o array de módulos conectados ao tracker
array = Array(mount=tracker,module_parameters=module,
              temperature_model_parameters=temperature_parameters,
              modules_per_string=1,strings=1)

#Criando a Modelchain do modelo que simula a atuação do Tracker de Eixo Único.
system_tracker = PVSystem(arrays=[array],inverter_parameters=inverter)
modelChain_tracker = ModelChain(system_tracker,location)

#Definindo a classe que implementa o Tracker de Eixo Duplo.
class DualAxisTrackerMount(AbstractMount):
    def get_orientation(self, solar_zenith, solar_azimuth):
        return {'surface_tilt': solar_zenith,'surface_azimuth':solar_azimuth}

tracker_eixo_duplo = DualAxisTrackerMount()

#Definindo o array de módulos conectados ao tracker de eixo duplo
array_tracker_duplo = Array(mount=tracker_eixo_duplo,module_parameters=module,
                            temperature_model_parameters=temperature_parameters,
                            modules_per_string=1,strings=1)

#Criando o PVSystem do modelo de tracker em eixo duplo
system_tracker_duplo = PVSystem(arrays=[array_tracker_duplo],inverter_parameters=inverter)
modelChain_tracker_duplo = ModelChain(system_tracker_duplo,location)

#Realizando a simulação dos três modelos para comparação.
modelChain_tracker_duplo.run_model(clear_sky)
modelChain_tracker.run_model(clear_sky)
modelChain.run_model(clear_sky)

#Plotando os resultados de potência CA gerada com e sem Tracker.
plt.style.use('bmh')
modelChain_tracker.results.ac.plot(figsize=(16,9))
modelChain_tracker_duplo.results.ac.plot(figsize=(16,9))
modelChain.results.ac.plot(figsize=(16,9))
plt.legend(['Geração com Tracker Eixo Simples','Geração com Tracker Eixo Duplo','Geração sem Tracker'])
plt.title('Comparação entre Potências CA geradas em sistemas fixos e com trackers de eixo duplo e simples')
plt.ylabel('Poténcia [W]')
plt.xlabel('Horário [Hora]')

plt.show()