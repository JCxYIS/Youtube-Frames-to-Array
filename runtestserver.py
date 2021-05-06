from flask import Flask, send_file, Response

import processing

app = Flask(__name__)


@app.route("/")
def home():
    return Response("haha")


@app.route("/output")
def output():
    # processing.main()
    # print("processing is done")
    return send_file(processing.OUTPUT_PATH)


@app.route("/badapple")
def send_mp3():
    # processing.main()
    # print("processing is done")
    return send_file("badapple.mp3")


if __name__ == '__main__':
    app.run(port=8763)