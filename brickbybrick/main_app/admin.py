from django.contrib import admin

# Register your models here.

from .models import Set, User, Collection

admin.site.register(Set)
admin.site.register(User)
admin.site.register(Collection)