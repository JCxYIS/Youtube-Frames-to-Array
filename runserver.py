import time

from flask import Flask, send_file, Response, request
from flask_cors import CORS,cross_origin

import processing


app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    """
    /
    """
    return Response("haha")


@app.route("/output")
def output():
    """
    send output file
    """
    return send_file(processing.FRAME_DATA_PATH)


@app.route("/refresh", methods=['POST'])
def refresh_post():
    setting = processing.PreprocessingSetting()
    if request.form.get('url'):
        setting.URL = request.form.get('url')

    processing.main(setting)
    return Response(str(time.time())+" Processed with "+setting.URL)


# @app.route('/refresh/<path:url>')
# def refresh_with_url(url):
#     processing.main(url)
#     return Response(str(time.time())+" Processed with "+url)


@app.route("/audio")
def send_mp3():
    """
    send mp3
    """
    # processing.main()
    # print("processing is done")
    return send_file(processing.AUDIO_PATH)


if __name__ == '__main__':
    app.run(port=8763, debug=True)