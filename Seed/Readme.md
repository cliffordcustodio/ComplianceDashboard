# Seed Data

## Overview

This folder contains the synthetic source data used by the Global Risk & Compliance Intelligence Platform.

The files in this directory serve as the initial data load ("seed data") for the platform and are uploaded to AWS S3, where they are subsequently processed by the Python ETL framework and loaded into SQL Server for reporting and analytics.

The datasets are intentionally designed to simulate real-world Governance, Risk, and Compliance (GRC) operations within a global financial services organization.

---

# Data Flow

```text
Seed CSV Files
        |
        v

AWS S3 Landing Zone
        |
        v

Python ETL Process
        |
        v

SQL Server Database
        |
        v

Power BI Dashboards
```

---

# Folder Structure

```text
seed/

│
├── BusinessEntities.csv
├── RegulatoryChanges.csv
├── RiskRegister.csv
├── Controls.csv
├── ImpactAssessments.csv
├── ControlTests.csv
├── AuditFindings.csv
├── RemediationActions.csv
├── ComplianceIncidents.csv
├── AccessReviews.csv
│
└── README.md
```

---

# Dataset Inventory

## BusinessEntities.csv

Contains organizational structure information.

Purpose:

- Legal entities
- Business units
- Regional structures
- Entity ownership

Example Data:

```text
EntityID
EntityName
Country
Region
BusinessLine
EntityType
EntityHead
```

Corresponding Database Table:

```text
dbo.BusinessEntities
```

---

## RegulatoryChanges.csv

Contains regulatory developments and compliance requirements.

Purpose:

- Regulatory tracking
- Compliance horizon scanning
- Regulatory impact analysis

Example Data:

```text
RegChangeID
RegulationName
Regulator
Country
Region
Priority
EffectiveDate
```

Corresponding Database Table:

```text
dbo.RegulatoryChanges
```

---

## RiskRegister.csv

Contains enterprise risk inventory data.

Purpose:

- Risk identification
- Risk assessment
- Risk reporting

Example Data:

```text
RiskID
RiskTitle
RiskCategory
Likelihood
Impact
InherentRiskScore
ResidualRiskScore
```

Corresponding Database Table:

```text
dbo.RiskRegister
```

---

## Controls.csv

Contains compliance and risk control inventory.

Purpose:

- Control governance
- Control ownership
- Control classification

Example Data:

```text
ControlID
ControlName
ControlDomain
ControlFrequency
ControlType
Criticality
```

Corresponding Database Table:

```text
dbo.Controls
```

---

## ImpactAssessments.csv

Contains assessments performed against regulatory changes.

Purpose:

- Regulatory applicability reviews
- Gap assessments
- Implementation tracking

Corresponding Database Table:

```text
dbo.ImpactAssessments
```

---

## ControlTests.csv

Contains control testing results.

Purpose:

- Effectiveness testing
- Exception reporting
- Control assurance activities

Example Data:

```text
TestID
ControlID
TestResult
SampleSize
ExceptionsCount
```

Corresponding Database Table:

```text
dbo.ControlTests
```

---

## AuditFindings.csv

Contains audit and compliance findings.

Purpose:

- Audit issue tracking
- Deficiency management
- Root cause analysis

Corresponding Database Table:

```text
dbo.AuditFindings
```

---

## RemediationActions.csv

Contains corrective action plans.

Purpose:

- Issue remediation
- Action tracking
- Compliance closure activities

Corresponding Database Table:

```text
dbo.RemediationActions
```

---

## ComplianceIncidents.csv

Contains compliance-related incidents.

Purpose:

- Compliance monitoring
- Incident reporting
- Regulatory investigations

Corresponding Database Table:

```text
dbo.ComplianceIncidents
```

---

## AccessReviews.csv

Contains access certification review results.

Purpose:

- Access governance
- User certification
- Segregation of Duties validation

Corresponding Database Table:

```text
dbo.AccessReviews
```

---

# AWS S3 Storage Structure

The seed files are uploaded into the AWS S3 landing zone before ETL processing.

Recommended structure:

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

# File Standards

All seed files should conform to the following standards.

## Format

```text
CSV
```

## Encoding

```text
UTF-8
```

## Delimiter

```text
Comma (,)
```

## Header Row

Required.

Example:

```csv
EntityID,EntityName,Country,Region
```

---

# Data Quality Rules

The seed files should satisfy the following controls before loading.

### Completeness

Required fields must contain values.

### Uniqueness

Primary key values must be unique.

### Referential Integrity

Foreign key records must exist in parent datasets.

### Valid Dates

Date values must contain valid calendar dates.

### Valid Status Values

Statuses must use approved business values.

Examples:

```text
Open
Closed
In Progress
Completed
Active
Inactive
```

---

# ETL Processing Sequence

The datasets are loaded in dependency order.

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

This sequence ensures parent records are loaded before dependent child records.

---

# Sample ETL Workflow

```python
Extract
    ↓
Validate
    ↓
Transform
    ↓
Load
    ↓
Audit Logging
```

Example:

```python
df = pd.read_csv("RiskRegister.csv")

validate(df)

transform(df)

load_to_sql(df)
```

---

# Synthetic Data Disclaimer

All files contained within this folder utilize synthetic data created solely for educational, demonstration, and portfolio purposes.

The datasets do not contain:

- Real employees
- Real customers
- Real organizations
- Real regulatory investigations
- Confidential information
- Personally identifiable information (PII)

---

# Related Documentation

```text
/docs/Architecture.md
/docs/DataModel.md
/docs/ETLDesign.md

/sql/README.md
/python/README.md
```

These documents collectively describe the end-to-end architecture, data model, ETL processing, reporting framework, and governance metrics for the Global Risk & Compliance Intelligence Platform.
