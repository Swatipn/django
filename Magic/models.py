from django.db import models

# Create your models here.
class Contact(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    phone=models.IntegerField()
    description=models.TextField(max_length=150)


    def __str__(self):
        return self.email + " by " + self.name

class BlogPosts(models.Model):
    sno=models.AutoField(primary_key=True)
    title=models.CharField(max_length=100)
    content=models.TextField()
    author=models.CharField(max_length=100)
    img=models.ImageField(upload_to='blog', blank=True , null=True)
    timestamp=models.DateField(auto_now_add=True , blank=True)


    def __str__(self):
        return self.author
    