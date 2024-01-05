from flask import *
import random
import string
import base64
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
def random_str():
    return ''.join([random.choice(string.ascii_lowercase) for _ in range(20)])

@app.route('/')
def index():
    return make_response('Hello World')
    
@app.route('/doc-cache.txt', methods=['GET'])
def doc():
    identifier = random_str()
    res = make_response(identifier)
    res.cache_control.max_age = 36400 * 365
    return res

@app.route('/redir', methods=['GET'])
def redir():
    identifier = random_str()
    res = redirect(f'/redir/{identifier}', code=301)
    res.cache_control.max_age = 36400 * 365
    return res

@app.route('/redir/<identifier>', methods=['GET'])
def redir_identifier(identifier):
    res = make_response(identifier)
    return res

@app.route('/etag.gif', methods=['GET'])
def etag():
    # detect if If-None-Match is set
    if request.headers.get('If-None-Match'):
        print(f"Return visitor: {request.headers.get('If-None-Match')}")
        return make_response('', 304)

    identifier = random_str()
    print(f"New visitor: {identifier}")

    pixel_data = base64.b64decode("R0lGODlhAQABAIAAAP8AAP8AACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==")
    res = make_response(pixel_data)
    res.set_etag(identifier)
    res.mimetype = "image/gif"
    return res

app.run(host="0.0.0.0", port="5000")