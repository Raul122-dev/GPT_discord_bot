import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import openai

from PIL import Image
from io import BytesIO

import aiohttp

from methods_db import _set_api_key, _get_api_key, _update_api_key, _create_user, _get_user, _set_last_messages, _update_last_messages, _get_last_messages
from stable_diffusion import generate_image

from buttons import MyButtons

import logging
log = logging.getLogger("logger_bot")
log.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
log.addHandler(console_handler)

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
TOKEN = os.getenv("DISCORD_TOKEN") 
PREFIX = '/'

# Constants from behavior of GPT
MAX_TOKENS = 150
STOP = "\n"
SYSTEM = "You are a helpful assistant. Your answers must be in Spanish."
MODEL = "gpt-3.5-turbo"
TEMPERATURE = 0.9


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# ------------------ Functions Utils ------------------

def create_image_grid(images):
    width, height = images[0].size
    grid_width = 1 * width
    grid_height = 1 * height

    grid_image = Image.new("RGB", (grid_width, grid_height))

    for index, image in enumerate(images):
        x = (index % 2) * width
        y = (index // 2) * height
        grid_image.paste(image, (x, y))

    return grid_image

def generate_message(store, text, user_id):
    messages = []
    messages.append({"role": "system", "content": SYSTEM})

    for message in store.get("messages", []):
        messages.append(message)
    
    messages.append({"role": "user", "content": text})

    log.info("Messages: " + str(messages) + "\n")
    return messages
    
def _get_format_chat(user_id, store):

    exists = _get_api_key(user_id)

    if exists:
        messages = store
        chat = ""
        for message in messages:
            if message["role"] == "user":
                chat = chat + "Usuario: " + message["content"] + "\n"
            else:
                chat = chat + message["role"] + ": " + message["content"] + "\n"
        return chat
    else:
        return "No hay mensajes almacenados para este usuario"

# ------------------ Bot events ------------------

async def user_have_api_key(ctx):
    user_id = ctx.author.id

    exist_api = await _get_api_key(user_id)

    if ctx.author.id == "637099150097514507" or ctx.author.id == "1105163963840331837":
        return False
    
    if exist_api:
        return True
    else:
        await ctx.send("No tienes una API key registrada")
        return False

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user.name}")

@bot.command(
    name="chat",
)
# @commands.check(user_have_api_key)
async def chat(ctx, arg):
    log.info("Envio de data a OpenAI")
    log.info("--> Store last message from user")
    log.info(ctx.author.id)
    log.info(arg)

    async with ctx.typing():

        if len(arg) > MAX_TOKENS:
            await ctx.send("El mensaje es demasiado largo")
            return

        user_id = ctx.author.id
        text_message = arg

        last_messages = await _get_last_messages(user_id)
    
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=generate_message(last_messages, text_message, user_id),
        )
        log.info(response)

        response_from_ia = response.choices[0].message.content
        response_role = response.choices[0].message.role

        if last_messages.get('messages', []):
            last_messages = last_messages['messages'] + [
                {"role": "user", "content": text_message},
                {"role": response_role, "content": response_from_ia}
            ]
            await _update_last_messages(user_id, last_messages)
        else:
            messages = [
                {"role": "user", "content": arg},
                {"role": response_role, "content": response_from_ia}
            ]
            await _set_last_messages(user_id, messages)

    await ctx.send(response_from_ia, reference=ctx.message)

@chat.error
async def chat_error(ctx, error):
    log.info(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("No se puede enviar un mensaje vacío")
    elif isinstance(error, commands.TooManyArguments):
        await ctx.send("El mensaje es demasiado largo")
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send("Error al enviar el mensaje")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("El comando no existe")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("No tienes los permisos para ejecutar este comando")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("No tengo los permisos para ejecutar este comando")
    else:
        log.error(error)
        await ctx.send("Error al ejecutar el comando: " + str(error))

@bot.command(
    name="img",
)
@commands.check(user_have_api_key)
async def img(ctx, *arg):
    async with ctx.typing():
        message = 'Para generar imagenes puedes usar los comandos:\n\n'
        message += '`/img-stablediff <prompt>`\n'
        message += '`/img-dalle <prompt>`\n'
    await ctx.send(message)

@bot.command(
    name="img-stablediff",
)
@commands.check(user_have_api_key)
async def image_stablediff(ctx, arg):
    async with ctx.typing():
        user_id = ctx.author.id
        prompt_text = arg

        await ctx.send("Your monthly limit exceeded, upgrade subscription now on https://stablediffusionapi.com/pricing")

        # response = await generate_image(prompt_text)

        # if response == 'error':
        #     await ctx.send("Error al generar la imagen")
        #     return

        # images_urls = []
        # images_urls.append(response)

        # # Descarga las imágenes y las almacena en una lista
        # images = []
        # for url in images_urls:
        #     async with aiohttp.ClientSession() as session:
        #         async with session.get(url) as resp:
        #             image_data = await resp.read()
        #             images.append(Image.open(BytesIO(image_data)))

        #  # Crea la cuadrícula de imágenes
        # grid_image = create_image_grid(images)

        # with BytesIO() as image_binary:
        #     grid_image.save(image_binary, "PNG")
        #     image_binary.seek(0)
        #     await ctx.send(file=discord.File(fp=image_binary, filename="image_grid.png"), view=MyButtons(), reference=ctx.message)

@image_stablediff.error
async def image_generate_error(ctx, error):
    log.info(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("No se puede enviar un mensaje vacío")
    elif isinstance(error, commands.TooManyArguments):
        await ctx.send("El mensaje es demasiado largo")
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send("Error al enviar el mensaje")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("El comando no existe")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("No tienes los permisos para ejecutar este comando")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("No tengo los permisos para ejecutar este comando")
    else:
        log.error(error)
        await ctx.send("Error al ejecutar el comando: " + str(error))

@bot.command(
    name="img-dalle",
)
@commands.check(user_have_api_key)
async def image_dalle(ctx, arg):
    async with ctx.typing():
        user_id = ctx.author.id
        prompt_text = arg

        await ctx.send("Your monthly limit exceeded, upgrade subscription now on https://stablediffusionapi.com/pricing")

        # response = openai.Image.create(
        #     prompt = prompt_text,
        #     n=1,
        #     size="1024x1024",
        # )

        # images_urls = []
        # for img in response['data']:
        #     images_urls.append(img['url'])
        
        # # Descarga las imágenes y las almacena en una lista
        # images = []
        # for url in images_urls:
        #     async with aiohttp.ClientSession() as session:
        #         async with session.get(url) as resp:
        #             image_data = await resp.read()
        #             images.append(Image.open(BytesIO(image_data)))

        #  # Crea la cuadrícula de imágenes
        # grid_image = create_image_grid(images)

        # with BytesIO() as image_binary:
        #     grid_image.save(image_binary, "PNG")
        #     image_binary.seek(0)
        #     await ctx.send(file=discord.File(fp=image_binary, filename="image_grid.png"), view=MyButtons(), reference=ctx.message)

@image_dalle.error
async def image_dalle_error(ctx, error):
    log.info(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("No se puede enviar un mensaje vacío")
    elif isinstance(error, commands.TooManyArguments):
        await ctx.send("El mensaje es demasiado largo")
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send("Error al enviar el mensaje")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("El comando no existe")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("No tienes los permisos para ejecutar este comando")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("No tengo los permisos para ejecutar este comando")
    else:
        log.error(error)
        await ctx.send("Error al ejecutar el comando: " + str(error))

@bot.command()
async def setApiKey(ctx, arg):
    log.info("Set API key")
    log.info(arg)

    async with ctx.typing():
        user_id = ctx.author.id
        api_key = arg
        exist_api = await _get_api_key(user_id)

        response = ''

        if not exist_api:
            new_user = await _create_user(ctx.author.id, ctx.author.name)
            if new_user:
                if await _set_api_key(user_id, api_key):
                    response = "API key registrada correctamente" 
                else:
                    response = "Error al registrar la API key, pruebe a intentarlo de nuevo"
            else:
               response = "Error al crear el usuario, pruebe a intentarlo de nuevo"
        else:
            response = f"Ya tienes una API key registrada, puede revisar con el comando {PREFIX}getApiKey \nSi desea cambiarla puede usar el comando {PREFIX}changeApiKey"

    await ctx.send(response)

@setApiKey.error
async def setApiKey_error(ctx, error):
    log.info(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("No se puede enviar un mensaje vacío, se necesita ingregasr la API key")
    elif isinstance(error, commands.TooManyArguments):
        await ctx.send("El mensaje es demasiado largo")
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send("Error al enviar el mensaje")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("El comando no existe")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("No tienes los permisos para ejecutar este comando")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("No tengo los permisos para ejecutar este comando")
    else:
        log.error(error)
        await ctx.send("Error al ejecutar el comando: " + str(error))

@bot.command()
async def changeApiKey(ctx, arg):
    log.info("Change API key")
    log.info(arg)

    async with ctx.typing():
        user_id = ctx.author.id
        api_key = arg
        api_key = await _get_api_key(user_id)

        response = ''

        if api_key:
            api_key = await _get_api_key(user_id)
            exist_user = await _get_user(user_id)
            
            if await _update_api_key(user_id, api_key):
                response = "API key actualizada correctamente para el usuario " + exist_user
            else:
                response = "Error al actualizar la API key, pruebe a intentarlo de nuevo"
        else:
            response = f"No tienes una API key registrada, puede registrarla con el comando {PREFIX}setApiKey"

    await ctx.send(response)

@changeApiKey.error
async def changeApiKey_error(ctx, error):
    log.info(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("No se puede enviar un mensaje vacío, se necesita ingregasr la API key")
    elif isinstance(error, commands.TooManyArguments):
        await ctx.send("El mensaje es demasiado largo")
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send("Error al enviar el mensaje")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("El comando no existe")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("No tienes los permisos para ejecutar este comando")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("No tengo los permisos para ejecutar este comando")
    else:
        log.error(error)
        await ctx.send("Error al ejecutar el comando: " + str(error))

@bot.command()
async def getApiKey(ctx):
    log.info("Get API key")
    async with ctx.typing():
        user_id = ctx.author.id
        api_key = await _get_api_key(user_id)

    if api_key:
        await ctx.send("Tu API key es: " + api_key)
    else:
        await ctx.send("No tienes una API key registrada, puede registrarla con el comando " + PREFIX + "setApiKey")

@bot.command()
async def infoStore(ctx):
    log.info("--> Store last message from user")
    async with ctx.typing():

        user_id = ctx.author.id
        messages_from_user = await _get_last_messages(user_id)
        #chat_history = _get_format_chat(user_id, messages_from_user)

        if messages_from_user:
            messages_from_user = str(messages_from_user["messages"])[0:2000]
            await ctx.send("Dev: Last message from user stored in memory" + "\n" + str(messages_from_user))
        else:    
            await ctx.send("Dev: No messages stored in memory")

    await ctx.send("Dev: Last message from user stored in memory" + "\n" + str(messages_from_user))

bot.run(TOKEN)




