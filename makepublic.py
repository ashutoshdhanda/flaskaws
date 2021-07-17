from google.cloud import storage
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/ashutosh/python_scripts_test/flaskaws/videobackup-317718-8dc2e1565986.json"
bucket_name = "respaldo_grabaciones"
def set_bucket_public_iam(bucket_name):
    """Set a public IAM Policy to bucket"""

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    policy = bucket.get_iam_policy(requested_policy_version=3)
    policy.bindings.append(
        {"role": "roles/storage.objectViewer", "members": {"allUsers"}}
    )

    bucket.set_iam_policy(policy)

    print("Bucket {} is now publicly readable".format(bucket.name))
set_bucket_public_iam(bucket_name)