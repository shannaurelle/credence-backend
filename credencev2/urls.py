"""
URL configuration for credencev2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from credencev2_1.views import *
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

#10-27-2026 - 5:06 PM
from django.urls import path
from credencev2_1.views import current_user

urlpatterns = [
    path('api/users/', UserListCreateAPIView.as_view(), name='user-list-create'),
    path('api/users/<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'),
    path('admin/', admin.site.urls),

    path('api/user_accounts/', UserAccountListCreateAPIView.as_view(), name='user-account-list-create'),
    path('api/user_accounts/<int:pk>/', UserAccountListDetailAPIView.as_view(), name='user-account-list-detail'),

    path('api/user_profile/<int:pk>/',ProfileView.as_view(),name='user-profile'),

    # Edit Profile Details
    path('api/user_profile/update/<int:pk>/',ProfileUpdate.as_view(),name='user-profile-update'),

    # Connected Bank Accounts
    path('api/connected_bank/update/<int:pk>/',ConnectedBankUpdateView.as_view(),name='user-bank-update'),

    # Vault
    path('api/vault/update/<int:pk>/',VaultUpdateView.as_view(),name='user-vault-update'),

    # User Health Score
    path('api/uhs/update/<int:pk>/',UserHealthScoreUpdateView.as_view(),name='user-uhs-update'),

    # Loan Information
    path('api/loaninfo/update/<int:pk>/',LoanInfoUpdateView.as_view(),name='user-loaninfo-update'),

    # Investment Information
    path('api/investmentinfo/update/<int:pk>/',InvestmentInfoUpdateView.as_view(),name='user-investmentinfo-update'),

    # Insurance Information
    path('api/insuranceinfo/update/<int:pk>/',InsuranceInfoUpdateView.as_view(),name='user-insuranceinfo-update'),
    
    # Login and token refresh
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    #Get the id of the current user
     path("users/me/", current_user, name="current-user")
]


