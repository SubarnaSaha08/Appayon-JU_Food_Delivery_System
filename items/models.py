from django.db import models
from PIL import Image

from items.constants import CATEGORIES, LOCATIONS, AREAS

class Shop(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50, choices=LOCATIONS)
    area = models.CharField(max_length=50, choices=AREAS)

    def __str__(self):
        return self.name

            
class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    category = models.CharField(max_length=50, choices=CATEGORIES)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="shop")
    rate = models.DecimalField(max_digits=5, decimal_places=2)
    is_non_veg = models.BooleanField(default=False)    
    stock = models.IntegerField(default=10)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5)
    image = models.ImageField(verbose_name="Feature Image", upload_to="item_pics", default="media/default_item.png")
    #non_availablity_time = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height>300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
            
