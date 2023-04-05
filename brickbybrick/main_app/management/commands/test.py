
import csv
import pandas as pd


def reorder_replace_add_serialized_id(csv_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    # Reorder the columns
    # Add a serialized id
    #replace the is_spare column with a boolean
    df.replace({'is_spare': {'t': True, 'f': False}}, inplace=True)
    # # Write the reordered, replaced, and serialized DataFrame back to the CSV file

    
    
    # # Add a serialized id
    df['id'] = df.index + 1
    #reorder the columns
    
    df = df.reindex(columns=['id', 'quantity', 'is_spare', 'img_url', 'color_id_id','inventory_id_id', 'part_num_id'])
    
    
    # Write the reordered, replaced, and serialized DataFrame back to the CSV file
    df.to_csv(csv_file, index=False)

#reorder_replace_add_serialized_id('/Users/jimcreel/Downloads/inventory_parts.csv')