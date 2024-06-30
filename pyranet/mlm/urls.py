from django.urls import path
from . import views

urlpatterns = [
    path('member/<int:member_id>/', views.member_detail, name='member_detail'),
    path('create-user/', views.create_user, name='create_user'),
    path('user-created/<str:username>/<int:member_id>/', views.user_created, name='user_created'),
    path('', views.homepage, name='homepage'),
    path('find-member/', views.find_member, name='find_member'),
    # path('member/<int:member_id>/network/', views.member_network, name='member_network'),
]
