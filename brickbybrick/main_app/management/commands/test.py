
import csv

filepath = '/Users/jimcreel/Downloads/themes.csv'

with open(filepath, 'r') as csvfile:
        reader = csv.reader(csvfile)

        # Skip header ro


        for row in reader:
            # Use get_or_create() to retrieve an existing Set object or create a new one
            if row[2] == '':
                row[2] = 0
                print('wrote 0')
