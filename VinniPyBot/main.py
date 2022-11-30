import os
import time
import asyncio
from telepot import glance
from telepot.loop import MessageLoop
from telepot.aio import Bot
from functools import partial
from random import choice
from jupyter_client.multikernelmanager import MultiKernelManager

import botconstants
from mysecrets import TOKEN, ADMINTOKEN

class PythonBot(Bot):
    def __init__(self, *args, **kwargs):
        super(PythonBot, self).__init__(*args, **kwargs)
        self.admins = set()
        self.users = set()
        self.userauthtoken = "defaultcomplexandlongrandomusertoken"
        self.mkm = MultiKernelManager()

    def execute(self, user_id, command):
        """
        Executes command for custom user
        If connections was closed  returns None,
        else returns command result
        """
        if not all((user_id, command)):
            return None

        client = self.mkm.get_kernel(user_id).client()
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

    async def on_chat_message(self, msg):
        content_type, chat_type, chat_id = glance(msg)
        print('Chat Message:', content_type, chat_type, chat_id, msg)
        if msg['text'] == '/start':
            await self.sendMessage(chat_id, botconstants.START)
        if msg['text'] == '/about':
            await self.sendMessage(chat_id, botconstants.ABOUT)
        elif msg['text'] == '/ping':
            await self.sendMessage(chat_id, 'pong')
        elif msg['text'] == '/help':
            await self.sendMessage(chat_id, botconstants.HELP)
        elif msg['text'].startswith('/authorize'):
            if msg['text'].endswith(ADMINTOKEN):
                self.admins.add(chat_id)
                self.mkm.start_kernel(kernel_id = chat_id)
                await self.sendMessage(chat_id, "Ur my admin <3")
            elif msg['text'].endswith(self.userauthtoken):
                self.users.add(chat_id)
                self.mkm.start_kernel(kernel_id = chat_id)
                await self.sendMessage(chat_id, "Ur my user <3")
            else:
                await self.sendMessage(chat_id, "I don't know you")
        elif msg['text'].startswith("/decide"):
            await self.sendMessage(chat_id, choice(msg['text'][7:].split(" or ")))
        
        # Authorized parts
        elif msg['text'] == '/restart':
            if chat_id in self.users:
                self.mkm.get_kernel(chat_id).restart_kernel()
                await self.sendMessage(chat_id, "Restarted")
            else:
                await self.sendMessage(chat_id, "Nothing to reset")
        elif msg['text'] == '/reset':
            if chat_id in self.admins:
                self.mkm.shutdown_all()
                self.admins = set()
                self.users = set()
                await self.sendMessage(chat_id, "Reset done")
            else:
                await self.sendMessage(chat_id, botconstants.NOADMIN)
        elif msg['text'].startswith("/usertoken"):
            if chat_id in self.admins:
                self.userauthtoken = msg['text'][11:]
            else:
                await self.sendMessage(chat_id, botconstants.NOADMIN)
        elif chat_id in self.users or chat_id in self.admins:
            if r := self.execute(chat_id, msg['text']):
                await self.sendMessage(chat_id, r)
        else:
            await self.sendMessage(chat_id, "Not authorized, feels bad man.")

if __name__ == "__main__":
    bot = PythonBot(TOKEN)
    
    loop = asyncio.get_event_loop()

    loop.create_task(bot.message_loop())
    print('Listening ...')

    loop.run_forever()