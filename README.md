Bot de Telegram para la Alimentación de Mascotas

## Requisitos
Para el desarrollo de este proyecto se utilizó Python en su versión *3.11.1*.
 **Librerías utilizadas:**
- from telegram import Update
- from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
- import json, re, random, asyncio, time

## Resumen

1. **Interactivo y fácil de usar**: El bot debe ser fácil de usar e interactivo, respondiendo a las preguntas de los usuarios de manera oportuna y precisa.

2. **Información precisa y útil**: El bot proporcionará información precisa y útil sobre qué alimentos son seguros para las mascotas de los usuarios y cuáles podrían ser tóxicos o incluso mortales.

3. **Respuestas detalladas y bien investigadas**: Los usuarios podrán hacer preguntas específicas y recibirán respuestas detalladas y bien investigadas.

## Diseño de alto nivel

El bot se implementará utilizando Python y la API de Telegram Bot. La base de datos de información sobre la alimentación de mascotas se almacenará en un arhcivo de tipo JSON.

### Componentes principales

1. **Interfaz de usuario**: Interfaz de chat de Telegram para interactuar con los usuarios.

2. **Motor de chat**: Maneja la lógica de las conversaciones y genera respuestas a las preguntas de los usuarios.

3. **Base de datos de alimentación de mascotas**: Almacena la información sobre qué alimentos son seguros y cuáles son tóxicos para diferentes tipos de mascotas.

## Plan de implementación

1. **Fase 1 - Diseño de la base de datos**: Diseñar y construir la base de datos de alimentación de mascotas.

2. **Fase 2 - Implementación del motor de chat**: Desarrollar la lógica del bot para responder a las preguntas de los usuarios basándose en la información de la base de datos.

3. **Fase 3 - Integración con Telegram**: Integrar el bot con Telegram y realizar pruebas exhaustivas.

4. **Fase 4 - Lanzamiento y recopilación de feedback**: Lanzar el bot al público y recoger feedback para futuras mejoras.
