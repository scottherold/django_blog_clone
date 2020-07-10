from django import forms
from blog.models import Post,Comment

# Create your forms here.
class PostForm(forms.ModelForm):
    """Form for the Post model"""
    class Meta():
        """Meta information to be used by the ModelForm class

        Attributes:
            model (Post): The blog.models.Post class to map the form's data.
            fields (tuple): The fields from the model attribute that will be
            accessible in the form.
            widgets (dict): Applies attributes (such as CSS class names) to the
            'fields' provided in the fields attribute.
        """
        model = Post
        fields = ('author','title','text')

        widgets = {
            'title':forms.TextInput(attrs={'class':'textinput'}),
            'text':forms.TextArea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }


class CommentForm(forms.ModelForm):
    """Form for the Comment model"""
    class Meta():
        """Meta information to be used by the ModelForm class

        Attributes:
            model (Comment): The blog.models.Post class to map the form's data.
            fields (tuple): The fields from the model attribute that will be
            accessible in the form.
            widgets (dict): Applies attributes (such as CSS class names) to the
            'fields' provided in the fields attribute.
        """
        model = Comment
        fields = ('author','text')

        widgets = {
            'author':forms.TextInput(attrs={'class':'textinput'}),
            'text':forms.TextArea(attrs={'class':'editable medium-editor-textarea'})
        }