from django.contrib import admin
from post.models import Post,Like,Comment
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ['user','post_name','post_file_name','time_date','dsec']


admin.site.register(Post, PostAdmin)

class LikeAdmin(admin.ModelAdmin):
    model = Like
    list_display = ['post','user','status']


admin.site.register(Like, LikeAdmin)


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ['post','user','status','message']


admin.site.register(Comment, CommentAdmin)
