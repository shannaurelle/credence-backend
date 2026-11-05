from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
from django.db import models
from django.conf import settings
from datetime import date
from datetime import datetime
from django.utils import timezone

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    contact = models.DecimalField(max_digits=11,decimal_places=0)
    address = models.CharField(max_length=128)
    password = models.CharField(max_length=128,default="gigworker")

    def __str__(self):
        return self.name

class UserAccount(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="useraccount"
    )
    contact_number = PhoneNumberField(blank=True, null=True, unique=True) 

    def __str__(self):
        return f"UserAccount {self.user.id}"



class PHMinimumWagesPerRegion(models.Model):
      region_name = models.CharField(max_length=100)
      minimum_wage = models.FloatField(default=0.0)
      def __str__(self):
            return self.region_name

class Address(models.Model):
    user_account = models.OneToOneField(
        UserAccount,
        on_delete=models.CASCADE,
        related_name="address",
        primary_key=True,
    )
    region_id = models.ForeignKey(
        PHMinimumWagesPerRegion,
        on_delete=models.CASCADE,
        related_name="regional_minimum_wage",
        null=True
    )
    region = models.CharField(max_length=150)
    province = models.CharField(max_length=150)
    municipality_city = models.CharField(max_length=150)
    barangay = models.CharField(max_length=150)
    street_address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.barangay}, {self.municipality_city}"



class Bank (models.Model):
     bank_name = models.CharField(max_length=150)

     def __str__(self):
        return self.bank_name

class ConnectedBankAccount (models.Model):
    user_account = models.ForeignKey(
        UserAccount,
        related_name='user_2_connected_bank',
        on_delete=models.CASCADE,
    )
    bank = models.ForeignKey(
        Bank,
        related_name='connected_bank_2_bank',
        on_delete=models.CASCADE,
    )
    account_type = models.CharField(max_length=100)
    bank_balance = models.FloatField(default =0.0)
    

    def __str__(self):
            return f"{self.user_account}'s Bank Account No. {self.id}"


class Platform (models.Model):
    platform_name = models.CharField(max_length=100,unique=True)
    platform_type = models.CharField(max_length=100)
    def __str__(self):
        return self.platform_name

class JobInfo (models.Model):
    user_account= models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    connected_bank_account = models.ForeignKey(ConnectedBankAccount, on_delete=models.CASCADE,null=True)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    job_name  = models.CharField(max_length=100)
    job_type  = models.CharField(max_length=100)
    job_description = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.user_account} - {self.job_name}"

class Lender(models.Model):
     lender_name = models.CharField(max_length=100,unique=True)
     def __str__(self):
        return self.lender_name

class LoanInfo(models.Model):

    user_account = models.ForeignKey(
            UserAccount,
            on_delete=models.CASCADE,
        )
    lender = models.ForeignKey(
            Lender,
            on_delete=models.CASCADE,
        )
    loan_type = models.CharField(max_length=100)
    loan_amount = models.FloatField(default=0.0)
    no_of_terms = models.IntegerField()
    interest_rate = models.FloatField(default=0.0)
    payment_amount = models.FloatField(default=0.0)
    disbursement_date = models.DateField(default=date.today)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
                return f"{self.user_account}'s Loan No. {self.id}"

class InvestmentProvider (models.Model):
     investment_provider_name = models.CharField(max_length=100,unique=True)
     def __str__(self):
        return self.investment_provider_name

class TransactionHistory(models.Model):
      connected_bank_account = models.ForeignKey(
            ConnectedBankAccount,
            on_delete=models.CASCADE,
        )
      user_account = models.ForeignKey(
                  UserAccount,
                  on_delete=models.CASCADE,
                  null=True
              )
      transaction_name = models.CharField(max_length=100)
      transaction_date = models.DateField(default=date.today)
      transaction_time = models.TimeField(
    default=timezone.now
)
      transaction_amount = models.FloatField(default=0.0)

      def __str__(self):
                    return f"Transaction Number {self.id} of {self.user_account}"


class MonthlyRecurringPayment(models.Model):

      user_account = models.ForeignKey(
                        UserAccount,
                        on_delete=models.CASCADE,
                        null=True
                    )
      type = models.CharField(max_length=100, null=True)
      monthly_payment = models.FloatField(default=0.0)
      def __str__(self):
            return f"Monthly Payment No. {self.id} of {self.user_account} for {self.type}"

class Income(models.Model):
    user_account = models.ForeignKey(
                              UserAccount,
                              on_delete=models.CASCADE,
                              null=True
                          )
    job_info = models.ForeignKey(
                              JobInfo,
                              on_delete=models.CASCADE,
                              null=True
                          )
    income_2_bankacct = models.ForeignKey(
                              ConnectedBankAccount,
                              on_delete=models.CASCADE,
                              null=True
                          )
    income_amount = models.FloatField(default=0.0)
    i_date = models.DateField(null=True)
    i_time = models.TimeField(null=True)
    i_isVerified = models.BooleanField(default=False)
    def __str__(self):
        return f"Income of {self.user_account}, {self.i_date} - {self.i_time}" 

class Expense(models.Model):
    user_account = models.ForeignKey(
                              UserAccount,
                              on_delete=models.CASCADE,
                              null=True
                          )
    expense_2_bankacct = models.ForeignKey(
                              ConnectedBankAccount,
                              on_delete=models.CASCADE,
                              null=True
                          )
    
    expense_amount = models.FloatField(default=0.0)
    e_date = models.DateField( null=True)
    e_time = models.TimeField( null=True)
    e_isVerified = models.BooleanField(default=False)
    def __str__(self):
        return f"Expense of {self.user_account}, {self.e_date} - {self.e_time}" 


class Vault (models.Model):
    user_account = models.OneToOneField(
            UserAccount,
            on_delete=models.CASCADE,
            related_name="vault",
            primary_key=True,
        )
    vault_type = models.CharField(max_length=150)
    vault_balance = models.FloatField(default=0.0)

    
    def __str__(self):
            return f"Vault of {self.user_account}"

class DistanceTravelled (models.Model):
     user_account = models.ForeignKey(
                                   UserAccount,
                                   on_delete=models.CASCADE,
                                   null=True
                               )
     t_date = models.DateField(null=True)
     t_time = models.TimeField(null=True)
     start_latitude = models.FloatField(default=0.0)
     start_longitude = models.FloatField(default=0.0)
     end_latitude = models.FloatField(default=0.0)
     end_longitude = models.FloatField(default=0.0)
     km = models.FloatField(default=0.0)
     vehicle_type = models.CharField( max_length=50,null=True,blank=True)



     
    
