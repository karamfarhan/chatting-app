from django.shortcuts import redirect, render
from .models import Contact,ChatRoom,Message
from django.db.models import Max,Min
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.postgres.aggregates import ArrayAgg
from django.contrib import messages
from django.http import HttpResponseRedirect

@login_required(login_url='account:login')
def home(request):
    context = {}
    user = request.user

    try:
        rooms = ChatRoom.objects.filter(Q(contact__user=user)|Q(auther__user=user)).annotate(last_msg=Max("message__text")).annotate(last_date=Max("message__created"))
        room =rooms[0]
        messages = room.message.all()
    except:
        rooms =None
        room=None
        messages=None
    
    context['rooms'] = rooms
    context['room_act'] = room
    context['messages'] = messages
    return render(request,"chat/chat.html",context=context)


def Room(request,id):
    context={}
    user = request.user


    room = ChatRoom.objects.get(id=id)
    messages = room.message.all()
    rooms = ChatRoom.objects.filter(Q(contact__user=user)|Q(auther__user=user)).annotate(last_msg=Max("message__text")).annotate(last_date=Max("message__created"))
        
    context['rooms'] = rooms
    context['room_act'] = room
    context['messages'] = messages
    return render(request,"chat/chat.html",context=context)

def NewRoom(request):
    context={}
    user = request.user
    user_contact = Contact.objects.get(user=user)

    if request.POST:
        user_with = request.POST.get("username")
        try:
            contact = Contact.objects.get(user__username=user_with)
            if_frend_ex = ChatRoom.objects.filter(Q(auther=user_contact,contact=contact)|Q(auther=contact,contact=user_contact)).exists()
            if if_frend_ex:
                new_room = ChatRoom.objects.filter(Q(auther=user_contact,contact=contact)|Q(auther=contact,contact=user_contact))[0]
            else:
                new_room = ChatRoom.objects.create(auther=user_contact,contact=contact)
            return redirect('chat:room',id=new_room.id)
        except:
            messages.add_message(request, messages.ERROR,'There is Noe user with this username ')
            return HttpResponseRedirect(request.path_info)

    return render(request,'chat/newchat.html')