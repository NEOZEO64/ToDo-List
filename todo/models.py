from django.db import models
from django.utils import timezone

class Todo(models.Model):
    title=models.CharField(max_length=100)
    date=models.DateTimeField(default=timezone.now)
    date2=0 #the real date in our timezone
 
    def __str__(self):
        return self.title
# Create your models here.
