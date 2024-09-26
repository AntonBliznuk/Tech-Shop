from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self) -> str:
        return f"{self.name}"
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']



class Product(models.Model):
    brand = models.CharField(blank=True, max_length=15)
    name = models.CharField(blank=True, max_length=35)
    description = models.TextField()
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.brand} {self.name} ({self.category})"
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['brand', 'name', 'price']



class ImageProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    name = models.CharField(max_length=25, blank=True)
    image = models.ImageField(upload_to='media/product_images/')

    def __str__(self) -> str:
        return f"{self.name} --> {self.product}"
    
    class Meta:
        verbose_name = 'Image of Product'
        verbose_name_plural = 'Images of Product'
        ordering = ['name']



class ViewProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user} --> {self.product} --> ({self.viewed_at})"
    
    class Meta:
        verbose_name = 'View of Product'
        verbose_name_plural = 'Views of Product'
        ordering = ['-viewed_at']


class WhisList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    list_name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.list_name} ({self.user})"
    
    class Meta:
        verbose_name = 'WhisList'
        verbose_name_plural = 'WhisLists'