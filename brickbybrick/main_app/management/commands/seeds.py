from django.core.management.base import BaseCommand
import csv
from main_app.models import *

def import_sets_from_csv(filepath):
    with open(filepath, 'r') as csvfile:
        reader = csv.reader(csvfile)

        # Skip header row
        next(reader)

        for row in reader:
            # Use get_or_create() to retrieve an existing Set object or create a new one
            set_obj, created = Set.objects.get_or_create(
                set_num=row[0],
                defaults={
                    "name": row[1],
                    "year": row[2],
                    "theme_id": row[3],
                    "num_parts": row[4],
                    "img_url": row[5]
                }
            )

            if created:
                print(f"Created new set: {set_obj}")
            else:
                print(f"Set already exists: {set_obj}")

# Call the function to import sets from a CSV file
import_sets_from_csv('/Users/jimcreel/Downloads/sets.csv')

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
import_parts_from_csv('/Users/jimcreel/Downloads/parts.csv')

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

create_set_parts('/Users/jimcreel/Downloads/rebrickable_parts_75192-1-millennium-falcon.csv', '75192-1')