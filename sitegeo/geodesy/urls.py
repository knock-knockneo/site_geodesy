from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('services/', views.services, name='services'),
    path('useful_info/', views.useful_info, name='info'),
    path('contact/', views.contact, name='contact'),
    path('call_back/', views.call_back, name='call'),

    path('service/<slug:service_slug>/', views.show_service, name='service'),
    path('post/<slug:post_slug>/', views.show_post, name='post'),

]
