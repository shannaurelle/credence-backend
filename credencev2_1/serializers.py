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

class JobInfoSerializer(serializers.ModelSerializer):
    platform_name = serializers.CharField(
        source='platform.platform_name',
        read_only=True
    )

    platform_type = serializers.CharField(
        source='platform.platform_type',
        read_only=True
    )

    bank_name = serializers.CharField(
        source='connected_bank_account.bank.bank_name',
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = JobInfo
        fields = [
            'id',
            'user_account',
            'connected_bank_account',
            'bank_name',
            'platform',
            'platform_name',
            'platform_type',
            'job_name',
            'job_type',
            'job_description',
        ]

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

class TransactionHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = TransactionHistory
        fields = [
            'id',
            'connected_bank_account',
            'user_account',
            'transaction_name',
            'transaction_date',
            'transaction_time',
            'transaction_amount',
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

class LoanInfoSerializer(serializers.ModelSerializer):
    lender_name = serializers.CharField(source='lender.lender_name',read_only=True) 
    class Meta:
        model= LoanInfo
        fields = [
            "id",
            "lender",
            "lender_name",
            "loan_type",
            "loan_amount",
            "no_of_terms",
            "interest_rate",
            "payment_amount",
            "disbursement_date",
            "start_date",
            "end_date",
            "user_account"

        ]

class MonthlyRecurringPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model=MonthlyRecurringPayment
        fields=[
            'id',
            'user_account',
            'type',
            'monthly_payment'
        ]

class PHMinimumWagesPerRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model=PHMinimumWagesPerRegion
        fields='__all__'

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Income
        fields='__all__'

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Expense
        fields='__all__'

class DistanceTravelledSerializer(serializers.ModelSerializer):
    class Meta:
        model=DistanceTravelled
        fields='__all__'