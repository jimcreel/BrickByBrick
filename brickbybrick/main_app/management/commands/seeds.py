from django.core.management.base import BaseCommand
import csv
from main_app.models import Set

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
