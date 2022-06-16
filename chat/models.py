from django.forms import ValidationError
from account.models import Account
from django.db.models import Q
from django.db import models



class Contact(models.Model):
    user = models.OneToOneField(Account,on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', blank=True)
    blocks = models.ManyToManyField('self',blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class ChatRoom(models.Model):
    auther = models.ForeignKey(Contact,related_name='auther',on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact,related_name='contact',on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    
    class Meta:
       unique_together = ('auther', 'contact',)

    def save(self, *args, symmetric=True, **kwargs):
        if_ex = ChatRoom.objects.filter(auther=self.contact,contact=self.auther).exists()
        if if_ex:
            raise TypeError('bidiractinal error')
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)



class Message(models.Model):
    contact = models.ForeignKey(Contact,on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom,related_name="message",on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created',]
    def __str__(self) :
        return self.text

    



