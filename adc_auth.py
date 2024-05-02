from google.cloud import storage

projectID = 'Vertex AI Project ID'

def authenticate_implicit_with_adc(project_id=projectID):
    storage_client = storage.Client(project=project_id)
    buckets = storage_client.list_buckets()
    print("Buckets:")
    for bucket in buckets:
        print(bucket.name)
    print("Listed all storage buckets.")
    
authenticate_implicit_with_adc(project_id=projectID)