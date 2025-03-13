from django.urls import path
from . import views

urlpatterns = [
    path('auth/', views.auth_connect, name='auth_connect'),
    path('auth/callback/', views.oauth_callback, name='oauth_callback'),
    path('contacts/', views.get_contacts, name='get_contacts'),
    path('update-contact/<str:contact_id>/', views.update_contact, name='update_contact_field'),
]
