from flask import Flask, Response
from decouple import config

from listen import stream_messages


app = Flask(__name__)


@app.route('/message/<channel>', methods=['GET'])
def get_messages(channel):
    return Response(stream_messages(channel), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(config('PORT')))
