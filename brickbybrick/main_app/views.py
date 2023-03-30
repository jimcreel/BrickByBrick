from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models.aggregates import Count
from django.views import View

from secrets import * 
from .models import *
from .forms import *


REBRICKABLE_API_KEY = settings.REBRICKABLE_API_KEY
print(REBRICKABLE_API_KEY)
# Create your views here.
 
def home(request):
    count = Set.objects.all().count()
    rand_list = []
    for i in range(0, 5):
        rand_list.append(Set.objects.order_by('?').first())
    
    return render(request, 'home.html', {'sets': rand_list})

def about(request):
    return render(request, 'about.html')

def sets_index(request):
    # sets = []
    # minis = []
    # for item in my_sets:
    #     url = f'https://rebrickable.com/api/v3/lego/sets/{item}/?key=1ed8ac4859da5604bdb3fa343f93c829'
    #     mini_url = f'https://rebrickable.com/api/v3/lego/sets/{item}/minifigs/?key=1ed8ac4859da5604bdb3fa343f93c829'
    #     req = requests.get(mini_url)
    #     r = requests.get(url)
    #     set = r.json()
    #     minifigs = req.json()
    #     set['minifigs'] = minifigs['results']
    #     sets.append(set)
    sets = Set.objects.all()
    return render(request, 'sets/index.html', {'sets': sets})
        
    # return render(request, 'sets/index.html', {
    #     'sets': sets,
    #     'minis': minis
    # })

def sets_detail(request, set_id):
    set = Set.objects.get(id=set_id)
    collection = Collection.objects.first()
    return render(request, 'sets/detail.html', {'set': set, 'collection': collection})

class SetCreate(CreateView):
    model = Set
    fields = '__all__'
    success_url = '/sets/{set_id}'

class SetUpdate(UpdateView):
    model = Set
    fields = [  'set_img_url', 'set_url']

class SetDelete(DeleteView):
    model = Set
    success_url = '/sets/'

def collections_index(request):
    collections = Collection.objects.all()
    return render(request, 'collections/index.html', {'collections': collections})

def collections_detail(request, collection_id):
    collections = Collection.objects.get(id=collection_id)
    print(collections.set.all())
    return render(request, 'collections/detail.html', {'collections': collections})

def collections_add(request, set_id):
    collections = Collection.objects.first()
    set = Set.objects.get(id=set_id)
    collections.set.add(set)
    return render(request, 'collections/detail.html', {'collections': collections})

class CollectionUpdate(UpdateView):
    model = Collection
    fields = [  'name', 'id' ]
    success_url = '/collections/{collection_id}'

class CollectionDelete(DeleteView):
    model = Collection
    success_url = '/collections/'

class CollectionCreate(CreateView):
    model = Collection
    fields = '__all__'
    success_url = '/collections/{collection_id}'

class AddSetToCollection(View):
    def post(self, request, collection_id, set_id):
        collection = Collection.objects.get(id=collection_id)
        set = Set.objects.get(id=set_id)
        collection.set.add(set)
        return redirect('collections_detail', collection_id=collection_id)