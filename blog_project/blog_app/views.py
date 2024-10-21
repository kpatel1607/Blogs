from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Blog
from .serializers import BlogSerializer, UserSerializer
from rest_framework.parsers import FormParser, MultiPartParser
from django.core.cache import cache
import json


class ExportBlogsView(APIView):
    def get(self, request):
        # Fetch all blog data
        blogs = Blog.objects.values('id', 'title', 'content', 'author__name', 'created_at')

        # Convert the QuerySet to a list of dictionaries
        blogs_list = []
        for blog in blogs:
            # Convert datetime to string
            blog['created_at'] = blog['created_at'].isoformat() if blog['created_at'] else None
            blogs_list.append(blog)

        # Store the data in Redis as JSON
        cache.set('exported_blogs', json.dumps(blogs_list), timeout=None)  # No expiration

        # Return a response indicating the data has been cached
        return Response({'message': 'Blogs data cached successfully!', 'count': len(blogs_list)})
    
    
class DownloadBlogsView(APIView):
    def get(self, request):
        # Retrieve the exported data from Redis
        exported_data = cache.get('exported_blogs')

        if exported_data is None:
            return JsonResponse({'error': 'No data found for export.'}, status=404)

        # Set the response to download the data as a JSON file
        response = HttpResponse(exported_data, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="exported_blogs.json"'
        
        return response

# View for listing and creating blogs
class BlogListView(APIView):
    parser_classes = [FormParser, MultiPartParser]
    def get(self, request):
        blogs = Blog.objects.all()  # Fetch all blogs using Django ORM
        return render(request, 'blog_list.html', {'blogs': blogs})

    def post(self, request):
        print(request.POST)  # For debugging

        # Handle form submission
        title = request.POST.get('title')
        content = request.POST.get('content')
        author_id = request.POST.get('author')

        if title and content and author_id:
            try:
                author = User.objects.get(pk=author_id)  # Fetch the author using Django ORM
                blog = Blog(title=title, content=content, author=author)
                blog.save()
                return redirect('blog-list')  # Redirect to the blog list after saving
            except User.DoesNotExist:
                return render(request, 'blog_list.html', {'blogs': Blog.objects.all(), 'error': 'Author not found.'})
            except Exception as e:
                print(f"Error creating blog: {e}")
                return render(request, 'blog_list.html', {'blogs': Blog.objects.all(), 'error': 'Error creating blog.'})
        else:
            return render(request, 'blog_list.html', {'blogs': Blog.objects.all(), 'error': 'Invalid form submission.'})

# View for blog details, update, and delete
class BlogDetailView(APIView):
    parser_classes = [FormParser, MultiPartParser]
    def get(self, request, blog_id):
        blog = get_object_or_404(Blog, pk=blog_id)  # Fetch the blog using Django ORM
        return render(request, 'blog_detail.html', {'blog': blog})

    def post(self, request, blog_id):
        print("Received POST request with data:", request.POST)

        # Handle update or delete based on the request data
        if request.POST.get('_method') == 'PUT':
            return self.put(request, blog_id)
        elif request.POST.get('_method') == 'DELETE':
            return self.delete(request, blog_id)

        return Response({'error': 'Invalid method'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, blog_id):
        blog = get_object_or_404(Blog, pk=blog_id)

        title = request.POST.get('title')  # Use POST data here
        content = request.POST.get('content')
        if title and content:
            blog.title = title
            blog.content = content
            blog.save()
            return Response(BlogSerializer(blog).data, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, blog_id):
        blog = get_object_or_404(Blog, pk=blog_id)
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  # Return no content status for successful deletion
    
    
class UserListView(APIView):
    parser_classes = [FormParser, MultiPartParser]

    def get(self, request):
        users = User.objects.all()  # Fetch all users using Django ORM
        return render(request, 'user_list.html', {'users': users})

    def post(self, request):
        # Use request.POST for form data
        data = request.POST

        # Pass data to the serializer
        serializer = UserSerializer(data=data)

        if serializer.is_valid():
            try:
                # Create user using Django ORM
                User.objects.create(
                    name=serializer.validated_data['name'],
                    email=serializer.validated_data['email']
                )
                return redirect('user-list')  # Redirect after successful creation
            except Exception as e:
                # Log the error for debugging (optional)
                print(f"Error creating user: {e}")
                # Handle the error and re-render the form with a general error message
                users = User.objects.all()  # Fetch the current user list
                return render(request, 'user_list.html', {
                    'users': users,
                    'error': 'An error occurred while creating the user. Please try again.'
                })
        else:
            # Handle invalid form data and re-render form with errors
            users = User.objects.all()  # Fetch the current user list
            return render(request, 'user_list.html', {
                'users': users,
                'error': 'Invalid form submission.',  # Generic error message
                'field_errors': serializer.errors  # Detailed field errors for debugging
            })
