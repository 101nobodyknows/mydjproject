from django.db import models

category_choice = [
    ('Clothing', 'Clothing'),
    ('Footwear', 'Footwear'),
    ('Accessories', 'Accessories'),
    ('Jewellery', 'Jewellery')
]

class new_product(models.Model):
    product_name = models.CharField(max_length=40)
    product_price = models.FloatField()
    product_desc = models.TextField()
    product_quantity = models.IntegerField(default=0)
    product_rating = models.IntegerField(default=5)
    product_img = models.ImageField(upload_to="static/product_images", blank=True)
    product_category = models.CharField(
        max_length=20,
       choices=category_choice
    )
    
    def __str__(self):
        return self.product_name
    
class team(models.Model):
    name = models.CharField(max_length=30)
    position = models.TextField()
    email = models.CharField(max_length=40)
    user_img = models.ImageField(upload_to="static/team_images", blank=True)
    whatsapp = models.CharField(max_length=20)
    instagram = models.TextField()
    twitter = models.TextField()
    phone_number = models.CharField(max_length=20)
    user_cover = models.ImageField(upload_to="static/team_images", blank=True)
    
    def __str__(self):
        return self.name
    
class New_task(models.Model):
    new_task = models.TextField()
    
    def __str__(self):
        return self.new_task