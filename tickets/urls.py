from django.urls import path
from . import views

urlpatterns = [
    # Dashboard / Home
    path('', views.dashboard, name='dashboard'),
    
    # Auth (These are the names Django is looking for)
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),  # <--- This fixes your error
    
    # Ticket Actions
    path('new/', views.create_ticket, name='create_ticket'),
    path('ticket/<int:pk>/', views.ticket_detail, name='ticket_detail'),
    path('ticket/close/<int:pk>/', views.close_ticket, name='close_ticket'),
]