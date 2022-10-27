from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class BlogPost(models.Model):
    """
    Model for the blog
    """
    title = models.CharField(max_length=260)
    blog_date = models.DateTimeField('Blog Date')
    blog_image = CloudinaryField('image', default='https://res.cloudinary.com/dokp7kv2b/image/upload/v1665433332/laser_main_ld3azo.jpg')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.TextField()

    def __str__(self):
        return self.title
