from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User,Category,Listing,Comment,Bid


def index(request):
    activeListings=Listing.objects.filter(isActive=True)
    AllCategories=Category.objects.all()
    return render(request, "auctions/index.html",{
        "Listings":activeListings,
        "category":AllCategories
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
    return HttpResponseRedirect(reverse('index'))


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
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "auctions/register.html")

def listing(request):
    #Using Get method we are displaying the form to create
    if request.method=="GET":
        CategoriesItem=Category.objects.all()
        return render(request,"auctions/create.html",{
            "category":CategoriesItem
        })
    else:
        #In this POST method we take details from the user insert them into Django Admin Database
        #step1:Retreving Details from the user
        title=request.POST["title"]
        description=request.POST["description"]
        imageUrl=request.POST["imageUrl"]
        price=request.POST["price"]
        category=request.POST["category"]
        #user detils
        currUser=request.user
        #Retrieving category data from models.py
        categoryData=Category.objects.get(categoryName=category)
        #Bid object
        bidObj=Bid(bid=int(price),user=currUser)
        bidObj.save()
        #step2:Creating a new Listing object for the class i.e created in models.py 
        listing=Listing(
            title=title,
            description=description,
            imageurl=imageUrl,
            price=bidObj,
            category=categoryData,
            owner=currUser
        )
        listing.save()
        return HttpResponseRedirect(reverse('index'))
def categoryPage(request):
    if request.method=="POST":
        category_page=request.POST["category"]
        category=Category.objects.get(categoryName=category_page)
        #similar to index
        activeListings=Listing.objects.filter(isActive=True,category=category)
        AllCategories=Category.objects.all()
        return render(request, "auctions/index.html",{
            "Listings":activeListings,
            "category":AllCategories
        })
def listingItem(request,id):
    listingData=Listing.objects.get(pk=id)
    isListingInWatchList=request.user in listingData.watchList.all()
    #Checking from the details of product whether the user is in the WatchList or not
    allComments=Comment.objects.filter(listing=listingData)
    isOwner=request.user.username==listingData.owner.username
    #comparing the user is owner or not
    return render(request,"auctions/listingItem.html",{
        "listingItem":listingData,
        "isListingInWatchList":isListingInWatchList,
        "comments":allComments,
        "id":id,
        "isOwner":isOwner
    })
def add(request,id):
    listingData=Listing.objects.get(pk=id)
    currUser=request.user
    listingData.watchList.add(currUser)
    #Spacing is important after id i.e after args
    return HttpResponseRedirect(reverse('listingItem',args=(id, )))
def remove(request,id):
    listingData=Listing.objects.get(pk=id)
    currUser=request.user
    listingData.watchList.remove(currUser)
    #Spacing is important after id i.e after args
    return HttpResponseRedirect(reverse('listingItem',args=(id, )))
def watchList(request):
    #Step1:Get user details
    currUser=request.user
    watchList=currUser.watchList.all()
    return render(request,"auctions/watchList.html",{
        "WatchListItem":watchList
    })
def addComment(request,id):
    currUser=request.user
    listingData=Listing.objects.get(pk=id)
    message=request.POST['comment']
    #same as adding a newflight
    newComment=Comment(
        author=currUser,
        listing=listingData,
        message=message
    )
    newComment.save()
    return HttpResponseRedirect(reverse('listingItem',args=(id, )))
def addBid(request,id):
    newBid=request.POST['addBid']
    listingData=Listing.objects.get(pk=id)
    isOwner=request.user.username==listingData.owner.username
    isListingInWatchList=request.user in listingData.watchList.all()
    #Checking from the details of product whether the user is in the WatchList or not
    allComments=Comment.objects.filter(listing=listingData)
    if int(newBid)>listingData.price.bid:
        updateBid=Bid(user=request.user,bid=int(newBid))
        updateBid.save()
        listingData.price=updateBid
        listingData.save()
        return render(request,"auctions/listingItem.html",{
            "listingItem":listingData,
            "message":"Bid was updated sucessfully",
            "updated":True,
            "isListingInWatchList":isListingInWatchList,
            "comments":allComments,
            "isOwner":isOwner
            
        })
    else:
            return render(request,"auctions/listingItem.html",{
            "listingItem":listingData,
            "message":"Bid was unsucessfull",
            "updated":False,
            "isListingInWatchList":isListingInWatchList,
            "comments":allComments,
            "isOwner":isOwner
        })
def closeAuction(request,id):
    listingData=Listing.objects.get(pk=id)
    listingData.isActive=False
    #so,that this object cannot be displayed in active listings
    listingData.save()
    isListingInWatchList=request.user in listingData.watchList.all()
    #Checking from the details of product whether the user is in the WatchList or not
    allComments=Comment.objects.filter(listing=listingData)
    isOwner=request.user.username==listingData.owner.username
    #comparing the user is owner or not
    return render(request,"auctions/listingItem.html",{
        "listingItem":listingData,
        "isListingInWatchList":isListingInWatchList,
        "comments":allComments,
        "id":id,
        "isOwner":isOwner,
        "closeMessage":"You Have Closed Your Auction"
    })








