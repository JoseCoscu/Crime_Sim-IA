from openai import OpenAI


import tkinter as tk

texto_guardado = ""  # Variable global para almacenar el texto

def guardar_texto():
    global texto_guardado  # Acceder a la variable global
    texto_guardado = entrada_texto.get()
    print("Texto guardado:", texto_guardado)
    ventana.destroy()  # Cerrar la ventana después de guardar el texto

# Crear la ventana
ventana = tk.Tk()
ventana.title("Introducir Texto")

# Crear un campo de entrada de texto con marcador de posición
entrada_texto = tk.Entry(ventana, width=50)
entrada_texto.insert(0, "Introduzca la descripción de la ciudad")  # Texto de marcador de posición
entrada_texto.pack(pady=10)

# Función para eliminar el marcador de posición cuando se hace clic en el campo de entrada
def eliminar_placeholder(event):
    if entrada_texto.get() == "Introduzca la descripción de la ciudad":
        entrada_texto.delete(0, tk.END)

entrada_texto.bind("<FocusIn>", eliminar_placeholder)

# Botón para guardar el texto
boton_guardar = tk.Button(ventana, text="Guardar Texto", command=guardar_texto)
boton_guardar.pack()

# Ejecutar el bucle principal de la ventana
ventana.mainloop()

# Después de que se cierra la ventana, puedes acceder al texto guardado
print("Texto guardado fuera de la ventana:", texto_guardado)




# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

completion = client.chat.completions.create(
    messages=[
        {"role": "system",
         "content": "Dada la siguiente descripcion de una ciudad, extrae los siguientes datos en forma de json"
                    "habitantes:"
                    "criminales:"
                    "oficiales:"
                    "bomberos:"
                    "habitantes por casa:"
                    "si los datos estan expresados en % haz la conversion"
                    "y devuelveme un numero ademas no escribas nada mas solo devuelve el json generado"
                    "si no hay mensaje devuelve valores por defecto pequenos enteros"},
        {"role": "user",
         "content": "   "

         }
    ],
    model="text-davinci-002",  # Specify the model here
    temperature=0.7,
)

# print(completion.choices[0].message.content)

while True:
    try:
        dic = eval(completion.choices[0].message.content)
        if dic:
            print(dic)
            break
    except:
        continue

