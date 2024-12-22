# fetch-homework-assignment
Showcasing my data analytics/engineering skills for Fetch Rewards.

## 1.Steps to reproduce

### 1. Environment setup
From the root directory, run 
 ``` bash
 pip install -r requirements.txt
 ```

### 2. Setup .env
The following values must be provided

```
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5433
DB_NAME=fetch_rewards

USERS_FILE=../data/users.json
BRANDS_FILE=../data/brands.json
RECEIPTS_FILE=../data/receipts.jsonl
```

### 1. Run the docker-compose.yml file
In a terminal, navigate to `/sql`. Run: 
```bash
docker compose up
```
Note the credentials in the `docker-compose.yml` file and use them for access to the db

### 2. Run database_schema.sql file
In pgAdmin, open the file `database_schema.sql` and run it. This should build out the database and schemas I created.

### 3. Import data
Once everything is setup, navigate to `/python_scripts` and execute main.py

### 4. Data quality and analysis
Finally, run the queries in `/sql/queries.sql` and the Jupyter notebook located in `/DQ notebooks/analysis.ipynb`

