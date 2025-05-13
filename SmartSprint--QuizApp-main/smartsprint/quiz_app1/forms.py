from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['product_name', 'rating', 'review_content', 'author']
        widgets = {
            'review_content': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        }
