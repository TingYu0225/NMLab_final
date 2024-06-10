from flask import Flask, request
from flask_cors import CORS ,cross_origin
import time

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["POST"])
@cross_origin()
def user_upload():
    print(request.form)

    image_file = request.form.get('image')
    print(image_file)

    return "ok"

if __name__ == "__main__":
     app.run(host='0.0.0.0', port=5000, debug=True)