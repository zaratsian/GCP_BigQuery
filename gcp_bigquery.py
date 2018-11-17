

####################################################################################################
#
#   Google BigQuery - Helpful Functions and Notes
#
#   https://cloud.google.com/bigquery/docs/
#
####################################################################################################



'''
GENERAL NOTES
'''
'''

Renaming Datasets
Currently, you cannot change the name of an existing dataset, and you cannot copy a dataset and give it a new name.
If you need to change the dataset name, follow these steps to recreate the dataset:
    1. Create a new dataset and specify the new name.
    2. Copy the tables from the old dataset to the new one.
    3. Recreate the views in the new dataset.
    4. Delete the old dataset to avoid additional storage costs.

Copying Datasets
Currently, you cannot copy a dataset. Instead follow these steps to recreate the dataset:
    1. Create a new dataset (with a unique name per project)
    2. Copy the tables from the old dataset to the new one.
    3. Recreate the views in the new dataset.
    4. Delete the old dataset to avoid additional storage costs.



To Review:
    [ ] How-to Guides: Running and Managing Jobs
    [X] Can I secure access to only one table within a Dataset? No, see here https://cloud.google.com/bigquery/docs/datasets
    [ ] Great content in Working with Datasets: Create and Using Datasets



'''


####################################################################################################
#
#   Python Libraries
#
####################################################################################################


import os

from google.cloud import bigquery

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/dzaratsian/zproject201807-d5eb54b6371e.json'


####################################################################################################



# Create BigQuery Dataset
def bq_create_dataset(dataset_id):
    '''
        Creates a BigQuery Dataset
        
        Input(s): Dataset ID (Dataset Name)
        
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
        dataset_obj.location = 'US'
        dataset              = client.create_dataset(dataset_obj)
        print('[ INFO ] Successfully created Dataset: {}'.format(dataset_id))
    except Exception as e:
        print('[ ERROR ] {}'.format(e))




def bq_list_datasets():
    '''
        List Datasets within a Project
        
        Usage:
        bq_list_datasets()
        
        Required Permissions:
        Only datasets for which you have bigquery.datasets.get permissions are returned.
        This includes any dataset to which you have been granted dataset-level READER access.
    
    '''
    try:
        client   = bigquery.Client()
        datasets = list(client.list_datasets())
        project  = client.project
        
        if datasets:
            print('Datasets in project {}:'.format(project))
            for i,dataset in enumerate(datasets):  # API request(s)
                print('\t{}\t{}'.format(i, dataset.dataset_id))
        else:
            print('{} project does not contain any datasets.'.format(project))
    
    except Exception as e:
        print('[ ERROR ] {}'.format(e))





def bq_dataset_metadata(dataset_id):
    '''
        List all metadata for a BigQuery Dataset
        
        USAGE:
        bq_dataset_metadata('ztest1')
        
        Required Permissions:
        Must be assigned the dataset-level READER role,
        or you must be assigned a project-level IAM role that includes bigquery.datasets.get permissions.
       
    '''
    try:
        client = bigquery.Client()
        dataset_ref = client.dataset(dataset_id)
        dataset = client.get_dataset(dataset_ref)
        
        # View dataset properties
        print('Dataset ID:     {}'.format(dataset_id))
        print('Dataset Path:   {}'.format(dataset.path))
        print('Description:    {}'.format(dataset.description))
        print('Created:        {}'.format(str(dataset.created)))
        print('Location:       {}'.format(dataset.location))
        print('Expiration(ms): {}'.format(dataset.default_table_expiration_ms))
        print('Labels:')
        labels = dataset.labels
        if labels:
            for label, value in labels.items():
                print('\t{}: {}'.format(label, value))
        else:
            print("\tDataset has no labels defined.")
        
        # View tables in dataset
        print('Tables:')
        tables = list(client.list_tables(dataset_ref))
        if tables:
            for table in tables:
                print('\t{}'.format(table.table_id))
        else:
            print('\tThis dataset does not contain any tables.')
        
        # Get Access Entries
        print('Access Entries:')
        for access_entry in dataset.access_entries:
            print('\tEntity Role: {}'.format(access_entry.role))
            print('\tEntity Type: {}'.format(access_entry.entity_type))
            print('\tEntity ID:   {}'.format(access_entry.entity_id))
            print('')
    
    except Exception as e:
        print('[ ERROR ] {}'.format(e))





def bq_update_access_to_dataset(dataset_id, role, entity_type, entity_id):
    '''
        Update access control for a BigQuery Dataset
        
        USAGE:
        bq_modify_access_to_dataset('ztest1','READER','userByEmail','dtz001@gmail.com')
        
        Required Permissions:
        bigquery.dataOwner
        bigquery.admin
    
    '''
    try:
        client = bigquery.Client()
        dataset = client.get_dataset(client.dataset(dataset_id))
        
        entry = bigquery.AccessEntry(
                    role=role,                  # 'READER', 'WRITER', 'OWNER'
                    entity_type=entity_type,    # 'userByEmail', 'groupByEmail', 'domain','specialGroup', 'view'
                    entity_id=entity_id         # User or resource to grant access to
                )
        
        assert entry not in dataset.access_entries
        entries = list(dataset.access_entries)
        entries.append(entry)
        dataset.access_entries = entries
        
        dataset = client.update_dataset(dataset, ['access_entries'])  # API request
        
        assert entry in dataset.access_entries
    
    except Exception as e:
        print('[ ERROR ] {}'.format(e))





def bg_update_default_table_expiration(dataset_id, new_default_table_expiration_ms):
    '''
        Update the DEFAULT expiration (in ms) for all Tables in a Dataset (moving forward)
        
        USAGE:
        bg_update_default_table_expiration('ztest1', 3600000)
        NOTE: 3600000 ms is equal to 1 hour (60 * 60 * 1000)
        
        Required Permissions:
        Must have OWNER access at the dataset level,
        or you must be assigned a project-level IAM role that includes bigquery.datasets.update permissions.
            bigquery.dataOwner
            bigquery.admin
        
        Notes:
            - You can set a DEFAULT table expiration time at the DATASET level,
              or you can set a table's expiration time when the table is created.
            - If you set the expiration when the table is created, the dataset's default table expiration is ignored.
            - When you update a dataset's default table expiration setting:
                - If you change the value from Never to a defined expiration time, any tables that already exist in the
                  dataset will not expire unless the expiration time was set on the table when it was created.
                - If you are changing the value for the default table expiration, any tables that already exist expire
                  according to the original table expiration setting. Any new tables created in the dataset have the new
                  table expiration setting applied unless you specify a different table expiration on the table when it is created.
            - The value for default table expiration is expressed differently depending on where the value is set.
                - BigQuery web UI, expiration is expressed in days.
                - Command-line tool, expiration is expressed in seconds.
                - API, expiration is expressed in milliseconds.
    
    '''
    try:
        client      = bigquery.Client()
        dataset_ref = client.dataset(dataset_id)
        dataset     = client.get_dataset(dataset_ref)
        
        # Update Dataset Tables Default Expiration Time (start at this point forward)
        assert dataset.default_table_expiration_ms is None
        dataset.default_table_expiration_ms = new_default_table_expiration_ms
        dataset = client.update_dataset(dataset, ['default_table_expiration_ms'])
        assert dataset.default_table_expiration_ms == new_default_table_expiration_ms
    except Exception as e:
        print('[ ERROR] {}'.format(e))





def bg_update_dataset_desc(dataset_id, new_dataset_desc):
    '''
        Update the Dataset Description property
        
        USAGE:
        bg_update_dataset_desc('ztest1', 'This is a new dataset description')
        
        Required Permissions:
        Must have OWNER access at the dataset level,
        or you must be assigned a project-level IAM role that includes bigquery.datasets.update permissions.
            bigquery.dataOwner
            bigquery.admin
        
        Notes:
            - You can set a DEFAULT table expiration time at the DATASET level,
              or you can set a table's expiration time when the table is created.
            - If you set the expiration when the table is created, the dataset's default table expiration is ignored.
            - When you update a dataset's default table expiration setting:
                - If you change the value from Never to a defined expiration time, any tables that already exist in the
                  dataset will not expire unless the expiration time was set on the table when it was created.
                - If you are changing the value for the default table expiration, any tables that already exist expire
                  according to the original table expiration setting. Any new tables created in the dataset have the new
                  table expiration setting applied unless you specify a different table expiration on the table when it is created.
            - The value for default table expiration is expressed differently depending on where the value is set.
                - BigQuery web UI, expiration is expressed in days.
                - Command-line tool, expiration is expressed in seconds.
                - API, expiration is expressed in milliseconds.
    
    '''
    try:
        client      = bigquery.Client()
        dataset_ref = client.dataset(dataset_id)
        dataset     = client.get_dataset(dataset_ref)
        
        # Update Dataset Description
        assert dataset.description == 'Original description.'
        dataset.description = new_dataset_desc
        dataset = client.update_dataset(dataset, ['description'])
        assert dataset.description == 'Updated description.'
    except Exception as e:
        print('[ ERROR] {}'.format(e))





def bq_delete_dataset(dataset_id):
    '''
        Deletes a Dataset (Deleting a dataset is permanent)
        
        USAGE:
        bq_delete_dataset('ztest1')
        
        Required Permissions:
        Must have OWNER access at the dataset level,
        or you must be assigned a project-level IAM role that includes bigquery.datasets.delete permissions.
        If the dataset contains tables, bigquery.tables.delete is also required.
        The following predefined, project-level IAM roles include both bigquery.datasets.delete and bigquery.tables.delete permissions:
            bigquery.dataOwner
            bigquery.admin
    
    '''
    try:
        client = bigquery.Client()
        dataset_ref = client.dataset(dataset_id)
        client.delete_dataset(dataset_ref, delete_contents=True)  # Set delete_contents=True to delete Dataset Tables
        print('Dataset {} deleted.'.format(dataset_id))
    except Exception as e:
        print('[ ERROR] {}'.format(e))





# Create BigQuery Table




# Load Data

# Query Table



# Create BigQuery Table (Ingestion-Time Partitioned Table)

# Load Data (into Ingestion-Time Partitioned Table)

# Query (into Ingestion-Time Partitioned Table)



# Create BigQuery Table (Partitioned Table)

# Load Data (into Partitioned Table)

# Query (Partitioned Table)



# Export Data

# Copy Data






#ZEND
