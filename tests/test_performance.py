"""
This script is used solely for determining the ETL operation times for larger product data sets.
The script executes the normal ETL pipeline with a timer, but uses the genereate_data.py script 
to create mock product data of 50k lines. S
The subsequent transform.py -> load.py execute and a final time is given after all 50k lines 
are loaded to Neon PostgreSQL.
"""

from generate_data import generate_data
from transform import transform
from load import load_data
import time

# Generate and process 50k records
df = generate_data(50000)
start = time.perf_counter()
clean_df = transform(df)
load_data(clean_df)
print(f"⏱️  50k records processed in {time.perf_counter() - start:.2f}s")