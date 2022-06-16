from django.urls import path

from . import views
app_name = 'account'
urlpatterns = [
    path('', views.getRouts),
    path('login/', views.loginUser, name="login"),
    path('register/', views.registerUser, name="register"),
    path('account/', views.profileUser, name="account_view"),
    path('account/edit/', views.updateprofileUser, name="account_edit"),
    path('check_email/', views.does_account_exist_view,name="check_email"),
    path('change_password/', views.ChangePasswordView.as_view(),name="change_password"),
    # path('reset_password/', views.ChangePasswordView.as_view(),name="reset_password"),

]
