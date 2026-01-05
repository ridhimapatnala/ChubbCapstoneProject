# Student Dropout Risk & Education Retention Analytics System

## Project Overview

This project delivers an **end-to-end education retention analytics system** that integrates data engineering, analytics, orchestration, and visualization to identify students at risk of dropping out, analyze risk patterns and support data-driven intervention strategies .

### Business Objectives

* Identify students at high risk of dropout using academic, attendance, and demographic indicators
* Analyze historical retention patterns to support early intervention
* Build an analytics pipeline and provide actionable insights through dashboards for educators and administrators


## Data Overview
This pipeline is built on **four datasets** that together form a **star-schema structure** centered on the student entity.

### Datasets Used:

#### 1. `dim_student_demographics`

* Student master and reference data
* Demographic and socio-economic attributes (e.g. Age, Gender, Family Income, Urban/Rural Indicators)

#### 2. `fact_student_academics`

* Academic performance metrics (e.g. Subject Scores, Grades, Pass/Fail Status)
* One row per student per academic year

#### 3. `fact_student_attendance`

* Attendance and engagement records (e.g. Attendance Percentage, Participation Scores etc.)
* Grain: one row per student per subject

####  4. `fact_student_retention`

* Retention outcome data (e.g. Dropout Flags, Reasons, Performance etc.)
* Target variable for analytics
* Retention data represents **historical cohorts**, independent of current demographic simulation

## Data Preprocessing & Feature Engineering



### Key Processing Steps

* Dataset-wise cleaning using Pandas

  * Duplicate removal
  * Data type correction
  * Standardization of categorical values
* Statistically driven missing value imputation
* Standardization of:

  * Academic year formats
  * Institution codes
  * Gender values
  * Urban / rural indicators

### Feature Engineering

* Academic features:

  * Total score
  * Grade (A–F)
  * Pass / fail status
  * Academic performance score
* Attendance features:

  * Attendance rate
  * Participation score aggregated at student-year level
* Demographic features:

  * Income bands
  * Socio-economic risk flags
  * Age-risk flags
  * First-generation learner indicator
* Retention features:
    
    Risk indicators derived such as:

  * academic_risk_flag
  * attendance_risk_flag 
  * socio_economic_risk_flag
  * age_risk_flag

## Architecture 
                 ┌──────────────────────────┐
                 │      Raw Source Data     │
                 │   (CSV / External Files) │
                 └─────────────┬────────────┘
                               │
                               ▼
        ┌────────────────────────────────────────────┐
        │               BRONZE LAYER                 │
        │--------------------------------------------│
        │ • Raw ingestion from source files          │
        │ • Original schema preserved                │
        │ • Duplicates, nulls, inconsistencies kept  │
        │ • Used for audit and reprocessing          │
        └──────────────────────┬─────────────────────┘
                               │
                               ▼
        ┌───────────────────────────────────────────┐
        │               SILVER LAYER                │
        │-------------------------------------------│
        │ • Data cleaning and standardization       │
        │ • Missing value handling                  │
        │ • Categorical normalization               │
        │ • Feature engineering                     │
        │ • Analytics-ready datasets                │
        └─────────────────────┬─────────────────────┘
                              │
                              ▼
        ┌───────────────────────────────────────────┐
        │                GOLD LAYER                 │
        │-------------------------------------------│
        │ • Business-level aggregates               │
        │ • Student risk indicators                 │
        │ • Retention and dropout trends            │
        │ • Optimized for Power BI consumption      │
        └───────────────────────────────────────────┘



## Technology Stack

- **Data Processing:** Python, Pandas , Numpy
- **Big Data & Analytics:** Databricks, Pyspark
- **Workflow Orchestration:** Apache Airflow
- **Storage:** CSV, Delta Tables
- **Visualization:** Power BI
  
## Execution Steps

### Project Structure

* **data/**
  Raw input datasets (CSV files)

* **notebooks/analytics/**
  Databricks notebooks for:

  * Bronze – Data Ingestion
  * Silver – Data Cleaning & Feature Engineering
  * Gold – Dropout Risk & Retention Analytics

* **notebooks/eda/**
  Exploratory Data Analysis and data validation notebooks

* **dashboard/**
  Power BI dashboard files

* **capstone-airflow/**
  Apache Airflow setup

  * `Dockerfile`
  * `docker-compose.yml`
  * `requirements.txt`
  * `airflow-dags/student_dropout_dag.py`

---

###  1. Upload Input Data to Databricks Volumes 

#### 1.1 Before running any notebooks, the raw CSV files must be uploaded to Databricks storage.
1. Go to **Databricks > Catalog > Volumes**
2. Choose an existing catalog and schema, or create one
3. Create a folder structure, for example:

```
/Volumes/main/default/student_dropout/data/
```

4. Upload all CSV files from the local `data/` folder into this volume path


#### 1.2 Update Paths in Notebooks

Update file paths to point to the Databricks volume location.

Example:

```python
BASE_PATH = "/Volumes/main/default/student_dropout/data/student_academics.csv"
```

---

### 2. Databricks Job Setup

#### 2.1 Import Analytics Notebooks

Import all notebooks into your Databricks Workspace from:

```
notebooks/analytics/
  Bronze_Data_Ingestion
  Silver_Cleaning_and_FE
  Gold_Risk_Analytics
```

#### 2.2 Create Databricks Job

1. Go to **Databricks > Jobs & Pipelines > Create Job**
2. Add three tasks in order (Bronze > Silver > Gold) using notebook paths from your workspace.
3. Attach a cluster
4. Save the job and **note the Job ID**

---

### 3. Airflow Setup Using Docker

#### 3.1 Navigate to Airflow Directory

```bash
cd capstone-airflow
```

#### 3.2 Initialize Airflow metadata DB

```bash
docker compose run --rm airflow-webserver airflow db init
```

#### 3.3 Create Airflow Admin user

```bash
docker compose run --rm airflow-webserver airflow users create \
  --username admin \
  --firstname <first_name> \
  --lastname <last_name> \
  --role Admin \
  --email <email> \
  --password admin
```

#### 3.4 Start Airflow 

```bash
docker compose up -d
```

#### 3.5 Access Airflow UI
Go to [http://localhost:8080](http://localhost:8080) and log in with credentials set up as above.

---

### 4. Configure Databricks Connection in Airflow

1. In the Airflow UI, go to **Admin > Connections**
2. Create or edit connection:
   * Connection ID: `databricks_default`
3. Set:

   * Host: Databricks workspace URL
   * Login: leave empty
   * Password: Databricks Personal Access Token
  
     (Databricks > User Settings > Developer > Access Tokens)
4. Save

---

### 5. Run the Pipeline

1. Go to **DAGs** in Airflow
2. Open **student_dropout_dag**
3. Click **Trigger DAG**
4. Monitor:

   * Task status
   * Logs in Airflow
   * Databricks Job execution

---


## Results & Conclusion

* Clear correlation identified between:

  * Low attendance, academics and higher dropout risk
  * Lower income bands and retention challenges
  * Poor academic performance and dropout probability
* Urban, low-income, and first-generation students showed higher risk patterns
* Presence of positive outliers confirmed that intervention can change outcomes

### Key outcomes:

* Successfully transformed raw, inconsistent datasets into analytics-ready layers
* Built explainable dropout risk indicators
* Implemented real-world ETL workflow orchestration using Airflow
* Delivered actionable insights through Power BI dashboards




