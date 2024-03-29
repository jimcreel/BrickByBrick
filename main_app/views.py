from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models.aggregates import Count, Sum
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import F

from secrets import *
from .models import *
from .forms import *



# Create your views here.

def build_context(request, context):
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

def sets_index(request, theme_name='Star Wars'):
        
    theme_list = Theme.objects.filter(name=theme_name).values_list('id', flat=True)
    set_list = Set.objects.filter(theme_id__in=theme_list).order_by('?', 'year').values_list('set_num', 'name', 'img_url', 'year')
    paginator = Paginator(set_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'sets': page_obj, 'theme_name': theme_name}
    context = build_context(request, context)
    print(context)
    return render(request, 'sets/index.html', context)

@login_required
def sets_detail(request, set_num):
    sets = Set.objects.get(set_num=set_num)
    # grab the inventory associated with the set and pre-fetch the part and minifigure
    inventories = Inventories.objects.filter(set_num_id=set_num).select_related('set_num')
    # grab the parts associated with the inventory and pre-fetch the part
    
    inv_list = Inventory_Part.objects.filter(inventory_id__in=inventories).select_related('part_num')
    mini_list = Inventory_MiniFig.objects.filter(inventory_id__in=inventories).select_related('fig_num')
    mini_flat_list = mini_list.values_list('fig_num', 'quantity', 'fig_num__name', 'fig_num__img_url')
    inventory_flat_list = inv_list.values_list('part_num', 'quantity', 'img_url', 'part_num__part_name')
    
    collection = Collection.objects.filter(user=request.user)
    #if the set is in a user's collection
    if collection.filter(set=set_num).exists():
        set_owned = True
        percentage_match = 100
    else:
        set_owned = False
        collection_parts = Collection_Part.objects.filter(collection_id__in=collection).values_list('part_num', 'quantity')
        set_parts = inv_list.values_list('part_num', 'quantity')

        collection_part_dict = {part[0]: part[1] for part in collection_parts}
        set_part_dict = {part[0]: part[1] for part in set_parts}

        total_set_quantity = 0
        matched_set_quantity = 0
        
        for part_num, quantity in set_part_dict.items():
            if part_num in collection_part_dict:
                matched_set_quantity += min(quantity, collection_part_dict[part_num])
            total_set_quantity += quantity

        if total_set_quantity == 0:
            percentage_match = 0
        else:
            percentage_match = round(((matched_set_quantity / total_set_quantity) * 100), 1)

    paginator = Paginator(inventory_flat_list, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'sets/detail.html', {'sets': sets, 'minifigs': mini_flat_list, 'inventories': page_obj, 'collections': collection, 'range': 6, 'percentage': percentage_match, 'set_owned': set_owned})


# @login_required
# def parts_missing(request, set_num):
#     sets = Set.objects.get(set_num=set_num)
#     # grab the inventory associated with the set and pre-fetch the part and minifigure
#     inventories = Inventories.objects.filter(set_num_id=set_num).select_related('set_num')
#     # grab the parts associated with the inventory and pre-fetch the part
    
#     inv_list = Inventory_Part.objects.filter(inventory_id__in=inventories).select_related('part_num')
#     inventory_flat_list = inv_list.values_list('part_num', 'quantity', 'img_url')
    
#     collection = Collection.objects.filter(user=request.user)
    
#     collection_parts = Collection_Part.objects.filter(collection_id__in=collection).values_list('part_num', 'quantity')
#     set_parts = inv_list.values_list('part_num', 'quantity')
    
#     collection_part_dict = {part[0]: part[1] for part in collection_parts}
#     set_part_dict = {part[0]: part[1] for part in set_parts}
#     #find the parts in set_parts that are not in collection_parts
#     missing_parts = set_part_dict.items() - collection_part_dict.items()
#     display_list = []
#     for part, quantity in missing_parts:
#         #get the part object from inv_list
#         part_obj = set_parts.first(part_num=part)
#         collection_part_obj = collection_parts.first(part_num=part)
#         part_obj['quantity'] = part_obj['quantity'] - collection_part_obj['quantity']
#     paginator = Paginator(missing_parts, 25)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'sets/parts_missing.html', {'sets': sets, 'inventories': page_obj, 'collections': collection, 'range': 25})


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
    return render(request, 'collections/index.html', {'collections': collections, 'parts': collection_parts})

@login_required
def collections_detail(request, collection_id):
    current_collection = Collection.objects.get(id=collection_id)
    sets = Set.objects.filter(collection = collection_id)
    parts = Collection_Part.objects.filter(collection_id_id = collection_id)
    context = {}
    context = build_context(request, context)
    context['parts'] = parts
    context['sets'] = sets
    context['collection'] = current_collection

    return render(request, 'collections/detail.html', context)





def collection_parts(request, collection_id):
    if collection_id == 0:
        collection = Collection.objects.filter(user=request.user)
        inventory_flat_list = Collection_Part.objects.filter(collection_id__in=collection).values_list('part_num', 'quantity', 'img_url', 'part_num__part_name')
        total_parts = Collection_Part.objects.filter(collection_id__in=collection).aggregate(Sum('quantity'))
    else:
        collection = Collection.objects.get(id=collection_id)
        inventory_flat_list = Collection_Part.objects.filter(collection_id_id=collection_id).values_list('part_num', 'quantity', 'img_url', 'part_num__part_name')
        total_parts = Collection_Part.objects.filter(collection_id_id=collection_id).aggregate(Sum('quantity'))
    paginator = Paginator(inventory_flat_list, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'inventories': page_obj, 'collection': collection, 'range': 6, 'total_parts': total_parts, 'collection_id': collection_id}
    context = build_context(request, context)
    return render(request, 'collections/parts.html', context)

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
        set = Set.objects.get(set_num=set_num)
        set.collection.add(collection)
        collection.last_img = set.img_url
        collection.save()
        existing_parts = Collection_Part.objects.filter(
        collection_id=collection_id,
        part_num__in=Inventory_Part.objects.filter(inventory_id__set_num_id=set_num).values_list('part_num', flat=True)
        )

        existing_part_dict = {}
        for part in existing_parts:
            part_key = (part.part_num_id, part.is_spare, part.color_id_id)
            existing_part_dict[part_key] = part

        new_parts = []
        for inventory_part in Inventory_Part.objects.filter(inventory_id__set_num_id=set_num):
            part_key = (inventory_part.part_num_id, inventory_part.is_spare, inventory_part.color_id_id)
            if part_key in existing_part_dict:
                existing_part_obj = existing_part_dict[part_key]
                existing_part_obj.quantity += inventory_part.quantity
                existing_part_obj.save()
                del existing_part_dict[part_key]
            else:
                img_url = inventory_part.img_url if inventory_part.img_url else ' '
                collection_part = Collection_Part(
                    collection_id_id=collection_id,
                    part_num_id=inventory_part.part_num_id,
                    is_spare=inventory_part.is_spare,
                    color_id_id=inventory_part.color_id_id,
                    img_url=img_url,
                    quantity=inventory_part.quantity,
                )
                new_parts.append(collection_part)

        # Bulk create the new Collection_Part objects
        if new_parts:
            Collection_Part.objects.bulk_create(new_parts)

        # Delete the old Collection_Part objects that were not updated
        if existing_part_dict:
            Collection_Part.objects.filter(
                collection_id=collection_id,
                part_num__in=[part[0] for part in existing_part_dict.keys()],
                is_spare__in=[part[1] for part in existing_part_dict.keys()],
                color_id__in=[part[2] for part in existing_part_dict.keys()],
            ).delete()


        return redirect('collections_detail', collection_id=collection_id)




class RemoveSetFromCollection(LoginRequiredMixin, View):
    def post(self, request, collection_id, set_num):
        collection = Collection.objects.get(id=collection_id)
        set = Set.objects.get(set_num = set_num)
        set.collection.remove(collection)
        parts = Inventory_Part.objects.filter(inventory_id__set_num_id=set_num)
        for part in parts:
            collection_part = Collection_Part.objects.filter(collection_id=collection_id, part_num_id=part.part_num_id)
            if collection_part:
                collection_part = collection_part[0]
                collection_part.quantity -= part.quantity
                if collection_part.quantity <= 0:
                    collection_part.delete()
                collection_part.save()
        return redirect('collections_detail', collection_id=collection_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/collections/')
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







