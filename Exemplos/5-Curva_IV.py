#INTRODUÇÃO AO PVLIB - Exemplo 5: Plotando a Curva IV do arranjo.
#==========================================================================================
#Autor: Cristhian Gabriel da Rosa de Oliveira | Departamento de Engenharia Elétrica, UFMT
#Jun. 2023
#==========================================================================================

#Importando as bibliotecas e módulos necessários para a execução do código.
from pvlib import pvsystem
import pandas as pd
import matplotlib.pyplot as plt

#Definindo os parâmetros do módulo usado para traçar a curva IV do arranjo. Dados do módulo Canadian Solar CS5P-220M.
parametros = {
    'Name': 'Canadian Solar CS5P-220M',
    'BIPV': 'N',
    'Date': '10/5/2009',
    'T_NOCT': 42.4,
    'A_c': 1.7,
    'N_s': 96,
    'I_sc_ref': 5.1,
    'V_oc_ref': 59.4,
    'I_mp_ref': 4.69,
    'V_mp_ref': 46.9,
    'alpha_sc': 0.004539,
    'beta_oc': -0.22216,
    'a_ref': 2.6373,
    'I_L_ref': 5.114,
    'I_o_ref': 8.196e-10,
    'R_s': 1.065,
    'R_sh_ref': 381.68,
    'Adjust': 8.7,
    'gamma_r': -0.476,
    'Version': 'MM106',
    'PTC': 200.1,
    'Technology': 'Mono-c-Si',
}
#Definindo os casos nos quais a curva IV será traçada, sendo o par de valores referente, respectivamente, a nível de irradiância (W/m^2) e temperatura (°C), e armazenando-os em um Pandas Dataframe.
casos = [
    (1000, 55),
    (800, 55),
    (600, 55),
    (400, 25),
    (400, 40),
    (400, 55)
]
condicoes = pd.DataFrame(casos, columns=['Irrad.', 'Temp.'])

# Ajusta os parâmetros de referência de acordo com os casos definidos usando o modelo descrito por De Soto no artigo:
# W. De Soto et al., “Improvement and validation of a model for photovoltaic array performance”, Solar Energy, vol 80, pp. 78-88, 2006.
IL, I0, Rs, Rsh, nNsVth = pvsystem.calcparams_desoto(
    condicoes['Irrad.'],
    condicoes['Temp.'],
    alpha_sc=parametros['alpha_sc'],
    a_ref=parametros['a_ref'],
    I_L_ref=parametros['I_L_ref'],
    I_o_ref=parametros['I_o_ref'],
    R_sh_ref=parametros['R_sh_ref'],
    R_s=parametros['R_s'],
    EgRef=1.121,
    dEgdT=-0.0002677
)
#Anexando os parâmetros no objeto PVSystem para cálculo das curvas IV.
curve_info = pvsystem.singlediode(
    photocurrent=IL,
    saturation_current=I0,
    resistance_series=Rs,
    resistance_shunt=Rsh,
    nNsVth=nNsVth,
    ivcurve_pnts=100,
    method='lambertw'
)

# Plotagem das curvas IV
plt.figure()
for i, caso in condicoes.iterrows():
    label = (
        "$Irrad.$ " + f"{caso['Irrad.']} $W/m^2$\n"
        "$Temp.$ " + f"{caso['Temp.']} $Celsius$"
    )
    plt.plot(curve_info['v'][i], curve_info['i'][i], label=label)
    v_mp = curve_info['v_mp'][i]
    i_mp = curve_info['i_mp'][i]
    # mark the MPP
    plt.plot([v_mp], [i_mp], ls='', marker='o', c='k')

plt.legend(loc=(1.0, 0))
plt.xlabel('Tensão do Módulo [V]')
plt.ylabel('Corrente no Módulo [A]')
plt.title(parametros['Name'])
plt.show()
plt.gcf().set_tight_layout(True)

#Printando os resultados obtidos de tensão, corrente e potência.
print(pd.DataFrame({
    'i_sc': curve_info['i_sc'],
    'v_oc': curve_info['v_oc'],
    'i_mp': curve_info['i_mp'],
    'v_mp': curve_info['v_mp'],
    'p_mp': curve_info['p_mp'],
}))