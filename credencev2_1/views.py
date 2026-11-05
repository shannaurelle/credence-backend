from rest_framework.viewsets import generics
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from decimal import Decimal, InvalidOperation
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# List and Create new Users
class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserAccountListCreateAPIView(generics.ListCreateAPIView):
    queryset = UserAccount.objects.select_related('user').all()
    serializer_class = UserAccountSerializer

class UserAccountListDetailAPIView(generics.RetrieveAPIView):
    queryset = UserAccount.objects.select_related('user').all()
    serializer_class = UserAccountSerializer
    lookup_field='pk'

class UserAccountListDetailEdit(generics.UpdateAPIView):
    queryset = UserAccount.objects.select_related('user').all()
    serializer_class = UserAccountSerializer
    lookup_field='pk'

class ProfileView(generics.RetrieveAPIView):
    queryset = UserAccount.objects.select_related(
        'user',
        'address'
    ).all()
    serializer_class = ProfileDetailsSerializer
    lookup_field='pk'

class ProfileUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserAccount.objects.select_related('user', 'address').all()
    serializer_class = ProfileDetailUpdateSerializer
    lookup_field='pk'

class ConnectedBankUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset =ConnectedBankAccount.objects.select_related('user_account', 'bank').all()
    serializer_class = ConnectedBankAccountsSerializer
    lookup_field='pk'

class ConnectedBanksListView(generics.ListAPIView):
    serializer_class = ConnectedBankAccountsSerializer
    lookup_field='user_account'
    def get_queryset(self):
        user_account_id = self.kwargs['user_account']

        return ConnectedBankAccount.objects.select_related(
            'user_account', 'bank'
        ).filter(user_account_id=user_account_id)


class VaultUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vault.objects.select_related('user_account').all()
    serializer_class = VaultSerializer
    lookup_field='user_account'

class LoanInfoListView(generics.ListAPIView):
    queryset = LoanInfo.objects.select_related('user_account', 'lender').all()
    serializer_class = LoanInfoSerializer
    lookup_field='user_account'

class LoanInfoUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LoanInfo.objects.select_related('user_account', 'lender').all()
    serializer_class = LoanInfoSerializer
    lookup_field='pk'


#monthly recurring Payment
class MonthlyRecurringPaymentListView(generics.ListAPIView):
    queryset = MonthlyRecurringPayment.objects.select_related('user_account').all()
    serializer_class = MonthlyRecurringPaymentSerializer
    lookup_field='user_account'

class MonthlyRecurringPaymentUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MonthlyRecurringPayment.objects.select_related('user_account').all()
    serializer_class = MonthlyRecurringPaymentSerializer
    lookup_field='pk'

class PHMinimumWagesPerRegionListView(generics.ListAPIView):
    queryset = PHMinimumWagesPerRegion.objects.select_related().all()
    serializer_class = PHMinimumWagesPerRegionSerializer

class PHMinimumWagesPerRegionView(generics.ListAPIView):
    queryset = PHMinimumWagesPerRegion.objects.select_related().all()
    serializer_class = PHMinimumWagesPerRegionSerializer
    lookup_field='pk'

#Income
class IncomeListView(generics.ListAPIView):
    queryset = Income.objects.select_related('user_account').all()
    serializer_class = IncomeSerializer
    lookup_field='user_account'
class IncomeUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Income.objects.select_related('user_account').all()
    serializer_class = IncomeSerializer
    lookup_field='user_account'

#Expenses
class ExpenseListView(generics.ListAPIView):
    queryset = Expense.objects.select_related('user_account').all()
    serializer_class = ExpenseSerializer
    lookup_field='user_account'
class ExpenseUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.select_related('user_account').all()
    serializer_class = ExpenseSerializer
    lookup_field='user_account'


#Distance Travelled
class DistanceTravelledUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset =DistanceTravelled.objects.select_related('user_account').all()
    serializer_class = DistanceTravelledSerializer
    lookup_field='pk'

class DistanceTravelledListView(generics.ListAPIView):
    serializer_class = DistanceTravelledSerializer
    lookup_field='user_account'
    def get_queryset(self):
        user_account_id = self.kwargs['user_account']

        return DistanceTravelled.objects.select_related(
            'user_account'
        ).filter(user_account_id=user_account_id)


    # List and Create new Users
class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user

    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "date_joined": user.date_joined,
        "time_joined": user.date_joined.time(),                # HH:MM:SS object
        "time_joined_formatted": user.date_joined.strftime("%I:%M %p"), # "10:03 AM"
    })


class StashSurplusView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):

        try:
            # 1. Retrieve the UserAccount linked to the authenticated user
            user_account = UserAccount.objects.get(
                user_id=request.user.id
            )

            # 2. Retrieve request data
            bank_id = request.data.get("bank_id")
            raw_amount = request.data.get("amount")

            if not bank_id or raw_amount is None:
                return Response(
                    {"error": "Bank ID and amount are required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            amount = Decimal(str(raw_amount))

            if not amount.is_finite() or amount <= 0:
                return Response(
                    {"error": "Invalid stash amount."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 3. Retrieve the user's connected bank account
            bank = ConnectedBankAccount.objects.select_for_update().get(
                id=bank_id,
                user_account=user_account
            )

            # 4. Retrieve the user's vault
            vault = Vault.objects.select_for_update().get(
                user_account=user_account
            )

            # 5. Check available bank balance
            if Decimal(str(bank.bank_balance)) < amount:
                return Response(
                    {"error": "Insufficient bank balance."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 6. Transfer the amount
            bank.bank_balance = float(
                Decimal(str(bank.bank_balance)) - amount
            )
            bank.save(update_fields=["bank_balance"])

            vault.vault_balance = float(
                Decimal(str(vault.vault_balance)) + amount
            )
            vault.save(update_fields=["vault_balance"])

            return Response({
                "message": "Surplus successfully transferred to your vault.",
                "user_account_id": user_account.pk,
                "bank_id": bank.id,
                "amount_stashed": float(amount),
                "remaining_bank_balance": bank.bank_balance,
                "vault_balance": vault.vault_balance
            }, status=status.HTTP_200_OK)

        except UserAccount.DoesNotExist:
            return Response(
                {
                    "error": "No UserAccount is linked to the authenticated Django user.",
                    "authenticated_user_id": request.user.id
                },
                status=status.HTTP_404_NOT_FOUND
            )

        except ConnectedBankAccount.DoesNotExist:
            return Response(
                {"error": "Connected bank account not found for this user."},
                status=status.HTTP_404_NOT_FOUND
            )

        except Vault.DoesNotExist:
            return Response(
                {"error": "Vault not found for this user."},
                status=status.HTTP_404_NOT_FOUND
            )

        except (InvalidOperation, TypeError, ValueError):
            return Response(
                {"error": "Invalid transfer amount."},
                status=status.HTTP_400_BAD_REQUEST
            )