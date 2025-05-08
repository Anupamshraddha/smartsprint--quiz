from django.shortcuts import render, redirect
from .models import Review
from .forms import ReviewForm

def reviews(request):
    reviews = Review.objects.all().order_by('-created_at')  # Get all reviews ordered by creation date
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new review
            return redirect('reviews')  # Redirect to the same page to show updated reviews
    else:
        form = ReviewForm()

    return render(request, 'reviews.html', {'reviews': reviews, 'form': form})


import requests
from django.shortcuts import render

def flask_reviews_view(request):
    try:
        response = requests.get('http://127.0.0.1:5000/api/reviews')  # URL of your Flask API
        if response.status_code == 200:
            reviews = response.json()
        else:
            reviews = []
    except Exception as e:
        print("Error fetching reviews:", e)
        reviews = []

    return render(request, 'reviews_from_flask.html', {'reviews': reviews})
