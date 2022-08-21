#    Copyright (c) 2021 Ayush
#    
#    This program is free software: you can redistribute it and/or modify  
#    it under the terms of the GNU General Public License as published by  
#    the Free Software Foundation, version 3.
# 
#    This program is distributed in the hope that it will be useful, but 
#    WITHOUT ANY WARRANTY; without even the implied warranty of 
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
#    General Public License for more details.
# 
#    License can be found in < https://github.com/Ayush7445/telegram-auto_forwarder/blob/main/License > .

from telethon import TelegramClient, events
from decouple import config
import logging
from telethon.sessions import StringSession

from iqoptionapi.stable_api import IQ_Option 
import time

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

print("Starting...")

# Basics
APP_ID = config("APP_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
SESSION = config("SESSION")
FROM_ = config("FROM_CHANNEL")

USER = ("IQ_UserNmae")
     
PWS = ("IQ_PWS")
      
FROM = [int(i) for i in FROM_.split()]

try:
    BotzHubUser = TelegramClient(StringSession(SESSION), APP_ID, API_HASH)
    BotzHubUser.start()
except Exception as ap:
    print(f"ERROR - {ap}")
    exit(1)

    
    
ACTIVES="EURUSD"
Money=1
order = "put"
receivedHTM = "GO"

@BotzHubUser.on(events.NewMessage(incoming=True, chats=FROM))
async def sender_bH(event):
    while True:
        if receivedHTM in (event.message).lower():
	    #if receivedHTM == "GO":
		    if order == "put":
			    #ACTION_call="put"
			
        	    #order_sell,id_put=I_want_money.buy(Money,ACTIVES,ACTION_call,expirations_mode)
			    order_put,id_put = API.buy_digital_spot("EURUSD",1, "put",1) 
			    print("Order Put")
			    if order_put == True: 
				    while True:
					    check_put, win_put = API.check_win_digital_v2(id_put) 
					    if check_put == True:
						    break
				    if win_put > 0:
					    print("Put win") 
				    else:
					    print("Put LOSE")
				
		    if order == "call":
			    #ACTION_call="call"
        	    #order_buy,id_call=I_want_money.buy(Money,ACTIVES,ACTION_call,expirations_mode)
			    order_call,id_call = API.call_digital_spot("EURUSD",1, "call",1) 
			    print("Order Put")
			    if order_call == True: 
				    while True:
					    check_call, win_call = API.check_win_digital_v2(id_call) 
					    if check_call == True:
						    break
				    if win_call > 0:
					    print("Call win") 
				    else:
					    print("Call LOSE")

print("Bot has started.")
BotzHubUser.run_until_disconnected()
