import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Create SQLAlchemy engine
engine = create_engine(
    f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@"
    f"{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DB')}"
)

# List of tables and views to export
objects_to_export = [
    "staging_prices",
    "staging_reddit",
    "prices",
    "sentiment",
    "daily_metrics"
]

# Directory to save CSVs
output_dir = "exports"
os.makedirs(output_dir, exist_ok=True)

# Export each object to CSV
for obj in objects_to_export:
    try:
        df = pd.read_sql(f"SELECT * FROM {obj}", engine)
        file_path = os.path.join(output_dir, f"{obj}.csv")
        df.to_csv(file_path, index=False)
        print(f"Exported {obj} to {file_path}")
    except Exception as e:
        print(f"Failed to export {obj}: {e}")
