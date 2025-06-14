from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    slug = models.SlugField()
    date= models.DateTimeField(auto_now_add=True)
    # Method to return the string representation of the model
    def __str__(self):
        return self.title