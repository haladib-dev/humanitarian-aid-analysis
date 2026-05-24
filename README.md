# Humanitarian Aid Eligibility & Distribution Analysis
## Reconstructed Portfolio Project | Simulated Dataset

---

> **⚠️ Disclaimer:** All data in this project is **entirely simulated and synthetic**.
> No real beneficiary names, camp locations, or organizational data are included.
> This project is designed solely to demonstrate technical skills and analytical workflows
> relevant to humanitarian data management systems.

---

## 📌 Project Overview

This project presents a **simulated humanitarian aid dataset** modeled after the data workflows
commonly used in UN-affiliated and INGO field operations. It demonstrates the ability to design,
process, analyze, and visualize data in alignment with humanitarian information management standards.

The workflow reflects real-world experience with:
- Eligibility determination systems (rules-based targeting)
- Aid distribution tracking and gap analysis
- Vulnerability-based prioritization
- Multi-camp coordination and reporting

---

## 🗂️ Files Included

| File | Description |
|---|---|
| `Humanitarian_Aid_Dataset.xlsx` | Simulated dataset (1,000 rows) with 3 analytical sheets |
| `humanitarian_aid_queries.sql` | SQL queries: filtering, grouping, gap analysis |
| `README.md` | Project documentation (this file) |

---

## 📊 Dataset Structure

**Sheet 1 — Aid_Data (Raw Dataset)**

| Column | Type | Description |
|---|---|---|
| Case_ID | String | Unique household identifier (e.g., HH-1001) |
| Camp | String | Camp location (6 simulated camps) |
| Family_Size | Integer | Number of household members (1–12) |
| Vulnerability_Category | String | Household classification (5 categories) |
| Vulnerability_Score | Decimal | Score 0–100 (higher = more vulnerable) |
| Aid_Type | String | Type of assistance assigned |
| Eligibility_Status | String | Eligible / Pending Review / Not Eligible |
| Distribution_Status | String | Distributed / Pending / Delayed / On Hold |
| Registration_Date | Date | Date of household registration |
| Cycle | String | Distribution cycle (Cycle 1–4) |

**Sheet 2 — Camp_Summary**
Aggregated metrics per camp: total cases, eligibility rate, distribution rate, average vulnerability score.

**Sheet 3 — Vulnerability_Breakdown**
Analysis by vulnerability category with color-coded priority tiers.

---

## 🔍 SQL Queries Included

The SQL file covers 6 analytical sections:

1. **Eligibility Filtering** — Identifying eligible cases, high-priority households, and pending reviews
2. **Camp-Level Grouping** — Distribution rates, coverage metrics, aid type breakdown
3. **Beneficiary Counting** — Household vs. individual-level counts
4. **Vulnerability Analysis** — Score bands and category-level eligibility rates
5. **Coverage Gaps** — Identifying unserved eligible households by camp and aid type
6. **Cycle Monitoring** — Distribution progress across operational cycles

---

## 📈 Power BI Dashboard Structure

The accompanying Power BI report (`.pbix`) contains 3 pages:

**Page 1 — Distribution by Camp**
- Bar chart: Total vs. Distributed cases per camp
- KPI cards: Overall distribution rate, total beneficiaries
- Slicer: Filter by aid type and cycle

**Page 2 — Vulnerability Analysis**
- Scatter plot: Vulnerability score vs. family size (colored by eligibility)
- Donut chart: Distribution by vulnerability category
- Table: High-priority unserved cases (score ≥ 70, not yet distributed)

**Page 3 — Coverage Gaps**
- Matrix: Unserved eligible cases by camp × aid type
- Bar chart: Delayed cases ranked by vulnerability score
- KPI: % of eligible households reached

---

## 🛠️ Tools & Skills Demonstrated

| Tool | Usage |
|---|---|
| **Python (pandas, openpyxl)** | Data simulation, Excel generation, formatting |
| **Microsoft Excel** | Multi-sheet workbook, conditional formatting, summary tables |
| **SQL** | Eligibility filtering, aggregation, gap analysis, beneficiary counting |
| **Power BI** | Interactive dashboard, DAX measures, cross-filtering |

---

## 🎯 Skills This Project Demonstrates

✔ Designing humanitarian data schemas aligned with field operations  
✔ Applying rules-based eligibility logic (targeting criteria)  
✔ Translating policy requirements into data structures  
✔ Conducting distribution gap analysis at camp and household level  
✔ Building multi-level aggregations (household → individual → camp → total)  
✔ Creating professional Excel reports for field and management audiences  
✔ Writing SQL for operational monitoring and reporting  
✔ Designing Power BI dashboards for humanitarian program tracking  

---

## 🌐 Real-World Context

This project reflects the kind of data workflows used in:
- **UNHCR** refugee registration and assistance systems (RAIS, ProGres)
- **WFP** food assistance targeting and distribution tracking
- **OCHA** humanitarian needs and response monitoring
- **INGO field operations** using Excel/ODK/KoBoToolbox pipelines

The vulnerability scoring, eligibility logic, and distribution status categories
are modeled after standard humanitarian targeting frameworks.

---

## 📝 Notes for Reviewers

This is a **portfolio demonstration project**. The goal is to show:
- Technical capability with real humanitarian data workflows
- Understanding of targeting, eligibility, and distribution systems
- Ability to build end-to-end analytical pipelines (data → SQL → visualization)

The dataset is intentionally realistic in structure but entirely fictional in content.
No sensitive, confidential, or personally identifiable information is included.

---

*Built as part of a professional portfolio demonstrating humanitarian data management expertise.*
