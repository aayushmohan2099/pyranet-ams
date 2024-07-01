from django.urls import path
from . import views

urlpatterns = [
    path('member/<int:member_id>/', views.member_detail, name='member_detail'),
    path('create-user/', views.create_user, name='create_user'),
    path('user-created/<str:username>/<int:member_id>/', views.user_created, name='user_created'),
    path('', views.homepage, name='homepage'),
    path('find-member/', views.find_member, name='find_member'),
    path('relation-established/<str:parent>/<str:child>/<int:member_id>/', views.relation_established, name='relation_established'),
    path('establish-relationship/', views.establish_relationship, name='establish_relationship'),
]
