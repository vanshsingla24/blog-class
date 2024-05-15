from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import login, logout

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from django.views.generic import View, FormView, TemplateView, ListView, DetailView, CreateView, UpdateView, RedirectView

from blog.models import Blog
from blog.forms import BlogForm, CommentForm


class WelcomeView(TemplateView):
    """Welcome View."""
    template_name = 'welcome.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add custom context here
        context['custom_variable'] = 'Custom value here'
        return context


class CustomLoginView(SuccessMessageMixin, LoginView):
    """Custom Login View."""
    success_url = reverse_lazy('home')  
    success_message = "Successfully logged in."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add custom context here
        context['custom_variable'] = 'Custom value here'
        return context


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
        queryset = Blog.objects.all()
        
        # Check if tags are provided in the request parameters
        tags = self.request.GET.get('tag')
        if tags:
            queryset = queryset.filter(tags__name__in=tags)
            print(queryset)
        
        queryset = queryset.order_by('-created_at')
        
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


class BlogsView(ListView):
    """Blogs View."""
    model = Blog
    template_name = 'blogs.html'
    context_object_name = 'blogs'
    paginate_by = 5


class ViewBlogView(SuccessMessageMixin, DetailView):
    """View Blog View after log in"""
    model = Blog
    template_name = 'view_blog.html'
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
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
            return redirect('view_blog', pk=blog.pk)  # Redirect to the same page or wherever appropriate
        else:
            # Handle invalid form submission
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


class ViewBlogsView(DetailView):
    """View Blogs View without log in"""
    model = Blog
    template_name = 'view_blogs.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all() 
        return context


class LikeBlogView(LoginRequiredMixin, RedirectView, SuccessMessageMixin):
    """Like Blog View."""
    def get_redirect_url(self, *args, **kwargs):
        blog = get_object_or_404(Blog, pk=self.kwargs['pk'])
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
        blog = get_object_or_404(Blog, pk=self.kwargs['pk'])
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
