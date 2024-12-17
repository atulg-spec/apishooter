from rest_framework import serializers
from .models import EmailAccounts
from django.contrib.auth.models import User

class EmailAccountsSerializer(serializers.ModelSerializer):
    user = serializers.CharField()  # Accept username instead of User ID

    class Meta:
        model = EmailAccounts
        fields = ['user', 'email', 'password', 'google_token']
