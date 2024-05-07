# import matplotlib.pyplot as plt

# # Datos para el gráfico
# categorias = ['A', 'B', 'C', 'D']
# valores = [15, 24, 12, 10]
# colores = ['blue', 'green', 'red', 'yellow']

# # Crear el gráfico de barras con colores personalizados
# plt.bar(categorias, valores, color=colores)

# # Personalizar el gráfico
# plt.title('Gráfico de barras')
# plt.xlabel('Categorías')
# plt.ylabel('Valores')

# # Mostrar el gráfico
# plt.show()

import pandas as pd
import statsmodels.api as sm

def guardar_datos():
    # Crear un diccionario con tus datos
    data = {
        'cant_a': [10, 12, 8, 15],
        'cant_b': [8, 6, 9, 7],
        'cant_c': [15, 18, 12, 10],
        'x': [25.2, 27.5, 22.1, 24.8]
    }

    # Crear el DataFrame a partir del diccionario
    df = pd.DataFrame(data)

    # Guardar el DataFrame en un archivo CSV
    df.to_csv('datos.csv', index=False)
    datos=pd.read_csv('datos.csv')
    x=datos[['cant_a']]
    print(x)

def Reg_lin_mult():
    datos = pd.read_csv('datos.csv')
    X = datos[['cant_a', 'cant_b', 'cant_c']]
    y = datos['x']

    # add const de datos de entrada
    X = sm.add_constant(X)

    # ajustar el modelo
    modelo = sm.OLS(y, X).fit()
    # acceder a los resultados
    print(modelo.params)

    # imprimir resultados
    print(modelo.summary())


#guardar_datos()
Reg_lin_mult()