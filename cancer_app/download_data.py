from tracemalloc import Snapshot
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os

load_dotenv()

account = os.environ['ACCOUNT_NAME']   # Azure account name
key = os.environ['ACCOUNT_KEY']      # Azure Storage account access key  
connect_str = os.environ['CONNECTION_STRING'] # Azure Storage account connection string
container = os.environ['CONTAINER'] # Container name
blobname = 'overview.csv'

blob_service_client = BlobServiceClient.from_connection_string(connect_str)
blob_client_instance = blob_service_client.get_blob_client(container, blobname, snapshot=None)

# blob_list = blob_client_instance.list_blobs()
# for blob in blob_list:
#     print("\t" + blob.name)

blob_data = blob_client_instance.download_blob()
data = blob_data.readall()
print(data)