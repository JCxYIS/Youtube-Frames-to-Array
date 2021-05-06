from flask import Flask, send_file, Response

import processing

app = Flask(__name__)


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


@app.route("/refresh")
def refresh():
    processing.main()
    return Response("ok")


@app.route("/audio")
def send_mp3():
    """
    send mp3
    """
    # processing.main()
    # print("processing is done")
    return send_file(processing.AUDIO_PATH)


if __name__ == '__main__':
    app.run(port=8763)