from flask import Flask, Response
from decouple import config

import psycopg2.extensions
import select

app = Flask(__name__)


def stream_messages(channel):
    conn = psycopg2.connect(
        database=config('DB_NAME'),
        user=config('DB_USER'),
        password=config('DB_PASSWORD'),
        host=config('DB_HOST')
    )

    conn.set_isolation_level(
        psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT
    )

    curs = conn.cursor()
    curs.execute('LISTEN channel_%d;' % int(channel))

    while True:
        select.select([conn], [], [])

        conn.poll()

        while conn.notifies:
            notify = conn.notifies.pop()
            yield 'data: ' + notify.payload + '\n\n'


@app.route('/message/<channel>', methods=['GET'])
def get_messages(channel):
    return Response(stream_messages(channel), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(config('PORT')))
