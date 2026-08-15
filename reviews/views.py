from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TicketForm
from .models import Ticket


@login_required
def feed(request):
    return render(request, 'reviews/feed.html')

@login_required
def create_ticket(request):
    form = TicketForm()

    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            return redirect('feed')

    return render(
        request,
        'reviews/create_ticket.html',
        {'form': form},
    )

@login_required
def feed(request):
    tickets = Ticket.objects.all()

    return render(
        request,
        'reviews/feed.html',
        {'tickets': tickets},
    )
@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(
    Ticket,
    id=ticket_id,
    user=request.user
    )

    form = TicketForm(instance=ticket)

    if request.method == 'POST':
        form = TicketForm(
            request.POST,
            request.FILES,
            instance=ticket
        )

        if form.is_valid():
            form.save()
            return redirect('feed')

    return render(
        request,
        'reviews/edit_ticket.html',
        {'form': form},
    )
@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        ticket.delete()
        return redirect('feed')

    return render(
        request,
        'reviews/delete_ticket.html',
        {'ticket': ticket},
    )
