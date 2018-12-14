from flask import Flask, jsonify, request
from functools import wraps

app = Flask(__name__)


def get_client_id():
    return request.headers.get('X-Client-Id', None)


class api:
    def make_api(rule, method, **options):
        def decorate(f):

            skip_auth = options.pop('skip_auth', False)

            @wraps(f)
            def wrapper(*args, **kwargs):

                if not get_client_id() and not skip_auth:
                    return '401 Unauthorized\n', 401

                response = f(*args, **kwargs)
                return jsonify(response)

            if 'methods' not in options:
                options['methods'] = [method]
            app.add_url_rule(rule, '%s.%s' % (f.__module__, f.__name__), view_func=wrapper, **options)
            return wrapper

        return decorate

    def get(rule, **options):
        return api.make_api(rule, 'GET', **options)

    def put(rule, **options):
        return api.make_api(rule, 'PUT', **options)

    def post(rule, **options):
        return api.make_api(rule, 'POST', **options)

    def delete(rule, **options):
        return api.make_api(rule, 'DELETE', **options)
