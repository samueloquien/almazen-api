from flask import Response

class JsonResponse(Response):

    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            rv = jsonify(rv)
        return super(MyResponse, cls).force_type(rv, environ)