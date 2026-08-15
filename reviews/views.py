from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def feed(request):
    return render(request, 'reviews/feed.html')
