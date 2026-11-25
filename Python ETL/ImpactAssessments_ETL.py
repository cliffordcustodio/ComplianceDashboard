import boto3
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from datetime import datetime

# =============================
# S3 Bucket Configuration
# =============================

BUCKET_NAME = 'c3-compliance'
FILE_KEY = 'seed/ImpactAssessments.csv'

VALID_ASSESSMENT_STATUS = ['Completed', 'In Progress', 'Not Started', 'Overdue']
VALID_IMPACT_LEVELS = ['High', 'Medium', 'Low', 'Critical', 'Not Applicable']

# =============================
# Database Configuration
# =============================

connection_string = quote_plus("DRIVER={ODBC Driver 17 for SQL Server};"
                                    "SERVER=localhost;"
                                    "DATABASE=GlobalRiskCompliance;"
                                    "Trusted_Connection=yes;")

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={connection_string}")

# =============================
# Extract from S3 Bucket
# =============================

print(f"Extracting data from S3 bucket: {BUCKET_NAME}, file: {FILE_KEY}")

s3 = boto3.client('s3') # Create an S3 client
obj = s3.get_object(Bucket=BUCKET_NAME, 
                    Key=FILE_KEY) # Get the object from S3

try:
    df = pd.read_csv(obj['Body']) # Read the CSV data into a DataFrame
finally:
    obj['Body'].close() # Close the S3 object body

source_row = len(df) # Count the number of rows read from the CSV
print(f"Rows read from csv: {source_row} ")

# =============================
# VALIDATIONS
# =============================

validation_error = [] # intiailiaze a blank array to contains any validation issues


# =============================
# Required Field Validation
# =============================

required_fields = [
    'AssessmentID',
    'RegChangeID',
    'EntityID',
    'AssessmentDate',
    'ImpactLevel',
    'Applicability',
    'GapIdentified',
    'AssessmentOwner',
    'TargetCompletionDate',
    'AssessmentStatus',
    'Comments'
]


missing_fields = df[
    df[required_fields].isnull().any(axis=1)
].copy() # Filter rows with missing required fields
print(f"Rows with missing required fields: {len(missing_fields)}")

if not missing_fields.empty:
    missing_fields["RejectReason"] = "Required Field Missing"
    validation_error.append(missing_fields)

# =============================
# Date Validation
# ===========================

df['AssessmentDate'] = pd.to_datetime(df['AssessmentDate'], errors='coerce') # Convert AssessmentDate to datetime, coerce errors
df['TargetCompletionDate'] = pd.to_datetime(df['TargetCompletionDate'], errors= 'coerce') # Convert TargetCompletionDate to datetime, coerce errors

invalid_dates = df[ df['AssessmentDate'].isna() | df['TargetCompletionDate'].isna() ] # Filter rows with invalid dates
print(f"Rows with invalid dates: {len(invalid_dates)}")

if not invalid_dates.empty:
    invalid_dates["RejectReason"] = "Invalid Date"
    validation_error.append(invalid_dates)

# =============================
# Business Rule Validation
# =============================


# ============================
# Duplicate Check
# =========================

duplicate_rows = df[df.duplicated(subset=['AssessmentID'], keep=False)] # Identify duplicate rows based on AssessmentID
print(f"Rows with duplicate AssessmentIDs: {len(duplicate_rows)}")

if not duplicate_rows.empty:
    duplicate_rows["RejectReason"] = "Duplicate Assessment ID in File"
    validation_error.append(duplicate_rows)

# ============================
# Duplicate Check Database
# ============================

existing_ids = pd.read_sql("SELECT AssessmentID FROM ImpactAssessments",
                            engine) # Query existing AssessmentIDs from the database

duplicatein_db = df[df['AssessmentID'].isin(existing_ids['AssessmentID'])]
print(f"Rows with AssessmentIDs already in database: {len(duplicatein_db)}")

if not duplicatein_db.empty:
    duplicatein_db["RejectReason"] = "Assessment ID already exists"
    validation_error.append(duplicatein_db)


# ============================
# Impact level validation & Assessment Status validation
# ============================

invalid_impact = df[~df['ImpactLevel'].isin(VALID_IMPACT_LEVELS)] # Filter rows with invalid ImpactLevel
print(f"Rows with invalid ImpactLevels: {len(invalid_impact)}")

if invalid_impact.empty:
    invalid_impact["RejectReason"] = "Invalid Impact Level"
    validation_error.append(invalid_impact)

invalid_assessment_status = df[~df['AssessmentStatus'].isin(VALID_ASSESSMENT_STATUS)] # Filter rows with invalid AssessmentStatus
print(f"Rows with invalid AssessmentStatus: {len(invalid_assessment_status)}")

if invalid_assessment_status.empty:
    invalid_assessment_status["RejectReason"] = "Invalid Assessment Status"
    validation_error.append(invalid_assessment_status)

# ============================
# Foreign Key Validation
# ============================

valid_reg_changes = pd.read_sql("SELECT RegChangeID FROM RegulatoryChanges", engine) # Query valid RegChangeIDs from the database
invalid_reg_changes = df[~df['RegChangeID'].isin(valid_reg_changes['RegChangeID'])] # Filter rows with invalid RegChangeIDs
print(f"Rows with invalid RegChangeIDs: {len(invalid_reg_changes)}")

if not valid_reg_changes.empty:
    valid_reg_changes["RejectReason"] = "Invalid RegChangeID"
    validation_error.append( valid_reg_changes)

# ===========================
# Business Entity Validation
# ===========================

valid_entities = pd.read_sql("SELECT EntityID FROM BusinessEntities", engine)   
invalid_entity = df[ ~df["EntityID"].isin(valid_entities['EntityID'])]

if not invalid_entity.empty:
    invalid_entity["RejectReason"] = "Invalid EntityID"
    validation_error.append( invalid_entity)


# ============================
# Build the Reject file
# ============================

if validation_error:
    rejects = pd.concat (validation_error, ignore_index=True)
else:
    rejects = pd.DataFrame()


# =============================
# Build the valid records
# =============================

if not rejects.empty:
    valid_records = df [ ~df["AssessmentID"].isin (rejects["AssessmentID"])].copy()

else:
    valid_records = df.copy()


timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
)

reject_file = (
    f"ImpactAssessments_Rejects_{timestamp}.csv"
)

if not rejects.empty:
    rejects.to_csv(
        reject_file,
        index=False
    )

# =========================================
# Load the valida records
# =========================================


loaded_rows = 0

if not valid_records.empty:

    valid_records.to_sql(
        "ImpactAssessments",
        con=engine,
        schema="dbo",
        if_exists="append",
        index=False
    )

    loaded_rows = len(valid_records)


# =================================================
# ETL AUDIT LOGGING
# =================================================

audit_record = pd.DataFrame([{
    "ProcessName":
        "ImpactAssessments_ETL",

    "SourceFile":
        "ImpactAssessments.csv",

    "LoadDate":
        datetime.now(),

    "SourceRows":
        source_row,

    "RejectedRows":
        len(rejects),

    "LoadedRows":
        loaded_rows,

    "Status":
        "SUCCESS"
}])

audit_record.to_sql(
    "ETL_Audit",
    con=engine,
    schema="dbo",
    if_exists="append",
    index=False
)

# =================================================
# SUMMARY
# =================================================

print("\n========================")
print("ETL LOAD COMPLETE")
print("========================")

print(f"Source Rows  : {source_row}")
print(f"Rejected Rows: {len(rejects)}")
print(f"Loaded Rows  : {loaded_rows}")

print("\nAudit Record Written")