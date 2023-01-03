from decouple import config

import psycopg2.extensions
import select


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
