from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager , PermissionsMixin
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from django.utils.translation import gettext_lazy as _
from PIL import Image

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid

from django.core.mail import EmailMessage
from django.core.mail import send_mail
import threading

class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None, **other_fields):
		if not email:
			raise ValueError(_('Users must have an email address'))
		if not username:
			raise ValueError(_('Users must have a username'))

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password, **other_fields):


		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
			**other_fields,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.is_active = True
		user.save(using=self._db)
		return user


def get_profile_image_filepath(self, filename):
	return f"profile_images/{str(self.pk)}/profile_image.png"

def get_default_profile_image():
	return "images/default/default.jpg"



class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()



class Account(AbstractBaseUser, PermissionsMixin):
	id                      = models.UUIDField(primary_key=True,default=uuid.uuid4)
	email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
	username 				= models.CharField(max_length=30, unique=True)
	first_name              = models.CharField(max_length=150, blank=True)
	last_name  				= models.CharField(max_length=30, blank=True)
	about                   = models.TextField(max_length=500,blank=True)
	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)

	is_admin				= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=False)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)
	profile_image			= models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image)
	hide_email				= models.BooleanField(default=True)

	objects = MyAccountManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	class Meta:
		verbose_name = "Accounts"
		verbose_name_plural = "Accounts"

	

	def __str__(self):
		return self.username


	def save(self, *args, **kwargs):
		super(Account, self).save(*args, **kwargs)

		img = Image.open(self.profile_image.path)

		if img.height > 500 or img.width > 500:
			output_size = (500, 500)
			img.thumbnail(output_size)
			img.save(self.profile_image.path)



	def email_user(self, subject, message):
		email = EmailMessage(
			subject=subject, 
			body=message,
			from_email=settings.DEFAULT_FROM_EMAIL,
			to=[self.email])

		EmailThread(email).start()

	def get_profile_image_filename(self):
		return str(self.profile_image)[str(self.profile_image).index(f"profile_images/{str(self.pk)}/"):]

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)