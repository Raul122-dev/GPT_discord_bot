# GPT_discord_bot

Para correr el bot se debe crear un archivo .env con las siguientes variables de entorno:
```
OPENAI_API_KEY=
DISCORD_TOKEN=
MONGO_URL=
```
Para instalar las librerias de python se debe correr el siguiente comando:
```
pip install -r requirements.txt
```
Para correr el bot se debe correr el siguiente comando:
```
python bot.py
```

El bot es un chatbot que utiliza la api de OpenAI para generar respuestas a partir de un texto de entrada. El bot funciona de la siguiente manera:
1. El usuario envia un mensaje al bot.
2. El bot envia el mensaje a la api de OpenAI para generar una respuesta.
3. El bot envia la respuesta al usuario.
4. El bot guarda el mensaje y la respuesta en una base de datos.
5. El bot utiliza el mensaje y la respuesta para entrenar el modelo de OpenAI.
6. El bot repite el proceso desde el paso 1.
7. El bot se entrena cada 10 mensajes.
8. El bot se entrena cada 10 minutos.
9. El bot se entrena cada 10 mensajes o cada 10 minutos, lo que ocurra primero.
10. El bot se entrena cada 10 mensajes y cada 10 minutos.
11. 

