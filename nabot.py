#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import time, datetime, os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    archivo = open('help', 'r')
    output = archivo.readlines()
    out =''
    for i in output:
        out +=i
    update.message.reply_text(out)
    archivo.close()

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def compra(update, context):
    try:
        fecha()
        archivo = open('compra', 'r')
        precios = []
        usuarios = []
        user = update.message.from_user.name
        print(user)
        new_price = int(context.args[0])
        n = 0
        entrada = archivo.readlines()
        size = int(entrada[0])
        output = ''
        if (size > 0):
            while (n < size):
                precios.append(int(entrada[n+1]))
                usuarios.append(entrada[size+n+1])
                n+=1
            archivo.close()

            if user+'\n' in usuarios:
                precios[usuarios.index(user+'\n')] = new_price
            else:
                precios.append(new_price)
                usuarios.append(user+'\n')
                size+=1
            
            ordenar_compra(precios, usuarios)
        else:
            precios.append(new_price)
            usuarios.append(user+'\n')
            size+=1

        output += str(size)+'\n'
        for i in range(len(precios)):
            output+=str(precios[i])+'\n'
        for i in range(len(usuarios)):
            output+=usuarios[i]


        archivo = open('compra', 'w')
        archivo.write(output)
        archivo.close()
        
        update.message.reply_text("Tu precio se subió correctamente.")

    except(ValueError):
        update.message.reply_text("Algo ha ido mal.Revisa que has introducido un numero sin decimales y otros caracteres extraños.")


def venta(update, context):
    try:
        fecha()
        archivo = open('venta', 'r')
        precios = []
        usuarios = []
        user = update.message.from_user.name
        print(user)
        new_price = int(context.args[0])
        n = 0
        entrada = archivo.readlines()
        size = int(entrada[0])
        output = ''
        if (size > 0):
            while (n < size):
                precios.append(int(entrada[n+1]))
                usuarios.append(entrada[size+n+1])
                n+=1
            archivo.close()

            if user+'\n' in usuarios:
                precios[usuarios.index(user+'\n')] = new_price
            else:
                precios.append(new_price)
                usuarios.append(user+'\n')
                size+=1
            
            ordenar_venta(precios, usuarios)
        else:
            precios.append(new_price)
            usuarios.append(user+'\n')
            size+=1

        output += str(size)+'\n'
        for i in range(len(precios)):
            output+=str(precios[i])+'\n'
        for i in range(len(usuarios)):
            output+=usuarios[i]


        archivo = open('venta', 'w')
        archivo.write(output)
        archivo.close()
        
        update.message.reply_text("Tu precio se subió correctamente.")
    except(ValueError):
        update.message.reply_text("Algo ha ido mal.Revisa que has introducido un numero sin decimales y otros caracteres extraños.")

def precios(update, context):
    try:
        fecha()
        modo = 'venta'
        if (datetime.datetime.now().weekday() == 6):
            modo = 'compra'
        archivo = open(modo, 'r')
        precios = []
        usuarios = []
        n = 0
        entrada = archivo.readlines()
        size = int(entrada[0])
        output = 'Los precios de '+modo+' son:\n\n'
        if (size > 0):
            while (n < size):
                precios.append(int(entrada[n+1]))
                usuarios.append(entrada[size+n+1])
                n+=1
            archivo.close()

            for i in range(size):
                output+=entrada[1+i+size]+str(int(entrada[1+i]))+' bayas\n\n'

            update.message.from_user.send_message(output)

        else:
            update.message.reply_text("No hay precios subidos actualmente. Sube el tuyo con /venta [precio].")
        
    except(ValueError):
        update.message.reply_text("No puedo mandarte mensajes. Para ello hablame por privado y usa el comando /start")

def ordenar_venta(v, user, *arg):
    for i in range(len(v)-1):
        for j in range(len(v)-1):
            if (v[j] < v[j+1]):
                temp = v[j+1]
                v[j+1] = v[j]
                v[j] = temp
                
                temp = user[j+1]
                user[j+1] = user[j]
                user[j] = temp

def ordenar_compra(v, user, *arg):
    for i in range(len(v)-1):
        for j in range(len(v)-1):
            if (v[j] > v[j+1]):
                temp = v[j+1]
                v[j+1] = v[j]
                v[j] = temp
                
                temp = user[j+1]
                user[j+1] = user[j]
                user[j] = temp

def fecha():
    ahora = time.time()
    archivo = open('date_manager', 'r')
    entrada = archivo.readlines()
    archivo.close()
    
    if (ahora-float(entrada[0]) > 86400):
        delete()
        archivo = open('date_manager', 'w')
        archivo.write(str(ahora)+'\n'+str(datetime.datetime.now().hour))
        archivo.close()
    elif (datetime.datetime.now().hour < int(entrada[1])):
        delete()
        archivo = open('date_manager', 'w')
        archivo.write(str(ahora)+'\n'+str(datetime.datetime.now().hour))
        archivo.close()
    elif (datetime.datetime.now().hour < 12 and int(entrada[1]) >= 12):
        delete()
        archivo = open('date_manager', 'w')
        archivo.write(str(ahora)+'\n'+str(datetime.datetime.now().hour))
        archivo.close()
    elif (datetime.datetime.now().hour >= 12 and int(entrada[1]) < 12):
        delete()
        archivo = open('date_manager', 'w')
        archivo.write(str(ahora)+'\n'+str(datetime.datetime.now().hour))
        archivo.close()


def delete():
    archivo = open('venta', 'w')
    archivo.write("0")
    archivo.close()
    archivo = open('compra', 'w')
    archivo.write("0")
    archivo.close()


def restart(update,context):
    if (update.message.from_user.username == 'PavroKatsu'):
        delete()
        update.message.from_user.send_message("Archivos restablecidos.")
    else:
        update.message.reply_text("Permiso denegado.")


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(os.environ['TELEGRAM_TOKEN'], use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("venta", venta))
    dp.add_handler(CommandHandler("compra", compra))
    dp.add_handler(CommandHandler("precios", precios))
    dp.add_handler(CommandHandler("restart", restart))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()