# serializers.py
from rest_framework import serializers
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

User = get_user_model()

class UserAccountSerializer(serializers.ModelSerializer):
    # Get fields from the related Django User model
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = UserAccount
        fields = [
            'user',
            'first_name',
            'last_name',
            'email',
            'contact_number',
        ]
        read_only_fields = ['user']

class ProfileDetailsSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(source='user.first_name',read_only=True)
    last_name = serializers.CharField(source='user.last_name',read_only=True)
    email = serializers.EmailField(source='user.email',read_only=True)
    contact_number = serializers.CharField(read_only=True)
    region = serializers.CharField(source='address.region',read_only=True)
    province = serializers.CharField(source='address.province', read_only=True)
    municipality_city = serializers.CharField(source='address.municipality_city',read_only=True)
    barangay = serializers.CharField(source='address.barangay',read_only=True)
    street_address = serializers.CharField(source='address.street_address',read_only=True, allow_null=True)

    class Meta:
        model = UserAccount
        fields = [
            'user',
            'first_name',
            'last_name',
            'email',
            'contact_number',
            'region',
            'province',
            'municipality_city',
            'barangay',
            'street_address',
        ]

class ProfileDetailUpdateSerializer(serializers.ModelSerializer):
    contact_number = serializers.CharField(read_only=True)
    region = serializers.CharField(source='address.region',read_only=True)
    province = serializers.CharField(source='address.province', read_only=True)
    municipality_city = serializers.CharField(source='address.municipality_city',read_only=True)
    barangay = serializers.CharField(source='address.barangay',read_only=True)
    street_address = serializers.CharField(source='address.street_address',read_only=True, allow_null=True)

    class Meta:
            model = UserAccount
            fields = [
                'contact_number',
                'region',
                'province',
                'municipality_city',
                'barangay',
                'street_address',
            ]

class ConnectedBankAccountsSerializer(serializers.ModelSerializer):
    bank_name = serializers.CharField(source='bank.bank_name',read_only=True) 
    class Meta:
        model = ConnectedBankAccount
        fields = [
            'id',
            'user_account',
            'bank',
            'bank_name',
            'account_type',
            'bank_balance'
        ]

class VaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vault
        fields = [
            'user_account',
            'vault_type',
            'vault_balance'
        ]

class UserHealthScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserHealthScore
        fields = [
            'user_account',
            'uh_score'
        ]
    