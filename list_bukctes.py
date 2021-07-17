from google.cloud import storage
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/ashutosh/python_scripts_test/flaskaws/prueba-lythium-1-e98267e6ddb6.json"


def list_buckets():
    """Lists all buckets."""

    storage_client = storage.Client()
    buckets = storage_client.list_buckets()

    for bucket in buckets:
        print(bucket.name)

list_buckets()