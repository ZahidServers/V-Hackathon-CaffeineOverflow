from django.db import models
from django.contrib.auth.models import User
STATUS = (
    (0,"Draft"),
    (1,"Publish")
)
class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    img = models.ImageField(upload_to='images/', blank=True)
    virtualtour= models.FileField(upload_to='images/', blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    viewcount=models.IntegerField(default=1,blank=True,null=True)
    tag_let_one = models.CharField(max_length=200, blank=True,null=True, choices=[('Natural', 'Natural'), ('Historical', 'Historical'), ('Industrial', 'Industrial')])
    class Meta:
        ordering = ['-created_on']
    def __str__(self):
        return self.title
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    class Meta:
        ordering = ['created_on']
    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
class DataTracking(models.Model):
    blogtitle=models.CharField(max_length=200)
    country=models.CharField(max_length=200)
    viewcount=models.IntegerField(default=None,blank=True,null=True)
