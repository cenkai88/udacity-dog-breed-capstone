from flask import Flask, abort, flash, request, redirect, url_for, send_from_directory
from flask_cors import CORS
# from werkzeug.utils import secure_filename

from utils.model import image_predictor

app = Flask(__name__)
CORS(app, supports_credentials=True)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def is_file_allowed(filename):
    """
    Parameter:
    filename: filename of the file user uploads
    
    Returns:
    Whether the file is supported by the app
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/image/dog_breed_classification/v1', methods=["POST"])
def dog_breed_classification():
    if request.method == 'POST':
        try:
            file = request.files['file']
            if file and is_file_allowed(file.filename):
                result = image_predictor(file.stream.read())
                return { 'result': result }
            else:
                # file not supported
                abort(400)
        except Exception as err:
            print(err)
            # invalid input parameter
            abort(500)
    else:
        # unsupported method
        abort(405)


def main():
    app.run(host='localhost', port=3000, debug=True)

if __name__ == '__main__':
    print('----- Web page needs to be launched in web folder -----')
    print('----- api schema can be found in api-doc.yaml -----')
    main()

