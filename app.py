import sys

from flask import Flask, render_template, request, redirect, send_file, url_for
from google_api import list_blobs, generate_download_signed_url_v4

app = Flask(__name__)

bucket_name = "respaldo_grabaciones"


@app.route('/')
def entry_point():
    return 'Hello World!'


@app.route("/storage")
def storage():
    contents = list_blobs(bucket_name)
    return render_template('storage.html', contents=contents)

# def list_blobs(bucket_name):
#     """Lists all the blobs in the bucket."""
#     bucket_name = "respaldo_grabaciones"

#     storage_client = storage.Client()

#     # Note: Client.list_blobs requires at least package version 1.17.0.
#     blobs = storage_client.list_blobs(bucket_name)

#     for blob in blobs:
#         print(blob.name)


@app.route("/buckets")
def buckets():
    contents = list_buckets()
    return render_template('storage.html', contents=contents)


@app.route("/download/<filename>", methods=['GET'])
def download(filename):
    if request.method == 'GET':
        output = generate_download_signed_url_v4(bucket_name, filename)
        return render_template('storage.html', url=output)


if __name__ == '__main__':
    app.run(debug=True)
