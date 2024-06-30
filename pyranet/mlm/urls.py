from django.urls import path
from . import views

urlpatterns = [
    path('member/<int:member_id>/', views.member_detail, name='member_detail'),
]
