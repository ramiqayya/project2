from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from .models import User, Auction_Listing, Bid, Comment


class CreateListing(forms.Form):
    title = forms.CharField(label="name", max_length=64)
    description = forms.CharField(max_length=500)
    starting_bid = forms.IntegerField()
    image = forms.URLField()
    category = forms.CharField(max_length=64)


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Auction_Listing.objects.all(),

    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def view_listing(request, listing_id):
    if "l_item" not in request.session:
        request.session["l_item"] = []
    something = Auction_Listing.objects.get(pk=listing_id)
    print(something)
    return render(request, "auctions/view_listing.html", {
        "listing": something,
        "l_item": request.session["l_item"]
    })


def add(request):
    if request.method == "POST":
        form = CreateListing(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            starting_bid = form.cleaned_data['starting_bid']
            image = form.cleaned_data['image']
            category = form.cleaned_data['category']

            Auction_Listing.objects.create(seller=user, title=title, description=description,
                                           starting_bid=starting_bid, image=image, category=category)
            return redirect("index")
    else:
        form = CreateListing()

    return render(request, "auctions/add_listing.html", {
        "form": form
    })
# This updated version uses a Django form called CreateListing, which should be created in a separate forms.py file in the same directory as the view. The form handles the validation of the form data and makes it easier to manipulate the data before it is saved to the database.
