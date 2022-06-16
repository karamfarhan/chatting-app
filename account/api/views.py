from decimal import Context
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status
from rest_framework.response import Response
from account.models import Account
from .serializers import  RegisterationSerilizers, AccountProfileSerilizers, ChangePasswordSerializer, UpdateAccountProfileSerilizers
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate
from rest_framework.generics import UpdateAPIView



@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def getRouts(request):
    routes = [
        'GET   /api                   INFORMATION ABOUT THE AVILABLE ROUTE',
        'GET   /api/account/          RETURN THE DETIAL FOR THE ACCOUNT',
        'GET   /api/check_email/      CHECK IF THE EMAIL EXISTS IN THE DATA',

        'POST  /api/register/         REGISTERATION POINT',
        'POST  /api/login/            LOGIN POINT',

        'PUT   /api/account/edit/     UPDATE YOUR ACCOUNT DETIAL',
        'PUT   /api/change_password/  CHANGE THE ACCOUNT PASSWORD',
    ]
    return Response(routes)


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def registerUser(request):
    if request.method == 'POST':
        data = {}
        email = request.data.get('email', '0')
        if validate_email(email) != None:
            data['error_message'] = 'That email is already in use.'
            data['response'] = 'Error'
            return Response(data)

        username = request.data.get('username', '0')
        if validate_username(username) != None:
            data['error_message'] = 'That username is already in use.'
            data['response'] = 'Error'
            return Response(data)

        serializer = RegisterationSerilizers(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.is_active = True
            user.save()
            data['response'] = 'successfully registered new user.'
            data['email'] = user.email
            data['username'] = user.username
            data['pk'] = user.pk
            token = Token.objects.get(user=user).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)


def validate_email(email):
    account = None
    try:
        account = Account.objects.get(email=email)
    except Account.DoesNotExist:
        return None
    if account != None:
        return email


def validate_username(username):
    account = None
    try:
        account = Account.objects.get(username=username)
    except Account.DoesNotExist:
        return None
    if account != None:
        return username
###############################


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def loginUser(request):
    if request.method == 'POST':
        context = {}
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            context['response'] = "Successfully authenticated."
            context['pk'] = user.pk
            context['email'] = user.email
            context['token'] = token.key
        else:
            context['response'] = "Error"
            context['error_message'] = "Invalid credentials"
        return Response(context)

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


@api_view(['GET', ])
def profileUser(request):
    try:
        user = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = AccountProfileSerilizers(user)
        return Response(serializer.data)


@api_view(['PUT', ])
def updateprofileUser(request):
    try:
        user = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "PUT":
        serializer = UpdateAccountProfileSerilizers(user, data=request.data, partial=True)
        context = {}
        if serializer.is_valid():
            serializer.save()
            context["response"] = "Successfully updated"
            context['pk'] = user.pk
            context['email'] = user.email
            context['username'] = user.username
            context['hide_email'] = user.hide_email
            image_url = str(request.build_absolute_uri(user.profile_image.url))
            if "?" in image_url:
                image_url = image_url[:image_url.rfind("?")]
            context['profile_image'] = image_url
            return Response(context)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# http://127.0.0.1:8000/api/check_email/?email=www.karam777krm@gmail.com
@api_view(['GET', ])
@permission_classes([])
@authentication_classes([])
def does_account_exist_view(request):

	if request.method == 'GET':
		email = request.GET['email'].lower()
		data = {}
		try:
			account = Account.objects.get(email=email)
			data['response'] = email
		except Account.DoesNotExist:
			data['response'] = "Account does not exist"
		return Response(data)



class ChangePasswordView(UpdateAPIView):

    serializer_class = ChangePasswordSerializer
    model = Account
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            # confirm the new passwords match
            new_password = serializer.data.get("new_password")
            confirm_new_password = serializer.data.get("confirm_new_password")
            if new_password != confirm_new_password:
                return Response({"new_password": ["New passwords must match"]}, status=status.HTTP_400_BAD_REQUEST)

            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"response": "successfully changed password"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


