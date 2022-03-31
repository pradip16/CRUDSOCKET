"""
ASGI config for CRUDSOCKET project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CRUDSOCKET.settings')

# application = get_asgi_application()



from CRUDSOCKET.Consumer import Consumer
import os
import django
from django.core.asgi import get_asgi_application
from django.conf.urls import url
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter


# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BMS_host.settings')
# django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            # url(r'^api/(?P<user_id>\w+)/$', Consumer.as_asgi()),
             url(r'^api/', Consumer.as_asgi()),
        ])
    ),
})
