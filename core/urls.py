from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from chat.views import home
urlpatterns = [
    path('',home, name="home"),
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls', namespace="chat")),
    path('account/',include('account.urls',namespace='account')),
    path('api/', include('account.api.urls', namespace="apiaccount")),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='account/password_reset/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset/password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset/password_reset_new_form.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset/password_reset_complete.html'),name='password_reset_complete'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='account/password_reset/password_change.html', success_url="/"),name='password_change'),
    # path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='account/password_reset/password_change_done.html'), name='password_change_done'),
]



# MEANS IF WE NOT IN PRODUCTION IF WE IN OUR DEVELOPMENT INVIROMENT
# GIVE HIM THE URL FOR STATIC AND MEDIA FILES
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)