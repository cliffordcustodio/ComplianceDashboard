# ETL Folder

## Overview

The `etl/` folder contains the executable Python ETL processes responsible for extracting data from AWS S3, validating data quality, transforming data, and loading approved records into SQL Server.

Each ETL script is designed to process a specific source dataset and target table while enforcing enterprise-grade data quality controls, audit logging, reject processing, and reconciliation.

The folder serves as the operational processing layer of the GlobalCompliance platform.

---

# Folder Structure

```text
Python ETL/

├── accessreview_etl.py
├── regulatorychanges_etl.py
├── impactassessments_etl.py
├── controltesting_etl.py
├── policyexceptions_etl.py
├── riskissues_etl.py
├── auditfindings_etl.py
├── regulatoryobligations_etl.py
├── kriresults_etl.py
└── ...
```

---

# ETL Design Pattern

Each ETL follows the same processing lifecycle:

```text
Extract
   ↓
Validate
   ↓
Transform
   ↓
Load
   ↓
Audit
   ↓
Reconcile
```

This standardized approach ensures consistent processing across all compliance datasets.

---

# ETL Responsibilities

## Extract

Each ETL retrieves source data directly from AWS S3 using Boto3.

Example:

```python
obj = s3.get_object(
    Bucket="c3-compliance",
    Key="seed/ImpactAssessments.csv"
)

df = pd.read_csv(obj["Body"])
```

Responsibilities:

- Connect to AWS S3
- Retrieve source files
- Load file contents into Pandas DataFrames

---

## Validate

Before data is loaded into SQL Server, multiple validation controls are executed.

Supported validation types include:

### Required Field Validation

Ensures mandatory fields contain values.

Example:

```text
AssessmentID
EntityID
AssessmentDate
```

Records with missing required values are rejected.

---

### Duplicate Detection

Two levels of duplicate detection are supported.

#### File-Level Duplicates

Detects duplicate records within the incoming source file.

#### Database-Level Duplicates

Detects existing business keys already loaded into SQL Server.

Example:

```text
AssessmentID already exists in ImpactAssessments
```

---

### Date Validation

Verifies valid date formats.

Examples:

```text
AssessmentDate
TargetCompletionDate
AnnouncementDate
EffectiveDate
```

Invalid dates are rejected.

---

### Business Rule Validation

Validates business-specific logic.

Examples:

```text
TargetCompletionDate >= AssessmentDate
```

```text
EffectiveDate >= AnnouncementDate
```

---

### Domain Validation

Validates values against approved domains.

Examples:

```text
ImpactLevel

Low
Medium
High
Critical
```

```text
GapIdentified

Yes
No
```

---

### Reference Validation

Validates foreign key relationships before data is loaded.

Examples:

```text
RegChangeID
```

must exist in:

```text
RegulatoryChanges
```

and

```text
EntityID
```

must exist in:

```text
BusinessEntities
```

---

### Length Validation

Validates source values against SQL column definitions.

Example:

```text
AssessmentID VARCHAR(12)
```

Values exceeding column length are rejected.

---

# Validation Logger

All ETL jobs use the centralized `ValidationLogger` component.

Features include:

- Consolidated validation tracking
- Unique reject counting
- Multiple validation failures per record
- Audit-friendly reject reporting

Example:

```text
AssessmentID = IA000123

Reject Reasons:

Invalid Date
Invalid EntityID
Invalid RegChangeID
```

Stored as:

```text
Invalid Date;
Invalid EntityID;
Invalid RegChangeID
```

---

# Transform

Transformation logic standardizes and prepares data for loading.

Examples:

```python
df["AssessmentDate"] = pd.to_datetime(
    df["AssessmentDate"],
    errors="coerce"
)
```

Typical transformations include:

- Data type conversion
- Date conversion
- Data normalization
- Standardization
- Field formatting

---

# Load

Validated records are loaded into SQL Server target tables.

Example:

```python
valid_records.to_sql(
    "ImpactAssessments",
    con=engine,
    schema="dbo",
    if_exists="append",
    index=False
)
```

Load behavior:

- Append-only processing
- Referential integrity enforcement
- Existing key validation
- Transaction-safe operations

---

# Reject Processing

Invalid records are written to reject files for review and remediation.

Example:

```text
ImpactAssessments_Rejects_20261124_220000.csv
```

Reject files contain:

- Original source record
- Reject reason(s)
- Validation failure details

---

# Audit Logging

Every ETL execution writes an audit entry to:

```sql
dbo.ETL_Audit
```

Captured metrics:

```text
ProcessName
SourceFile
LoadDate
SourceRows
RejectedRows
LoadedRows
Status
Comments
```

Example:

```text
ProcessName   : ImpactAssessments_ETL
SourceRows    : 1500
RejectedRows  : 5
LoadedRows    : 1495
Status        : SUCCESS
```

---

# Reconciliation Controls

Every ETL performs source-to-target reconciliation.

Formula:

```text
Source Rows =
Loaded Rows +
Rejected Rows
```

Example:

```text
Source Rows    : 1500
Loaded Rows    : 1495
Rejected Rows  : 5
```

```text
1500 = 1495 + 5
```

If reconciliation fails, the ETL process terminates and logs an exception.

---

# Current ETL Processes

| ETL Process | Target Table |
|-------------|-------------|
| AccessReview | dbo.AccessReview |
| RegulatoryChanges | dbo.RegulatoryChanges |
| ImpactAssessments | dbo.ImpactAssessments |

Additional ETL processes will be added as the GlobalCompliance data model expands.

---

# Design Standards

All ETL processes follow common design principles:

- Reusable validation framework
- Centralized audit logging
- Consistent error handling
- Row-count reconciliation
- Standardized reject processing
- Metadata-driven design readiness
- Enterprise governance controls

This approach ensures scalability, maintainability, auditability, and regulatory compliance across all ETL processes.

---

# Future Enhancements

Planned improvements include:

- BaseETL framework
- Metadata-driven configuration
- Incremental loading
- Parallel execution
- Data lineage tracking
- Data quality scorecards
- Automated notifications
- Power BI ETL monitoring dashboard
- CI/CD deployment pipeline
- Unit testing framework

The long-term objective is to transition all ETL processes into a configurable, metadata-driven architecture requiring minimal code changes for onboarding new datasets.
