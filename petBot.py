from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import json, re, random, asyncio, time

# Abre y carga el archivo JSON que contiene la información de los alimentos para mascotas
with open('DatosMascotas/alimentos.json', encoding='utf-8') as file:
    data = json.load(file)

# Abre y carga el archivo JSON que contiene respuestas en caso de no encontrar una mascota o un alimento.
with open('DatosMascotas/respuestas.json', encoding= 'utf-8') as file:
    respuestas = json.load(file)

# Abre y carga el archivo JSON que contiene información en caso de ingesta de alimentos malos
with open('DatosMascotas/reacciones.json', encoding= 'utf-8') as file:
    reacciones = json.load(file) 

token = '7040554508:AAFUhP7cgQPH0j1DiA3aec9zGRsHIjmHfjk'
usrName = 'PetFoodieBot'

ultimoMsj = None

# Comandos de inicio
async def start(update: Update, context: ContextTypes):
    await update.message.reply_text('Hola, soy PetFoodieBot, te respondo preguntas respecto a la alimentación de tus mascotas. ¿En qué puedo ayudarte?')

async def help(update: Update, context: ContextTypes):
    await update.message.reply_text('Para obtener información precisa asegúrate de que tu mensaje cuente con el tipo de mascota que tienes y el alimento que quieras darle.\n\t'
                                    + '\n\t **Ej. ¿Puedo darle carne a mi perro?** \n' +
                                    '\nNo te preocupes si no pones los signos, entenderé tu pregunta de igual manera.')

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
        reaccionesMascota = {reaccion["nombre"].lower():
                             reaccion for reaccion in reacciones["Mascotas"][tipo_mascota]} if tipo_mascota else{}
        reaccion_nombre = None
        reacciones = None
        recomendaciones = None
        tratamiento = None

        for reaccion in list(reaccionesMascota.keys()):
            if re.search(r'\\b' + reaccion + r'\\b', textoProcesado):
                reaccion_nombre = reaccion
                reacciones = reaccionesMascota[reaccion]["reacciones"]
                recomendaciones = reaccionesMascota[reaccion]["recomendaciones"]
                tratamiento = reaccionesMascota[reaccion]["tratamiento"]
                break
            # Respuesta para cuando la reacción al alimento es encontrada en el JSON
            return f'Si tu {tipo_mascota} ha ingerido {reaccion_nombre}, puede presentar las siguientes reacciones: {reacciones}. Te recomendamos: {recomendaciones}. Tratamiento: {tratamiento}'

        response = random.choice(respuestas['AlimentoNoEncontrado'])
        log(text, response)
    else:
        response = random.choice(respuestas['MascotaNoEncontrada'])
        log(text, response)
        
    return response

#Función para evaluar si el bot esta siendo contactado personalmente o desde un grupo en el que fue añadido y mencionado
async def handle_message(update: Update, context: ContextTypes):
    global ultimoMsj
    message_type = update.message.chat.type
    text = update.message.text

    # Actualiza la hora del último mensaje
    ultimoMsj = time.time()

    # Comprueba si el mensaje es un agradecimiento
    agradecimientos = ['gracias', 'muchas gracias', 'gracias por tu ayuda', 'te lo agradezco']
    if any(agradecimiento in text.lower() for agradecimiento in agradecimientos):
        response = random.choice(respuestas['Agradecimientos'])
    else:
        # Si no es un agradecimiento, procesa el mensaje como antes
        if message_type == 'group':
            if text.startswith(usrName):
                new_text = text.replace(usrName, '')
                response = handle_response(new_text, context, update)
            else:
                return
        else:
            response = handle_response(text, context, update)

    await update.message.reply_text(response)

async def check_inactivity():
    global ultimoMsj
    while True:
        await asyncio.sleep(60)
        if time.time() - ultimoMsj > 120:
            print('La sesión ha terminado, si desesas algo más no dudes en pedirlo.')
            break

async def error(update: Update, context: ContextTypes):
    print(context.error)
    await update.message.reply_text('Ocurrió un error...')
    
def log(question: str, response: str):
    with open('DatosMascotas/log.txt', 'a') as f:
        f.write(f'Pregunta Usuario: {question}\nRespuesta: {response}\n\n')

if __name__ == '__main__':
    print('Bot iniciando...')
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_error_handler(error)

    print('El bot ha iniciado')
    app.run_polling(poll_interval=1, timeout=10)

    # Ejecuta la funcion en segundo plano para comprobar la inactividad
    asyncio.run(check_inactivity())