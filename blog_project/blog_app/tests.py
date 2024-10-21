from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Blog, User

class BlogTests(APITestCase):
    def setUp(self):
        # Create a user instance
        self.user = User.objects.create(
            name='Test User',
            email='testuser@example.com'
        )

        # Prepare blog data with the user instance as author
        self.blog_data = {
            'title': 'Test Blog',
            'content': 'This is a test blog post.',
            'author': self.user,  # Assign the user instance here
        }

        # Create a blog instance for further tests
        self.blog = Blog.objects.create(**self.blog_data)
        self.blog_url = reverse('blog-list')
        self.blog_detail_url = reverse('blog-detail', args=[self.blog.id])
    def test_create_blog(self):
        response = self.client.post(self.blog_url, self.blog_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Expect a redirect after successful creation
        self.assertEqual(Blog.objects.count(), 1)  # Check if the blog was created
        self.assertEqual(Blog.objects.get(title='Test Blog').title, 'Test Blog')  # Verify the blog's title

    def test_create_blog_invalid_data(self):
        # Test with missing title
        invalid_data = {
            'content': 'This is a test blog.',
            'author': self.user.id
        }
        response = self.client.post(self.blog_url, invalid_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Expect to render with error
        self.assertContains(response, 'Invalid form submission.')  # Check for error message

        # Test with missing content
        invalid_data = {
            'title': 'Test Blog',
            'author': self.user.id
        }
        response = self.client.post(self.blog_url, invalid_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Expect to render with error
        self.assertContains(response, 'Invalid form submission.')  # Check for error message

    def test_get_blog_list(self):
        response = self.client.get(self.blog_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.blog.title)

    def test_get_blog_detail(self):
        blog_detail_url = reverse('blog-detail', args=[self.blog.id])  # Use the created blog ID
        response = self.client.get(blog_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.blog.title)

    def test_get_non_existing_blog_detail(self):
        response = self.client.get(reverse('blog-detail', args=[9999]))  # Non-existing ID
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_blog(self):
        blog_detail_url = reverse('blog-detail', args=[self.blog.id])  # Use the created blog ID
        updated_data = {
            '_method':'PUT',
            'title': 'Updated Blog',
            'content': 'This is an updated test blog.',
            'author': self.user.id
        }
        response = self.client.post(blog_detail_url, updated_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.blog.refresh_from_db()
        self.assertEqual(self.blog.title, 'Updated Blog')

    def test_update_non_existing_blog(self):
        updated_data = {
            '_method':'PUT',
            'title': 'Updated Blog',
            'content': 'This is an updated test blog.',
            'author': self.user.id
        }
        response = self.client.post(reverse('blog-detail', args=[9999]), updated_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_blog(self):
        blog_detail_url = reverse('blog-detail', args=[self.blog.id])  # Use the created blog ID
        response = self.client.post(blog_detail_url, {'_method': 'DELETE'}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Blog.objects.count(), 0)  # Ensure the blog is deleted

    def test_delete_non_existing_blog(self):
        response = self.client.post(reverse('blog-detail', args=[9999]), {'_method': 'DELETE'}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserTests(APITestCase):

    def setUp(self):
        self.user_data = {
            'name': 'Test User',
            'email': 'test@example.com'
        }
        self.user_url = reverse('user-list')

    def test_create_user(self):
        response = self.client.post(self.user_url, self.user_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # Expect a redirect after successful creation
        self.assertEqual(User.objects.count(), 1)  # Ensure user is created

    def test_create_user_invalid_data(self):
        # Test with missing name
        invalid_data = {
            'email': 'test@example.com'
        }
        response = self.client.post(self.user_url, invalid_data, format='multipart')
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Expect to render with error
        self.assertContains(response, 'Invalid form submission.')  # Check for error message

        # Test with missing email
        invalid_data = {
            'name': 'Test User'
        }
        response = self.client.post(self.user_url, invalid_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Expect to render with error
        self.assertContains(response, 'Invalid form submission.')  # Check for error message


    def test_get_user_list(self):
        self.client.post(self.user_url, self.user_data, format='multipart')
        response = self.client.get(self.user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.user_data['name'])