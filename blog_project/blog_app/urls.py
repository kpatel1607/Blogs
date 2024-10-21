from django.urls import path
from .views import BlogListView, BlogDetailView, DownloadBlogsView, ExportBlogsView, UserListView

urlpatterns = [
    path('blogs/', BlogListView.as_view(), name='blog-list'),
    path('blogs/<str:blog_id>/', BlogDetailView.as_view(), name='blog-detail'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('export-blogs/', ExportBlogsView.as_view(), name='export-blogs'),
    path('download-blogs/', DownloadBlogsView.as_view(), name='download-blogs'),
]
