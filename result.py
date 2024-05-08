import matplotlib.pyplot as plt

# Datos para el gráfico

import pandas as pd
import statsmodels.api as sm

def graf_pastel():
    valores = [30, 20, 25, 10, 15]
    etiquetas = ['A', 'B', 'C', 'D', 'E']

    fig, ax = plt.subplots()
    ax.pie(valores, labels=etiquetas)
    ax.set_title('Gráfico de Pastel')

    plt.show()
def graficar():
    categorias = ['A', 'B', 'C', 'D']
    valores = [15, 24, 12, 10]
    colores = ['blue', 'green', 'red', 'yellow']

    # Crear el gráfico de barras con colores personalizados
    plt.bar(categorias, valores, color=colores)

    # Personalizar el gráfico
    plt.title('Gráfico de barras')
    plt.xlabel('Categorías')
    plt.ylabel('Valores')

    # Mostrar el gráfico
    plt.show()


def crear_tabla():
    # Crear un diccionario con tus datos
    data = {
        'cuid': [],
        'empl': [],
        'crim': [],
        'bomb': [],
        'ofic': [],
        'ind_agre': [],
        'ind_crim': [],
        'robos': [],
        'herd': [],
        'incen': [],
        'crim_cap': [],
        'robos_rep': [],
        'robos_att': [],
    }

    # Crear el DataFrame a partir del diccionario
    df = pd.DataFrame(data)

    # Guardar el DataFrame en un archivo CSV
    df.to_csv('datos.csv', index=False)
    datos=pd.read_csv('datos.csv')


def Reg_lin_mult(cuid,empl,crim,bomb,ofic,ind_agre,ind_crim,var_dep):
    datos = pd.read_csv('datos.csv')
    X = datos[[cuid,crim,bomb,ofic,ind_agre,ind_crim]]
    y = datos[var_dep]

    # add const de datos de entrada
    X = sm.add_constant(X)

    # ajustar el modelo
    modelo = sm.OLS(y, X).fit()
    # acceder a los resultados
    print(modelo.params)

    # imprimir resultados
    print(modelo.summary())
def add_data(cuid,empl,crim,bomb,ofic,ind_agre,ind_crim,robos,herd,incen,crim_cap,robos_rep,robos_att):
    datos = pd.read_csv('datos.csv')
    print(datos)
    new_data = {
        'cuid': [cuid],
        'empl': [empl],
        'crim': [crim],
        'bomb': [bomb],
        'ofic': [ofic],
        'ind_agre': [ind_agre],
        'ind_crim': [ind_crim],
        'robos': [robos],
        'herd': [herd],
        'incen': [incen],
        'crim_cap': [crim_cap],
        'robos_rep': [robos_rep],
        'robos_att': [robos_att]
    }
    df = pd.DataFrame(new_data)
    datos = datos._append(df, ignore_index=True)
    datos.to_csv('datos.csv', index=False)
    datos=pd.read_csv('datos.csv')

# Reg_lin_mult(cuid='cuid',empl='empl',crim='crim',bomb='bomb',ofic='ofic',ind_agre='ind_agre',ind_crim='ind_crim',var_dep='crim_cap')