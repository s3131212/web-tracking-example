from flask import *
import random
import string
import base64

app = Flask(__name__)
def random_str():
    return ''.join([random.choice(string.ascii_letters) for _ in range(20)])

@app.route('/')
def index():
    identifier = random_str()
    print(f'Assign identifier {identifier}')
    return render_template('index.html', identifier=identifier)
    
@app.route('/pixel.gif', methods=['GET'])
def doc():
    identifier = request.args.get('identifier')
    page_url = request.args.get('page_url')

    print(f'identifier {identifier} visited page {page_url}')
    
    pixel_data = base64.b64decode("R0lGODlhAQABAIAAAP8AAP8AACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==")
    res = make_response(pixel_data)
    res.set_etag(identifier)
    res.mimetype = "image/gif"
    return res

# Run the server using the port specified in the command line arguments
app.run(host="0.0.0.0", port=5000)