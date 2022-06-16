from rest_framework import serializers
from account.models import Account
from rest_framework.serializers import ModelSerializer
from PIL import Image


class RegisterationSerilizers(serializers.ModelSerializer):

    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        account = Account(
            username=self.validated_data['username'],
            email=self.validated_data['email'].lower()
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError(
                {'password': 'password must be mutch'})

        account.set_password(password)
        account.save()
        return account


class AccountProfileSerilizers(ModelSerializer):
    profile_image = serializers.SerializerMethodField('validate_image_url')

    class Meta:
        model = Account
        fields = ['pk', 'email', 'username', 'profile_image', 'hide_email','date_joined','last_login']

    def validate_image_url(self, user):
        profile_image = user.profile_image.url[:user.profile_image.url.rfind("?")]
        return profile_image


class UpdateAccountProfileSerilizers(ModelSerializer):

    class Meta:
        model = Account
        fields = ['email', 'username', 'profile_image', 'hide_email',]

    def validate(self,account):
        try:
            email = account['email'].lower()
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
                if account:
                    raise serializers.ValidationError({"response": "account with this email already exists."})
                username = account['username']
                account_username = Account.objects.exclude(pk=self.instance.pk).get(username=username)
                if account_username:
                    raise serializers.ValidationError({"response": "account with this or username already exists."})
                
            except Account.DoesNotExist:
                account['email'] = email
                return account
        except KeyError:
            return account



class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)
