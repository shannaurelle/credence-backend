from django.contrib import admin
from .models import User
from .models import UserAccount
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(UserAccount)
admin.site.register(Address)
admin.site.register(Platform)
admin.site.register(JobInfo)
admin.site.register(Vault)
admin.site.register(UserHealthScore)
admin.site.register(Bank)
admin.site.register(ConnectedBankAccount)
admin.site.register(Lender)
admin.site.register(LoanInfo)
admin.site.register(InvestmentProvider)
admin.site.register(InvestmentInfo)
admin.site.register(InsuranceProvider)
admin.site.register(InsuranceInfo)
admin.site.register(TransactionHistory)

