from sqlalchemy import create_engine
import pandas as pd
import requests

# Choose SQLite by default; for Baserow, swap fetch logic

def get_engine(sqlite_path="skus.db"):
    return create_engine(f"sqlite:///{sqlite_path}")

# Persist DataFrames to DB
def save_dataframe(df, table_name, engine):
    df.to_sql(table_name, engine, if_exists='replace', index=False)

# Optional: fetch mapping from Baserow
def fetch_baserow(api_token, table_id):
    url = f"https://api.baserow.io/api/database/rows/table/{table_id}/?user_field_names=true"
    resp = requests.get(url, headers={"Authorization": f"Token {api_token}"})
    data = pd.DataFrame(resp.json()['results'])
    return data[['SKU','MSKU']]