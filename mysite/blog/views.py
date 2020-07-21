from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView, TemplateView,
                                    DetailView, CreateView,
                                    UpdateView, DeleteView)

# Create your views here.
class AboutView(TemplateView):
    """A Template View Class for the About webpage.

    Attributes:
        template_name (str): The string for the file location of the template
        file for the class to render.
    """
    template_name = 'about.html'


class PostListView(ListView):
    """A ListView Class for a list of Post model objects in the database.
    
    Attributes:
        model (Class): The specific Model class to be used to map to
        map to the ListView class for database querying.
    """
    model = Post

    def get_queryset(self):
        """Returns all of the Post Model objects found in the database. Filters
        the posts by a post time of less than or equal to now. Orders the Post
        Model objects in descending order by 'published date'."""
        return Post.objects.filter(publish_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    """A DetailView class for a specific Post Model data object.

    Attributes:
        model (Class): The specific Model class to be used to map to
        map to the DetailView class for database querying.
    """
    model = Post


class CreatePostView(LoginRequiredMixin, CreateView):
    """A CreateView class for a specific Post Model data object. This class
    utlizes the LoginRequiredMixin to authenticate a user prior to allowing
    write access to the database.

    Attributes:
        login_url (str): The route to send the client if a User is not logged
        in.
        redirect_field_name (str): The route to send the client after a
        write (create) request to the database.
        form_Class (Class): The specific ModelForm class that can be
        used to map data from the client, to the Model mapped to the class.
        model (Class): The specific Model class to be used to map to
        map to the CreateView class for database querying.
    """
    login_url ='/login/'
    redirect_field_name ='blog/post_detail.html'
    form_class = PostForm
    model = Post


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """An UpdateView class for a specific Post Model data object. This class
    utlizes the LoginRequiredMixin to authenticate a user prior to allowing
    write access to the database.

    Attributes:
        login_url (str): The route to send the client if a User is not logged
        in.
        redirect_field_name (str): The route to send the client after a
        write (update) request to the database.
        form_Class (Class): The specific ModelForm class that can be
        used to map data from the client, to the Model mapped to the class.
        model (Class): The specific Model class to be used to map to
        map to the UpdateView class for database querying.
    """
    login_url ='/login/'
    redirect_field_name ='blog/post_detail.html'
    form_class = PostForm
    model = Post


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """A DeleteView class for a specific Post Model data object.

    Attributes:
        model (Class): The specific Model class to be used to map to
        map to the DeleteView class for database querying.
        success_url (function): Uses the reverse_lazy function to wait until 
        the delete from the database is confirmed, before routing the client to
        the post_list namespace from blog/urls.py.
    """
    model = Post
    success_url = reverse_lazy('post_list')


class DraftListView(LoginRequiredMixin, ListView):
    """An ListView class for a specific Post Model data object. This class
    utlizes the LoginRequiredMixin to authenticate a user prior to allowing
    read access to the database.

    Attributes:
        login_url (str): The route to send the client if a User is not logged
        in.
        redirect_field_name (str): The route to send the client after a
        read (select) request to the database.
        model (Class): The specific Model class to be used to map to
        map to the ListView class for database querying.
    """
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        """Returns all of the Post Model objects found in the database. Filters
        the for Post data that have a published date of null (not published).
        Orders the Post Model object data in ascending order by 'created date'.
        """
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


##################################################
################ Function Views ##################
##################################################
@login_required
def post_publish(request, pk):
    """Requires an authenticated User to be logged in.
    
    Returns and redirects the client to blog/urls.py post_detail namespace
    route after running the Post class's publish function if a Post Model
    object data is located in the database using the primary key argument.
    
    Keyword arguments:
    request -- the HTTP request type.
    pk -- the primary key provided by the url route.
    """
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
def add_comment_to_post(request, pk):
    """Requires an authenticated User to be logged in.
    
    Returns and redirects the client to blog/urls.py post_detail namespace
    route if a Post Model object data is located in the database using the
    primary key argument and the HTTP request is type post.

    Otherwise, returns the http request passed as an argument and
    blog/comment_form.html with a blank CommentForm() as context.
    
    Keyword arguments:
    request -- the HTTP request type.
    pk -- the primary key provided by the url route.
    """
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})


@login_required
def comment_approve(request, pk):
    """Requires an authenticated User to be logged in.

    Returns and redirects the client to blog/urls.py post_detail namespace
    route after running the Comment class's approve function if a Comment Model
    object data is located in the database using the primary key argument.

    Keyword arguments:
    request -- the HTTP request type.
    pk -- the primary key provided by the url route.
    """
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    """Requires an authenticated User to be logged in.

    Returns and redirects the client to blog/urls.py post_detail namespace
    route using the instantiated Comment Model's Post Model primary key after
    running the Comment class's delete function if a Comment Model object data
    is located in the database using the primary key argument.

    Keyword arguments:
    request -- the HTTP request type.
    pk -- the primary key provided by the url route.
    """
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)