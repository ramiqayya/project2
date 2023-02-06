from django import forms


class CreateListing(forms.Form):
    title = forms.CharField(label="name", max_length=64, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    description = forms.CharField(
        max_length=500, widget=forms.TextInput(attrs={'class': 'form-control'}))
    starting_bid = forms.IntegerField(
        min_value=0, widget=forms.TextInput(attrs={'class': 'form-control'}))
    image = forms.URLField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    category = forms.CharField(
        max_length=64, widget=forms.TextInput(attrs={'class': 'form-control'}))


class BidListing(forms.Form):
    bid = forms.IntegerField(
        min_value=0, widget=forms.TextInput(attrs={'placeholder': 'Bid', 'class': 'form-control mb-3'}))
