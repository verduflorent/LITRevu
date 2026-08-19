from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Q

from .forms import FollowUserForm, ReviewForm, TicketForm
from .models import Review, Ticket, UserFollows

User = get_user_model()


@login_required
def feed(request):
    followed_users = UserFollows.objects.filter(
        user=request.user
    ).values_list(
        'followed_user',
        flat=True
    )

    tickets = Ticket.objects.filter(
        Q(user=request.user) |
        Q(user__in=followed_users)
    )

    reviews = Review.objects.filter(
        Q(user=request.user) |
        Q(user__in=followed_users) |
        Q(ticket__user=request.user)
    )

    for ticket in tickets:
        ticket.content_type = 'TICKET'

    for review in reviews:
        review.content_type = 'REVIEW'

    posts = list(tickets) + list(reviews)

    posts.sort(
        key=lambda post: post.time_created,
        reverse=True
    )

    return render(
        request,
        'reviews/feed.html',
        {
            'tickets': tickets,
            'reviews': reviews,
            'posts': posts,
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
    ticket = get_object_or_404(
        Ticket,
        id=ticket_id,
        user=request.user
    )

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

@login_required
def follow_users(request):
    form = FollowUserForm()

    if request.method == 'POST':
        form = FollowUserForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']

            try:
                followed_user = User.objects.get(username=username)
            except User.DoesNotExist:
                messages.error(
                    request,
                    "Cet utilisateur n'existe pas."
                )
                return redirect('follow_users')

            if followed_user == request.user:
                messages.error(
                    request,
                    "Vous ne pouvez pas vous suivre vous-même."
                )
                return redirect('follow_users')

            follow, created = UserFollows.objects.get_or_create(
                user=request.user,
                followed_user=followed_user
            )

            if created:
                messages.success(
                    request,
                    "Utilisateur suivi."
                )
            else:
                messages.info(
                    request,
                    "Vous suivez déjà cet utilisateur."
                )

            return redirect('follow_users')

    following = UserFollows.objects.filter(
        user=request.user
    )

    followers = UserFollows.objects.filter(
        followed_user=request.user
    )

    return render(
        request,
        'reviews/follow_users.html',
        {
            'form': form,
            'following': following,
            'followers': followers,
        },
    )

@login_required
def unfollow_user(request, user_id):
    followed_user = get_object_or_404(
        User,
        id=user_id
    )

    follow = get_object_or_404(
        UserFollows,
        user=request.user,
        followed_user=followed_user
    )

    if request.method == 'POST':
        follow.delete()

    return redirect('follow_users')
