from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Ticket
from .forms import TicketForm
from .models import Ticket, Comment
from django.core.mail import send_mail

@login_required
def dashboard(request):
    # Logic: Support sees ALL tickets; Customers see only THEIR tickets
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
            # Send email (simulation)
            send_mail(
                subject=f'New Ticket Created: {ticket.title}',
                message=f'User {request.user.username} has created a new ticket.\n\nDescription:\n{ticket.description}',
                from_email='system@example.com',
                recipient_list=['admin@example.com'],
                fail_silently=False,
            )
            return redirect('dashboard')
    else:
        form = TicketForm()

    # CRITICAL: This line must be back here, ALIGNED with the 'if' above, not inside 'else'
    return render(request, 'tickets/create_ticket.html', {'form': form})

# Simple logic to close a ticket (for demo)
@login_required
def close_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    # Only allow if user is support or owns the ticket
    if request.user.is_support or ticket.customer == request.user:
        ticket.status = 'CLOSED'
        ticket.save()
    return redirect('dashboard')

@login_required
def ticket_detail(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    
    # Security Check: Only allow Owner or Support Agent
    if request.user != ticket.customer and not request.user.is_support:
        return redirect('dashboard')

    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Comment.objects.create(ticket=ticket, user=request.user, text=text)
            return redirect('ticket_detail', pk=pk)

    return render(request, 'tickets/ticket_detail.html', {'ticket': ticket})