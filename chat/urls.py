from django.urls import path
from .views import Room,NewRoom

app_name = 'chat'


urlpatterns = [
    path('room/<str:id>/',Room,name='room'),
    path('newroom/',NewRoom,name='newroom')
]