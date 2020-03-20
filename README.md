# desafio_indicium

## 1. Description

This repository was created in order to solve Indicium's selective process challenge. 
Given the data bellow, the algorithm gives 3 outputs:
- deals_per_contact.csv: total amount bought per contact
- deals_per_month.csv: total amount sold per month
- sector_rank.csv: monthly rank of amount sold per sectors


## 2. Data

Four datasets were given:

**-deals.tsv:** contains data relative to the deals closed. The columns are: 
| Column name |Description  |
|--|--|
| dealsId | deal identifier | 
| dealsDateCreated | deal date | 
| dealsPrice | deal price | 
| contactsId | contact identifier |
| companiesId | companies identifier |


**-contacts.tsv:** contais data relative to the contats. The columns are: 
| Column name |Description  |
|--|--|
| contactsId | contact identifier | 
| contactsName | contact name | 
| contactsDateCreate| date when contact was created | 
| contactsCreatedBy | user responsible for contacts creation |
| contactsEmail | contact's email |
| contactsPhone | contact's phone |
| emplyersId | companie's identifier |
| contactsHomeAdress | contact's home adress |
| contactsLatLong | contact's latitude and longitude |
| contactsRelatedToLead | relation between lead and contact |
| contactsResponsible | name of contact's responsible |


**-companies.tsv:** contais data relative to the companies. The columns are: 
| Column name |Description  |
|--|--|
| companiesId | companies identifier | 
| companiesName | companies name | 
| companiesDateCreated | date when companie's contact was created |
| createdBy | user responsible for contacts creation |
| companiesEmail | companies's email |
| companiesPhone | companies's phone |
| employeesId | companie's contact identifier |
| employeesName | contact's name |
| userResponsible | name of user's responsible |
| sectorKey | sectorIdentifier |


**-sector.tsv:** contais data relative to sectors. The columns are: 
| Column name |Description  |
|--|--|
| sectorKey | sector identifier | 
| sector | sector's name | 


## 3. Steps to use
The project is composed by one script (main.py).

### 3.1 Seting up the enviroment
Create a enviroment
```bash
python3 -m venv indicium_challenge
```
Activate enviroment
```bash
. ./indicium_challenge/bin/activate
```
Install requirements
```bash
pip install -r requirements.txt
```

### 3.2 Running script
Run script **main.py** to generate the outputs. The following arguments must be passed:

- --sector_data_filepath or -s: filepath to sector.csv
- --contacts_data_filepath or -c: filepath to contats.csv
- --deals_data_filepath or -d: filepath to deals.csv
- --companies_data_filepath or -cp: filepath to companies.csv
- --output_filepath or -o: path desired to save the outputs

Example: 
```bash
python3 main.py -s '/Users/macbook/Downloads/sectors.tsv' -c '/Users/macbook/Downloads/contacts.tsv' -d '/Users/macbook/Downloads/deals.tsv' -cp '/Users/macbook/Downloads/companies.tsv' -o '/Users/macbook/Downloads'
```













