# 🏥 Healthcare Claims Pipeline  

This repository contains my implementation of a **healthcare claims data pipeline** project.  
The purpose of this project is to process, validate, and filter insurance claim records from a dataset (`emr_beta_sample.json`) while applying custom rules to detect missing fields, denied claims, and invalid records.  

---

## 📌 Project Overview
The project simulates a **data engineering workflow** for healthcare claims:
1. Load claims data from a JSON file (`emr_beta_sample.json`).
2. Validate and filter the claims:
   - ✅ Include only claims with a valid `patient_id`.
   - ❌ Exclude claims that do not have a `patient_id`.
   - ❌ Exclude claims that are **not denied**.
3. Print excluded claims along with the **reason** for exclusion.
4. Generate a clean dataset of valid claims that can later be used for further analysis or machine learning tasks.

---

## 🛠️ What I Have Done So Far
Here’s a breakdown of what has been completed in this project:

### ✔️ 1. Data Loading
- Implemented Python code to read claims data from the JSON file.
- Verified file structure and ensured it was parsed correctly.

### ✔️ 2. Data Validation Rules
- Defined validation criteria:
  - Claims **must have a `patient_id`**.
  - Claims **must be marked as denied** to be included in the final set.  
- Excluded invalid claims and added reasons for exclusion.

### ✔️ 3. Exclusion Logging
- Implemented logging for excluded claims:
  - Example:  
    ```
    Excluded claims with reasons:
    - A125: Missing patient_id
    - A126: Not denied
    - AUTO_1: Missing patient_id
    - AUTO_2: Missing patient_id
    - AUTO_3: Missing patient_id
    - AUTO_4: Missing patient_id
    ```
- This gives transparency about why certain records were not processed.

### ✔️ 4. Clean Output Generation
- Produced a final dataset containing only the **valid claims**.
- Ensured clean separation between accepted claims and excluded claims.

---

## 📂 Project Structure
📁 healthcare-claims-pipeline
├──date
   ├── emr_beta_sample.json # Input dataset
   ├── process_claims.py # Main Python script for processing claims
├── README.md # Project documentation (this file)
├──pipeline.py
├──resubmission_candidates.json

