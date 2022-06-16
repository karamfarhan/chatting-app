from .models import Account
from chat.models import Contact
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save,sender=Account)
def create_contact(sender,instance,created,**kwargs):
    if created:
        Contact.objects.create(user=instance)

@receiver(post_save,sender=Account)
def save_contact(sender,instance,**kwargs):
    instance.contact.save()