from django import forms
from blog.models import Blog, Comment


class BlogForm(forms.ModelForm):
    
    class Meta:
        model = Blog
        fields = ['title', 'content', 'tags']


class CommentForm(forms.ModelForm):

    class Meta:
        
        model = Comment
        fields = ['content']
        labels = {'content': ''}  # Hide label for content field

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({'placeholder': 'Write your comment here...'})