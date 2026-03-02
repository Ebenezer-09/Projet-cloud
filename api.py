import os
import logging
import requests

BASE_URL = os.getenv('CLOUD_API_URL', 'https://cloud-backend-80wx.onrender.com')
TIMEOUT_SECONDS = int(os.getenv('API_TIMEOUT_SECONDS', '15'))
logger = logging.getLogger(__name__)

# use a single Session object to preserve cookies between calls
_session = requests.Session()

class APIError(Exception):
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code


def _request(method, path, token=None, **kwargs):
    url = BASE_URL.rstrip('/') + path
    logger.debug(
        "API request -> %s %s headers=%s params=%s json=%s",
        method,
        url,
        kwargs.get('headers'),
        kwargs.get('params'),
        kwargs.get('json'),
    )
    headers = kwargs.pop('headers', {}) or {}
    headers.setdefault('Accept', 'application/json')
    if token:
        headers['Authorization'] = f'Bearer {token}'
    # for JSON body convenience
    if 'json' in kwargs:
        headers.setdefault('Content-Type', 'application/json')
    # use persistent session so cookies (e.g. from login) are preserved
    try:
        response = _session.request(method, url, headers=headers, timeout=TIMEOUT_SECONDS, **kwargs)
    except requests.exceptions.RequestException as exc:
        # network-level error
        raise APIError(str(exc))
    # debugging information
    try:
        data = response.json()
    except ValueError:
        data = None
    if not response.ok:
        detail = None
        if data and isinstance(data, dict):
            detail = data.get('detail') or data.get('message')
        msg = detail or response.text or f'Status {response.status_code}'
        raise APIError(msg, status_code=response.status_code)
    return data

# health / test

def health():
    return _request('GET', '/')

def test_db():
    return _request('GET', '/test-db')

# auth

def signup(email, password, name=None):
    payload = {'email': email, 'password': password}
    if name:
        payload['name'] = name
    return _request('POST', '/signup', json=payload)


def login(email, password):
    payload = {'email': email, 'password': password}
    return _request('POST', '/login', json=payload)


def list_users(token=None):
    return _request('GET', '/users', token=token)

# files

def upload_file(file_obj, user_id, name=None, status='private', description=None, token=None):
    # file_obj can be a werkzeug FileStorage (from Flask request.files)
    # or a plain file object opened in binary mode. Requests accepts any
    # file-like object in the files tuple.
    filename = None
    mimetype = None
    # detect attributes
    if hasattr(file_obj, 'filename'):
        filename = file_obj.filename
    elif hasattr(file_obj, 'name'):
        filename = os.path.basename(file_obj.name)
    else:
        filename = 'file'
    if hasattr(file_obj, 'mimetype'):
        mimetype = file_obj.mimetype
    else:
        # guess mimetype from filename, ignore failures
        import mimetypes
        mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
    files = {'file': (filename, file_obj, mimetype)}
    data = {'user_id': user_id, 'status': status}
    if name:
        data['name'] = name
    if description is not None:
        # backend may ignore unknown fields, but include if provided
        data['description'] = description
    return _request('POST', '/upload', token=token, files=files, data=data)


def get_user_files(user_id, token=None):
    return _request('GET', f'/files/{user_id}', token=token)


def get_all_files(token=None):
    return _request('GET', '/files', token=token)


def update_file_status(file_id, status, token=None):
    return _request('PATCH', f'/files/{file_id}/status', token=token, json={'status': status})


def delete_file(file_id, token=None):
    return _request('DELETE', f'/files/{file_id}', token=token)
