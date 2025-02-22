from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('member/<int:member_id>/', views.member_detail, name='member_detail'),
    path('create-user/', views.create_user, name='create_user'),
    path('user-created/<str:username>/<int:member_id>/', views.user_created, name='user_created'),
    path('', views.homepage, name='homepage'),
    path('find-member/', views.find_member, name='find_member'),
    path('relation-established/<str:parent>/<str:child>/<int:member_id>/', views.relation_established, name='relation_established'),
    path('establish-relationship/', views.establish_relationship, name='establish_relationship'),
    path('update-user/<str:username>/', views.update_user, name='update_user'),
    path('user-updated/<str:username>/', views.user_updated, name='user_updated'),
    path('edit-relationship/<int:relationship_id>/', views.edit_member_relationship, name='edit_member_relationship'),
    path('relationship-updated/<int:relationship_id>/', views.relationship_updated, name='relationship_updated'),
    path('manage-products/', views.manage_products, name='manage_products'),
    path('manage-companies/', views.manage_companies, name='manage_companies'),
    path('browse-products/', views.browse_products, name='browse_products'),
    path('user-login/', views.user_login, name='user_login'),
    path('user-dashboard/<int:member_id>/', views.user_dashboard, name='user_dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)