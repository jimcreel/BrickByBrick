from django.db import models
from django.urls import reverse

# Create your models here.

class Set(models.Model):
    name = models.CharField(max_length=100)
    set_num = models.CharField(max_length=100, primary_key=True)
    year = models.IntegerField()
    num_parts = models.IntegerField()
    theme_id = models.IntegerField()
    set_img_url = models.CharField(max_length=200)
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'set_id': self.set_num})

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Collection(models.Model):
    name = models.CharField(max_length=100)
    set = models.ManyToManyField(Set)
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'collection_id': self.id})
# class Part(models.Model):
#     part_num = models.CharField(max_length=20, primary_key=True)
#     name = models.CharField(max_length=100)
#     part_cat_id = models.IntegerField()
    
# class Inventories(models.Model):
#     id = models.IntegerField(primary_key=True)
#     version = models.IntegerField()
#     set_num = models.ForeignKey(Set, on_delete=models.CASCADE)

# class Inventory_MiniFig(models.Model):
#     inventory_id = models.ForeignKey(Inventories, on_delete=models.CASCADE)
#     fig_num = models.CharField(max_length=20)
#     quantity = models.IntegerField()

# class Inventory_Set(models.Model):
#     inventory_id = models.ForeignKey(Inventories, on_delete=models.CASCADE)
#     set_num = models.CharField(max_length=20)
#     quantity = models.IntegerField()

# class Theme(models.Model):
#     id = models.IntegerField(primary_key=True)
#     name = models.CharField(max_length=100)
#     parent_id = models.IntegerField()

# class Minifig(models.Model):
#     fig_num = models.CharField(max_length=20, primary_key=True)
#     name = models.CharField(max_length=100)
#     num_parts = models.IntegerField()

# class Inventory_Part(models.Model):
#     inventory_id = models.ForeignKey(Inventories, on_delete=models.CASCADE)
#     part_num = models.CharField(max_length=20)
#     color_id = models.IntegerField()
#     quantity = models.IntegerField()
#     is_spare = models.BooleanField()




