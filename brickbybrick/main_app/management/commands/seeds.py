from django.core.management.base import BaseCommand
import csv
from main_app.models import *
import pandas as pd

def import_sets_from_csv(filepath):
    tmp_data = pd.read_csv(filepath, sep=',')
    sets = [
        Set(
            set_num=row[0],
            name=row[1],
            year=row[2],
            theme_id_id=Theme.objects.get(id=row[3]),
            num_parts=row[4],
            img_url=row[5]
        )

        for row in tmp_data.values
    ]
    Set.objects.bulk_create(sets)
#import_sets_from_csv('/Users/jimcreel/Downloads/sets-4.csv')

def import_parts_from_csv(filepath):
    with open(filepath, 'r') as csvfile:
        reader = csv.reader(csvfile)
        
        next(reader)
        
        for row in reader:
            
            part_obj, created = Part.objects.get_or_create(
                part_num=row[0],
                defaults={
                    "part_name": row[1],
                    "part_cat_id": row[2],
                    "part_material": row[3]
                }
            )
            if created:
                print(f"Created new part: {part_obj}")
            else:
                print(f"Part already exists: {part_obj}")
#import_parts_from_csv('/Users/jimcreel/Downloads/parts.csv')

def create_set_parts(filepath, set_num):
    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile)
        next(reader)
        for row in reader:
            set_part_obj, created = SetPart.objects.get_or_create(
                set_num=Set.objects.get(set_num=set_num),
                part_num=Part.objects.get(part_num=row['Part']),
                defaults={
                    'color': row['Color'],
                    'quantity': row['Quantity'],
                    'is_spare': row['Is Spare'] == 'Y'
                }
            )
            if created:
                print(f"Created new set_part: {set_part_obj}")
            else:
                print(f"Set_part already exists: {set_part_obj}")

#create_set_parts('/Users/jimcreel/Downloads/rebrickable_parts_75192-1-millennium-falcon.csv', '75192-1')

def create_themes_from_csv(filepath):
    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile)
        next(reader)
        for row in reader:
            if row['parent_id'] == '':
                row['parent_id'] = 0
            theme_obj, created = Theme.objects.get_or_create(
                id=row['id'],
                defaults={
                    'name': row['name'],
                    'parent_id': row['parent_id']
                }
            )
            if created:
                print(f"Created new theme: {theme_obj}")
            else:
                print(f"Theme already exists: {theme_obj}")

#create_themes_from_csv('/Users/jimcreel/Downloads/themes.csv')

def create_colors_from_csv(filepath):
    with open(filepath) as csvfile:
        reader  = csv.DictReader(csvfile)
        next(reader)
        for row in reader:
            if row['is_trans'] == 'f':
                row['is_trans'] = False
            else:
                row['is_trans'] = True
            color_obj, created = Color.objects.get_or_create(
                id=row['id'],
                defaults={
                    'name': row['name'],
                    'rgb': row['rgb'],
                    'is_trans': row['is_trans']
                }
            )
            if created:
                print(f"Created new color: {color_obj}")
            else:
                print(f"Color already exists: {color_obj}")
#create_colors_from_csv('/Users/jimcreel/Downloads/colors.csv')

def import_minifigs_from_csv(filepath):
    tmp_data = pd.read_csv(filepath, sep=',')
    minifigs = [
        Minifig(
            fig_num=row[0],
            name=row[1],
            num_parts=row[2],
            img_url=row[3]
        )   
        for row in tmp_data.values
    ]
    Minifig.objects.bulk_create(minifigs)
#import_minifigs_from_csv('/Users/jimcreel/Downloads/minifigs.csv')

def create_inventory_minifig(filepath):
    tmp_data = pd.read_csv(filepath, sep=',')
    inventory_minifigs = [
        Inventory_MiniFig(
            inventory_id=Inventories.objects.get(id=row[0]),
            minifig_id=Minifig.objects.get(fig_num=row[1]),
            quantity=row[2]
        )
        for row in tmp_data.values
    ]
    Inventory_MiniFig.objects.bulk_create(inventory_minifigs)
#create_inventory_minifig('/Users/jimcreel/Downloads/inventory_minifigs.csv')

def import_inventories_from_csv(filepath):
    tmp_data = pd.read_csv(filepath, sep=',')
    for row in tmp_data.values:
        inventories = Inventories.objects.create(
            id=row[0],
            version=row[1],
            set_num_id = row[2],
        )

    Inventories.objects.bulk_create([inventories], ignore_conflicts=True, batch_size=1000)
import_inventories_from_csv('/Users/jimcreel/Downloads/inventories-4.csv')
        
def import_inventory_set_from_csv(filepath):
    tmp_data = pd.read_csv(filepath, sep=',')
    index_id = 0
    for row in tmp_data.values:
        index_id += 1
        inventory_sets = Inventory_Set.objects.create(
            id = index_id,
            inventory_id_id=Inventories.objects.get(id=row[0]),
            set_num_id=Set.objects.get(set_num=row[1]),
            quantity=row[2]            
        )
    Inventory_Set.objects.bulk_create([inventory_sets], ignore_conflicts=True, batch_size=1000)
#import_inventory_set_from_csv('/Users/jimcreel/Downloads/inventory_sets.csv')
# def import_inventory_sets_to_inventories(filepath):
#     with open(filepath, 'r') as csvfile:
#         reader = csv.reader(csvfile)
        
#         next(reader)
        
#         for row in reader:
#             if not Inventories.objects.filter(id=row[0]).exists():
#                 part_obj, created = Inventories.objects.get_or_create(
#                     set_num_id = Set.objects.get(set_num=row[2]),
#                     defaults={
#                         'id': row[0],
#                         'version': 1
#                     }
#                 )
#                 if created:
#                     print(f"Created new part: {part_obj}")
#                 else:
#                     print(f"Part already exists: {part_obj}")
#             else:
#                 Inventories.objects.filter(id=row[0]).update(set_num_id=Set.objects.get(set_num=row[2]), version = row[1])

# import_inventory_sets_to_inventories('/Users/jimcreel/Downloads/inventories-4.csv')