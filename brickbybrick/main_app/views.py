from django.shortcuts import render
from django.conf import settings
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from secrets import * 
from .models import Set

REBRICKABLE_API_KEY = settings.REBRICKABLE_API_KEY
print(REBRICKABLE_API_KEY)
# Create your views here.
 
def home(request):
    return render(request, 'home.html')

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
    return render(request, 'sets/detail.html', {'set': set})

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