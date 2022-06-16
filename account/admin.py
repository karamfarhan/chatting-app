from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms.widgets import Textarea
from account.models import Account
from account.forms import RegistrationForm

class AccountAdmin(UserAdmin):
	list_display = ('email','username','date_joined', 'last_login', 'is_admin','is_staff','is_active')
	search_fields = ('email','username',)
	readonly_fields=('id', 'date_joined', 'last_login')

	ordering = ('-date_joined',)

	filter_horizontal = ()
	list_filter = ('email', 'username', 'is_admin', 'is_staff',)

	fieldsets = (
		(None ,         {'fields' : ('email', 'username')}),
		('Permissions', {'fields' : ('is_admin','is_staff', 'is_superuser' , 'is_active', 'groups', 'user_permissions')}),
		('Personal' ,   {'fields' : ('profile_image', 'hide_email','date_joined','last_login')})
	)

	# formfield_overrides = {
	# 	Account.email : {'widget' : Textarea(attrs={'rows':10, 'cols':40})}
	# }
	
	add_fieldsets = (
		(None,          {'fields' : ('email', 'username', 'password1', 'password2')}),
		('Permissions', {'fields' : ('is_admin','is_staff', 'is_superuser' , 'is_active', 'groups', 'user_permissions')}),
		('Personal' ,   {'fields' : ('profile_image', 'hide_email')})
	)

	add_form = RegistrationForm






# THIS IS FOR CHANGE THE FORM IN ADMIN PANEL HERE WE ADD A EMAIL FIELD IN THE FORM IN IT 
admin.site.register(Account, AccountAdmin)