from django.forms import ModelForm
from .models import *  

class CollectionForm(ModelForm):
    class Meta:
        model = Collection
        fields = '__all__'