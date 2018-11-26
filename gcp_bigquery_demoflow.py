

######################################################################################
#
#   Google Cloud BigQuery - demoflow
#
#   https://cloud.google.com/bigquery/docs/
#   https://googleapis.github.io/google-cloud-python/latest/bigquery/generated/google.cloud.bigquery.client.Client.html
#
######################################################################################


from google.cloud import bigquery


######################################################################################
#
#   Functions
#
######################################################################################



# Create BigQuery Dataset
def bq_create_dataset(dataset_id, location):
    '''
        Creates a BigQuery Dataset
        
        Input(s):   dataset_id: Dataset ID (name)
                    location:   US, EU, asia-northeast1 (Tokyo), europe-west2 (London), asia-southeast1 (Singapore), australia-southeast1 (Sydney)
        
        Datasets are top-level containers that are used to organize and control
        access to your tables and views. A table or view must belong to a dataset.
        
        Access Control:
        
            Tables and views are child resources of datasets — they inherit permissions from their parent dataset.
            You share access to BigQuery tables and views using project-level IAM roles and dataset-level access controls.
            Currently, you cannot apply access controls directly to tables or views.
    
            Project-level access controls determine the users, groups, and service accounts allowed to access all datasets, tables, views, and table data within a project.
            Dataset-level access controls determine the users, groups, and service accounts allowed to access the tables, views, and table data in a specific dataset.
            Access controls cannot be applied during dataset creation in the UI or command-line tool.
            However, Using the API, you can apply access controls during dataset creation by calling the datasets.insert method, or you can apply access controls after dataset creation by calling the datasets.patch method.
        Dataset Limitations:
        
            - Dataset names must be unique per project.
            - All tables referenced in a query must be stored in datasets in the same location.
            - When copying a table, datasets containing the source and destination table must reside in the same location.
            - After a dataset has been created, the geographic location becomes immutable. There are two options:
                1) Regional (Tokyo, Sydney, London, etc)
                2) Multi-Regional (US or EU)
        Location Considerations:
        
            - Colocate your BigQuery dataset and your external data source. (BigQuery must be in same region as data source)
            - Colocate your Cloud Storage buckets for loading data.
            - Colocate your Cloud Storage buckets for exporting data.
            EXCEPTION: If your dataset is in the US multi-regional location, you can load/export data from a Cloud Storage bucket in any regional or multi-regional location
        Moving BigQuery data between locations:
            - You cannot change the location of a dataset after it is created.
            - You cannot move a dataset from one location to another.
            - If you need to move a dataset from one location to another, follow this process:
                1) Export the data from your BigQuery tables to a regional or multi-region Cloud Storage bucket in the same location as your dataset.
                2) Copy or move the data from your Cloud Storage bucket to a regional or multi-region bucket in the new location
                3) Create a new BigQuery dataset (in the new location).
                4) Load your data from the Cloud Storage bucket into BigQuery.
    
    '''
    try:
        client               = bigquery.Client()
        dataset_ref          = client.dataset(dataset_id)
        dataset_obj          = bigquery.Dataset(dataset_ref)
        dataset_obj.location = location
        dataset              = client.create_dataset(dataset_obj)
        print('[ INFO ] Created {} at {}'.format(dataset_id, dataset.created))
    except Exception as e:
        print('[ ERROR ] {}'.format(e))





def bq_create_table_empty(dataset_id, table_id, schema):
    '''
        Creates an empty BigQuery Table
        
        USAGE:
        bq_create_table_empty(  dataset_id = 'ztest1',
                                table_id = 'ztable1',
                                schema = [
                                            bigquery.SchemaField('id',      'STRING'),
                                            bigquery.SchemaField('name',    'STRING'),
                                            bigquery.SchemaField('state',   'STRING'),
                                            bigquery.SchemaField('payment', 'FLOAT'),
                                            bigquery.SchemaField('flag',    'INTEGER'),
                                         ])
        
        Required Permissions:
        To create a table, you must have WRITER access at the dataset level,
        or you must be assigned a project-level IAM role that includes bigquery.tables.create permissions.
        The following predefined, project-level IAM roles include bigquery.tables.create permissions:
            bigquery.dataEditor
            bigquery.dataOwner
            bigquery.admin
    
    '''
    try:
        client      = bigquery.Client()
        dataset_ref = client.dataset(dataset_id)
        table_ref   = dataset_ref.table(table_id)
        table       = bigquery.Table(table_ref, schema=schema)
        table       = client.create_table(table)
        
        assert table.table_id == table_id
        print('[ INFO ] Created {} at {}'.format(table_id, table.created))
    except Exception as e:
        print('[ ERROR] {}'.format(e))





def bq_create_table_from_gcs(dataset_id, table_id, schema, gcs_path):
    '''
            
        USAGE:
        bq_create_table_from_gcs(  dataset_id='zdataset1',
                                table_id='ztable1',
                                schema= [
                                            bigquery.SchemaField('id',              'STRING',   mode='REQUIRED'),
                                            bigquery.SchemaField('member_id',       'STRING',   mode='REQUIRED'),
                                            bigquery.SchemaField('loan_amnt',       'INTEGER',  mode='NULLABLE'),
                                            bigquery.SchemaField('term_in_months',  'INTEGER',  mode='NULLABLE'),
                                            bigquery.SchemaField('interest_rate',   'FLOAT',    mode='NULLABLE'),
                                            bigquery.SchemaField('payment',         'FLOAT',    mode='NULLABLE'),
                                            bigquery.SchemaField('grade',           'STRING',   mode='NULLABLE'),
                                            bigquery.SchemaField('sub_grade',       'STRING',   mode='NULLABLE'),
                                            bigquery.SchemaField('employment_length', 'INTEGER',mode='NULLABLE'),
                                            bigquery.SchemaField('home_owner',      'INTEGER',  mode='NULLABLE'),
                                            bigquery.SchemaField('income',          'INTEGER',  mode='NULLABLE'),
                                            bigquery.SchemaField('verified',        'INTEGER',  mode='NULLABLE'),
                                            bigquery.SchemaField('default',         'INTEGER',  mode='NULLABLE'),
                                            bigquery.SchemaField('purpose',         'STRING',   mode='NULLABLE'),
                                            bigquery.SchemaField('zip_code',        'STRING',   mode='NULLABLE'),
                                            bigquery.SchemaField('addr_state',      'STRING',   mode='NULLABLE'),
                                            bigquery.SchemaField('open_accts',      'INTEGER',  mode='NULLABLE'),
                                            bigquery.SchemaField('credit_debt',     'INTEGER',  mode='NULLABLE')
                                        ],
                                gcs_path='gs://zdatasets1/loan_200k.csv')
    
    '''
    try:
        client      = bigquery.Client()
        dataset_ref = client.dataset(dataset_id)
        table       = bigquery.Table(dataset_ref.table(table_id), schema=schema)
        
        external_config = bigquery.ExternalConfig('CSV')
        external_config.source_uris = [gcs_path,]
        external_config.options.skip_leading_rows = 2  # optionally skip header row
        table.external_data_configuration = external_config
        
        # Create a permanent table linked to the GCS file
        table = client.create_table(table)
        
        assert table.table_id == table_id
        print('[ INFO ] Created {} at {}'.format(table_id, table.created))
    except Exception as e:
        print('[ ERROR] {}'.format(e))







def bq_insert_rows(dataset_id, table_id, rows_to_insert):
    '''
        Insert rows into a BigQuery Table via the streaming API
        
        Note:
            The table must already exist and have a defined schema
            rows_to_insert = List of variables (id, date, value1, value2, etc.)

    '''
    try:
        client    = bigquery.Client()
        table_ref = client.dataset(dataset_id).table(table_id)
        table     = client.get_table(table_ref)
        errors    = client.insert_rows(table, rows_to_insert)
        if errors == []:
            print('[ INFO ] Rows inserted into BigQuery table {}'.format(table_id))
    except Exception as e:
        print('[ ERROR] {}'.format(e))






def bq_query(query, location='US'):
    '''
        Query BigQuery Table(s)
        
        location: US, EU, asia-northeast1 (Tokyo), europe-west2 (London), asia-southeast1 (Singapore), australia-southeast1 (Sydney)
        
    '''
    client = bigquery.Client()
    
    query_job = client.query(query, location=location)
    
    for row in query_job:
        # Row values can be accessed by field name or index
        assert row[0] == row.name == row['name']
        print(row)





######################################################################################
#
#   Main
#
######################################################################################


if __name__ == "__main__":


    # Args
    dataset_id = ''
    table_id1  = ''     # Empty Table Name
    table_id2  = ''     # Table name for loaded data from Cloud Storage
    location   = ''



    # Create BigQuery Dataset
    bq_create_dataset(dataset_id, location)
    
    # Create BigQuery Table (empty table)
    bq_create_table_empty(dataset_id, table_id=table_id1)

    # Create BigQuery Table (from Google Cloud Storage)
    bq_create_table_from_gcs(   dataset_id='zdataset1',
                                table_id='ztable1',
                                schema= [
                                            bigquery.SchemaField('id',              'STRING'),
                                            bigquery.SchemaField('member_id',       'STRING'),
                                            bigquery.SchemaField('loan_amnt',       'INTEGER'),
                                            bigquery.SchemaField('term_in_months',  'INTEGER'),
                                            bigquery.SchemaField('interest_rate',   'FLOAT'),
                                            bigquery.SchemaField('payment',         'FLOAT'),
                                            bigquery.SchemaField('grade',           'STRING'),
                                            bigquery.SchemaField('sub_grade',       'STRING'),
                                            bigquery.SchemaField('employment_length', 'INTEGER'),
                                            bigquery.SchemaField('home_owner',      'INTEGER'),
                                            bigquery.SchemaField('income',          'INTEGER'),
                                            bigquery.SchemaField('verified',        'INTEGER'),
                                            bigquery.SchemaField('default',         'INTEGER'),
                                            bigquery.SchemaField('purpose',         'STRING'),
                                            bigquery.SchemaField('zip_code',        'STRING'),
                                            bigquery.SchemaField('addr_state',      'STRING'),
                                            bigquery.SchemaField('open_accts',      'INTEGER'),
                                            bigquery.SchemaField('credit_debt',     'INTEGER')
                                        ],
                                gcs_path='gs://zdatasets1/loan_200k.csv')
    
    # Insert data
    bq_insert_rows(dataset_id, table_id, rows_to_insert)
    
    # Query Table1
    
    
    # Query Table2
    
    
    # Query Both Tables
    
    
    # Create View on Loan Table
    
    
    # Cleanup - Delete Dataset and Tables




#ZEND
