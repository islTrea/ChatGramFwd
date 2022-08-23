from telethon import TelegramClient, events, sessions
import logging


class vars:
	debug = False
	api_id = 10802903
	api_hash = '3c274f7b6627d3e8bfe5c986ce20baca'
	session_str = '1BJWap1wBu6VRIUHwqQQvJvT5uEzlOw4c3vO2cBJKFb7i27XlHsNQARhpsZVsRe2DW4XXOAAH1R0SWWfSFvm9TzennLz6cRuFiDtegdKvMYSPHOpD_Vbq89YPiX-B3C6rsF3S3QApNLUz4tBptixdV1scCYUOIKkIC4vaD1xkGEP6AOs4GNXzyirdgjHYyDk_HZH_PQ8B_opOK8vpn7ZF8kVQLPNaCOl5Th8Y-F7mxOLvSu66nI9f2NKiX8OZBHTsfMMY2J21z_8IZWOplwpsdxhJm-0Xx0nLyM3y22RYMpBx7bBCFTLLUXdk8h2rZL7YBUCfhuTB2lU1BOeFx56K__TQkHn0fOM='
	from_chats = ["fxrashel",5094712949]
  
logging.basicConfig(level=logging.DEBUG if vars.debug else logging.WARNING)

app = TelegramClient(
	session=sessions.StringSession(vars.session_str),#if you have a session string, then you can use above version!
	#if you want a local sesion, then just a name would be fine here. (commented below)
	#session="mySession",
	api_id=vars.api_id,
	api_hash=vars.api_hash
).start()

@app.on(events.NewMessage(incoming=True, chats=vars.from_chats))
async def new_message(event):
  print(event.text) #this is the text what is being received and we got is printed!
  #print(event.date) #this is the Date what is being received and we got is printed!
  try:
      await app.send_message(-1001553122017,event.message)
  except Exception as e:
            print(e)

if __name__ == "__main__":
	print("TGram Bot started!!")
	app.run_until_disconnected()
