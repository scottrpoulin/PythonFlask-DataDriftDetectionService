from flask import Flask, render_template, send_file, abort, request
from datadriftdetectionservice.driftdetection import drift_detection
from gevent.pywsgi import WSGIServer
import os

app = Flask(__name__)


@app.route("/", methods=['GET'])
def main():
    return render_template("index.html")


@app.route("/last30days", defaults={'req_path': ''}, methods=['GET'])
@app.route('/last30days/<path:req_path>')
def last_30_days(req_path):
    drift_detection.data_drift_detection_previous(30)
    BASE_DIR = './datadriftdetectionservice/templates/results'
    SEND_DIR = 'templates/results'

    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)
    send_path = os.path.join(SEND_DIR, req_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(BASE_DIR):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(send_path)

    # Show directory contents
    files = os.listdir(abs_path)

    return render_template('browse-results.html', files=files)


@app.route("/lastXdays", defaults={'req_path': ''}, methods=['GET'])
@app.route('/lastXdays/<path:req_path>')
def last_X_days(req_path):
    if 'html' not in request.path:
        days = request.args.get('days')
        drift_detection.data_drift_detection_previous(int(days))
    BASE_DIR = './datadriftdetectionservice/templates/results'
    SEND_DIR = 'templates/results'

    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)
    send_path = os.path.join(SEND_DIR, req_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(BASE_DIR):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(send_path)

    # Show directory contents
    files = os.listdir(abs_path)

    return render_template('browse-results.html', files=files)


if __name__ == '__main__':
    # Debug/Development
    # app.run(debug=True, host="0.0.0.0", port="5000")
    # Production
    http_server = WSGIServer(('', 5001), app)
    http_server.serve_forever()
