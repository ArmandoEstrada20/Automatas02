from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import json
import re
import random

# Abre y carga el archivo JSON que contiene la información de los alimentos para mascotas
with open('DatosMascotas/alimentos.json', encoding='utf-8') as file:
    data = json.load(file)

# Abre y carga el archivo JSON que contiene respuestas en caso de no encontrar una mascota o un alimento.
with open('DatosMascotas/respuestas.json', encoding= 'utf-8') as file:
    respuestas = json.load(file)

token = '7040554508:AAFUhP7cgQPH0j1DiA3aec9zGRsHIjmHfjk'
usrName = 'PetFoodieBot'

# Comandos de inicio
async def start(update: Update, context: ContextTypes):
    await update.message.reply_text('Hola, soy PetFoodieBot, te respondo preguntas respecto a la alimentación de tus mascotas. ¿En qué puedo ayudarte?')

async def help(update: Update, context: ContextTypes):
    await update.message.reply_text('Ayuda')

#Función para manejar las respuestas del bot
def handle_response(text: str, context: ContextTypes, update: Update):
    textoProcesado = text.lower()
    print(textoProcesado)

    # Busca si alguna de las palabras coincide con un tipo de mascota en el JSON
    mascota_names = [k.lower() for k in data["Mascotas"].keys()]
    tipo_mascota = None
    for mascota in mascota_names:
        if mascota in textoProcesado:
            tipo_mascota = mascota
            break

    # Busca si alguna de las palabras coincide con un alimento en el JSON
    alimentosBuenos = {alimento["nombre"].lower(): alimento for alimento in data["Mascotas"][tipo_mascota]["alimentosBuenos"]} if tipo_mascota else {}
    alimentosMalos = {alimento["nombre"].lower(): alimento for alimento in data["Mascotas"][tipo_mascota]["alimentosMalos"]} if tipo_mascota else {}
    alimento_nombre = None
    descripcion = None
    for alimento in list(alimentosBuenos.keys()) + list(alimentosMalos.keys()):
        if re.search(r'\b' + alimento + r'\b', textoProcesado):
            alimento_nombre = alimento
            descripcion = (alimentosBuenos[alimento] if alimento in alimentosBuenos else alimentosMalos[alimento])["descripcion"]
            break

    #Respuesta cuando el alimento es encontrado en el JSON
    if tipo_mascota and alimento_nombre:
        if alimento_nombre in alimentosBuenos:
            return f'Sí, puedes darle {alimento_nombre} a tu {tipo_mascota}. {descripcion}'
        elif alimento_nombre in alimentosMalos:
            return f'No, no deberías darle {alimento_nombre} a tu {tipo_mascota}. {descripcion}'
    elif tipo_mascota:
        return random.choice(respuestas['no_alimento_encontrado'])
    else:
        return random.choice(respuestas['no_mascota_encontrada'])

#Función para evaluar si el bot esta siendo contactado personalmente o desde un grupo en el que fue añadido y mencionado
async def handle_message(update: Update, context: ContextTypes):
    message_type = update.message.chat.type
    text = update.message.text

    if message_type == 'group':
        if text.startswith(usrName):
            new_text = text.replace(usrName, '')
            response = handle_response(new_text, context, update)
        else:
            return
    else:
        response = handle_response(text, context, update)

    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes):
    print(context.error)
    await update.message.reply_text('Ocurrió un error...')

if __name__ == '__main__':
    print('Bot iniciando...')
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_error_handler(error)

    print('El bot ha iniciado')
    app.run_polling(poll_interval=1, timeout=10)