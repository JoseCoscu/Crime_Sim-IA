from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

completion = client.chat.completions.create(
    messages=[
        {"role": "system",
         "content": "dado la siguiente descripcion necesito que me saques los siguientes datos:cantidad de "
                    "habitantes,cantidad de criminales,cantidada de policias,moral promedio de los ciudadanos,"
                    "probabilidad de un ciudadano a denunciar un crimen,la caracteristica que  no exista ponla en null"
                    " y devuelve eso solo en un json "},
        {"role": "user", "content": f"{input()}"

         }
    ],
    model="text-davinci-002",  # Specify the model here
    temperature=0.7,
)

print(completion.choices[0].message.content)

