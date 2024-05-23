from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import login, logout

from django.contrib.auth.models import User
from django.db.models import Count, Prefetch
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from django.views.generic import View, FormView, TemplateView, ListView, DetailView, CreateView, UpdateView, RedirectView

from blog.models import Blog, Comment
from blog.forms import BlogForm, CommentForm

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from blog.serializer import BlogSerializer, CommentSerializer


class BlogList(APIView):
    """
    List all blogs or create a new blog.
    """
    def get(self, request, format=None):
        blogs = Blog.objects.select_related('user').prefetch_related('tags', 'likes', 'dislikes', 'comments__user')
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogDetail(APIView):
    """
    Retrieve, update or delete a blog post.
    """
    def get_object(self, pk):
        try:
            return Blog.objects.select_related('user').prefetch_related('tags', 'likes', 'dislikes', 'comments__user').get(pk=pk)
        except Blog.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        blog = self.get_object(pk)
        if blog is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BlogSerializer(blog)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        '''For entire modification'''
        blog = self.get_object(pk)
        if blog is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BlogSerializer(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk, format=None):
        '''For partial modifications'''
        blog = self.get_object(pk)
        if blog is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BlogSerializer(blog, data=request.data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        blog = self.get_object(pk)
        if blog is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentList(APIView):
    """
    List all comments or create a new comment.
    """
    def get(self, request, format=None):
        comments = Comment.objects.select_related('user', 'blog')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(APIView):
    """
    Retrieve, update or delete a comment.
    """
    def get_object(self, pk):
        try:
            return Comment.objects.select_related('user', 'blog').get(pk=pk)
        except Comment.DoesNotExist:
            return None

    def get(self, request, pk, format=None):
        comment = self.get_object(pk)
        if comment is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        '''For full modification'''
        comment = self.get_object(pk)
        if comment is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        '''For partial modifications'''
        comment = self.get_object(pk)
        if comment is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(comment, data=request.data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        comment = self.get_object(pk)
        if comment is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class WelcomeView(TemplateView):
    """Welcome View."""
    template_name = 'welcome.html'


class CustomLoginView(SuccessMessageMixin, LoginView):
    """Custom Login View."""
    success_url = reverse_lazy('home')  
    success_message = "Successfully logged in."


class LogoutView(SuccessMessageMixin, RedirectView):
    """Logout View."""
    url = reverse_lazy('welcome')
    success_message = "Successfully logged out."

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        messages.success(self.request, self.success_message)
        return super().get_redirect_url(*args, **kwargs)
    

class SignupView(SuccessMessageMixin, FormView):
    """Signup View."""
    template_name = 'signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    success_message = "Account created successfully. Please log in."

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error creating account. Please try again.')
        return super().form_invalid(form)


class HomeView(ListView):
    """Home View."""
    model = Blog
    template_name = 'home.html'
    context_object_name = 'blogs'
    paginate_by = 5

    def get_queryset(self):
        queryset = Blog.objects.select_related('user').annotate(
            likes_count=Count('likes'),
            dislikes_count=Count('dislikes')
        ).order_by('-created_at')

        tags = self.request.GET.get('tag')
        if tags:
            queryset = queryset.filter(tags__name__in=tags)

        # Prefetch likes and dislikes related to users
        queryset = queryset.prefetch_related(
            Prefetch('likes', queryset=User.objects.only('id')),
            Prefetch('dislikes', queryset=User.objects.only('id'))
        )

        return queryset
    

class CreateBlogView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Create Blog View."""
    model = Blog
    form_class = BlogForm
    template_name = 'create_blog.html'
    success_url = '/accounts/profile'
    success_message = "Blog created successfully."

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ViewBlogView(SuccessMessageMixin, DetailView):
    """View Blog View after log in"""
    model = Blog
    template_name = 'view_blog.html'
    context_object_name = 'blog'

    def get_queryset(self):
        queryset = Blog.objects.select_related('user')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = self.object

        # Prefetch comments with related users
        comments_with_users = blog.comments.select_related('user')

        context['comments'] = comments_with_users
        return context

    def post(self, request, *args, **kwargs):
        blog = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.user = request.user
            comment.save()
            success_message = "Comment added successfully."
            return redirect('view_blog', pk=blog.pk)
        else:
            # Handle invalid form submission
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


class LikeBlogView(LoginRequiredMixin, RedirectView, SuccessMessageMixin):
    """Like Blog View."""
    def get_redirect_url(self, *args, **kwargs):
        blog = get_object_or_404(Blog.objects.prefetch_related('likes'), pk=self.kwargs['pk'])
        if self.request.user not in blog.likes.all():
            blog.likes.add(self.request.user)
            self.success_message = 'Blog liked successfully.'
        else:
            self.success_message = 'You have already liked this blog.'
        messages.success(self.request, self.success_message)
        return reverse_lazy('home')


class DislikeBlogView(LoginRequiredMixin, RedirectView, SuccessMessageMixin):
    """Dislike Blog View."""
    def get_redirect_url(self, *args, **kwargs):
        blog = get_object_or_404(Blog.objects.prefetch_related('dislikes'), pk=self.kwargs['pk'])
        if self.request.user not in blog.dislikes.all():
            blog.dislikes.add(self.request.user)
            self.success_message = 'Blog disliked successfully.'
        else:
            self.success_message = 'You have already disliked this blog.'
        messages.success(self.request, self.success_message)
        return reverse_lazy('home')


class EditBlogView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Edit Blog View."""
    model = Blog
    form_class = BlogForm
    template_name = 'edit_blog.html'
    success_url = reverse_lazy('view_blog')  
    success_message = "Blog updated successfully."

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class DeleteBlogView(LoginRequiredMixin, SuccessMessageMixin, View):
    """Delete Blog View."""
    success_message = "Blog deleted successfully."

    def get_queryset(self):
        return Blog.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        blog = self.get_queryset().get(pk=kwargs['pk'])

        blog.delete()

        self.success_message = self.success_message.format(blog.title)
        return redirect('home')

    def get_success_message(self, cleaned_data):
        return self.success_message
