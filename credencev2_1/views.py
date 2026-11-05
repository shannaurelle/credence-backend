from rest_framework.viewsets import generics
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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