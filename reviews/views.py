from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ReviewForm, TicketForm
from .models import Review, Ticket


@login_required
def feed(request):
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()

    print("REVIEWS DANS LE FEED :", reviews.count())

    return render(
        request,
        'reviews/feed.html',
        {
            'tickets': tickets,
            'reviews': reviews,
        },
    )

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

@login_required
def create_review(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()

            return redirect('feed')

    return render(
        request,
        'reviews/create_review.html',
        {
            'form': form,
            'ticket': ticket,
        },
    )

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(
        Review,
        id=review_id,
        user=request.user
    )

    form = ReviewForm(instance=review)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)

        if form.is_valid():
            form.save()
            return redirect('feed')

    return render(
        request,
        'reviews/edit_review.html',
        {'form': form},
    )

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(
        Review,
        id=review_id,
        user=request.user
    )

    if request.method == 'POST':
        review.delete()
        return redirect('feed')

    return render(
        request,
        'reviews/delete_review.html',
        {'review': review},
    )

@login_required
def create_ticket_and_review(request):
    ticket_form = TicketForm()
    review_form = ReviewForm()

    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)

        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()

            return redirect('feed')

    return render(
        request,
        'reviews/create_ticket_and_review.html',
        {
            'ticket_form': ticket_form,
            'review_form': review_form,
        },
    )
