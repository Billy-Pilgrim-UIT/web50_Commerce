from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms

from .models import User, Listing, Category, Bids, Comments, Watchlist

class CreateListing(forms.Form):
    """ Django Form to Create a new Listing"""
    title = forms.CharField(label="Give your listing a descriptive title:")
    description = forms.CharField(label="Item Description:", widget=forms.Textarea,)
    startingbid = forms.DecimalField(label="Starting Bid: $", decimal_places=2)
    imageURL = forms.URLField(label="Image URL:", required=False)

    # retrieving list of categories and storing in a list of tuples.
    categories = Category.objects.all()
    CHOICES = []

    for category in categories:
        cat_tuple = (category.id, category.category)
        CHOICES.append(cat_tuple)

    category = forms.ChoiceField(widget=forms.RadioSelect,
        choices = CHOICES,
        initial = 'No Category Specified'
    )



class NewComment(forms.Form):
    """ Django Form to Add a NewComment """
    comment = forms.CharField(label="Add a Public Comment:", widget=forms.Textarea,)



def index(request):
    watchlist = False
    listings = Listing.objects.all().order_by('-id')
    return render(request, "auctions/index.html", {
        "listings": listings,
        "watchlist": watchlist
    })



def categories(request):
    if request.method == "POST":
        print("HERE")
        return redirect('/')

    else:
        # need to render a html page that shows a hyperlinked list of categories.

        # retrieve categories from Category database
        categories = Category.objects.all()

        return render(request, "auctions/categories.html", {
            "categories": categories
        })


def comment(request):

    form = NewComment(request.POST)
    listing_id = request.POST.get('id')

    if form.is_valid():

        #retrieve form values
        comment = request.POST.get('comment')
        commenter = request.user.username

        # save new Comment to database
        newComment = Comments(comment=comment, commenter=commenter, listing_id=listing_id)
        newComment.save()

    # reload Listing (showing new comment)
    address = 'listing/' + str(listing_id)
    return redirect(address)



def create(request):
    """Create a New Listing form"""
    if request.method == 'GET':
        form = CreateListing()
        return render(request, "auctions/create.html", {
            "form": form
        })

    # Save New Listing
    else:
        form = CreateListing(request.POST)

        #check whether form is valid
        if form.is_valid():

            #assign each individual form field to a variable.
            title = request.POST.get('title')
            description = request.POST.get('description')
            imageURL = request.POST.get('imageURL')
            price = request.POST.get('startingbid')
            category = request.POST.get('category')
            listed_by = request.user.username

            newListing = Listing(title=title, description=description,
                imageURL=imageURL, price=price, category=category, listed_by=listed_by )
            newListing.save()

            # Redirect to Listing Page so that user can see their new listing.
            redirectURL = 'listing/' + str(newListing.id)
            return redirect(redirectURL)

    ## Should actually redirect to listing page showing new listing.
    return redirect('/')


def list_item(request, item):
    """ retrieve item from database using unique id """
    item_entry = Listing.objects.get(id=int(item))

    #initialise variables
    yourbid = ""
    on_Watchlist = None
    creator = None

    #construct num_bids sentence
    if item_entry.num_bids == 1:
        bids_sentence = "There has been 1 bid on this item."
    else:
        bids_sentence = "There have been " + str(item_entry.num_bids) + " bids on this item."


    # determine if user is logged in
    if request.user.is_authenticated:
        logged_in = True

        # retrieve user name
        username = request.user.username

        # determine if current user is highest bidder
        if(item_entry.num_bids > 0):
            highest = Bids.objects.filter(listing_id=item).order_by('bid')[0]

            if (highest.bidder == username):
                yourbid = "Your bid is the current bid."
            else:
                yourbid = ""
        else:
                yourbid = ""

        # determine whether current user is creator of listing
        if (item_entry.listed_by == username):
            creator = True
        else:
            creator = False
    else:
        logged_in = False

    # establish minimum acceptable new bid price
    min_newbid = float(item_entry.price) + 0.01

    # retrieve category
    category = Category.objects.get(id=item_entry.category)

    # Add a Comment Form
    form = NewComment()

    # retrieve all Comments
    comments = Comments.objects.filter(listing_id=item)

    # determine whether user has already added item to their watchlist
    if logged_in == True:
        if Watchlist.objects.filter(listing_id=item, user=username).count() == 0:
            on_Watchlist = False
        else:
            on_Watchlist = True

    # then pass values into a html page.
    return render(request, "auctions/listing.html", {
        "item": item_entry,
        "category": category,
        "bids_sentence": bids_sentence,
        "logged_in": logged_in,
        "min_newbid": min_newbid,
        "yourbid": yourbid,
        "creator": creator,
        "form": form,
        "comments": comments,
        "on_Watchlist": on_Watchlist
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


def new_bid(request):
    if request.method == "POST":
        # get bid amount and lookup listing by its id
        bid = request.POST["new_bid"]
        listing_id = request.POST["id"]
        listing = Listing.objects.get(id=listing_id)

        # store new price in Listing table
        listing.price = bid
        num_bids = listing.num_bids + 1
        listing.num_bids = num_bids
        listing.save(update_fields=['price','num_bids'])


        # store bid in Bids table
        bidder = request.user.username
        bid_details = Bids(bid=bid, bidder=bidder, listing_id=listing_id)
        bid_details.save()

        #reload listing page showing new price
        redirectURL = '/' + str(listing_id)
        return redirect(redirectURL)

    return render(request, "auctions/index.html")



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

def watchlist(request):
    if request.method == "POST":
        listing_id = request.POST.get('id')

        #retrieve username
        user = request.user.username

        # save to Watchlist database
        if request.POST.get('add_remove') == "Add":

            newWatch = Watchlist(user=user, listing_id=listing_id)
            newWatch.save()

        # remove from Watchlist database
        elif request.POST.get('add_remove') == "Remove":

            deleteWatch = Watchlist.objects.filter(user=user, listing_id=listing_id)
            deleteWatch.delete()


        # reload Listing
        address = 'listing/' + str(listing_id)
        return redirect(address)

    else:
        # need to render a html page that shows only the listings on the watchlist.
        watchlist = True

        #retrieve username
        user = request.user.username

        # retrieve listings for items on Watchlist
        watchlist_ids = []
        items_onlist = Watchlist.objects.filter(user=user)
        print(items_onlist)
        for list_item in items_onlist:
            watchlist_ids.append(list_item.listing_id)
            print(watchlist_ids)

        listings = Listing.objects.filter(id__in=watchlist_ids).order_by('-id')

        print(listings)

        return render(request, "auctions/index.html", {
            "listings": listings,
            "watchlist": watchlist
        })
