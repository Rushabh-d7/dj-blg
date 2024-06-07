from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('post/<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('create/', views.CreatePost.as_view(), name='create_blog'),
    path('post/<slug:slug>/delete/', views.DeletePost.as_view(), name='delete_post'),
    path('comment/<int:pk>/delete/', views.DeleteComment.as_view(), name='delete_comment'),

]
