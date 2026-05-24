-- ============================================================
-- HUMANITARIAN AID ELIGIBILITY & DISTRIBUTION ANALYSIS
-- Simulated Dataset — For Portfolio Demonstration Only
-- Author: Hala Dib
-- Date: 2026
-- Note: All data is synthetic. Reflects UN-style data workflows.
-- ============================================================
-- SECTION 1: DATABASE SETUP
-- ============================================================

CREATE TABLE IF NOT EXISTS aid_data (
    Case_ID               VARCHAR(10)   PRIMARY KEY,
    Camp                  VARCHAR(50)   NOT NULL,
    Family_Size           INT           NOT NULL,
    Vulnerability_Category VARCHAR(30)  NOT NULL,
    Vulnerability_Score   DECIMAL(5,1)  NOT NULL,
    Aid_Type              VARCHAR(30)   NOT NULL,
    Eligibility_Status    VARCHAR(20)   NOT NULL,
    Distribution_Status   VARCHAR(25)   NOT NULL,
    Registration_Date     DATE          NOT NULL,
    Cycle                 VARCHAR(10)   NOT NULL
);


-- ============================================================
-- SECTION 2: ELIGIBILITY FILTERING
-- ============================================================

-- 2.1 All eligible cases
SELECT *
FROM aid_data
WHERE Eligibility_Status = 'Eligible'
ORDER BY Vulnerability_Score DESC;


-- 2.2 High-priority eligible cases (score >= 70 or large family)
SELECT 
    Case_ID,
    Camp,
    Family_Size,
    Vulnerability_Category,
    Vulnerability_Score,
    Aid_Type,
    Distribution_Status
FROM aid_data
WHERE Eligibility_Status = 'Eligible'
  AND (Vulnerability_Score >= 70 OR Family_Size >= 7)
ORDER BY Vulnerability_Score DESC, Family_Size DESC;


-- 2.3 Pending review cases — require follow-up
SELECT 
    Case_ID,
    Camp,
    Vulnerability_Score,
    Family_Size,
    Vulnerability_Category,
    Registration_Date
FROM aid_data
WHERE Eligibility_Status = 'Pending Review'
ORDER BY Vulnerability_Score DESC;


-- 2.4 Cases eligible but NOT yet distributed (coverage gap)
SELECT 
    Case_ID,
    Camp,
    Aid_Type,
    Vulnerability_Score,
    Distribution_Status
FROM aid_data
WHERE Eligibility_Status = 'Eligible'
  AND Distribution_Status IN ('Pending Distribution', 'Delayed')
ORDER BY Camp, Vulnerability_Score DESC;


-- ============================================================
-- SECTION 3: CAMP-LEVEL GROUPING & ANALYSIS
-- ============================================================

-- 3.1 Total cases per camp
SELECT 
    Camp,
    COUNT(*)                                              AS Total_Cases,
    SUM(CASE WHEN Eligibility_Status = 'Eligible'   THEN 1 ELSE 0 END) AS Eligible_Cases,
    SUM(CASE WHEN Eligibility_Status = 'Not Eligible' THEN 1 ELSE 0 END) AS Not_Eligible,
    SUM(CASE WHEN Eligibility_Status = 'Pending Review' THEN 1 ELSE 0 END) AS Pending_Review
FROM aid_data
GROUP BY Camp
ORDER BY Total_Cases DESC;


-- 3.2 Distribution rate per camp
SELECT 
    Camp,
    COUNT(*)                                                          AS Total_Eligible,
    SUM(CASE WHEN Distribution_Status = 'Distributed' THEN 1 ELSE 0 END) AS Distributed,
    SUM(CASE WHEN Distribution_Status = 'Pending Distribution' THEN 1 ELSE 0 END) AS Pending,
    SUM(CASE WHEN Distribution_Status = 'Delayed'    THEN 1 ELSE 0 END) AS Delayed,
    ROUND(
        100.0 * SUM(CASE WHEN Distribution_Status = 'Distributed' THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0), 1
    )                                                                  AS Distribution_Rate_Pct
FROM aid_data
WHERE Eligibility_Status = 'Eligible'
GROUP BY Camp
ORDER BY Distribution_Rate_Pct ASC;  -- lowest coverage first = most urgent


-- 3.3 Average vulnerability score per camp
SELECT 
    Camp,
    ROUND(AVG(Vulnerability_Score), 1)  AS Avg_Vulnerability_Score,
    ROUND(AVG(Family_Size), 1)          AS Avg_Family_Size,
    MIN(Vulnerability_Score)            AS Min_Score,
    MAX(Vulnerability_Score)            AS Max_Score
FROM aid_data
GROUP BY Camp
ORDER BY Avg_Vulnerability_Score DESC;


-- 3.4 Aid type distribution per camp
SELECT 
    Camp,
    Aid_Type,
    COUNT(*) AS Cases
FROM aid_data
WHERE Eligibility_Status = 'Eligible'
GROUP BY Camp, Aid_Type
ORDER BY Camp, Cases DESC;


-- ============================================================
-- SECTION 4: BENEFICIARY COUNTING
-- ============================================================

-- 4.1 Total beneficiaries (individuals, not households)
SELECT 
    Camp,
    SUM(Family_Size)                                                      AS Total_Individuals,
    SUM(CASE WHEN Eligibility_Status = 'Eligible' THEN Family_Size ELSE 0 END) AS Eligible_Individuals,
    SUM(CASE WHEN Distribution_Status = 'Distributed' THEN Family_Size ELSE 0 END) AS Served_Individuals
FROM aid_data
GROUP BY Camp
ORDER BY Total_Individuals DESC;


-- 4.2 Overall beneficiary summary
SELECT 
    COUNT(DISTINCT Case_ID)                                               AS Total_HH_Registered,
    SUM(Family_Size)                                                      AS Total_Individuals,
    SUM(CASE WHEN Eligibility_Status = 'Eligible' THEN 1 ELSE 0 END)    AS Eligible_HH,
    SUM(CASE WHEN Distribution_Status = 'Distributed' THEN 1 ELSE 0 END) AS Served_HH,
    SUM(CASE WHEN Distribution_Status = 'Distributed' THEN Family_Size ELSE 0 END) AS Served_Individuals,
    ROUND(
        100.0 * SUM(CASE WHEN Distribution_Status = 'Distributed' THEN 1 ELSE 0 END)
        / NULLIF(SUM(CASE WHEN Eligibility_Status = 'Eligible' THEN 1 ELSE 0 END), 0), 1
    ) AS Overall_Distribution_Rate_Pct
FROM aid_data;


-- ============================================================
-- SECTION 5: VULNERABILITY ANALYSIS
-- ============================================================

-- 5.1 Beneficiaries by vulnerability category
SELECT 
    Vulnerability_Category,
    COUNT(*)                                                              AS Total_Cases,
    ROUND(AVG(Vulnerability_Score), 1)                                   AS Avg_Score,
    SUM(CASE WHEN Eligibility_Status = 'Eligible' THEN 1 ELSE 0 END)    AS Eligible,
    SUM(CASE WHEN Distribution_Status = 'Distributed' THEN 1 ELSE 0 END) AS Distributed,
    ROUND(
        100.0 * SUM(CASE WHEN Eligibility_Status = 'Eligible' THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0), 1
    ) AS Eligibility_Rate_Pct
FROM aid_data
GROUP BY Vulnerability_Category
ORDER BY Avg_Score DESC;


-- 5.2 Score bands — classifying cases by severity
SELECT 
    CASE 
        WHEN Vulnerability_Score >= 75 THEN 'Critical (75-100)'
        WHEN Vulnerability_Score >= 55 THEN 'High (55-74)'
        WHEN Vulnerability_Score >= 35 THEN 'Medium (35-54)'
        ELSE                                 'Low (0-34)'
    END AS Score_Band,
    COUNT(*) AS Total_Cases,
    SUM(CASE WHEN Eligibility_Status = 'Eligible' THEN 1 ELSE 0 END) AS Eligible,
    SUM(CASE WHEN Distribution_Status = 'Distributed' THEN 1 ELSE 0 END) AS Distributed
FROM aid_data
GROUP BY Score_Band
ORDER BY MIN(Vulnerability_Score) DESC;


-- ============================================================
-- SECTION 6: COVERAGE GAPS & MONITORING
-- ============================================================

-- 6.1 Gaps: eligible but unserved by camp and aid type
SELECT 
    Camp,
    Aid_Type,
    COUNT(*) AS Unserved_Eligible_Cases,
    SUM(Family_Size) AS Unserved_Individuals
FROM aid_data
WHERE Eligibility_Status = 'Eligible'
  AND Distribution_Status != 'Distributed'
GROUP BY Camp, Aid_Type
ORDER BY Unserved_Eligible_Cases DESC;


-- 6.2 Delayed cases (high priority for follow-up)
SELECT 
    Camp,
    Case_ID,
    Vulnerability_Score,
    Family_Size,
    Aid_Type,
    Registration_Date
FROM aid_data
WHERE Distribution_Status = 'Delayed'
ORDER BY Vulnerability_Score DESC, Family_Size DESC;


-- 6.3 Distribution progress by cycle
SELECT 
    Cycle,
    COUNT(*) AS Total,
    SUM(CASE WHEN Distribution_Status = 'Distributed' THEN 1 ELSE 0 END) AS Distributed,
    ROUND(
        100.0 * SUM(CASE WHEN Distribution_Status = 'Distributed' THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0), 1
    ) AS Rate_Pct
FROM aid_data
WHERE Eligibility_Status = 'Eligible'
GROUP BY Cycle
ORDER BY Cycle;
