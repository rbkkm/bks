import pyarrow.parquet as pq
import os, json, time
from pathlib import Path
from datetime import datetime

# Configuration
input_parquet = "d:/data/w/HadCET_meantemp_monthly_2025.parquet"
output_txt = input_parquet + ".txt"
file_path = Path(input_parquet)
stats = file_path.stat()

# Load only the metadata (footer)
parquet_file = pq.ParquetFile(input_parquet)
metadata = parquet_file.metadata
schema = parquet_file.schema

with open(output_txt, "w") as f:

    # 1.  FILE METADATA
    f.write("--- FILE METADATA ---\n")
    f.write(f"File: {os.path.basename(input_parquet)}\n")
    f.write(f"Creation Time: {datetime.fromtimestamp(stats.st_birthtime)}\n")
    f.write(f"Created By: {metadata.created_by}\n")
    f.write(f"Total Rows: {metadata.num_rows}\n")
    f.write(f"Total Columns: {metadata.num_columns}\n")

    # Custom Metadata (if any exists, e.g., pandas index info)
    if metadata.metadata:
        f.write("\n--- CUSTOM KEY-VALUE METADATA ---\n")
        for key, value in metadata.metadata.items():
            f.write(f"{key.decode('utf-8')}: {value.decode('utf-8')[:100]}...\n")

    # 2. COLUMN-LEVEL DETAILS
    f.write("--- COLUMNS ---\n")
    row_group = metadata.row_group(0)

    for i in range(metadata.num_columns):
        col = row_group.column(i)
        f.write(f"{col.path_in_schema} - {col.physical_type}\n")


print(f"Metadata export complete. File saved as: {output_txt}")
