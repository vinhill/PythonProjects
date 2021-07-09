import os
import sys
import time
from datetime import datetime
import asyncio
import telepot
from telepot import glance
from telepot.loop import MessageLoop
from functools import partial
from random import choice
from jupyter_client.multikernelmanager import MultiKernelManager

import botconstants

admins = set()
users = set()
userauthtoken = "userauth"
mkm = MultiKernelManager()

bot = telepot.Bot(botconstants.TOKEN)

def execute(user_id, command):
    global mkm
    """
    Executes command for custom user
    If connections was closed  returns None,
    else returns command result
    """
    if not all((user_id, command)):
        return None

    client = mkm.get_kernel(user_id).client()
    client.execute(command)

    output = ''
    while True:
        msg = client.get_iopub_msg()

        if msg['msg_type'] == 'execute_result':
            output += msg['content']['data']['text/plain']
        elif msg['msg_type'] == 'stream':
            output += msg['content']['text']
        elif msg['msg_type'] == 'error':
            output += '\n'.join(msg['content']['traceback'])
        elif msg.get('content', {}).get('execution_state') == 'idle':
            break

    return output

def on_chat_message(msg):
    global admins, users, userauthtoken
    chat_id = msg["chat"]["id"]
    print(msg)
    if msg['text'] == '/start':
        bot.sendMessage(chat_id, botconstants.START)
    if msg['text'] == '/about':
        bot.sendMessage(chat_id, botconstants.ABOUT)
    elif msg['text'] == '/ping':
        bot.sendMessage(chat_id, 'pong')
    elif msg['text'] == '/help':
        bot.sendMessage(chat_id, botconstants.HELP)
    elif msg['text'].startswith('/authorize'):
        if msg['text'].endswith(botconstants.ADMINTOKEN):
            admins.add(chat_id)
            bot.sendMessage(chat_id, "Ur my admin <3")
        elif msg['text'].endswith(userauthtoken):
            users.add(chat_id)
            mkm.start_kernel(kernel_id = chat_id)
            bot.sendMessage(chat_id, "Ur my user <3")
        else:
            bot.sendMessage(chat_id, "I don't know you")
    elif msg['text'].startswith("/decide"):
        choices = msg['text'][7:].split(" or ")
        if len(choices) > 0:
            bot.sendMessage(chat_id, choice(choices))
        
    elif msg['text'] == '/restart':
        if chat_id in users:
            mkm.get_kernel(chat_id).restart_kernel()
            bot.sendMessage(chat_id, "Restarted")
        else:
            bot.sendMessage(chat_id, "Nothing to reset")
    elif msg['text'] == '/reset':
        if chat_id in admins:
            mkm.shutdown_all()
            admins = set()
            users = set()
            bot.sendMessage(chat_id, "Reset done")
        else:
            bot.sendMessage(chat_id, botconstants.NOADMIN)
    elif msg['text'].startswith("/usertoken"):
        if chat_id in admins:
            userauthtoken = msg['text'][11:]
        else:
            bot.sendMessage(chat_id, botconstants.NOADMIN)
    elif chat_id in users:
        if r := execute(chat_id, msg['text']):
            bot.sendMessage(chat_id, r)
    else:
        bot.sendMessage(chat_id, "Not authorized, feels bad man.")

if __name__ == "__main__":
    logfile = open("log.txt", "a")
    offset = 0
    print("VinniPy listening")
    
    while True:
        updates = bot.getUpdates(offset=offset)
        for update in updates:
            try:
                on_chat_message(update["message"])
            except:
                print("Error while trying to get / handle message")
            dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            logfile.write(f"{dt_string} - {update['message']['text']}\n")
            logfile.flush()
            
            offset = update["update_id"] + 1
        print(".")
        time.sleep(1)
    
    logfile.close()
    #TODO linux fails when executing something. Probably as mkm will try to create a file which the script has no permission for in its directory