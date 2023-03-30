from django.db import models
from django.urls import reverse

# Create your models here.

class Set(models.Model):
    set_num = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    theme_id = models.IntegerField()
    num_parts = models.IntegerField()
    img_url = models.CharField(max_length=200)
    part = models.ManyToManyField('Part', through='SetPart')
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
    
class Part(models.Model):
    part_num = models.CharField(max_length=20, primary_key=True)
    part_name = models.CharField(max_length=250)
    part_cat_id = models.IntegerField()
    part_material = models.CharField(max_length=100)

    def __str__(self):
        return self.part_name
    
class SetPart(models.Model):
    set_num = models.ForeignKey(Set, on_delete=models.CASCADE)
    part_num = models.ForeignKey(Part, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    color = models.CharField(max_length=100)
    category = models.CharField(max_length=200)
    design_id = models.IntegerField()
    part_name = models.CharField(max_length=200)
    image_url = models.CharField(max_length=300)
    set_count = models.IntegerField()

    def __str__(self):
        return f"{self.get_quantity_display()} of {self.part.part_name} in {self.set.name}"
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




