from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.BigIntegerField()
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return self.name
    
class Passwords(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    site = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    shifts = models.IntegerField()
    
    class Meta:
        verbose_name_plural = "Passwords"
    
    def __str__(self) -> str:
        return self.user.name