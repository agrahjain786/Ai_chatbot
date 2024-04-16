from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.message}'
    
    
    
class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question
    
    
    
class Doubt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.TextField()
    answer = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    solved_doubt_at = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.user.username}: {self.query}'
    
    
class ChatMonitor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    response_time = models.IntegerField()
    fallback = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.message}: {self.response_time}'
    
    
class feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __str__(self):
        return f'{self.user.username}: {self.message}'