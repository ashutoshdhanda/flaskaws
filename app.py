import sys
import os
import re

from flask import Flask, render_template, request, redirect, send_file, url_for, Response
from google_api import list_blobs, generate_download_signed_url_v4, list_buckets

app = Flask(__name__)

bucket_name = "respaldo_grabaciones"

@app.route('/')
def entry_point():
    return 'Hello World!'

@app.route("/storage")
def storage():
    contents = list_blobs(bucket_name)
    return render_template('storage.html', contents=contents)

@app.route("/buckets")
def buckets():
    contents = list_buckets()
    return render_template('storage.html', contents=contents)

'''
The download route is only used to create the url of the file and pass it on to the
render template with the HTML video tag as source.
''' 
@app.route("/download/<filename>", methods=['GET'])
def download(filename):
    if request.method == 'GET':
        output = generate_download_signed_url_v4(bucket_name, filename)
        #return request.response
        return render_template('storage.html', url=output)

@app.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response

def get_chunk(byte1=None, byte2=None):
    full_path = "meli.mp4"
    file_size = os.stat(full_path).st_size
    start = 0
    
    if byte1 < file_size:
        start = byte1
    if byte2:
        length = byte2 + 1 - byte1
    else:
        length = file_size - start

    with open(full_path, 'rb') as f:
        f.seek(start)
        chunk = f.read(length)
    return chunk, start, length, file_size

@app.route('/video')
def get_file():
    range_header = request.headers.get('Range', None)
    byte1, byte2 = 0, None
    if range_header:
        match = re.search(r'(\d+)-(\d*)', range_header)
        groups = match.groups()

        if groups[0]:
            byte1 = int(groups[0])
        if groups[1]:
            byte2 = int(groups[1])
       
    chunk, start, length, file_size = get_chunk(byte1, byte2)
    resp = Response(chunk, 206, mimetype='video/mp4',
                      content_type='video/mp4', direct_passthrough=True)
    resp.headers.add('Content-Range', 'bytes {0}-{1}/{2}'.format(start, start + length - 1, file_size))
    #return render_template('storage.html', )
    return resp

if __name__ == '__main__':
    app.run(threaded=True)