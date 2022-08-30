from telethon import TelegramClient, events, sessions
import logging
from decouple import config

import time
from iqoptionapi.stable_api import IQ_Option
from datetime import date

###################
UserName = config("IQ_UserName")
UserPass = config("IQ_PWS")

percentUsed = config("PERCENTAGE")
AccountType = config("ACCOUNT_TYPE")

Iq=IQ_Option(UserName, UserPass)
  
iqch1, iqch2=Iq.connect()
  	
if iqch1==True:
  print("IqOption Log In Successful!!") 
else:
  print("IqOption Log In failed!!")
  
##################
class vars:
  debug = False
  api_id = config("APP_ID", default=None, cast=int)
  api_hash = config("API_HASH", default=None)
  session_str = config("SESSION")
  

logging.basicConfig(level=logging.DEBUG if vars.debug else logging.WARNING)
FROM_ = config("FROM_CHANNEL")
to_chats = config("TO_CHANNEL")
app = TelegramClient(
  session='test2',#if249 you have a session string, then you can use above version!
	#if you want a local sesion, then just a name would be fine here. (commented below)
	#session="mySession",
  api_id=vars.api_id,
  api_hash=vars.api_hash
).start()

from_chats = [int(i) for i in FROM_.split()]

@app.on(events.NewMessage(incoming=True, chats=vars.from_chats))
async def new_message(event):
  print("Message: "+event.text) 
  today = date.today()
 
  Iq.change_balance(AccountType)

  my_blc=Iq.get_balance()
  try:
    await app.send_message(to_chats , "Message: "+event.text)  
  except Exception as e:
    print(e)
  
  ############################
  newmessage = str(event.text)

  #confirm = "WAIT CONFRIM"
  ## percentage of balance to trade
  percentOfBalance = float(0.1)
  Money = float("{:.2f}".format(my_blc * (percentOfBalance/100)))
  trade = ""
  expirations_mode = "5"
  market = "EUR/USD" 
  '''	
  if confirm in newmessage:
    try:
      await app.send_message(to_chats , "IqOption: Wait Confirm active")  
    except Exception as e:
      print(e)
    print("IqOption: Wait Confirm active")
    
    for z in newmessage.split():
      if z.isdigit():
        expirations_mode=int(z)
    #print(minutes)
    ##Direction
    if "call" in newmessage.lower():
      trade = "call"
      print("call detected")
    if "put" in newmessage.lower():
      trade = "put"
      print("put")
    pairList ={'EUR/USD':'EURUSD','EUR/GBP':'EURGBP','GBP/JPY':'GBPJPY'
               ,'EUR/JPY':'EURJPY','GBP/USD':'GBPUSD','USD/JPY':'USDJPY'
               ,'AUD/CAD':'AUDCAD','NZD/USD':'NZDUSD','USD/RUB':'USDRUB'
               ,'AUD/USD':'AUDUSD','USD/CAD':'USDCAD','AUD/JPY':'AUDJPY'
               ,'GBP/CAD':'GBPCAD','GBP/CHF':'GBPCHF','GBP/AUD':'GBPAUD'
               ,'EUR/CAD':'EURCAD','CHF/JPY':'CHFJPY','CAD/CHF':'CADCHF'
               ,'EUR/AUD':'EURAUD'
              }  
    for pair in pairList:
    	if pair in newmessage:
    		#print(pairList[pair])
  		  market = pairList[pair]
    
    try:
      await app.send_message(to_chats ,today+" -IqOption: Market Active: "+market+" Expiry: "+str(expirations_mode)+" Account Type: "+Account_Type+" Balance: "+str(my_blc))  
    except Exception as e:
      print(e)
    print("IqOption: Market Active: "+market+ " Expiry: "+str(expirations_mode))
  
    
  if "go" in newmessage.lower():
    try:
      await app.send_message(to_chats ,today+" -IqOption: GO is Active: ")  
    except Exception as e:
      print(e)
    print("IqOption: GO is Active: ")
	  '''
  if "i" in newmessage.lower() or "ok" in newmessage.lower():
    trade = "put" 
    
    print("I detected")
	
	
    #CALL OPTION 
    if trade == "call":
    #CALL OPTION 
      try:
        await app.send_message(to_chats,"IqOption: Trade: "+trade + " Currency Pair: "+market+ " Expiry: "+str(expirations_mode)+" Min "+ " $ "+str(Money) )  
      except Exception as e:
        print(e)
      
      print("Green")
      check, id=Iq.buy (float(Money), market, "call", int(expirations_mode))
      if check:
        print("'CALL' Option Placed.") 
        print("IqOption: Awaiting 'Call Option Result...") 
        try:
          await app.send_message(to_chats , "IqOption: Awaiting 'Call Option Result...")
        except Exception as e:
            print(e)
        #FUNCTION TO GET OPTION RESULT
        if(Iq.check_win_v3(id) !=""):
          trade = ""
          expirations_mode = ""
          market = ""
        if(Iq.check_win_v3(id) > 0):
          print("Win ✅")
          await app.send_message(to_chats , today+" - IqOption: Win ✅: " + str(float(Iq.check_win_v3(id))) + " IqOption: New Balance: "+str(Iq.get_balance()) )  
          print(float(Iq.check_win_v3(id))) 
        elif(Iq.check_win_v3(id) < 0):
          print("Loss ⛔️") 
          await app.send_message(to_chats , today+" -IqOption: Loss ⛔️: " + str(float(Iq.check_win_v3(id))) + " IqOption: New Balance: "+str(Iq.get_balance()) )  
          print(float(Iq.check_win_v3(id))) 
      else:  
        await app.send_message(to_chats , today+" -IqOption: 'Put' Option Failed.")
        print("IqOption: Call Option Failed.") 
  	 		
    elif trade == "put":
  	#PUT OPTION 
      try:
        await app.send_message(to_chats, today+" -IqOption: Trade: "+trade + " Currency Pair: "+market+ " Expiry: "+str(expirations_mode)+" Min "+ " $ "+str(Money) )  
      except Exception as e:
        print(e)
      print("Red") 
      check, id=Iq. buy (float(Money), market, "put", int(expirations_mode))
      if check:
        print("IqOption: 'PUT' Option Placed.") 
        print("IqOption: Awaiting 'Put' Option Result...") 
        await app.send_message(to_chats , "IqOption: Awaiting 'Call Option Result...")
        #FUNCTION TO GET OPTION RESULT
        if(Iq.check_win_v3(id) !=""):
          trade = ""
          expirations_mode = ""
          market = ""
         
        if(Iq.check_win_v3(id) > 0):
          print("Win ✅")
          await app.send_message(to_chats , today+" -IqOption: Win ✅: " + str(float(Iq.check_win_v3(id))) + " IqOption: New Balance: "+str(Iq.get_balance()) )  
          print(float(Iq.check_win_v3(id))) 
        elif(Iq.check_win_v3(id) < 0):
          print("Loss ⛔️")
          await app.send_message(to_chats , today+" -IqOption: Loss ⛔️: " + str(float(Iq.check_win_v3(id))) + " IqOption: New Balance: "+str(Iq.get_balance()) )  
          print(float(Iq.check_win_v3(id))) 
      else: 
        await app.send_message(to_chats ,today+" -IqOption: 'Put' Option Failed.")
        print("IqOption: 'Put' Option Failed.")

  #################################
  #print(event.text) #this is the text what is being received and we got is printed!
  #print(event.date) #this is the Date what is being received and we got is printed!
if __name__ == "__main__":
  print("TGram Bot started!!")
  app.run_until_disconnected()
