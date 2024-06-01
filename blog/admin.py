from django.contrib import admin
from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug','created_on')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'content', 'created_on')
    search_fields = ['author__username', 'content']
    list_filter = ('created_on', 'author')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
