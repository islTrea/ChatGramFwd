from telethon import TelegramClient, events, sessions
import logging
from decouple import config
from iqoptionapi.stable_api import IQ_Option

import time as t
from datetime import datetime
import datetime as dt
###################
UserName = config("IQ_UserName")
UserPass = config("IQ_PWS")

percentUsed = config("PERCENTAGE")
Account_Type = config("ACCOUNT_TYPE")

Iq=IQ_Option(UserName, UserPass)
  
iqch1, iqch2=Iq.connect()
  	
if iqch1==True:
  print("IqOption Log In Successful.") 
else:
  print("IqOption Log In failed.")
#################
class vars:
	debug = False
	api_id = config("APP_ID", default=None, cast=int)
	api_hash = config("API_HASH", default=None)
	session_str = config("SESSION")
	
logging.basicConfig(level=logging.DEBUG if vars.debug else logging.WARNING)

FROM_ = config("FROM_CHANNEL")
to_chats = config("TO_CHANNEL")

from_chats = [int(i) for i in FROM_.split()]

app = TelegramClient(
  session=sessions.StringSession(vars.session_str),#if you have a session string, then you can use above version!
	#if you want a local sesion, then just a name would be fine here. (commented below)
	#session="mySession",
  api_id=vars.api_id,
  api_hash=vars.api_hash
).start()

@app.on(events.NewMessage(incoming=True, chats=from_chats))
async def new_message(event):
  print(event.text) #this is the text what is being received and we got is printed!
  #print(event.date) #this is the Date what is being received and we got is printed!
  
  #################################
  
  if Iq.check_connect()==False: 
    iqch1, iqch2=Iq.connect()
  	
  if iqch1==True:
      print("IqOption reconnect In Successful.") 
  else:   
      print("IqOption reconnect failed.")

  #Iq.change_balance("REAL")
  
  Iq.change_balance("PRACTICE")
  
  my_blc=Iq.get_balance()
  app.send_message(to_chats , "Balance: "+str(my_blc))
  print(f"Balance: {my_blc} ")
  
  
  #SET TRADE PARAMETERS 
  #Money=10 #AMOUNT PER OPTION
  ####################################################
  #new_message = "EUR/JPY CALL 5 MINT WAIT CONFRIM"
  new_message = event.text
  
  confirm = "WAIT CONFRIM"
  ## percentage of balance to trade
  percentOfBalance = int(percentUsed)
  Money = float("{:.2f}".format(my_blc * (percentOfBalance/100)))
  trade = ""
  expirations_mode = ""
  market = ""
  tradeReady = False
  tradeON = False
  	
  	
  if tradeReady == False and confirm in new_message:
    tradeReady = True
    for z in new_message.split():
      if z.isdigit():
        expirations_mode=int(z)
    #print(minutes)
    ##Direction
    if "CALL" in new_message:
      trade = "call"
    if "PUT" in new_message:
      trade = "put"
    ##Curreny pair
    if 'EUR/USD' in new_message:
      market = 'EURUSD'
    if 'EUR/GBP' in new_message:
      market = 'EURGBP'
    if 'GBP/JPY' in new_message:
      market = 'GBPJPY'
    if 'EUR/JPY' in new_message:
      market = 'EURJPY'
    if 'GBP/USD' in new_message:
      market = 'GBPUSD'
    if 'USD/JPY' in new_message:
      market = 'USDJPY'
    if 'AUD/CAD' in new_message:
      market = 'AUDCAD'
    if 'NZD/USD' in new_message:
      market = 'NZDUSD'
    if 'USD/RUB' in new_message:
      market = 'USDRUB'
    if 'AUD/USD' in new_message:
      market = 'AUDUSD'
    if 'USD/CAD' in new_message:
      market = 'USDCAD'
    if 'AUD/JPY' in new_message:
      market = 'AUDJPY'
    if 'GBP/CAD' in new_message:
      market = 'GBPCAD'
    if 'GBP/CHF' in new_message:
      market = 'GBPCHF'
    if 'GBP/AUD' in new_message:
      market = 'GBPAUD'
    if 'EUR/CAD' in new_message:
      market = 'EURCAD'
    if 'CHF/JPY' in new_message:
      market = 'CHFJPY'
    if 'CAD/CHF' in new_message:
      market = 'CADCHF'
    if 'EUR/AUD' in new_message:
      market = 'EURAUD'
  		
    #print(expirations_mode)
    #print(trade)
    #print(market)
  
  if tradeReady == True and "GO" in new_message:
    #trade using all the variable
    print("trade is active")
    #then clear variables
    tradeON = True
  
  ####################################################
  #Money = 10
  #market = "EURUSD" #TARGET INSTRUMENT
  #expirations_mode=1 #EXPIRATION TIME IN MINUTES
  #trade = "put"
  #tradeOn = False
  #LET'S DO SOMETHING 
  #print("IQ Bot started ...")

  while tradeON == True:	
    #CALL OPTION 
    if trade == "call":
    #CALL OPTION 
      app.send_message(to_chats,"Trade: "+trade + " Currency Pair: "+market+ " Expiry: "+str(expirations_mode)+" Min "+ " $ "+str(Money) )
      print("Green")
      check, id=Iq.buy (Money, market, "call", expirations_mode)
      if check:
        print("'CALL' Option Placed.") 
        print("Awaiting 'Call Option Result...") 
        app.send_message(to_chats , "Awaiting 'Call Option Result...")
        #FUNCTION TO GET OPTION RESULT
        if(Iq.check_win_v3(id) !=""):
          tradeON = False
          trade = ""
          minutes = ""
          market = ""
          app.send_message(to_chats , "Win/Loss: " + Iq.check_win_v3(id) + "New Balance: "+str(Iq.get_balance()) )
          print(Iq.check_win_v3(id)) 
      else:
        tradeON = False
        tradeReady == False
        app.send_message(to_chats , " 'Put' Option Failed.")
        print("Call Option Failed.") 
  	 		
    elif trade == "put":
  	#PUT OPTION 
      app.send_message(to_chats , "Trade: "+trade + " Currency Pair: "+market+ " Expiry: "+str(expirations_mode)+" Min "+ " $ "+str(Money) )
      print("Red") 
      check, id=Iq. buy (Money, market, "put", expirations_mode)
      if check:
        print("'PUT' Option Placed.") 
        print("Awaiting 'Put' Option Result...") 
        app.send_message(to_chats , "Awaiting 'Call Option Result...")
        #FUNCTION TO GET OPTION RESULT
        if(Iq.check_win_v3(id) !=""):
          tradeON = False
          trade = ""
          minutes = ""
          market = ""
          app.send_message(to_chats , "Win/Loss: " + Iq.check_win_v3(id)+ "New Balance: "+str(Iq.get_balance()) )
          print(Iq.check_win_v3(id))  
      else: 
        tradeON = False
        tradeReady == False
        app.send_message(to_chats , " 'Put' Option Failed.")
        print(" 'Put' Option Failed.")
  

  #################################
  #print(event.text) #this is the text what is being received and we got is printed!
  #print(event.date) #this is the Date what is being received and we got is printed!
if __name__ == "__main__":
  print("TGram Bot started!!")
  app.run_until_disconnected()
