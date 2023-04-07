from django.contrib import admin

# Register your models here.

from .models import Set, Collection

admin.site.register(Set)
admin.site.register(Collection)