from openai import OpenAI
import tkinter as tk
import tkinter as tk

description = ""  # Variable global para almacenar el texto


def guardar_texto():
    global description  # Acceder a la variable global
    description = entrada_texto.get("1.0", "end-1c")
    ventana.destroy()  # Cerrar la ventana después de guardar el texto


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
               "- Cantidad de habitantes por casa\n\n" \
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

# Después de que se cierra la ventana, puedes acceder al texto guardado
print("Texto guardado fuera de:", description)

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

dic = {}

while True:
    print('Procesando......')
    completion = client.chat.completions.create(
        messages=[
            {"role": "system",
             "content": "Dada la siguiente descripcion de una ciudad, extrae los siguientes datos en forma de json"
                        "habitantes:"
                        "criminales:"
                        "oficiales:"
                        "bomberos:"
                        "habitantes por casa:"
                        "si no hay mensaje devuelve el json vacio,"
                        "si faltan datos devuelve los datos que falten como 0"
                        "escribe solo el json"},
            {"role": "user",
             "content": f"{description}"

             }

        ],
        model="text-davinci-002",  # Specify the model here
        temperature=0.7,
    )
    try:
        dic = eval(completion.choices[0].message.content)
        if dic:
            print(dic)
            break
    except:
        continue

habitantes = dic['habitantes']
criminales = dic['criminales']
oficiales = dic['oficiales']
bomberos = dic['bomberos']
hab_x_casa = dic['habitantes por casa']
