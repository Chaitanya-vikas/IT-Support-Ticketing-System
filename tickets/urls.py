from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Dashboard (Home Page)
    path('', views.dashboard, name='dashboard'),
    
    # Create Ticket Page
    path('new/', views.create_ticket, name='create_ticket'),
    
    # Close Ticket Logic
    path('close/<int:pk>/', views.close_ticket, name='close_ticket'),
    
    # Login/Logout (Built-in Django views)
    path('login/', auth_views.LoginView.as_view(template_name='tickets/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('ticket/<int:pk>/', views.ticket_detail, name='ticket_detail'),
]