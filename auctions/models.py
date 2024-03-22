from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
class Category(models.Model):
    categoryName=models.CharField(max_length=40)
    def __str__(self):
        return f"{self.categoryName}"

class Bid(models.Model):
    bid=models.IntegerField(default=0)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="userbid")



class Listing(models.Model):

    title=models.CharField(max_length=30)
    description=models.CharField(max_length=600)
    imageurl=models.URLField(max_length=5000)
    price=models.ForeignKey(Bid,on_delete=models.CASCADE,null=True,blank=True,related_name="BidPrice")
    isActive=models.BooleanField(default=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="user")
    category=models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True,related_name="category")
    watchList=models.ManyToManyField(User,blank=True,null=True,related_name="watchList")
    def __str__(self):
        return f"{self.title}"
class Comment(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="AuthorComment")
    listing=models.ForeignKey(Listing,on_delete=models.CASCADE,null=True,blank=True,related_name="ListingObject")
    message=models.CharField(max_length=200)

    def __str__(self):
        return f"{self.author} comment on {self.listing}"