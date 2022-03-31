import json
import logging
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from CRUD import operation


connected_user = []
i = "1"
class Consumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        global i
        self.user_id = i
        self.user_group = 'live_user_' + str(self.user_id)

        print(self.user_id, self.user_group)
        
        await self.channel_layer.group_add(
            self.user_group,
            self.channel_name
        )

        await self.accept()
        if self.user_group not in connected_user:
            connected_user.append({"user_id" : self.user_id,"user_group" : self.user_group,})
            logging.info("Connected Users Are : " + str(connected_user))
            i = int(self.user_id) + 1
        
        # await self.channel_layer.group_send(self.user_group, {
        #     'type': 'site_config',
        #     'response': str(self.user_id) +" - "+ str(self.user_group),
        # })

    async def disconnect(self, close_code):
        logging.info('User Disconnecting... Closing Code ' + str(close_code))
        self.channel_layer.group_discard("wss", self.channel_name)
        for user in connected_user:
            if self.user_group in user['user_group']:
                connected_user.remove(user)
                logging.info("Disconnectin User : " + self.user_group)            
                logging.info("Now Connected Users Are : " + str(connected_user))

    async def receive(self, text_data):
        """
        Receive message from WebSocket.
        Get the event and send the appropriate event
        """
        # print(json.loads(text_data),"------------------")
        try:

            response = json.loads(text_data)
            operation.opr(response)
            '''
            # oprs.check_opr(response)
            # print("==-==-=-=-=-=-==Resopons-==-=-=-=-=-=-===")
            # print(response)
            
            ##this for sending data on reposnse
            # await self.channel_layer.group_send(self.user_group, {
            #     'type': 'site_config',
            #     'response': str(self.user_id) +" - "+ str(self.user_group),
            # })

            ##This is sending to all connetect user
            # for user in connected_user:
            #     await self.channel_layer.group_send(user['user_group'], {
            #         'type': 'site_config',
            #         'response': str(self.user_id) +" - "+ str(self.user_group) +" - "+str(response),
            #     })
            '''
        except Exception as e:
            logging.info(f"Error: {e}")

    async def send_message(self, res):
        """ Receive message from room group """
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "payload": res,
        }))

    async def site_config(self, res):
        """ Receive message from room group """
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "status_code": 200,
            "payload": res,
        }))



## --- this use for when needed to send data from another file then used.

# from BMS_host import bms_consumer
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
# try:
#     logging.info(f"GetAllSTatus...")
#     channel_layer = get_channel_layer()
#     for user in bms_consumer.connected_user:
#         async_to_sync(channel_layer.group_send)(user['user_group'], {
#                     'type': 'site_config',
#                     'response': "hello word",
#                 })
# except Exception as e:
#     logging.info(f"GetAllSTatus: {e}")