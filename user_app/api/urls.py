from user_app.api.views import RegistrationView, UserDetailView, UserListView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register_view'),
    path('users/', UserListView.as_view(), name='user_list_view'),
    path('user/<str:username>/', UserDetailView.as_view(), name='user_detail_view'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
