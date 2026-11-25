from django.db import models

# Create your models here.
class Contact(models.Model):
    name=models.CharField(max_length=50)
    phone=models.CharField(max_length=50)
    email=models.EmailField()
    message=models.TextField()

class Category(models.Model):
    title=models.CharField(max_length=200)
    image=models.ImageField(upload_to='images',null=True)

    def __str__(self):
        return self.title
class Momo(models.Model):
    name=models.CharField(max_length=200)
    category=models.ForeignKey(Category, on_delete=models.CASCADE,related_name='items')
    price=models.DecimalField(max_digits=8,decimal_places=2)
    desc=models.CharField(max_length=200)
    image=models.ImageField(upload_to="images")