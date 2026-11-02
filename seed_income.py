import os
import django
import random
from datetime import date, timedelta

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credencev2.settings')
django.setup()

# Import your models
from credencev2_1.models import Income, UserAccount, JobInfo, ConnectedBankAccount

# Fixed foreign key IDs
USER_ACCOUNT_ID = 3
JOB_INFO_ID = 1
BANK_ACCOUNT_ID = 1

# Date range
START_DATE = date(2026, 10, 7)
END_DATE = date(2026, 11, 5)

# Retrieve related objects
user_account = UserAccount.objects.get(pk=USER_ACCOUNT_ID)
job_info = JobInfo.objects.get(pk=JOB_INFO_ID)
bank_account = ConnectedBankAccount.objects.get(pk=BANK_ACCOUNT_ID)

# Generate income records
current_date = START_DATE
records = []

while current_date <= END_DATE:

    income = Income(
        user_account=user_account,
        job_info=job_info,
        income_2_bankacct=bank_account,
        income_amount=round(random.uniform(0, 1500), 2),
        i_date=current_date
    )

    records.append(income)
    current_date += timedelta(days=1)

# Save all records
Income.objects.bulk_create(records)

print(f"Successfully created {len(records)} income records!")