from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/",views.listing,name="create"),
    path("category/",views.categoryPage,name="categoryPage"),
    path("listingItem/<int:id>",views.listingItem,name="listingItem"),
    path("add/<int:id>",views.add,name="addToWatchList"),
    path("remove/<int:id>",views.remove,name="removeFromWatchList"),
    path("watchList",views.watchList,name="watchList"),  
    path("comment/<int:id>",views.addComment,name="addComment"),
    path("addBid/<int:id>",views.addBid,name="addBid"),
    path("closeAuction/<int:id>",views.closeAuction,name="closeAuction")
]
 