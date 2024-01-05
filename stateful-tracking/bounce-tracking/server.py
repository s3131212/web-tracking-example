from flask import *
import random
import string
import sys
import time
import urllib.parse as urlparse

random.seed(time.time() * int(sys.argv[1]))

app = Flask(__name__)
def random_str():
    return ''.join([random.choice(string.ascii_letters) for _ in range(20)])

@app.route('/')
def index():
    return make_response('Hello World')
    
@app.route('/bounce', methods=['GET'])
def doc():
    next_url = request.args.get('next_url')
    dest_url = request.args.get('dest_url')

    if next_url:
        # parse next_url and add dest_url as a parameter
        parsed_url = urlparse.urlparse(urlparse.unquote(next_url))
        query = dict(urlparse.parse_qsl(parsed_url.query))
        query['dest_url'] = dest_url

        parsed_url = parsed_url._replace(query=urlparse.urlencode(query))
        res = make_response(redirect(parsed_url.geturl()))
    else:
        res = make_response(redirect(dest_url))

    # read identifier from cookie, otherwise create a new one
    identifier = request.cookies.get('identifier')
    if not identifier:
        identifier = random_str()
        print(f"New visitor {identifier} tries to visit {dest_url}")
        # set cookie
        res.set_cookie('identifier', identifier)
    else:
        print(f"Return visitor {identifier} tries to visit {dest_url}")

    return res

# Run the server using the port specified in the command line arguments
app.run(host="0.0.0.0", port=sys.argv[1])