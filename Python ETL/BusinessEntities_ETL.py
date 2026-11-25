import boto3
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# -- Extract from s3 bucket
s3 = boto3.client('s3')

obj = s3.get_object(Bucket='c3-compliance',
                    Key='seed/BusinessEntities.csv')


try:
    df = pd.read_csv(obj['Body'])
finally:
    obj['Body'].close()

# Convert EffectiveDate to datetime
df["EffectiveDate"] = pd.to_datetime(df["EffectiveDate"])

print(f"Rows read from csv: {len(df)} ")

# Connect to SQL Server
connection_string = quote_plus("DRIVER={ODBC Driver 17 for SQL Server};"
                                    "SERVER=localhost;"
                                    "DATABASE=GlobalRiskCompliance;"
                                    "Trusted_Connection=yes;")   

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={connection_string}")


# Load data into SQL Server
df.to_sql('BusinessEntities', con=engine, if_exists='append', index=False)


print("Load completed successfully.")
