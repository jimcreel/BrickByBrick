from django.forms import ModelForm
from .models import *  

class CollectionForm(ModelForm):
    class Meta:
        model = Collection
        fields = '__all__'

class SetForm(ModelForm):
    class Meta:
        model = Set
        fields = '__all__'

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'

class CollectionForm(ModelForm):
    class Meta:
        model = Collection
        fields = '__all__'