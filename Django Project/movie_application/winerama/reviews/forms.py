from django.forms import ModelForm, Textarea
from reviews.models import Review

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': Textarea(attrs={'cols': 40, 'rows': 15}),
        }


class SearchForm(ModelForm):
	class Meta:
		model = Review
		fields = ['comment']
		widgets ={
			'comment': Textarea(attrs={'cols':15, 'rows':1}),
		}