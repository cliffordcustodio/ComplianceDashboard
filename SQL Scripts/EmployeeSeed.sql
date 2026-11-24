TRUNCATE TABLE EmployeeSeed;
GO

;WITH Numbers AS
(
    SELECT TOP (500000)
        ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS N
    FROM sys.all_objects a
    CROSS JOIN sys.all_objects b
)

INSERT INTO EmployeeSeed
(
    EmployeeNumber,
    FirstName,
    LastName,
    EmailAddress,

    BusinessUnitName,
    LocationCode,
    GradeCode,
    EmploymentStatusName,

    ManagerEmployeeNumber,

    HireDate,
    TerminationDate,

    SourceSystem
)

SELECT

    CONCAT('E',FORMAT(N,'000000')),

    ------------------------------------------------
    -- First Names
    ------------------------------------------------
    CHOOSE
    (
        ((N-1)%40)+1,

        'James','Harry','Hermione','Ron',
        'John','Holly','Luna','Neville',
        'Emma','Olivia','Sophia','Liam',

        'Noah','William','Charlotte',
        'Priya','Amit','Rahul','Arjun',
        'Ananya',

        'Thabo','Nomsa','Sipho',
        'Lebo','Anele',

        'Sean','Siobhan','Patrick',
        'Niamh','Connor',

        'Miguel','Maria','Jose',
        'Isabella','Ramon',

        'Jihoon','Minseo','Seojun',
        'Yuna','Eunwoo'
    ),

    ------------------------------------------------
    -- Last Names
    ------------------------------------------------
    CHOOSE
    (
        ((N-1)%60)+1,

        -- Bond
        'Bond',
        'Leiter',
        'Tanner',
        'Moneypenny',
        'Lynd',
        'Swann',
        'Trevelyan',
        'Silva',
        'Greene',
        'Carver',

        -- Die Hard
        'McClane',
        'Powell',
        'Gruber',
        'Gennero',
        'Johnson',

        -- Harry Potter
        'Potter',
        'Weasley',
        'Granger',
        'Malfoy',
        'Black',
        'Lovegood',
        'Longbottom',
        'Diggory',
        'Snape',
        'Dumbledore',

        -- India
        'Kapoor',
        'Khan',
        'Kumar',
        'Chopra',
        'Bachchan',
        'Roshan',
        'Devgan',

        -- South Africa
        'Nkosi',
        'Dlamini',
        'Zulu',
        'Ndlovu',
        'Mokoena',
        'Khumalo',

        -- Philippines
        'Reyes',
        'Santos',
        'Garcia',
        'Cruz',
        'Flores',
        'Ramos',

        -- Ireland
        'Murphy',
        'Kelly',
        'Ryan',
        'Walsh',
        'Byrne',
        'Doyle',

        -- Canada
        'Campbell',
        'Clark',
        'Martin',
        'Anderson',
        'Mitchell',
        'Walker',
        'Taylor',
        'Wilson'
    ),

    CONCAT(
        'employee',
        N,
        '@sourcecompany.com'
    ),

    ------------------------------------------------
    -- Business Unit
    ------------------------------------------------
    CHOOSE
    (
        ((N-1)%6)+1,

        'Audit',
        'Tax',
        'Advisory',
        'Risk Consulting',
        'Independence',
        'Technology'
    ),

    ------------------------------------------------
    -- Office Location
    ------------------------------------------------
    CHOOSE
    (
        ((N-1)%20)+1,

        'LON',
        'MAN',
        'DUB',
        'TOR',
        'VAN',

        'NYC',
        'CHI',
        'SEA',

        'SEL',
        'BSN',

        'MUM',
        'DEL',

        'JHB',
        'CPT',

        'SIN',
        'HKG',

        'SYD',
        'MEL',

        'PAR',
        'BER'
    ),

    ------------------------------------------------
    -- Grade Distribution
    ------------------------------------------------
    CASE
        WHEN N % 100 < 50 THEN 'A1'
        WHEN N % 100 < 75 THEN 'A2'
        WHEN N % 100 < 90 THEN 'M1'
        WHEN N % 100 < 97 THEN 'SM1'
        ELSE 'P1'
    END,

    ------------------------------------------------
    -- Employment Status
    ------------------------------------------------
    CASE
        WHEN N % 100 < 94 THEN 'Active'
        WHEN N % 100 < 97 THEN 'Leave of Absence'
        WHEN N % 100 < 98 THEN 'Secondment'
        WHEN N % 100 < 99 THEN 'Retired'
        ELSE 'Terminated'
    END,

    ------------------------------------------------
    -- Manager Number
    ------------------------------------------------
    CASE
        WHEN N % 100 >= 97
            THEN NULL
        ELSE CONCAT
        (
            'E',
            FORMAT(((N % 3000)+1),'000000')
        )
    END,

    ------------------------------------------------
    -- Hire Date
    ------------------------------------------------
    DATEADD
    (
        DAY,
        -(N % 7000),
        CAST(GETDATE() AS DATE)
    ),

    ------------------------------------------------
    -- Termination Date
    ------------------------------------------------
    CASE
        WHEN N % 100 = 99
        THEN DATEADD
        (
            DAY,
            365,
            DATEADD
            (
                DAY,
                -(N % 7000),
                CAST(GETDATE() AS DATE)
            )
        )
        ELSE NULL
    END,

    ------------------------------------------------
    -- Source System
    ------------------------------------------------
    CHOOSE
    (
        ((N-1)%4)+1,

        'Workday',
        'SuccessFactors',
        'PeopleSoft',
        'SAP HCM'
    )

FROM Numbers;
GO
