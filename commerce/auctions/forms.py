from django import forms


class CreateListing(forms.Form):
    title = forms.CharField(label="name", max_length=64, widget=forms.TextInput(
        attrs={'class': 'form-control mb-2'}))
    starting_bid = forms.IntegerField(
        min_value=0, widget=forms.TextInput(attrs={'class': 'form-control mb-2'}))
    image = forms.URLField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    category = forms.CharField(
        max_length=64, widget=forms.TextInput(attrs={'class': 'form-control mb-2'}))
    description = forms.CharField(
        max_length=500, widget=forms.Textarea(attrs={'rows': '5', 'class': 'form-control mb-2'}))


class BidListing(forms.Form):
    bid = forms.IntegerField(
        min_value=0, widget=forms.TextInput(attrs={'placeholder': 'Bid', 'class': 'form-control mb-3'}))


class Comment_Form(forms.Form):
    comment = forms.CharField(max_length=250, widget=forms.Textarea(
        attrs={'placeholder': 'Write a Comment', 'rows': '5', 'class': 'form-control mb-2'}))
