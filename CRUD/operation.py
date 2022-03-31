import logging
import threading

from CRUDSOCKET import Consumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import CRUD_OPR
# from asgiref.sync import sync_to_async

def Response(res):
    print(res)
    try:
        channel_layer = get_channel_layer()
        for user in Consumer.connected_user:
            async_to_sync(channel_layer.group_send)(user['user_group'], {
                        'type': 'site_config',
                        'response': res,
                    })
    except Exception as e:
        logging.error(f"Error: {e}")


def opr(response):
    # logging.info(f"Response: {str(response)}")
    if "connection" in response:
        print("response....connection")
        threading.Thread(target=send_data,args=(response,)).start()

    elif "delete" in response['action']:
        logging.info(f"Response: {str(response)}")
        threading.Thread(target=deletedata,args=(response,)).start()

    elif "insert" in response['action']:
        threading.Thread(target=crud,args=(response,)).start()
    elif "update" in response['action']:
        # logging.info(f"Response: {str(response)}")
        threading.Thread(target=updatedata,args=(response,)).start()
        # threading.Thread(target=crud,args=(response,)).start()
  
def deletedata(response):
    CRUD_OPR.objects.get(pk=response['id']).delete()
    data = CRUD_OPR.objects.all()
    lst = []
    for i in data:
        d1 = {
            "id":i.pk,
            "name" : i.Name,
            "email" : i.Email,
            "password":i.Password
        }
        lst.append(d1)
    threading.Thread(target=Response,args=(lst,)).start()

def crud(response):
    name = response['name']
    email = response['email']
    password = response['password']
    add_datas = CRUD_OPR(Name=name,Email=email,Password=password)
    add_datas.save()
    data = CRUD_OPR.objects.all()
    lst = []
    for i in data:
        d1 = {
            "id":i.pk,
            "name" : i.Name,
            "email" : i.Email,
            "password":i.Password
        }
        lst.append(d1)
    threading.Thread(target=Response,args=(lst,)).start()

def send_data(response):
    data = CRUD_OPR.objects.all()
    lst = []
    for i in data:
        d1 = {
            "id":i.pk,
            "name" : i.Name,
            "email" : i.Email,
            "password":i.Password
        }
        lst.append(d1)
    threading.Thread(target=Response,args=(lst,)).start()


def updatedata(response):
    update_data = CRUD_OPR.objects.get(pk=response['id'])
    name = response['name']
    email = response['email']
    password = response['password']
    update_data.Name = name
    update_data.Email = email
    update_data.Password=password
    update_data.save()

    data = CRUD_OPR.objects.all()
    lst = []
    for i in data:
        d1 = {
            "id":i.pk,
            "name" : i.Name,
            "email" : i.Email,
            "password":i.Password
        }
        lst.append(d1)
    threading.Thread(target=Response,args=(lst,)).start()
# def call():
#     data = CRUD_OPR.objects.all()
#     lst = []
#     for i in data:
#         d1 = {
#             "name" : i.Name,
#             "email" : i.Email,
#             "password":i.Password
#         }
#         lst.append(d1)
#     print(lst,data)
# call()