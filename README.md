<h3>Google Cloud BigQuery</h3>

<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Fully managed Relational DB
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;No-ops, Serverless
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Analytics data warehouse
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Accepts both batch and streaming inserts
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;SQL Syntax (and legacy SQL)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Multi-Region (US or EU) or Regional (ie. asia-northeast)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;BigQuery is NOT recommended as a transactional database (use Cloud SQL or Spanner)
<br>
<br><b>Architecture</b>
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Columnar data store (each column is stored in its own storage point)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Storage and Compute are separate (compute = Dremel and storage = Colossus)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Based on Dremel
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Slots are a unit of computational capacity required to execute SQL queries
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;BQ automatically calculates how many slots are required by each query
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Per-account slot quota
<br>
<br><b><a href="https://cloud.google.com/bigquery/docs/access-control">IAM (Security)</a></b>
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Project-level access control
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Dataset-level access control
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;** NOT ** Table-level access control
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Public Datasets (“all authenticated users” ROLE)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Primitive Roles: Owner, Editor, and Viewer
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Predefined Roles:
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;roles/bigquery.admin (full access)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;roles/bigquery.dataOwner (Read, update, delete dataset. Read the dataset metadata and list tables in dataset)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;roles/bigquery.dataEditor (Read the dataset metadata and list tables in the dataset.)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;roles/bigquery.metadataViewer
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;roles/bigquery.dataViewer
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;roles/bigquery.jobUser (Permissions to run jobs, queries within project)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;roles/bigquery.user (Run jobs, queries, within the project. Most individuals, data scientists)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;When applying access to a dataset, you can grant access to:
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;User by e-mail - Gives an individual Google account access to the dataset
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;Group by e-mail - Gives members of a Google group access to the dataset
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;Domain - Gives users and groups in Google domain access to the dataset
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;All Authenticated Users - Makes the dataset public to Google Acct holders
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;Project Owners - Gives all project owners access to the dataset
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;Project Viewers - Gives all project viewers access to the dataset
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;Project Editors - Gives all project editors access to the dataset
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;Authorized View - Gives a view access to the dataset
<br>
<br><b>Reducing Cost</b>
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Less work = faster query = less cost
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;BigQuery charges for:
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;Storage
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;Queries
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;Streaming Inserts
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;<b>Use Caching</b>
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;BigQuery does not charge for cached queries
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;By default “use cached results” is checked
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;Caching is per user only!! (cached results are not shared)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Creating Custom Cost Controls:
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;Manage costs by requesting a custom quota that specifies a limit on the amount of query data processed per day
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;Creating a custom quota on query data allows you to control costs at the project-level or at the user-level
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;Project-level custom quotas limit the aggregate usage of all users in that project.
<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&ndash;&nbsp;User-level custom quotas are separately applied to each user or service account within a project.
<br><b>Best Practices</b>
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Avoid using Select * (query only the columns you need)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;LIMIT does NOT affect cost
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Denormalize data when possible
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Filter early and big with WHERE clause
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Do bigger joins first (and filter pre-join when possible)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Partition data by date (1) ingest time or (2) partition by date column
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Low cardinality GROUP BYs are faster
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Sample data using preview options (Don't run queries to explore or preview table data)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Price your queries before running them (use dryRun flag)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Limit query costs by restricting the number of bytes billed
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Materialize query results in stages
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;You can use nested and repeated fields to maintain relationships
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Use streaming inserts with caution  (extra cost associated with this)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Avoid excessive wildcard tables (be as specific as possible with wildcard prefix)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Avoid unbalanced joins
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Avoid skew (if possible, filter and/or use approximate functions)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Avoid Cross joins (Cartesian product)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Avoid single row operations (Batch your updates and inserts)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;Optimizing Storage (Use the expiration settings, lifecycle archival policies)
<br>
<br>

