from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.




class Theme(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    parent_id = models.IntegerField()
    

    def __int__(self):
        return self.id
    def get_absolute_url(self):
        return reverse('detail', kwargs={'set_id': self.id})
    
    
class Set(models.Model):
    set_num = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=250)
    year = models.IntegerField()
    theme_id = models.ForeignKey(Theme, on_delete=models.CASCADE)
    num_parts = models.IntegerField()
    img_url = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'set_id': self.set_num})


class Inventories(models.Model):
    id = models.IntegerField(primary_key=True)
    version = models.IntegerField()
    set_num = models.ForeignKey(Set, on_delete=models.CASCADE)

    def __int__(self):
        return self.id
        


class Inventory_Set(models.Model):
    inventory_id = models.ForeignKey(Inventories, on_delete=models.CASCADE)
    set_num = models.ForeignKey(Set, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.set_num} {self.quantity}"


class Minifig(models.Model):
    fig_num = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    num_parts = models.IntegerField()
    img_url = models.CharField(max_length=200)

    def __str__(self):
        return self.fig_num




class Inventory_MiniFig(models.Model):
    inventory_id = models.ForeignKey(Inventories, on_delete=models.CASCADE)
    fig_num = models.ForeignKey(Minifig, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.fig_num} {self.quantity}"

class Part_Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __int__(self):
        return self.id

class Color(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    rgb = models.CharField(max_length=100)
    is_trans = models.BooleanField(default = False)

    def __int__(self):
        return self.id


class Part(models.Model):
    part_num = models.CharField(max_length=20, primary_key=True)
    part_name = models.CharField(max_length=250)
    part_cat_id = models.IntegerField()
    part_material = models.CharField(max_length=100)

    def __int__(self):
        return self.part_num
    
class Inventory_Part(models.Model):
    inventory_id = models.ForeignKey(Inventories, on_delete=models.CASCADE)
    part_num = models.ForeignKey(Part, on_delete=models.CASCADE)
    color_id = models.ForeignKey(Color, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_spare = models.BooleanField()
    img_url = models.CharField(max_length=200)

    

class Collection(models.Model):
    name = models.CharField(max_length=100)
    set = models.ManyToManyField(Set)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'collection_id': self.id})
class SetPart(models.Model):
    set_num = models.ForeignKey(Set, on_delete=models.CASCADE)
    part_num = models.ForeignKey(Part, on_delete=models.CASCADE)
    color = models.IntegerField()
    quantity = models.IntegerField()
    is_spare = models.BooleanField()

    def __str__(self):
        return f"{self.get_quantity_display()} of {self.part_num.part_name} in {self.set_num.name}"

    def get_quantity_display(self):
        if self.quantity == 1:
            return f"{self.quantity} {self.part_num.part_name}"
        else:
            return f"{self.quantity} {self.part_num.part_name}s"


