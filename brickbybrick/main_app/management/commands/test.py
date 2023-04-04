
import csv
import pandas as pd


def reorder_replace_add_serialized_id(csv_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    # Reorder the columns
    df = df.reindex(columns=['id', 'quantity', 'fig_num', 'inventory_id',])
    
    
    # Add a serialized id
    
    
    # Write the reordered, replaced, and serialized DataFrame back to the CSV file
    df.to_csv(csv_file, index=False)

reorder_replace_add_serialized_id('/Users/jimcreel/Downloads/inventory_minifigs.csv')