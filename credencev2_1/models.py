from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
from django.db import models
from django.conf import settings
from datetime import date
from datetime import datetime

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

class Platform (models.Model):
    platform_name = models.CharField(max_length=100,unique=True)
    platform_type = models.CharField(max_length=100)
    def __str__(self):
        return self.platform_name

class JobInfo (models.Model):
    user_account= models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    job_name  = models.CharField(max_length=100)
    job_type  = models.CharField(max_length=100)
    job_description = models.CharField(max_length=300)

    def __str__(self):
        return self.job_name

class Address(models.Model):
    user_account = models.OneToOneField(
        UserAccount,
        on_delete=models.CASCADE,
        related_name="address"
    )

    region = models.CharField(max_length=150)
    province = models.CharField(max_length=150)
    municipality_city = models.CharField(max_length=150)
    barangay = models.CharField(max_length=150)
    street_address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.barangay}, {self.municipality_city}"

class Vault (models.Model):
    user_account = models.OneToOneField(
            UserAccount,
            on_delete=models.CASCADE,
            related_name="vault"
        )
    vault_type = models.CharField(max_length=150)
    vault_balance = models.FloatField(default=0.0)

    
    def __str__(self):
            return f"Vault No. {self.id}"

class UserHealthScore (models.Model):
    user_account = models.OneToOneField(
                UserAccount,
                on_delete=models.CASCADE,
                related_name="user_health_score"
            )

    def __str__(self):
        return f"User Health Score No. {self.id}"

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
            return f"User {self.user_account}'s Bank Account No. {self.id}"

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
                return f"User {self.user_account.id}'s Loan No. {self.id}"


class InvestmentProvider (models.Model):
     investment_provider_name = models.CharField(max_length=100,unique=True)
     def __str__(self):
        return self.investment_provider_name

class InvestmentInfo(models.Model):
     user_account = models.ForeignKey(
                 UserAccount,
                 on_delete=models.CASCADE,
             )
     
     investment_provider = models.ForeignKey(
        InvestmentProvider,
         on_delete=models.CASCADE,
             )
     date_availed = models.DateField()
     minimum_capital=models.FloatField(default=0.0)
     return1 = models.FloatField (default=0.0)
     mtd = models.FloatField (default=0.0)
     ytd = models.FloatField(default=0.0)
     nav = models.FloatField(default=0.0)
     navps = models.FloatField(default=0.0)
     rsi = models.FloatField(default=0.0)

     def __str__(self):
                     return f"User {self.user_account.id}'s Investment No. {self.id}"

class InsuranceProvider(models.Model):
     insurance_provider_name = models.CharField(max_length=100, unique=True)
     def __str__(self):
             return self.insurance_provider_name

class InsuranceInfo(models.Model):
     user_account = models.ForeignKey(
                      UserAccount,
                      on_delete=models.CASCADE,
                  )
          
     insurance_provider = models.ForeignKey(
             InsuranceProvider,
              on_delete=models.CASCADE,
                  )   
     insurance_type = models.CharField(max_length=100)
     date_availed =  models.DateField()
     premium = models.FloatField(default=0.0)
     deductible = models.FloatField(default=0.0)
     co_payment = models.FloatField(default=0.0)
     con_insurance= models.FloatField(default=0.0)
     policy_limit = models.FloatField(default=0.0)

     def __str__(self):
                          return f"User {self.user_account.id}'s Insurance No. {self.id}"

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
      transaction_time = models.DateField(auto_now_add=True)
      transaction_amount = models.FloatField(default=0.0)

      def __str__(self):
                    return f"Transaction Number {self.id} of User No. {self.user_account.id}"

    
