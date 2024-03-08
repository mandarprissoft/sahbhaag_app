from django.urls import path
from .views import LoginAPIView, UserAPIViewList, CenterAPIViewList, UserAPIViewDetail, CenterAPIViewDetail

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    # path('users/', UserAPIView.as_view(), name='trainer-trainee-create'),
    path('users/', UserAPIViewList.as_view(), name='user-create-retrieve'),
    path('users/<int:id>/', UserAPIViewDetail.as_view(), name='user-update-delete'),
    path('centers/', CenterAPIViewList.as_view(), name='center-create-retrieve'),
    path('center/<int:id>/', CenterAPIViewDetail.as_view(), name='center-update-delete'),
]