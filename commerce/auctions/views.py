from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from .models import User, Auction_Listing, Bid, Comment, Watchlist
from .forms import CreateListing, BidListing


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

    # print(f"current user is {takeha}")
    form = BidListing(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            bid = form.cleaned_data["bid"]

            listing = Auction_Listing.objects.get(pk=listing_id)
            if bid > listing.starting_bid and bid > listing.price:
                listing.price = bid
                listing.save()

            else:
                return render(request, "auctions/error.html", {
                    "message": "Bid must be greater than the current price",
                    "code": 403
                })

            new_bid = Bid.objects.create(
                bidder=request.user, bid=bid, listing=listing)
            return render(request, "auctions/view_listing.html", {
                "listing": listing,
                "user_l": request.user,
                "form": form,
                "bid": new_bid

                # "l_items": request.session["l_items"]
            })

        user = request.user
        watchlist = Watchlist.objects.filter(user_w=user)

        list_item = Auction_Listing.objects.get(pk=listing_id)
        check = True
        for w in watchlist:
            if list_item.title == w.list_item.title:
                check = False

        if check == True:
            Watchlist.objects.create(user_w=user, list_item=list_item)

    something = Auction_Listing.objects.get(pk=listing_id)
    # print(something.title)
    return render(request, "auctions/view_listing.html", {
        "listing": something,
        "user_l": request.user,
        "form": form
        # "l_items": request.session["l_items"]
    })


def watchlist(request):
    # print(watch_id)
    if request.method == "POST":
        item_id = request.POST.get("item_id")
        item = Watchlist.objects.get(pk=item_id)
        item.delete()
        return HttpResponseRedirect(reverse("watchlist"))

    return render(request, "auctions/watchlist.html", {
        "items": Watchlist.objects.filter(user_w=request.user)
    })


def category(request):
    listings = Auction_Listing.objects.all()

    categories = []
    for cat in listings:
        if cat.category not in categories:
            categories.append(cat.category)

    return render(request, "auctions/categories.html", {
        "listings": categories
    })


def view_cat(request, category):
    filtered_listings = Auction_Listing.objects.filter(
        category=category)

    # print(filtered_listings)
    return render(request, "auctions/view_cat.html", {
        "listings": filtered_listings
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
