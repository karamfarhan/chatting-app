from django.urls import path
from account.views import register_view, login_view, logout_view, edit_account_view, account_view_detail , account_activate


app_name = 'account'

urlpatterns = [
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('register/', register_view, name="register"),
    path('activate/<slug:uidb64>/<slug:token>)/', account_activate, name='activate'),

    path('<user_id>/', account_view_detail, name="account_view_detail"),
    path('<user_id>/edit/', edit_account_view, name="account_edit"),



]