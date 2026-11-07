# Student Exchange Mobility Dashboard

## Project Overview
This Power BI dashboard was developed during my tenure as a Data Analysis Assistant (May – August 2026) at the Centre for International Experience (CIE) at the University of Toronto.

The CIE manages global exchange programs for both outbound UofT students and incoming international students. For this project, I was tasked with analyzing outbound student exchange data spanning three academic years (2022–2025) to uncover mobility trends, shifting demographic patterns, and institutional pathway preferences. The insights generated from this dashboard actively inform the CIE’s strategy and resource allocation for forming future global partnerships.

***Note on Data Privacy:** Due to the confidential nature of the original student mobility data, the datasets in this repository (`exchange_applications_raw_*.csv`) have been entirely simulated using Python's `Faker` library. The simulated data perfectly mimics the original production schema, ensuring the Power BI data model and DAX measures function identically to the real-world deployment.*

## Key Insights & Business Impact
By analyzing the 2022–2025 mobility data, the dashboard surfaced several strategic findings for the CIE:
* **Underrepresented Regions:** The data identified Africa and Latin America as significantly underrepresented in current outbound student mobility, providing the CIE with a clear mandate to target these regions for future partnership development and resource allocation.
* **Regional Growth Clusters:** Uncovered strong, concentrated growth in specific host institutions in East Asia over the three-year period, indicating shifting student preferences. 
* **Admission Bottlenecks:** By analyzing the YoY Admission Rates, the dashboard highlighted institutions where application volume significantly outpaced available partnership spots.

## Data Architecture & Schema
To handle many-to-many relationships (such as students selecting multiple secondary programs or applying to up to three host institutions), the Power BI data model is built on a STAR schema. 

```mermaid
erDiagram
    Fact_Applications }o--|| Dim_Student : "Student ID"
    Fact_Applications }o--|| Dim_Host : "Host Institution"
    Fact_Applications }o--|| Dim_Academics : "Academic Key"
    Dim_Student ||--o{ Bridge_Student_Programs : "Student ID"

    Fact_Applications {
        string Academic_Key FK
        string Academic_Year
        string Host_Institution FK
        int Host_Institution_Choice
        string Pathway
        string Status
        int Student_ID FK
    }

    Dim_Student {
        int Student_ID PK
        string Citizenship
        string Disability
        string Gender
        string Indigenous_Status
        string Legal_Status_in_Canada
    }

    Dim_Host {
        string Host_Institution PK
        string Country_of_Institution
    }

    Dim_Academics {
        string Academic_Key PK
        string College
        string Faculty
        string Program_1
        string Program_2
        string Program_3
        string Program_of_Study_Combined
    }

    Bridge_Student_Programs {
        int Student_ID FK
        int Choice_Level
        string Master_Program_Name
    }