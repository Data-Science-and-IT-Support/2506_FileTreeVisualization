# Example usage:
#if __name__ == "__main__":
#    root = r'C:/Users/Email/Desktop/CAM'  # Replace with your path
#    df = build_directory_dataframe(root)
#    print(df)
#    df.to_csv("directory_structure.csv", index=False)  # Optional: save to CSV




import os
import pandas as pd

def build_directory_dataframe(root_dir):
    
    records = []

    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            filepath = os.path.join(dirpath, file)
            rel_path = os.path.relpath(filepath, root_dir)
            parts = rel_path.split(os.sep)
            file_size = os.path.getsize(filepath)
            dir_levels = parts[:-1]  # directories only
            filename = parts[-1]

            # Create a record starting with root directory, then all levels, then filename and size
            record = [root_dir] + dir_levels + [filename, file_size]
            records.append(record)

    # Determine the maximum directory depth to align all rows
    max_depth = max(len(r) for r in records)

    # Normalize all records to the same length
    for r in records:
        while len(r) < max_depth:
            r.insert(-2, "Null")  # insert before filename and size

    # Now generate correct column names
    num_levels = max_depth - 3  # subtract Root, File_Name, File_Size
    col_names = ['Root'] + [f"Level_{i}" for i in range(1, num_levels + 1)] + ['File_Name', 'File_Size']

    df = pd.DataFrame(records, columns=col_names)
    return df