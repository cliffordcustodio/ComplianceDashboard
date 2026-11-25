# ETL Design

## Overview

The Extract, Transform, and Load (ETL) framework is responsible for moving data from AWS S3 into the Global Risk & Compliance Intelligence Platform.

The ETL process standardizes, validates, enriches, and loads Governance, Risk, and Compliance (GRC) data into SQL Server where it can be consumed by Power BI dashboards and analytics solutions.

The design follows a layered architecture that promotes scalability, maintainability, auditability, and data quality.

---

# ETL Architecture

```text
+--------------------------------------------------+
|                 Source Layer                     |
+--------------------------------------------------+
|                                                  |
| AWS S3 Bucket                                    |
|                                                  |
| • BusinessEntities.csv                           |
| • RegulatoryChanges.csv                          |
| • RiskRegister.csv                               |
| • Controls.csv                                   |
| • ImpactAssessments.csv                          |
| • ControlTests.csv                               |
| • AuditFindings.csv                              |
| • RemediationActions.csv                         |
| • ComplianceIncidents.csv                        |
| • AccessReviews.csv                              |
|                                                  |
+--------------------------+-----------------------+
                           |
                           v
+--------------------------------------------------+
|                 Extract Layer                    |
+--------------------------------------------------+
|                                                  |
| Python                                           |
| boto3                                            |
| pandas                                           |
|                                                  |
+--------------------------+-----------------------+
                           |
                           v
+--------------------------------------------------+
|               Transformation Layer              |
+--------------------------------------------------+
|                                                  |
| Data Validation                                  |
| Data Cleansing                                   |
| Null Handling                                    |
| Reference Validation                             |
| KPI Derivations                                  |
| Standardization                                  |
| Data Quality Controls                            |
|                                                  |
+--------------------------+-----------------------+
                           |
                           v
+--------------------------------------------------+
|                 Load Layer                        |
+--------------------------------------------------+
|                                                  |
| SQL Server Staging Tables                        |
| SQL Server Operational Tables                    |
| SQL Server Reporting Tables                      |
|                                                  |
+--------------------------+-----------------------+
                           |
                           v
+--------------------------------------------------+
|               Analytics Layer                    |
+--------------------------------------------------+
|                                                  |
| Power BI                                         |
| Executive Dashboards                             |
| Compliance Reporting                             |
| Risk Analytics                                   |
|                                                  |
+--------------------------------------------------+
```

---

# ETL Objectives

The ETL process is designed to:

- Ingest source data from AWS S3
- Validate source records
- Enforce business rules
- Maintain referential integrity
- Load operational tables
- Produce reporting-ready data
- Maintain auditability
- Support historical reporting

---

# Source Data Layer

## Data Source

AWS S3 serves as the system landing zone.

### Raw Storage Structure

```text
s3://c3-compliance/

├── seed/
│   ├── BusinessEntities.csv
│   ├── RegulatoryChanges.csv
│   ├── RiskRegister.csv
│   ├── Controls.csv
│   ├── ImpactAssessments.csv
│   ├── ControlTests.csv
│   ├── AuditFindings.csv
│   ├── RemediationActions.csv
│   ├── ComplianceIncidents.csv
│   └── AccessReviews.csv
│
├── processed/
│
└── archive/
```

---

# Extraction Design

## Purpose

Retrieve source files from AWS S3 for processing.

## Technology

```text
Python
boto3
pandas
```

---

## Example Extraction Logic

```python
import boto3
import pandas as pd

s3 = boto3.client('s3')

obj = s3.get_object(
    Bucket='global-risk-compliance',
    Key='raw/RiskRegister.csv'
)

df = pd.read_csv(obj['Body'])
```

---

# Transformation Design

## Data Validation

Each dataset undergoes validation before loading.

Checks include:

```text
Required Fields
Data Types
Valid Dates
Duplicate Keys
Foreign Key Validation
Status Values
Numeric Ranges
```

---

## Required Field Validation

Example:

```python
required_columns = [
    'RiskID',
    'EntityID',
    'RiskTitle'
]
```

Records failing validation are rejected.

---

## Duplicate Detection

Example:

```python
duplicates = df[df.duplicated()]
```

Duplicate primary keys are logged for review.

---

## Date Validation

Example:

```python
df['IdentifiedDate'] = pd.to_datetime(
    df['IdentifiedDate'],
    errors='coerce'
)
```

Invalid dates are quarantined.

---

## Reference Validation

Validates:

```text
EntityID
ControlID
FindingID
RegChangeID
```

against parent tables.

---

# Data Standardization

Common transformations include:

## Status Standardization

Before:

```text
Open
OPEN
open
```

After:

```text
Open
```

---

## Trim Whitespace

Before:

```text
Risk Management
Risk Management
```

After:

```text
Risk Management
```

---

## Convert Text Casing

Standardization example:

```text
high
HIGH
High
```

Converted to:

```text
High
```

---

# Derived Metrics

The ETL process calculates reporting metrics.

## Control Failure Rate

```python
df['ControlFailureRate'] = (
    df['ExceptionsCount'] /
    df['SampleSize']
)
```

---

## Compliance Rate

```python
df['ComplianceRate'] = (
    df['ControlsPassed'] /
    df['ControlsTested']
)
```

---

## Finding Age

```python
df['FindingAgeDays'] = (
    pd.Timestamp.today() -
    pd.to_datetime(df['DateOpened'])
).dt.days
```

---

## Incident Resolution Days

```python
df['ResolutionDays'] = (
    pd.to_datetime(df['ResolutionDate']) -
    pd.to_datetime(df['IncidentDate'])
).dt.days
```

---

# Load Design

The load process follows a layered architecture.

## Stage 1

Staging Layer

Purpose:

- Raw ingestion
- Validation processing
- Error handling

Example:

```text
stgBusinessEntities
stgRiskRegister
stgControls
```

---

## Stage 2

Operational Layer

Purpose:

- Production data repository
- Transactional reporting
- Referential integrity

Tables:

```text
BusinessEntities
RegulatoryChanges
RiskRegister
Controls
ImpactAssessments
ControlTests
AuditFindings
RemediationActions
ComplianceIncidents
AccessReviews
```

---

## Stage 3

Analytics Layer

Purpose:

- Reporting optimization
- Dashboard performance
- Historical analysis

Fact Tables:

```text
FactRisk
FactControlTesting
FactAuditFindings
FactComplianceIncidents
FactAccessReviews
```

Dimension Tables:

```text
DimDate
DimEntity
DimControl
DimRegulation
DimRiskCategory
DimRegion
```

---

# Load Sequence

To maintain referential integrity, datasets must load in dependency order.

```text
1. BusinessEntities

2. RegulatoryChanges

3. RiskRegister

4. Controls

5. ImpactAssessments

6. ControlTests

7. AuditFindings

8. RemediationActions

9. ComplianceIncidents

10. AccessReviews
```

---

# Error Handling Framework

Failed records are written to an exceptions table.

Example:

```text
ETLExceptions
```

Columns:

```text
ExceptionID
SourceFile
RecordIdentifier
ErrorType
ErrorMessage
LoadDate
```

---

# Audit Logging

Each ETL run generates an audit record.

Example:

```text
ETLExecutionLog
```

Columns:

```text
ExecutionID
ProcessName
StartTime
EndTime
RecordsRead
RecordsLoaded
RecordsRejected
Status
```

---

# Incremental Load Strategy

Future enhancements may support incremental processing.

Strategy:

```text
Initial Load
    ↓
Full Refresh
    ↓
Incremental Updates
```

Methods:

- Change Detection
- Last Modified Date
- Delta Processing

---

# Data Quality Controls

The ETL process enforces the following controls.

| Control | Description |
|----------|------------|
| Completeness | Required fields populated |
| Accuracy | Data conforms to business rules |
| Consistency | Standardized values |
| Timeliness | Recent records loaded |
| Integrity | Relationship validation |
| Uniqueness | Duplicate prevention |

---

# Performance Optimization

Recommended optimization techniques:

- Batch processing
- Bulk inserts
- Parallel file processing
- SQL indexing
- Incremental loads
- Partitioned fact tables

---

# Security Design

## Data in Transit

```text
HTTPS
TLS Encryption
```

---

## Data at Rest

```text
AWS S3 Encryption
SQL Server Encryption
```

---

## Access Controls

```text
AWS IAM Roles
Database Roles
Power BI RLS
```

---

# Monitoring & Operations

ETL monitoring should track:

- Successful Loads
- Failed Loads
- Processing Duration
- Data Volumes
- Rejected Records
- SLA Compliance

---

# ETL Success Criteria

An ETL run is considered successful when:

- Source files are retrieved.
- Validation rules pass.
- Referential integrity is maintained.
- Records are successfully loaded.
- Audit logs are created.
- Power BI datasets are refreshed.

---

# Future Enhancements

Planned improvements include:

- Apache Airflow orchestration
- AWS Lambda processing
- Event-driven ingestion
- Data quality dashboards
- Automated anomaly detection
- AI-assisted compliance analytics
- Near real-time reporting

---

# Related Documentation

```text
README.md

docs/
├── Architecture.md
├── DataModel.md
├── ETLDesign.md
├── KPICatalog.md
├── PowerBIDesign.md

sql/
├── README.md

seed/
├── README.md
```

The ETL framework serves as the central data integration layer connecting AWS S3, SQL Server, and Power BI, enabling trusted compliance, risk, audit, and governance reporting across the platform.
