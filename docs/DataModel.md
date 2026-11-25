# Data Model

## Overview

The Global Risk & Compliance Intelligence Platform data model is designed to support governance, risk, compliance, controls testing, audit management, remediation tracking, compliance incident monitoring, and access governance.

The model follows a relational design within SQL Server and serves as the foundation for analytical reporting in Power BI.

The architecture consists of:

- Master Data Entities
- Regulatory Management
- Risk Management
- Controls Management
- Testing & Assurance
- Findings & Remediation
- Compliance Monitoring
- Access Governance

---

# Entity Relationship Overview

```text
BusinessEntities
│
├── RiskRegister
│
├── Controls
│     │
│     ├── ControlTests
│     │
│     └── AuditFindings
│              │
│              └── RemediationActions
│
├── ImpactAssessments
│
├── ComplianceIncidents
│
└── AccessReviews

RegulatoryChanges
│
└── ImpactAssessments
```

---

# Data Domains

## Organization Management

### BusinessEntities

Represents legal entities, business units, subsidiaries, regions, and operational organizations.

#### Primary Key

```text
EntityID
```

#### Business Purpose

Provides organizational hierarchy and ownership alignment for risk, compliance, and control activities.

#### Key Attributes

| Column | Description |
|----------|-------------|
| EntityID | Unique entity identifier |
| EntityName | Business unit or legal entity |
| Country | Operating country |
| Region | Geographic region |
| BusinessLine | Business function |
| EntityType | Type of entity |
| EntityHead | Accountable executive |
| IsActive | Active indicator |
| EffectiveDate | Effective date |

---

# Regulatory Change Management

### RegulatoryChanges

Stores regulatory developments affecting the organization.

#### Primary Key

```text
RegChangeID
```

#### Business Purpose

Supports regulatory horizon scanning and compliance impact assessments.

#### Key Attributes

| Column | Description |
|----------|-------------|
| RegChangeID | Regulatory change identifier |
| RegulationName | Regulation title |
| Regulator | Governing authority |
| Country | Applicable country |
| Region | Applicable region |
| Topic | Regulatory topic |
| AnnouncementDate | Publication date |
| EffectiveDate | Required implementation date |
| Priority | Regulatory priority |
| Summary | Overview description |
| SourceReference | External reference |

---

# Regulatory Impact Assessment

### ImpactAssessments

Tracks assessment activities related to new or changing regulations.

#### Primary Key

```text
AssessmentID
```

#### Foreign Keys

```text
RegChangeID
EntityID
```

#### Business Purpose

Determines business applicability, compliance gaps, and remediation requirements.

#### Key Attributes

| Column | Description |
|----------|-------------|
| AssessmentID | Assessment identifier |
| RegChangeID | Regulatory reference |
| EntityID | Impacted entity |
| AssessmentDate | Assessment completion date |
| ImpactLevel | Risk impact level |
| Applicability | Applicability determination |
| GapIdentified | Gap indicator |
| AssessmentOwner | Responsible assessor |
| TargetCompletionDate | Planned completion |
| AssessmentStatus | Assessment state |
| Comments | Assessment notes |

---

# Enterprise Risk Management

### RiskRegister

Stores enterprise and operational risks.

#### Primary Key

```text
RiskID
```

#### Foreign Key

```text
EntityID
```

#### Business Purpose

Central repository of identified risk exposures.

#### Key Attributes

| Column | Description |
|----------|-------------|
| RiskID | Risk identifier |
| EntityID | Business entity |
| RiskTitle | Risk name |
| RiskCategory | Risk category |
| RiskOwner | Accountable owner |
| Likelihood | Occurrence probability |
| Impact | Business impact |
| InherentRiskScore | Pre-control risk score |
| ResidualRiskScore | Post-control risk score |
| RiskRating | Risk classification |
| Status | Current status |
| IdentifiedDate | Discovery date |

---

# Controls Management

### Controls

Stores internal controls and compliance controls.

#### Primary Key

```text
ControlID
```

#### Foreign Key

```text
EntityID
```

#### Business Purpose

Provides inventory and management of controls designed to mitigate risks and satisfy regulatory requirements.

#### Key Attributes

| Column | Description |
|----------|-------------|
| ControlID | Control identifier |
| EntityID | Business entity |
| ControlName | Control name |
| ControlDomain | Control classification |
| ControlDescription | Description |
| ControlOwner | Responsible owner |
| ControlFrequency | Frequency |
| ControlType | Preventive or detective |
| Criticality | Importance |
| IsKeyControl | Key control indicator |
| Status | Current state |

---

# Controls Testing

### ControlTests

Stores testing results for individual controls.

#### Primary Key

```text
TestID
```

#### Foreign Keys

```text
ControlID
EntityID
```

#### Business Purpose

Measures control effectiveness and operational performance.

#### Key Attributes

| Column | Description |
|----------|-------------|
| TestID | Test identifier |
| ControlID | Tested control |
| EntityID | Related business entity |
| TestDate | Execution date |
| TestingPeriod | Test period |
| TestType | Methodology |
| TestResult | Outcome |
| SampleSize | Population sampled |
| ExceptionsCount | Number of exceptions |
| Tester | Tester name |
| Notes | Supporting comments |

---

# Audit & Compliance Findings

### AuditFindings

Stores findings identified through audits, compliance reviews, and testing activities.

#### Primary Key

```text
FindingID
```

#### Foreign Keys

```text
EntityID
ControlID
```

#### Business Purpose

Tracks deficiencies requiring corrective action.

#### Key Attributes

| Column | Description |
|----------|-------------|
| FindingID | Finding identifier |
| EntityID | Impacted entity |
| ControlID | Affected control |
| FindingTitle | Finding title |
| Severity | Risk severity |
| FindingSource | Audit source |
| DateOpened | Open date |
| DueDate | Target date |
| DateClosed | Completion date |
| Status | Finding status |
| FindingOwner | Responsible owner |
| Description | Finding details |

---

# Remediation Management

### RemediationActions

Tracks corrective actions intended to resolve findings.

#### Primary Key

```text
ActionID
```

#### Foreign Keys

```text
FindingID
EntityID
```

#### Business Purpose

Provides visibility into issue remediation progress.

#### Key Attributes

| Column | Description |
|----------|-------------|
| ActionID | Action identifier |
| FindingID | Related finding |
| EntityID | Responsible entity |
| ActionDescription | Corrective action |
| ActionOwner | Accountable owner |
| CreatedDate | Created date |
| DueDate | Due date |
| CompletionDate | Actual completion |
| Status | Action status |
| Priority | Priority level |
| EvidenceReference | Supporting evidence |

---

# Compliance Incident Management

### ComplianceIncidents

Stores compliance breaches, incidents, and regulatory events.

#### Primary Key

```text
IncidentID
```

#### Foreign Key

```text
EntityID
```

#### Business Purpose

Tracks compliance incidents and business impacts.

#### Key Attributes

| Column | Description |
|----------|-------------|
| IncidentID | Incident identifier |
| EntityID | Business entity |
| IncidentDate | Event date |
| IncidentType | Category |
| Severity | Incident severity |
| ReportedBy | Reporter |
| Status | Current status |
| ResolutionDate | Resolution date |
| PotentialImpactUSD | Estimated financial impact |
| Description | Incident details |

---

# Access Governance

### AccessReviews

Stores user access certification and review activity.

#### Primary Key

```text
AccessReviewID
```

#### Foreign Key

```text
EntityID
```

#### Business Purpose

Supports access governance and Segregation of Duties controls.

#### Key Attributes

| Column | Description |
|----------|-------------|
| AccessReviewID | Review identifier |
| EntityID | Business entity |
| ReviewPeriod | Review cycle |
| ApplicationName | Application reviewed |
| UserPopulation | Number reviewed |
| Reviewer | Reviewer name |
| ReviewDate | Review date |
| ExceptionsIdentified | Exceptions discovered |
| ExceptionsResolved | Exceptions resolved |
| ReviewStatus | Review state |
| CertificationStatus | Certification outcome |

---

# Relationship Matrix

| Parent Table | Child Table | Relationship |
|-------------|------------|-------------|
| BusinessEntities | RiskRegister | One-to-Many |
| BusinessEntities | Controls | One-to-Many |
| BusinessEntities | ImpactAssessments | One-to-Many |
| BusinessEntities | ControlTests | One-to-Many |
| BusinessEntities | AuditFindings | One-to-Many |
| BusinessEntities | RemediationActions | One-to-Many |
| BusinessEntities | ComplianceIncidents | One-to-Many |
| BusinessEntities | AccessReviews | One-to-Many |
| RegulatoryChanges | ImpactAssessments | One-to-Many |
| Controls | ControlTests | One-to-Many |
| Controls | AuditFindings | One-to-Many |
| AuditFindings | RemediationActions | One-to-Many |

---

# Reporting Model

For analytics and Power BI reporting, the operational model is transformed into a dimensional star schema.

## Fact Tables

```text
FactRisk
FactControlTesting
FactAuditFindings
FactRemediationActions
FactComplianceIncidents
FactAccessReviews
```

## Dimension Tables

```text
DimDate
DimEntity
DimRegion
DimCountry
DimRiskCategory
DimControl
DimRegulation
DimFindingSeverity
```

---

# Data Quality Standards

All data loaded into the platform should conform to the following standards:

- Primary keys must be unique.
- Foreign keys must maintain referential integrity.
- Mandatory fields cannot be null.
- Status values must use approved reference values.
- Dates must be valid and logically sequenced.
- Financial impacts must be non-negative.
- Risk scores must comply with approved scoring methodologies.

---

# Future Data Model Enhancements

Planned future entities include:

```text
RegulatoryObligations
PolicyManagement
ThirdPartyRisk
VendorAssessments
EmployeeTraining
IndependenceMonitoring
IssueManagement
CyberRiskAssessments
ControlMappings
```

These enhancements will support broader Governance, Risk, and Compliance (GRC) reporting and regulatory traceability.
