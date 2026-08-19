from django import forms

from .models import Review, Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
        label='Note',
    )

    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']


class FollowUserForm(forms.Form):
    username = forms.CharField(max_length=150)
