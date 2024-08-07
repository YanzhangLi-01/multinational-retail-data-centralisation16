# Multinational Retail Data Centralisation

## Table of Contents

1. [Project Description](#project-description)
2. [Installation Instructions](#installation-instructions)
3. [Usage Instructions](#usage-instructions)
4. [File Structure](#file-structure)
5. [License Information](#license-information)

## Project Description

**What it does:**
This project aims to centralize sales data for a multinational company by consolidating data from various sources into a single PostgreSQL database. The system allows for easier access and analysis of sales metrics, promoting a data-driven approach for decision-making.

**Aim of the Project:**
The goal is to create a unified system that stores the company's sales data in a central location, which serves as a single source of truth. This will facilitate up-to-date metrics and insights, enhancing the ability to make informed business decisions.

**What I Learned:**
Throughout this project, I gained experience in data extraction, cleaning, and storage processes. I also learned how to set up a PostgreSQL database with a star-based schema, and how to query this database for meaningful business metrics.

## Installation Instructions

**Prerequisites:**
- Python 3.x
- PostgreSQL
- Required Python libraries (listed in `requirements.txt`)

**Steps:**
1. Clone the repository: 
```python
git clone https://github.com/YanzhangLi-01/multinational-retail-data-centralisation16.git
```

2. Navigate into the project directory:
- For Windows users:
```python
cd C:\Users\YourUsername\path\to\project
```
- For MacOS users:
```python
cd /Users/YourUsername/path/to/project
```
3. Install any dependencies
- Dependencies in data_cleaning.py
```python
pip install pandas
pip install numpy
pip install re
pip install uuid
```
- Dependencies in data_extraction.py
```python
pip install tabula
pip install requests
pip install boto3
pip install json
```
- Dependencies in database_utils.py
```python
pip install yaml
```
- Dependencies in main.py
```python
pip install pandas
```
## Usage Instructions
**How to Use:**

1. **Run the data extraction and cleaning process:**
   - Ensure your PostgreSQL database named `sales_data` is set up and configured correctly.
   - Execute the main script to start the extraction, cleaning, and storage process:
     ```bash
     python main.py
     ```

2. **Generate and access metrics:**
   - Navigate to the `data_metrics` sub-repo.
   - Execute the provided SQL queries to generate the required metrics. The results will be stored as CSV files in the same directory.
   - Example command to execute a query (assuming you are using a PostgreSQL client like `psql`):
     ```bash
     psql -d sales_data -f data_metrics/your_query.sql -o data_metrics/your_result.csv
     ```
   - Here are some examples of the metrics you can generate:
     - Average sales time by years
     - Highest cost of sales
     - Percentage of sales by different store types
     - Staff headcount in German stores
     - Total number of stores in different countries
     - Total number of stores in different localities
     - Total amount of sales by store type
     - Monthly sales figures
## File Structure
```python
multinational-retail-data-centralisation16/
│
├── MRDC_project
        ├── .gitignore
        ├── data_cleaning.py
        ├── data_extraction.py
        ├── database_utils.py
        ├── main.py
        ├── creat_the_database_schema
                ├── changes_to_dim_products.sql
                ├── create_foreign_keys.sql
                ├── create_primary_keys.sql
                ├── dim_card_details__data_type.sql
                ├── dim_date_times_data_type.sql
                ├── dim_products_data_type.sql
                ├── dim_store_details_data_type.sql
                ├── dim_users_data_type.sql
                ├── orders_table_data_type.sql
        ├── data_metrics
                ├── avg_sales_time_by_year.sql
                ├── highest_cose_of_sales.sql
                ├── percentage_of_sales_by_store_type.sql
                ├── staff_headcount.sql
                ├── total_no_stores_in_countries.sql
                ├── total_no_stores_in_locality.sql
                ├── total_sales_by_store_type_DE.sql
                ├── total_sales_monthly.sql
        └── README.md/
```
## License Information
This project is licensed under the MIT License - see the [LICENSE](https://github.com/git/git-scm.com/blob/main/MIT-LICENSE.txt)
 file for details.
