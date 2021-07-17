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

media_url = 'https://storage.googleapis.com/respaldo_grabaciones/mergedVideo.mp4'

chunk_size = 50 * 1024 * 1024  # 50MB
stream = io.BytesIO()
download = ChunkedDownload(media_url, chunk_size, stream)
#response = download.consume_next_chunk(transport)
with open('videse.mp4','wb') as fp:
	download = ChunkedDownload(media_url, chunk_size, fp)
	download.consume_next_chunk(transport)
	#while not download.finished:
		#response = download.consume_next_chunk(transport)