import google.auth
import google.auth.transport.requests as tr_requests
from google.cloud import storage
from google.resumable_media.requests import ChunkedDownload
import datetime
import os
import io

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/ashutosh/python_scripts_test/flaskaws/videobackup-317718-8dc2e1565986.json"
ro_scope = u'https://www.googleapis.com/auth/devstorage.read_only'
credentials, _ = google.auth.default(scopes=(ro_scope,))
transport = tr_requests.AuthorizedSession(credentials)

def generate_download_signed_url_v4(bucket_name, blob_name):
    """Generates a signed URL for downloading a blob.

    Note that this method requires a service account key file. You can not use
    this if you are using Application Default Credentials from Google Compute
    Engine or from the Google Cloud SDK.
    """
    storage_client = storage.Client.from_service_account_json('videobackup-317718-8dc2e1565986.json')
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        # This URL is valid for 15 minutes
        expiration=datetime.timedelta(minutes=15),
        # Allow GET requests using this URL.
        method='GET'
        )

    print('Generated GET signed URL:')
    print(url)
    print('You can use this URL with any user agent, for example:')
    print('curl \'{}\''.format(url))
    return url

def list_buckets():
    """Lists all buckets."""

    storage_client = storage.Client()
    buckets = storage_client.list_buckets()

    for bucket in buckets:
        print(bucket.name)
    return buckets


def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    bucket_name = "respaldo_grabaciones"

    storage_client = storage.Client()

    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name)
    contents = []

    for blob in blobs:
        contents.append(blob.name)
    return contents

def download_file(file_name, bucket):
    """
    Function to download a given file from an S3 bucket
    """
    s3 = boto3.resource('s3')
    output = f"downloads/{file_name}"
    s3.Bucket(bucket).download_file(file_name, output)
    return output

def download_chunk(media_url):
    chunk_size = 50 * 1024 * 1024  # 50MB
    stream = io.BytesIO()
    download = ChunkedDownload(media_url, chunk_size, stream)
    response = download.consume_next_chunk(transport)
    return response