
from django.db import models

class Product(models.Model):
    url = models.URLField()
    category = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    img_url = models.URLField()
    bought = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    price = models.CharField(max_length=50, null=True, blank=True)
    MPR = models.CharField(max_length=50, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    size = models.CharField(max_length=255, null=True, blank=True)

    
    class Meta:
        db_table = 'products'