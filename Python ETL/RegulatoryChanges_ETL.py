import boto3
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from datetime import datetime

# =============================
# S3 Bucket Configuration
# =============================

BUCKET_NAME = 'c3-compliance'
FILE_KEY = 'seed/RegulatoryChanges.csv'

VALID_PRIORITIES = ['High', 'Medium', 'Low', 'Critical']


# ==============================
# Database Configuration
# ==============================

connection_string = quote_plus("DRIVER={ODBC Driver 17 for SQL Server};"
                                    "SERVER=localhost;"
                                    "DATABASE=GlobalRiskCompliance;"
                                    "Trusted_Connection=yes;")

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={connection_string}")


# =============================
# Extract from S3 Bucket        
# =============================

print(f"Extracting data from S3 bucket: {BUCKET_NAME}, file: {FILE_KEY}")

s3 = boto3.client('s3')                             # Create an S3 client

obj = s3.get_object(Bucket=BUCKET_NAME, 
                    Key=FILE_KEY)                   # Get the object from S3

try:
    df = pd.read_csv(obj['Body'])                   # Read the CSV data into a DataFrame
finally:
    obj['Body'].close()                             # Close the S3 object body

source_row = len(df)                                # Count the number of rows read from the CSV
print(f"Rows read from csv: {source_row} ")

# =============================
# Required Field Validation
# =============================

required_fields = [
        'RegChangeID', 
        'RegulationName',
        'Regulator',
        'Country',
        'Region',
        'Topic',
        'AnnouncementDate',
        'EffectiveDate',
        'Priority',
        'Summary',
        'SourceReference']

required_fields_missing = df[ df[required_fields].isnull().any(axis=1) ]   # Identify rows with missing required fields
print(f"Rows with missing required fields: {len(required_fields_missing)}")

# =============================
# Date Validation
# ============================= 

df["AnnouncementDate"] = pd.to_datetime(df["AnnouncementDate"], errors='coerce')  # Convert AnnouncementDate to datetime
df["EffectiveDate"] = pd.to_datetime(df["EffectiveDate"], errors='coerce')        # Convert EffectiveDate to datetime

invalid_dates = df[ df["AnnouncementDate"].isna() | df["EffectiveDate"].isna() ]  # Identify rows with invalid dates
print(f"Rows with invalid dates: {len(invalid_dates)}")

# =============================
# Business Rule Validation
# =============================

invalid_date_sequence = df[df["EffectiveDate"] < df["AnnouncementDate"] ]
print(f"Rows with invalid date sequence: {len(invalid_date_sequence)}")

# =============================
# Duplicate Check
# =============================

duplicate_rows = df[df.duplicated(subset=['RegChangeID'], keep=False)]  # Identify duplicate rows based on RegChangeID
print(f"Rows with duplicate RegChangeID: {len(duplicate_rows)}")

# =============================
# Duplicate Check in Database
# =============================

existing_ids_query = "SELECT RegChangeID FROM RegulatoryChanges"

existing_ids = pd.read_sql(existing_ids_query, con=engine)  # Fetch existing RegChangeID from the database

duplicate_in_db = df[df['RegChangeID'].isin(existing_ids['RegChangeID'])]

print(f"Rows with duplicate RegChangeID in database: {len(duplicate_in_db)}")

# ==============================
# Build Reject List from missing required fields, invalid dates, invalid date sequence, duplicate rows, and duplicates in the database
# ==============================

rejects = pd.concat([
    required_fields_missing,
    invalid_dates,
    invalid_date_sequence, 
    duplicate_rows, 
    duplicate_in_db
]).drop_duplicates() 

# ==============================
# Valid Records
# ==============================

valid_records = (
    df.merge(
            rejects[['RegChangeID']], 
            how='left', 
            on='RegChangeID', 
            indicator=True
    )
)

valid_records = valid_records[
    valid_records['_merge'] == 'left_only'
].drop(columns=['_merge'])  # Keep only valid records that are not in the rejects list

# =============================
# Save the rejects to a CSV file for review
# =============================

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Generate a timestamp for the reject file name
reject_file = (f"RegulatoryChanges_Rejected_{timestamp}.csv")  # Define the reject file name

rejects.to_csv(reject_file, index=False)  # Save the rejects DataFrame to a CSV file
print(f"Rejects saved to: {reject_file}")

# =============================
# Load valid records into SQL Server
# =============================

if len(valid_records) > 0:
    valid_records.to_sql(
        'RegulatoryChanges', 
        con=engine, 
        if_exists='append', 
        index=False
    )  # Load valid records into the database

    print(f"Load completed successfully. Rows loaded: {len(valid_records)}")

# =============================
# Summary of the ETL Process
# =============================

print(f"Source Rows read from CSV                : {source_row}")
print(f"Missing Required Fields                  : {len(required_fields_missing)}")
print(f"Invalid Dates                            : {len(invalid_dates)}")
print(f"Invalid Date Sequence                    : {len(invalid_date_sequence)}")
print(f"Duplicate Rows                           : {len(duplicate_rows)}")
print(f"Duplicate Rows in Database               : {len(duplicate_in_db)}")
print(f"Total rows rejected                      : {len(rejects)}")
print(f"Total rows loaded                        : {len(valid_records)}")
print("ETL process completed successfully.")
