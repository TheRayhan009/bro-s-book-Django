from django.db import models
from autoslug import AutoSlugField
      
class UserPost(models.Model):
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=30)
    user_name=models.CharField(max_length=50)
    post_up_date=models.DateField(auto_now=True)
    post_txt=models.CharField(max_length=15000)
    user_image = models.ImageField(upload_to="", blank=True, null=True, default="")
    post_image=models.ImageField(upload_to="", blank=True, null=True, default="")
    post_slug = AutoSlugField(populate_from= "generate_slug",unique=True ,null=True)
    
    def generate_slug(self):
        return f'{self.user_name}-{self.post_txt[:30]}'
    
    def __str__(self):
        return self.post_txt


class SBUser(models.Model):
    fname=models.CharField(max_length=50)
    lname=models.CharField(max_length=50)
    email=models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    dateOfBirthOfUser=models.CharField(max_length=20)
    profileImage=models.ImageField(upload_to="" , unique=True ,default="",blank=True)
    # post_user_liked_id= PickledObjectField(default=dict)
    # bio=models.CharField(max_length=5000,default="",null=True,unique=False)


class LikeOfUser(models.Model):
    user_name_Of_liked_user=models.CharField(max_length=200)
    liked_post_id=models.CharField(max_length=100000)

class CommentsOfUser(models.Model):
    user_name_Of_liked_user=models.CharField(max_length=200 ,blank=True)
    commented_post_id=models.CharField(max_length=100000,blank=True)
    comment_txt=models.CharField(max_length=1000000,blank=True)
    # profileImage=models.ImageField(upload_to="" , unique=True ,default="",blank=True)
    
    
class UserFollowData(models.Model):
    following_user=models.CharField(max_length=200 ,blank=True)
    followed_user=models.CharField(max_length=200 ,blank=True)
    flwOrNot=models.CharField(max_length=10 ,blank=True)