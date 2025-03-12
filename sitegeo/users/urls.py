from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('account/', views.account_user, name='account'),
    path('account/order/<int:order_id>/', views.order_user, name='order'),
    path('account/addorder/', views.addorder, name='addorder'),
    path('account/list_callback/', views.list_callback, name='list_callback'),

]

# path('logout/', LogoutView.as_view(), name='logout'),
# path('logout/', views.logout_user, name='logout'),
