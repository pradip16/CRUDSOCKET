from websocket import create_connection
import threading
ws = create_connection("ws://127.0.0.1:8000/api/")
# ws.send('{"method": "recentbuytrades"}')
# result =  ws.recv()
# print ("Received '%s'" % result)

def recevice():
  while True:
    result =  ws.recv()
    print ("Received '%s'" % result)


t1 = threading.Thread(target=recevice)
t1.start()

while True:
    msg = input("Enter Msg: ")
    ws.send(f"""{{"msg": "{msg}"}}""")


ws.close()