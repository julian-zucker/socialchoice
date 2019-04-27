import functools
import json
import traceback

import jsonschema

pg_pool = None


def cloudfunction(in_schema=None, out_schema=None):
    """

    :param in_schema: the schema for the input, or a falsy value if there is no input
    :param out_schema: the schema for the output, or a falsy value if there is no output
    :return: the cloudfunction wrapped function
    """
    # Both schemas must be valid according to jsonschema draft 7, if they are provided.
    if in_schema:
        jsonschema.Draft7Validator.check_schema(in_schema)
    if out_schema:
        jsonschema.Draft7Validator.check_schema(out_schema)

    def cloudfunction_decorator(f):
        """ Wraps a function with two arguments, the first of which is a json object that it expects to be sent with the
        request, and the second is a postgresql pool. It modifies it by:
         - setting CORS headers and responding to OPTIONS requests with `Allow-Origin *`
         - passing a connection from a global postgres connection pool
         - adding logging, of all inputs as well as error tracebacks.

        :param f: A function that takes a `request` and a `pgpool` and returns a json-serializable object
        :return: a function that accepts one argument, a Flask request, and calls f with the modifications listed
        """

        @functools.wraps(f)
        def wrapped(request):
            global pg_pool

            if request.method == 'OPTIONS':
                return cors_options()

            # If it's not a CORS OPTIONS request, still include the base header.
            headers = {'Access-Control-Allow-Origin': '*'}

            if not pg_pool:
                pg_pool = get_pool()

            try:
                conn = pg_pool.getconn()

                if in_schema:
                    request_json = request.get_json()
                    print(repr({"request_json": request_json}))
                    jsonschema.validate(request_json, in_schema)
                    function_output = f(request_json, conn)
                else:
                    function_output = f(conn)

                if out_schema:
                    jsonschema.validate(function_output, out_schema)

                conn.commit()
                print(repr({"response_json": function_output}))

                response_json = json.dumps(function_output)
                # TODO allow functions to specify return codes in non-exceptional cases
                return (response_json, 200, headers)
            except:
                print("Error: Exception traceback: " + repr(traceback.format_exc()))
                return (traceback.format_exc(), 500, headers)
            finally:
                # Make sure to put the connection back in the pool, even if there has been an exception
                try:
                    pg_pool.putconn(conn)
                except NameError:  # conn might not be defined, depending on where the error happens above
                    pass

        return wrapped

    return cloudfunction_decorator


# If given an OPTIONS request, tell the requester that we allow all CORS requests (pre-flight stage)
def cors_options():
    # Allows GET and POST requests from any origin with the Content-Type
    # header and caches preflight response for an 3600s
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600'
    }

    return ('', 204, headers)


from os import getenv
from psycopg2 import OperationalError, connect
from psycopg2.pool import SimpleConnectionPool

INSTANCE_CONNECTION_NAME = getenv('INSTANCE_CONNECTION_NAME', "")

POSTGRES_USER = getenv('POSTGRES_USER', "")
POSTGRES_PASSWORD = getenv('POSTGRES_PASSWORD', "")
POSTGRES_NAME = getenv('POSTGRES_DATABASE', "postgres")

pg_config = {
    'user': POSTGRES_USER,
    'password': POSTGRES_PASSWORD,
    'dbname': POSTGRES_NAME
}


def get_pool():
    try:
        return __connect(f'/cloudsql/{INSTANCE_CONNECTION_NAME}')
    except OperationalError:
        # If production settings fail, use local development ones
        return __connect('localhost')


def __connect(host):
    """
    Helper functions to connect to Postgres
    """
    pg_config['host'] = host
    return SimpleConnectionPool(1, 1, **pg_config)


def get_connection(conn_details=None):
    if conn_details:
        return connect(**conn_details)
    else:
        return connect(**pg_config)
