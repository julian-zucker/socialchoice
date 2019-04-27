from src.app.cloudfunction import cloudfunction


@cloudfunction({}, {})
def hello(request_json, conn):
    return "hello"