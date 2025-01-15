from django.contrib import admin
from data.models import SBUser,UserPost,LikeOfUser,CommentsOfUser,UserFollowData,UserMessageData,VoiceMessage

admin.site.register(UserPost)
admin.site.register(SBUser)
admin.site.register(LikeOfUser)
admin.site.register(CommentsOfUser)
admin.site.register(UserFollowData)
admin.site.register(UserMessageData)
admin.site.register(VoiceMessage)
