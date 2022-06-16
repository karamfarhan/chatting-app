
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from account.models import Account
from account.forms import RegistrationForm , AccountAuthenticationForm , AccountUpdateForm
from django.conf import settings
from django.shortcuts import render
from account.decorators import unauthenticated_user
from django.contrib.auth.decorators import login_required

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import account_activation_token
from django.urls import reverse

from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
import threading

from django.http import HttpResponseRedirect




class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


@unauthenticated_user
def register_view(request, *args, **kwargs):
	form = RegistrationForm()
	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = form.save()
			# email = form.cleaned_data.get('email').lower()
			# raw_password = form.cleaned_data.get('password1')
			# account = authenticate(email=email, password=raw_password)
			# if account:
			# SENDING AN VERFECATION EMAIL
			send_vervication_email(request,user)
			messages.add_message(request, messages.SUCCESS,'registered succesfully and activation sent.go and activate your account from your email.')
			return redirect('account:login')
		else:
			context['registration_form'] = form

	context['registration_form'] = form
	return render(request, 'account/registeration/register.html', context)



def send_vervication_email(request,user):
	current_site = get_current_site(request)
	subject = 'Activate your Account'
	message = render_to_string('account/registeration/account_activation_email.html', {
			'user': user,
			'domain': current_site.domain,
			'uid': urlsafe_base64_encode(force_bytes(user.pk)),
			'token': account_activation_token.make_token(user),
		})
	user.email_user(subject=subject, message=message)



def account_activate(request, uidb64, token):
	try:
		uid = force_str(urlsafe_base64_decode(uidb64))
		user = Account.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, user.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		messages.add_message(request, messages.SUCCESS,'Email verified, you can now login')
		return redirect('account:login')
	
	return render(request, 'account/registeration/activation_invalid.html')



def logout_view(request):
	logout(request)
	return redirect("home")


@unauthenticated_user
def login_view(request, *args, **kwargs):
	form = AccountAuthenticationForm()
	context = {}
	

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			
			account_exists = Account.objects.filter(email=email).exists()
			"""
			Thank you @harryghgim for helping me out. Error is resolved now basically, 
			there's a concept while using the authenticate() function. It returns None if user.is_active = False. 
			Make sure your is_active is True When you are going to use authenticate. It will only work for active users.
			"""
			if account_exists:
				user = authenticate(request,email=email,password=password)
				if user:
					if user.is_active:
						login(request, user)
						destination = get_redirect_if_exists(request)
						if destination:
							return redirect(destination)
						return redirect("home")
				else:
					messages.add_message(request, messages.ERROR,'The Account Is not Acitve, We sent an activation link to your email!. Or The Password Is Incorect.')
					return HttpResponseRedirect(request.path_info)
					
			
			else:
				messages.add_message(request, messages.ERROR,'Invalid credentials, Email or Password is Incorect')
				return HttpResponseRedirect(request.path_info)
		
	context['login_form'] = form

	return render(request, "account/login.html", context)


def get_redirect_if_exists(request):
	redirect = None
	if request.GET:
		if request.GET.get("next"):
			redirect = str(request.GET.get("next"))
	return redirect


@login_required(login_url='account:login')
def account_view_detail(request, *args, **kwargs):
	"""
	- Logic here is kind of tricky
		is_self (boolean)
			is_friend (boolean)
				-1: NO_REQUEST_SENT
				0: THEM_SENT_TO_YOU
				1: YOU_SENT_TO_THEM
	"""
	context = {}
	user_id = kwargs.get("user_id")
	try:
		account = Account.objects.get(pk=user_id)
	except:
		return HttpResponse(f"Something went wrong6666.")
	if account:
		context['id'] = account.id
		context['username'] = account.username
		context['email'] = account.email
		context['profile_image'] = account.profile_image.url
		context['hide_email'] = account.hide_email

		# Define state template variables
		is_self = True
		is_friend = False
		user = request.user
		if user.is_authenticated and user != account:
			is_self = False
		elif not user.is_authenticated:
			is_self = False
			
		# Set the template variables to the values
		context['is_self'] = is_self
		context['is_friend'] = is_friend
		context['BASE_URL'] = settings.BASE_URL
		return render(request, "account/account.html", context)



@login_required(login_url='account:login')
def edit_account_view(request, *args, **kwargs):


	user_id = kwargs.get("user_id")
	account = Account.objects.get(pk=user_id)
	if account.pk != request.user.pk:
		return HttpResponse("You cannot edit someone elses profile.")
	context = {}
	if request.POST:
		form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
		if form.is_valid():
			form.save()
			return redirect("account:account_view_detail", user_id=account.pk)
		else:
			form = AccountUpdateForm(request.POST, instance=request.user,
				initial={
					"id": account.pk,
					"email": account.email, 
					"username": account.username,
					"profile_image": account.profile_image,
					"hide_email": account.hide_email,
				}
			)
			context['form'] = form
	else:
		form = AccountUpdateForm(
			initial={
					"id": account.pk,
					"email": account.email, 
					"username": account.username,
					"profile_image": account.profile_image,
					"hide_email": account.hide_email,
				}
			)
		context['form'] = form
	context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
	return render(request, "account/edit_account.html", context)