
import os
import django
import random
from datetime import date, datetime, time, timedelta

# ==========================================
# DJANGO CONFIGURATION
# ==========================================

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credencev2.settings')
django.setup()

django.setup()

from credencev2_1.models import (
    TransactionHistory,
    ConnectedBankAccount,
    UserAccount
)

# ==========================================
# CONFIGURATION
# ==========================================

USER_ACCOUNT_ID = 3
CONNECTED_BANK_ACCOUNT_ID = 1

START_DATE = date(2026, 10, 7)
END_DATE = date(2026, 11, 5)

MIN_AMOUNT = 100
MAX_AMOUNT = 300

MIN_TRANSACTIONS_PER_DAY = 1
MAX_TRANSACTIONS_PER_DAY = 3

START_HOUR = 7
END_HOUR = 21

DELETE_EXISTING = True

# Optional: reproducible random results
# Set to None for different results every run.
RANDOM_SEED = None

if RANDOM_SEED is not None:
    random.seed(RANDOM_SEED)


# ==========================================
# GET ACCOUNT
# ==========================================

try:
    user_account = UserAccount.objects.get(
    user_id=USER_ACCOUNT_ID
)

    connected_bank_account = ConnectedBankAccount.objects.get(
        id=CONNECTED_BANK_ACCOUNT_ID,
        user_account=user_account
    )

except UserAccount.DoesNotExist:
    print("User account does not exist.")
    exit()

except ConnectedBankAccount.DoesNotExist:
    print("Connected bank account does not exist.")
    exit()


# ==========================================
# DELETE EXISTING SEEDED TRANSACTIONS
# ==========================================

if DELETE_EXISTING:

    deleted_count, _ = TransactionHistory.objects.filter(
        user_account=user_account,
        connected_bank_account=connected_bank_account,
        transaction_date__range=(START_DATE, END_DATE),
        transaction_name__startswith="Buffer Vault"
    ).delete()

    print(f"Deleted {deleted_count} existing transactions.")


# ==========================================
# GENERATE TRANSACTIONS
# ==========================================

transaction_types = [
    "Buffer Vault - Deposit",
    "Buffer Vault - Withdrawal"
]

transactions = []

current_date = START_DATE

while current_date <= END_DATE:

    daily_transaction_count = random.randint(
        MIN_TRANSACTIONS_PER_DAY,
        MAX_TRANSACTIONS_PER_DAY
    )

    # Generate unique times for each day
    daily_times = set()

    while len(daily_times) < daily_transaction_count:

        random_hour = random.randint(
            START_HOUR,
            END_HOUR
        )

        random_minute = random.randint(0, 59)
        random_second = random.randint(0, 59)

        daily_times.add(
            time(
                random_hour,
                random_minute,
                random_second
            )
        )

    # Sort transactions chronologically
    daily_times = sorted(daily_times)

    for transaction_time in daily_times:

        transaction_name = random.choice(
            transaction_types
        )

        transaction_amount = round(
            random.uniform(MIN_AMOUNT, MAX_AMOUNT),
            2
        )

        transactions.append(
            TransactionHistory(
                connected_bank_account=connected_bank_account,
                user_account=user_account,
                transaction_name=transaction_name,
                transaction_date=current_date,
                transaction_time=transaction_time,
                transaction_amount=transaction_amount
            )
        )

    current_date += timedelta(days=1)


# ==========================================
# BULK CREATE
# ==========================================

TransactionHistory.objects.bulk_create(
    transactions,
    batch_size=500
)

# ==========================================
# CONFIGURATION
# ==========================================

USER_ACCOUNT_ID = 3
CONNECTED_BANK_ACCOUNT_ID = 1

# ==========================================
# GET ACCOUNT
# ==========================================

try:
    user_account = UserAccount.objects.get(
        user_id=USER_ACCOUNT_ID
    )

    connected_bank_account = ConnectedBankAccount.objects.get(
        id=CONNECTED_BANK_ACCOUNT_ID,
        user_account=user_account
    )

except UserAccount.DoesNotExist:
    print("User account does not exist.")
    exit()

except ConnectedBankAccount.DoesNotExist:
    print("Connected bank account does not exist.")
    exit()

# ==========================================
# SUMMARY
# ==========================================

deposits = [
    t for t in transactions
    if t.transaction_name.endswith("Deposit")
]

withdrawals = [
    t for t in transactions
    if t.transaction_name.endswith("Withdrawal")
]

total_deposits = sum(
    t.transaction_amount for t in deposits
)

total_withdrawals = sum(
    t.transaction_amount for t in withdrawals
)


# ==========================================
# DISPLAY GENERATED TRANSACTIONS
# ==========================================

print("\n========== GENERATED TRANSACTIONS ==========")

for transaction in sorted(
    transactions,
    key=lambda t: (t.transaction_date, t.transaction_time)
):

    print(
        f"{transaction.transaction_date} "
        f"{transaction.transaction_time} | "
        f"{transaction.transaction_name} | "
        f"PHP {transaction.transaction_amount:,.2f}"
    )


# ==========================================
# FINAL SUMMARY
# ==========================================

print("\n==========================================")
print("TRANSACTION HISTORY SEEDING COMPLETED")
print("==========================================")

print(f"User Account ID: {USER_ACCOUNT_ID}")
print(f"Connected Bank Account ID: {CONNECTED_BANK_ACCOUNT_ID}")

print(f"Date Range: {START_DATE} to {END_DATE}")
print(f"Total Days: 30")
print(f"Total Transactions: {len(transactions)}")

print("------------------------------------------")

print(f"Deposit Count: {len(deposits)}")
print(f"Total Deposits: PHP {total_deposits:,.2f}")

print("------------------------------------------")

print(f"Withdrawal Count: {len(withdrawals)}")
print(f"Total Withdrawals: PHP {total_withdrawals:,.2f}")

print("------------------------------------------")

print(
    f"Net Buffer Vault Movement: "
    f"PHP {total_deposits - total_withdrawals:,.2f}"
)

print("==========================================")
