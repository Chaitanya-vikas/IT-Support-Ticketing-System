from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Ticket, Comment
from .forms import TicketForm
from django.core.mail import send_mail

# --- Auth Views ---

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'tickets/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

# --- App Views ---

@login_required
def dashboard(request):
    if request.user.is_support:
        tickets = Ticket.objects.all().order_by('-created_at')
    else:
        tickets = Ticket.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'tickets/dashboard.html', {'tickets': tickets})

@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.customer = request.user
            ticket.save()
            # Email Simulation
            print(f"Sending email to admin: New ticket '{ticket.title}' from {request.user.username}")
            return redirect('dashboard')
    else:
        form = TicketForm()
    return render(request, 'tickets/create_ticket.html', {'form': form})

@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    
    # Security: Only allow owner or support
    if request.user != ticket.customer and not request.user.is_support:
        return redirect('dashboard')

    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Comment.objects.create(ticket=ticket, user=request.user, text=text)
            return redirect('ticket_detail', pk=pk)

    return render(request, 'tickets/ticket_detail.html', {'ticket': ticket})

@login_required
def close_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.user.is_support:
        ticket.status = 'CLOSED'
        ticket.save()
    return redirect('dashboard')