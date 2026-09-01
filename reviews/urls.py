"""Routes des tickets, critiques, flux et abonnements."""

from django.urls import path

from . import views


urlpatterns = [
    path('feed/', views.feed, name='feed'),
    path('tickets/create/', views.create_ticket, name='create_ticket'),
    path(
        'tickets/<int:ticket_id>/edit/',
        views.edit_ticket,
        name='edit_ticket',
    ),
    path(
        'tickets/<int:ticket_id>/delete/',
        views.delete_ticket,
        name='delete_ticket',
    ),
    path(
        'tickets/<int:ticket_id>/review/',
        views.create_review,
        name='create_review',
    ),
    path(
        'reviews/<int:review_id>/edit/',
        views.edit_review,
        name='edit_review',
    ),
    path(
        'reviews/<int:review_id>/delete/',
        views.delete_review,
        name='delete_review',
    ),
    path(
        'reviews/create/',
        views.create_ticket_and_review,
        name='create_ticket_and_review',
    ),
    path('follows/', views.follow_users, name='follow_users'),
    path(
        'follows/<int:user_id>/delete/',
        views.unfollow_user,
        name='unfollow_user',
    ),
    path('posts/', views.posts, name='posts'),
]
