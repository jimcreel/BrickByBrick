
import csv
import pandas as pd

filepath = '/Users/jimcreel/Downloads/inventory_parts-4.csv'
csv_input = pd.read_csv(filepath, sep=',', header= 0)
print(len(csv_input.index))

