from django.contrib import admin
from data.models import SBUser,UserPost,LikeOfUser,CommentsOfUser

admin.site.register(UserPost)
admin.site.register(SBUser)
admin.site.register(LikeOfUser)
admin.site.register(CommentsOfUser)
