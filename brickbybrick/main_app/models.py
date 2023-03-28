from django.db import models

# Create your models here.

class Set(models.Model):
    name = models.CharField(max_length=100)
    set_num = models.CharField(max_length=100)
    year = models.IntegerField()
    num_parts = models.IntegerField()
    theme_id = models.IntegerField()
    num_minifigs = models.IntegerField()
    set_img_url = models.CharField(max_length=200)
    set_url = models.CharField(max_length=200)
    last_modified_dt = models.DateTimeField()
    def __str__(self):
        return self.name