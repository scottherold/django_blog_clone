from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    """A data model for a blog post. This model is used when creating a new
    blog and saving it to the database, or when retrieving a blog's data from
    the database.

    Attributes:
        author (auth.User): The User model that created the blog post.
        title (str): The title of the blog post. Max characters is set to 200.
        text (str): The text of the blog post.
        created_date (datetime): The date that the blog post was created.
        published_date (datetime): The date the blog was published.
    """
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True,null=True)

    def publish(self):
        """Sets the published_date attribute using the timezone.now() function
        from the django.utils library and saves the updated Post data in the
        database.
        """
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        """Filters and returns the comments attribute if the approved_comments
        field is equal to True.
        """
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        """Routes the client to the post_detail route, and passes the the Post
        instance's Primary Key as a keyword argument
        """
        return reverse("post_detail", kwargs={'pk':self.pk})

    def __str__(self):
        """String representation of the Post model instance. Returns the title
        attribute as a representation of the model instance.
        """
        return self.title


class Comment(models.Model):
    """A data model for a blog post comment. This model is used when creating a
    new blog post comment and saving it to the database, or when retrieving a
    blog post comment's data from the database.

    Attributes:
        post (blog.Post): The Post model on which the comment was made.
        author (str): The name provided for the author of the comment.
        text (str): The text of the comment.
        created_date (datetime): The date that the comment was created.
        approved (bool): Whether the comment has been approved by the Post
        author, or not.
    """
    post = models.ForeignKey('blog.post', related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        """Sets the approved_comment attribute to True and saves the updated
        Comment data in the database.
        """
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        """Routes the client to the posts route"""
        return reverse("post_list")

    def __str__(self):
        """String representation of the Comment model instance. Returns the 
        text attribute as a representation of the model instance.
        """
        return self.text