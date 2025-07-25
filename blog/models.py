from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    category_name=models.CharField(max_length=50,unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural='Categories'
    def __str__(self):
        return self.category_name

STATUS_CHOICES=(
    ("Draft","Draft"),
    ("Published","Published")
)    
class Blog(models.Model):
    title=models.CharField(max_length=100)
    slug=models.SlugField(max_length=150,unique=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    featured_image=models.ImageField(upload_to='upload/%Y/%M/%d')
    short_description=models.TextField(max_length=2000)
    blog_body=models.TextField(max_length=5000)
    status=models.CharField(max_length=50,choices=STATUS_CHOICES,default='Draft')
    is_featured=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE)
    comment=models.TextField(max_length=250)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.comment
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, related_name='likes', on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user', 'blog')
    def __str__(self):
        return f'{self.user.username} likes {self.blog.title}'
    
class Dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, related_name='dislikes', on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user', 'blog')

    def __str__(self):
        return f'{self.user.username} dislikes {self.blog.title}'
