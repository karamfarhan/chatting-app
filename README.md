# chatting-app!
> How to run the app on your localhost

1 - download the zip file and unpack it

OPEN TERMINAL :

2 - create venv
```
python -m venv venv_name
```
3 - activate your venv :
   windows ```venv_name\scripts\activate.bat```
   linux,mac ```source venv_name/bin/activate```

> Now you need to run Redis server
> if you run the redis server localy 
```
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}
```
> if the redis server is external<br/>
Change the ```"hosts"``` to the url of your redis server

> Or you can run the app in development  wihout need to user redis puting this code
```
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}
```


4 - install the requirements file ```pip install -r requirements.txt```.<br />
5 - run the command to make migrations ```python manage.py makemigrations```.<br />
6 - run the command to make the tables ```python manage.py migrate```.<br />
7 - make superuser and give it username and password by running ```python manage.py createsuperuser```.<br />
9 - run the project by running ```python manage.py runserver```.<br />
10 - open your browser and go to the link (localhost:8000).<br />

> Do not forget to put your environment variables in the settings like  <br />
SECRET_KEY <br/>
```
SECRET_KEY = env("SECRET_KEY", default="unsafe-secret-key")
```
EMAIL CONFIGRATIONS<br/>
```
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
DEFAULT_FROM_EMAIL= env('DEFAULT_FROM_EMAIL')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```
AND POSTGRESS CONFIG (IF YOU DECIDED TO USER IT)
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASS'),
        'HOST': env('DATABASE_HOST'),
        'PORT':5432,
    }
}
```

# DOCUMENTATION
## Chatting app
> This is an chatting app built using (Django-channels) in the backend and (HTML-BOOTSTRAB-CSS-JAVASCRIPT) in the front end
## Features

 - Full authentication system 
 - in time chatting 
 - nice theem
 - redis - websocket


## Projects files
```
.
├── account
│   ├── admin.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── apps.py
│   ├── backends.py
│   ├── decorators.py
│   ├── forms.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── signals.py
│   ├── templates
│   │   └── account
│   │       ├── account.html
│   │       ├── edit_account.html
│   │       ├── home.html
│   │       ├── login.html
│   │       ├── password_reset
│   │       │   ├── password_change_done.html
│   │       │   ├── password_change.html
│   │       │   ├── password_reset_complete.html
│   │       │   ├── password_reset_done.html
│   │       │   ├── password_reset_email.html
│   │       │   ├── password_reset_form.html
│   │       │   ├── password_reset_new_form.html
│   │       │   └── password_reset_subject.txt
│   │       └── registeration
│   │           ├── account_activation_email.html
│   │           ├── activation_invalid.html
│   │           └── register.html
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
├── chat
│   ├── admin.py
│   ├── apps.py
│   ├── consumers.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── routing.py
│   ├── templates
│   │   └── chat
│   │       ├── chat.html
│   │       ├── conversation.html
│   │       ├── messages.html
│   │       ├── newchat.html
│   │       └── websocket.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── core
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── docker-compose.yml
├── manage.py
├── media
│   ├── images
│   │   └── default
│   │       └── default.jpg
│   ├── profile_images
│   │   └── profile_images.txt
│   └── temp
│       └── temp.txt
├── requirements.txt
├── static
│   ├── images
│   │   └── my-logo.png
│   └── mainme.css
└── templates
    └── base.html

20 directories, 61 files

```
## SOME IMAGES FORM THE APP 

![Default Home View](__screenshots/register.png?raw=true "register")
![Default Home View](__screenshots/home.png?raw=true "home")
![Default Home View](__screenshots/adduser.png?raw=true "adduser")
![Default Home View](__screenshots/profile.png?raw=true "profile")
![Default Home View](__screenshots/chatt.png?raw=true "chatt")


TO CONTACT ME SEND EMAIL ON www.karam777krm@gmail.com
