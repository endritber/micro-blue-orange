from django.urls import path, include
from .views import *

from rest_framework_simplejwt import views as jwt_views

# Create your urls here.
urlpatterns = [
    #root api
    path('', ApiRoot.as_view(), name=ApiRoot.name),

    # api clients/authentication
    path('api/clients/v1', ClientListCreateView.as_view(), name=ClientListCreateView.name),
    path('api/client/<str:pk>', ClientDetailUpdate.as_view(), name=ClientDetailUpdate.name),
    path('api/authentication', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    # api client address
    path('api/address/v1', AddressListCreateView.as_view(), name=AddressListCreateView.name),
    path('api/address/<str:pk>', AddressDetailUpdateDestroy.as_view(), name=AddressDetailUpdateDestroy.name),
]