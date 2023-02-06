from django import forms


class CreateListing(forms.Form):
    title = forms.CharField(label="name", max_length=64)
    description = forms.CharField(max_length=500)
    starting_bid = forms.IntegerField(min_value=0)
    image = forms.URLField()
    category = forms.CharField(max_length=64)


class BidListing(forms.Form):
    bid = forms.IntegerField(
        min_value=0, widget=forms.TextInput(attrs={'placeholder': 'Bid', 'class': 'form-control mb-3'}))
