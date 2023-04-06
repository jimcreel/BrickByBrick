from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models.aggregates import Count
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from secrets import *
from .models import *
from .forms import *


REBRICKABLE_API_KEY = settings.REBRICKABLE_API_KEY
print(REBRICKABLE_API_KEY)
# Create your views here.

def build_context(request, context):
    context = {}
    if request.user.is_authenticated:
        collections = Collection.objects.filter(user = request.user)
        context['collections'] = collections
    return context

def home(request):
    rand_list = []
    theme_id = 158
    for i in range(0, 5):
        rand_list.append(Set.objects.filter(theme_id=theme_id).order_by('?').first())
    
    context = {'sets': rand_list}
    context = build_context(request, context)

    return render(request, 'home.html', context)

def about(request):
    
    context = {}
    context = build_context(request, context)

    return render(request, 'about.html', context)

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
    set = Set.objects.get(set_num=set_num)
    # grab the inventory associated with the set and pre-fetch the part

    inventories = Inventories.objects.filter(set_num_id=set_num).select_related('set_num')
    # grab the parts associated with the inventory and pre-fetch the part
    
    inv_list = Inventory_Part.objects.filter(inventory_id__in=inventories).select_related('part_num')
    part_list = Part.objects.filter(pk__in=inv_list.values_list('part_num_id', flat=True)).distinct()
    top_level_inv = Inventories.objects.filter(set_num_id=set_num).first()
    top_level_part_list = Inventory_Part.objects.filter(inventory_id=top_level_inv.id, part_num__isnull=False).select_related('part_num') if top_level_inv else []
    inventory_flat_list = inv_list.values_list('part_num', 'quantity', 'img_url')
    
    collections = request.user.collection_set.all()
    # print(inventory_flat_list)
    paginator = Paginator(inventory_flat_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'sets/detail.html', {'set': set, 'inventories': page_obj, 'collections': collections, 'range': 6})


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

    context = {}
    context = build_context(request, context)

    context['sets'] = sets
    context['collection'] = current_collection

    return render(request, 'collections/detail.html', context)


# OLD JIM CODE
# def collections_detail(request, collection_id):
#     current_collection = Collection.objects.get(id=collection_id)
#     sets = Set.objects.filter(collection = collection_id)
#     # print(sets)
#     context = {}
#     context = build_context(request, context)


#     return render(request, 'collections/detail.html', {'sets': sets, 'collection': current_collection})


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
        set.collection.remove(collection)
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
    context = {}
    context = build_context(request, context)

    if request.method == "POST":
        searchWord = request.POST.get('searchWord')
        searchSets = Set.objects.filter(Q(name__icontains=searchWord)|Q(set_num__icontains=searchWord))
        if not searchSets:
            search_mini_figs = Minifig.objects.filter(name__icontains=searchWord)
        if searchSets:
            context.update({ 'searchWord': searchWord, 'searchSets': searchSets })
            return render(request, 'search.html', context)
        elif search_mini_figs:
            context.update({ 'searchWord': searchWord, 'search_mini_figs': search_mini_figs })
            return render(request, 'search.html', context)
        else:
            return render(request, 'search.html', context)







# Chat GTP
#     if request.method == "POST":
#         searchWord = request.POST.get('searchWord')
#         searchSets = Set.objects.filter(Q(name__icontains=searchWord) | Q(set_num__icontains=searchWord))

#         if not searchSets:
#             search_mini_figs = Minifig.objects.filter(name__icontains=searchWord)
#             context = {}
#             context = build_context(request, context)
#             return render(request, 'search.html', 
#                         {'searchWord': searchWord,
#                         'search_mini_figs': search_mini_figs}, 
#                         context=context)
#         else:
#             context = {}
#             context = build_context(request, context)
#             return render(request, 'search.html', 
#                         {'searchWord': searchWord,
#                         'searchSets': searchSets}, 
#                         context=context)
#     else:
#         context = {}
#         context = build_context(request, context)
#         return render(request, 'search.html', context=context)



    # if request.method == "POST":
    #     searchWord = request.POST.get('searchWord')
    #     searchSets = Set.objects.filter(Q(name__icontains=searchWord)|Q(set_num__icontains=searchWord))
    #     search_mini_figs = Minifig.objects.filter(name__icontains=searchWord)
    #     context = {}
    #     context = build_context(request, context)

    #     print(context)

    #     search = {
    #         'searchWord': searchWord,
    #         'searchSets': searchSets,
    #         'search_mini_figs': search_mini_figs,
    #     }
                   
    #     return render(request, 'search.html', search, context)
    

        # context = build_context(request, context)
        # if not searchSets:
        #     search_mini_figs = Minifig.objects.filter(name__icontains=searchWord)
        # if searchSets:
        #     return render(request, 'search.html',
        #     { 'searchWord': searchWord,
        #      'searchSets': searchSets,
        #      'search_mini_figs': search_mini_figs,
        #      'context': context})
        # elif search_mini_figs:
        #     return render(request, 'search.html', context,
        #     { 'searchWord': searchWord,
        #      'search_mini_figs': search_mini_figs })
        # else:
        #     return render(request, 'search.html')





# JIM MODIFY
    # if request.method == "POST":
    #     searchWord = request.POST.get('searchWord')
    #     searchSets = Set.objects.filter(Q(name__icontains=searchWord)|Q(set_num__icontains=searchWord))
    #     if not searchSets:
    #         search_mini_figs = Minifig.objects.filter(name__icontains=searchWord)
    #     if searchSets:
    #         context = { 'searchWord': searchWord,'searchSets': searchSets }
    #         context = build_context(request, context)

    #         return render(request, 'search.html', context)
    #     elif search_mini_figs:
    #         context = { 'searchWord': searchWord,'search_mini_figs': search_mini_figs }
    #         context = build_context(request, context)

    #         return render(request, 'search.html', context)
    #     else:
    #         context = { 'searchWord': searchWord }
    #         context = build_context(request, context)

    #         return render(request, 'search.html', context)


# OG ORIGINAL 
    #     if request.method == "POST":
    #         searchWord = request.POST.get('searchWord')
    #         searchSets = Set.objects.filter(Q(name__icontains=searchWord)|Q(set_num__icontains=searchWord))
    #         if not searchSets:
    #             search_mini_figs = Minifig.objects.filter(name__icontains=searchWord)
    #         if searchSets:
    #             return render(request, 'search.html', 
    #             { 'searchWord': searchWord,
    #              'searchSets': searchSets })
    #         elif search_mini_figs:
    #             return render(request, 'search.html', 
    #             { 'searchWord': searchWord,
    #              'search_mini_figs': search_mini_figs })
    #         else:
    #             return render(request, 'search.html')