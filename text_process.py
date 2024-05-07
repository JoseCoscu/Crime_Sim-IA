from openai import OpenAI
import tkinter as tk

description = ""  # Variable global para almacenar el texto
default_dic = {'habitantes': 150, 'criminales': 10, 'oficiales': 20, 'bomberos': 10, 'indice_criminalidad': 'Medio',
               'indice_agresividad': 'Medio'}


def guardar_texto():
    global description  # Acceder a la variable global
    description = entrada_texto.get("1.0", "end-1c")
    ventana.destroy()  # Cerrar la ventana después de guardar el texto


# region Ventana

# Crear la ventana
ventana = tk.Tk()
ventana.title("Descripción de Ciudad")

# Ajustar el tamaño de la ventana
ventana.geometry("500x300")

# Introducción
introduccion = "Por favor describa su ciudad lo más preciso y sencillo posible, agregue datos como:\n" \
               "- Cantidad de habitantes\n" \
               "- Cantidad de criminales\n" \
               "- Cantidad de oficiales\n" \
               "- Cantidad de bomberos\n" \
               "- Agresividad de los criminales(Alto, Medio, Bajo)\n\n" \
               "- OJO: Modere la cantidad de ciudadanos dependiendo de los recursos de su sistema"

# Etiqueta para la introducción
etiqueta_intro = tk.Label(ventana, text=introduccion)
etiqueta_intro.pack(pady=10)

# Crear un campo de entrada de texto con marcador de posición
entrada_texto = tk.Text(ventana, width=50, height=5)
entrada_texto.insert("1.0", "")  # Texto de marcador de posición
entrada_texto.pack(pady=10)

# Función para eliminar el marcador de posición cuando se hace clic en el campo de entrada


entrada_texto.bind("<FocusIn>")

# Botón para guardar el texto
boton_guardar = tk.Button(ventana, text="Guardar Texto", command=guardar_texto)
boton_guardar.pack()

# Ejecutar el bucle principal de la ventana
ventana.mainloop()

# endregion

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")


def procesate_text(description):
    dic = {}
    i = 1
    while True:
        if i >= 4:
            return default_dic
        print(f'Procesando......{i}')
        completion = client.chat.completions.create(
            messages=[
                {"role": "system",
                 "content": "Dada la siguiente descripcion de una ciudad, extrae los siguientes datos en forma de json"
                            "habitantes:"
                            "criminales:"
                            "oficiales:"
                            "bomberos:"
                            "indice_criminalidad:"
                            "indice_agresiviad:"
                            "si no hay mensaje devuelve el json vacio,"
                            "el indice de criminalidad que tenga solo uno de estos valores  Alto, Medio o Bajo"
                            "la indide de agresividad que tenga solo uno de estos valores  Alto, Medio o Bajo"
                            "la indice agresividad lo pones en Alto, Medio o Bajo"
                            "si faltan datos devuelve los datos que falten como 0"
                            "escribe solo el json y nada mas no hagas ningun comentario"},
                {"role": "user",
                 "content": f"{description}"

                 }

            ],
            model="LLaMA v2",  # Specify the model here
            temperature=0.7,
        )
        try:
            dic = eval(completion.choices[0].message.content)
            if dic:
                print(dic)
                break
        except:
            i += 1
            continue
    return dic


if description != "":
    dic = procesate_text(description)
else:
    dic = default_dic
try:
    habitantes = dic['habitantes'] if dic['habitantes'] != 0 else default_dic['habitantes']
except:
    habitantes = default_dic['habitantes']
try:
    criminales = dic['criminales'] if dic['criminales'] != 0 else default_dic['criminales']
except:
    criminales = default_dic['criminales']
try:
    oficiales = dic['oficiales'] if dic['oficiales'] != 0 else default_dic['oficiales']
except:
    oficiales = default_dic['oficiales']

try:
    bomberos = dic['bomberos'] if dic['bomberos'] != 0 else default_dic['bomberos']
except:
    bomberos = default_dic['bomberos']

try:
    indice_crim = dic['indice_criminalidad'] if dic['bomberos'] != 0 else default_dic['indice_criminalidad']
except:
    indice_crim = default_dic['indice_criminalidad']

try:
    indice_agresividad = dic['indice_agresividad'] if dic['indice_agresividad'] != 0 else default_dic['indice_agresividad']
except:
    indice_agresividad = default_dic['indice_agresividad']
