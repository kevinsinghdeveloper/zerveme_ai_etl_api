from functools import wraps

import jwt
from flask import request, jsonify


def token_required(app):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({"error": "Token is missing"}), 401

            try:
                # Decode the token using the passed-in app instance
                jwt.decode(token, app.config['SECRET_KEY'],
                           algorithms=["HS256"])
            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token has expired"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"error": "Invalid token"}), 401

            return f(*args, **kwargs)

        return decorated

    return decorator
