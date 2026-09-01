"""Vues de gestion du flux, des publications et des abonnements."""

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import FollowUserForm, ReviewForm, TicketForm
from .models import Review, Ticket, UserFollows

User = get_user_model()


@login_required
def feed(request):
    """Affiche le flux personnalisé de l'utilisateur connecté."""
    # Le flux contient les publications de l'utilisateur et de ses abonnements.
    # On interroge la table UserFollows et on récupères toute les relations d'abonnement du User connecté
    followed_users = UserFollows.objects.filter(
        user=request.user
    ).values_list(
        'followed_user',
        flat=True,
    )

    # Dans la table Ticket on récupéres tout les ticket User ou Followed User
    tickets = Ticket.objects.filter(
        Q(user=request.user) |
        Q(user__in=followed_users)
    )

    # Dans la table Review on récupère en plus les Réponses au Tickets du User
    reviews = Review.objects.filter(
        Q(user=request.user) |
        Q(user__in=followed_users) |
        Q(ticket__user=request.user)
    )

    # Cet ensemble évite de proposer une seconde critique du même ticket.
    reviewed_ticket_ids = set(
        # On cherche les tickets auquel le User a répondu et on extrait les ID
        Review.objects.filter(
            user=request.user
        ).values_list(
            'ticket_id',
            flat=True,
        )
    )

    for ticket in tickets:
        # Ces attributs temporaires pilotent le rendu commun des publications.
        # On ajoute temporairement une propriété python pour savoir si l'objet est un ticket
        ticket.content_type = 'TICKET'
        # On compares les Id pour savoir si le User a deja répondu a la review avec un ticket
        ticket.can_review = ticket.id not in reviewed_ticket_ids
        # Si le test renvoie True alors le User peut répondre a la Review

    for review in reviews:
        review.content_type = 'REVIEW'

    # On crée une collection python commune pour harmoniser les modèles QuerySets Django
    posts = list(tickets) + list(reviews)

    posts.sort(
        # On trie chaque objet en fonction de sa date + heure de création
        key=lambda post: post.time_created,
        # Le reverse True permet d'inverser l'ordre chronologique pour afficher en premier les posts récents
        reverse=True,
    )

    return render(
        # On transmet la requete et on indique le template Django à utiliser
        request,
        'reviews/feed.html',
        {
            # On transmet au template la collection d'objet a afficher
            'posts': posts,
        },
    )


@login_required
def create_ticket(request):
    """Crée un ticket au nom de l'utilisateur connecté."""
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
    """Modifie un ticket uniquement si l'utilisateur courant en est l'auteur."""
    ticket = get_object_or_404(
        Ticket,
        id=ticket_id,
        user=request.user,
    )

    form = TicketForm(instance=ticket)

    if request.method == 'POST':
        form = TicketForm(
            request.POST,
            request.FILES,
            instance=ticket,
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
    """Supprime après confirmation un ticket appartenant à l'utilisateur."""
    ticket = get_object_or_404(
        Ticket,
        id=ticket_id,
        user=request.user,
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
    """Publie une unique critique de l'utilisateur pour le ticket demandé."""
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if Review.objects.filter(
        ticket=ticket,
        user=request.user,
    ).exists():
        messages.error(
            request,
            "Vous avez déjà publié une critique pour ce ticket.",
        )
        return redirect('feed')

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
    """Modifie une critique appartenant à l'utilisateur connecté."""
    review = get_object_or_404(
        Review,
        id=review_id,
        user=request.user,
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
    """Supprime après confirmation une critique appartenant à l'utilisateur."""
    review = get_object_or_404(
        Review,
        id=review_id,
        user=request.user,
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
    """Crée en une opération un ticket et la critique qui lui répond."""
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
    """Ajoute un abonnement et affiche abonnements et abonnés de l'utilisateur."""
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
                    "Cet utilisateur n'existe pas.",
                )
                return redirect('follow_users')

            if followed_user == request.user:
                messages.error(
                    request,
                    "Vous ne pouvez pas vous suivre vous-même.",
                )
                return redirect('follow_users')

            follow, created = UserFollows.objects.get_or_create(
                user=request.user,
                followed_user=followed_user,
            )

            if created:
                messages.success(
                    request,
                    "Utilisateur suivi.",
                )
            else:
                messages.info(
                    request,
                    "Vous suivez déjà cet utilisateur.",
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
    """Supprime l'abonnement courant vers l'utilisateur indiqué."""
    followed_user = get_object_or_404(
        User,
        id=user_id,
    )

    follow = get_object_or_404(
        UserFollows,
        user=request.user,
        followed_user=followed_user,
    )

    if request.method == 'POST':
        follow.delete()

    return redirect('follow_users')


@login_required
def posts(request):
    """Affiche les publications de l'utilisateur et les réponses reçues."""
    tickets = Ticket.objects.filter(
        user=request.user
    )

    reviews = Review.objects.filter(
        user=request.user
    )

    reviews_on_my_tickets = Review.objects.filter(
        ticket__user=request.user
    ).exclude(
        user=request.user
    )

    reviewed_ticket_ids = set(
        Review.objects.filter(
            user=request.user
        ).values_list(
            'ticket_id',
            flat=True,
        )
    )

    for ticket in tickets:
        ticket.can_review = ticket.id not in reviewed_ticket_ids

    return render(
        request,
        'reviews/posts.html',
        {
            'tickets': tickets,
            'reviews': reviews,
            'reviews_on_my_tickets': reviews_on_my_tickets,
        },
    )
