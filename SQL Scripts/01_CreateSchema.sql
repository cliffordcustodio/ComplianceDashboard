/* Global Risk & Compliance sample database - synthetic demonstration data */


CREATE TABLE
    dbo.BusinessEntities (
        EntityID varchar(10) NOT NULL PRIMARY KEY,
        EntityName nvarchar (150) NOT NULL,
        Country nvarchar (80) NOT NULL,
        Region nvarchar (40) NOT NULL,
        BusinessLine nvarchar (40) NOT NULL,
        EntityType nvarchar (40) NOT NULL,
        EntityHead nvarchar (80) NOT NULL,
        IsActive varchar(3) NOT NULL,
        EffectiveDate date NOT NULL
    );

CREATE TABLE
    dbo.RegulatoryChanges (
        RegChangeID varchar(12) NOT NULL PRIMARY KEY,
        RegulationName nvarchar (180) NOT NULL,
        Regulator nvarchar (100) NOT NULL,
        Country nvarchar (80) NOT NULL,
        Region nvarchar (40) NOT NULL,
        Topic nvarchar (80) NOT NULL,
        AnnouncementDate date NOT NULL,
        EffectiveDate date NOT NULL,
        Priority varchar(20) NOT NULL,
        Summary nvarchar (300) NOT NULL,
        SourceReference varchar(40) NOT NULL
    );

CREATE TABLE
    dbo.RiskRegister (
        RiskID varchar(12) NOT NULL PRIMARY KEY,
        EntityID varchar(10) NOT NULL,
        RiskTitle nvarchar (180) NOT NULL,
        RiskCategory nvarchar (50) NOT NULL,
        RiskOwner nvarchar (80) NOT NULL,
        Likelihood int NOT NULL,
        Impact int NOT NULL,
        InherentRiskScore decimal(5, 1) NOT NULL,
        ResidualRiskScore decimal(5, 1) NOT NULL,
        RiskRating varchar(20) NOT NULL,
        Status varchar(20) NOT NULL,
        IdentifiedDate date NOT NULL,
        CONSTRAINT FK_RiskRegister_Entity FOREIGN KEY (EntityID) REFERENCES dbo.BusinessEntities (EntityID)
    );

CREATE TABLE
    dbo.Controls (
        ControlID varchar(12) NOT NULL PRIMARY KEY,
        EntityID varchar(10) NOT NULL,
        ControlName nvarchar (150) NOT NULL,
        ControlDomain nvarchar (80) NOT NULL,
        ControlDescription nvarchar (300) NOT NULL,
        ControlOwner nvarchar (80) NOT NULL,
        ControlFrequency varchar(20) NOT NULL,
        ControlType varchar(20) NOT NULL,
        Criticality varchar(20) NOT NULL,
        IsKeyControl varchar(3) NOT NULL,
        Status varchar(20) NOT NULL,
        CONSTRAINT FK_Controls_Entity FOREIGN KEY (EntityID) REFERENCES dbo.BusinessEntities (EntityID)
    );

CREATE TABLE
    dbo.ImpactAssessments (
        AssessmentID varchar(12) NOT NULL PRIMARY KEY,
        RegChangeID varchar(12) NOT NULL,
        EntityID varchar(10) NOT NULL,
        AssessmentDate date NOT NULL,
        ImpactLevel varchar(30) NOT NULL,
        Applicability varchar(30) NOT NULL,
        GapIdentified varchar(3) NOT NULL,
        AssessmentOwner nvarchar (80) NOT NULL,
        TargetCompletionDate date NOT NULL,
        AssessmentStatus varchar(20) NOT NULL,
        Comments nvarchar (300) NOT NULL,
        CONSTRAINT FK_Impact_Reg FOREIGN KEY (RegChangeID) REFERENCES dbo.RegulatoryChanges (RegChangeID),
        CONSTRAINT FK_Impact_Entity FOREIGN KEY (EntityID) REFERENCES dbo.BusinessEntities (EntityID)
    );

CREATE TABLE
    dbo.ControlTests (
        TestID varchar(12) NOT NULL PRIMARY KEY,
        ControlID varchar(12) NOT NULL,
        EntityID varchar(10) NOT NULL,
        TestDate date NOT NULL,
        TestingPeriod varchar(10) NOT NULL,
        TestType varchar(40) NOT NULL,
        TestResult varchar(30) NOT NULL,
        SampleSize int NOT NULL,
        ExceptionsCount int NOT NULL,
        Tester nvarchar (80) NOT NULL,
        Notes nvarchar (300) NOT NULL,
        CONSTRAINT FK_Test_Control FOREIGN KEY (ControlID) REFERENCES dbo.Controls (ControlID),
        CONSTRAINT FK_Test_Entity FOREIGN KEY (EntityID) REFERENCES dbo.BusinessEntities (EntityID)
    );

CREATE TABLE
    dbo.AuditFindings (
        FindingID varchar(12) NOT NULL PRIMARY KEY,
        EntityID varchar(10) NOT NULL,
        ControlID varchar(12) NOT NULL,
        FindingTitle nvarchar (180) NOT NULL,
        Severity varchar(20) NOT NULL,
        FindingSource varchar(40) NOT NULL,
        DateOpened date NOT NULL,
        DueDate date NOT NULL,
        DateClosed date NULL,
        Status varchar(20) NOT NULL,
        FindingOwner nvarchar (80) NOT NULL,
        Description nvarchar (300) NOT NULL,
        CONSTRAINT FK_Finding_Entity FOREIGN KEY (EntityID) REFERENCES dbo.BusinessEntities (EntityID),
        CONSTRAINT FK_Finding_Control FOREIGN KEY (ControlID) REFERENCES dbo.Controls (ControlID)
    );

CREATE TABLE
    dbo.RemediationActions (
        ActionID varchar(12) NOT NULL PRIMARY KEY,
        FindingID varchar(12) NOT NULL,
        EntityID varchar(10) NOT NULL,
        ActionDescription nvarchar (180) NOT NULL,
        ActionOwner nvarchar (80) NOT NULL,
        CreatedDate date NOT NULL,
        DueDate date NOT NULL,
        CompletionDate date NULL,
        Status varchar(20) NOT NULL,
        Priority varchar(20) NOT NULL,
        EvidenceReference varchar(40) NOT NULL,
        CONSTRAINT FK_Action_Finding FOREIGN KEY (FindingID) REFERENCES dbo.AuditFindings (FindingID),
        CONSTRAINT FK_Action_Entity FOREIGN KEY (EntityID) REFERENCES dbo.BusinessEntities (EntityID)
    );

CREATE TABLE
    dbo.ComplianceIncidents (
        IncidentID varchar(12) NOT NULL PRIMARY KEY,
        EntityID varchar(10) NOT NULL,
        IncidentDate date NOT NULL,
        IncidentType varchar(50) NOT NULL,
        Severity varchar(20) NOT NULL,
        ReportedBy nvarchar (80) NOT NULL,
        Status varchar(30) NOT NULL,
        ResolutionDate date NULL,
        PotentialImpactUSD decimal(14, 2) NOT NULL,
        Description nvarchar (300) NOT NULL,
        CONSTRAINT FK_Incident_Entity FOREIGN KEY (EntityID) REFERENCES dbo.BusinessEntities (EntityID)
    );

CREATE TABLE
    dbo.AccessReviews (
        AccessReviewID varchar(12) NOT NULL PRIMARY KEY,
        EntityID varchar(10) NOT NULL,
        ReviewPeriod varchar(10) NOT NULL,
        ApplicationName nvarchar (100) NOT NULL,
        UserPopulation int NOT NULL,
        Reviewer nvarchar (80) NOT NULL,
        ReviewDate date NOT NULL,
        ExceptionsIdentified int NOT NULL,
        ExceptionsResolved int NOT NULL,
        ReviewStatus varchar(20) NOT NULL,
        CertificationStatus varchar(40) NOT NULL,
        CONSTRAINT FK_Access_Entity FOREIGN KEY (EntityID) REFERENCES dbo.BusinessEntities (EntityID)
    );
