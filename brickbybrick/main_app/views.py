from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models.aggregates import Count
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from secrets import *
from .models import *
from .forms import *


REBRICKABLE_API_KEY = settings.REBRICKABLE_API_KEY
print(REBRICKABLE_API_KEY)
# Create your views here.


def home(request):
    rand_list = []
    theme_id = 158
    for i in range(0, 5):
        rand_list.append(Set.objects.filter(theme_id=theme_id).order_by('?').first())
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
@login_required
def sets_detail(request, set_num):
    #get all inventories from set
    #get all parts from inventories
    #get all colors from parts
    #get all images from colors
    #get all minifigs from set
    #get all images from minifigs
    set = Set.objects.get(set_num=set_num)
    inventories = Inventories.objects.filter(set_num=set_num)
    collections = Collection.objects.filter(user=request.user)
    print(inventories)
    return render(request, 'sets/detail.html', {'set': set, 'inventories': inventories, 'collections': collections})

class SetCreate(CreateView):
    model = Set
    fields = '__all__'
    success_url = '/sets/'

class SetUpdate(UpdateView):
    model = Set
    fields = [ 'img_url']
    success_url = '/sets/{set_num}'

class SetDelete(DeleteView):
    model = Set
    success_url = '/'

@login_required
def collections_index(request):
    collections = Collection.objects.filter(user=request.user)
    return render(request, 'collections/index.html', {'collections': collections})

@login_required
def collections_detail(request, collection_id):
    current_collection = Collection.objects.get(id=collection_id)
    sets = Set.objects.filter(collection = collection_id)
    print(sets)
    return render(request, 'collections/detail.html', {'sets': sets, 'collection': current_collection})


class CollectionUpdate(LoginRequiredMixin, UpdateView):
    model = Collection
    fields = [  'name', 'id' ]
    success_url = '/collections/{collection_id}'


class CollectionDelete(LoginRequiredMixin, DeleteView):
    model = Collection
    success_url = '/collections/'


class CollectionCreate(LoginRequiredMixin, CreateView):
    model = Collection
    fields = ['name']
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    success_url = '/collections/'


class AddSetToCollection(LoginRequiredMixin, View):
    def post(self, request, collection_id, set_num):
        collection = Collection.objects.get(id=collection_id)
        set = Set.objects.get(set_num = set_num)
        set.collection.add(collection)
        return redirect('collections_detail', collection_id=collection_id)


class RemoveSetFromCollection(LoginRequiredMixin, View):
    def post(self, request, collection_id, set_num):
        collection = Collection.objects.get(id=collection_id)
        set = Set.objects.get(set_num = set_num)
        collection.set.remove(set)
        return redirect('collections_detail', collection_id=collection_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

def search(request):
    
    return render(request, 'search.html')
    # search_term = request.GET.get('search')
    # url = f'https://rebrickable.com/api/v3/lego/sets/?key={REBRICKABLE_API_KEY}&search={search_term}'
    # r = requests.get(url)
    # sets = r.json()
    # return render(request, 'sets/index.html', {'sets': sets})