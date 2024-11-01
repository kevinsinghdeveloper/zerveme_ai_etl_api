from flask import Flask, request, jsonify
from dataclasses import dataclass, asdict
from typing import Optional
from functools import wraps
import jwt
import datetime

app = Flask(__name__)

# Secret key for JWT encoding/decoding (make sure to store securely in production)
app.config['SECRET_KEY'] = 'your_secret_key'


@dataclass
class RecommendRequest:
    itemUrl: str
    itemTitle: Optional[str]
    itemPrice: float


# Function to create a unique API key (for demonstration purposes)
def create_api_key():
    # In a production scenario, this would involve more security (e.g., UUIDs or hashing)
    return 'sample_api_key'


# Decorator to require JWT token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({"error": "Token is missing"}), 401

        try:
            # Decode the token to validate it
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated


# Endpoint to log in and receive a JWT token
@app.route('/login', methods=['POST'])
def login_session():
    data = request.json
    api_key = data.get('apiKey')

    # Validate the API key
    if api_key != create_api_key():
        return jsonify({"error": "Invalid API Key"}), 401

    # Generate JWT token
    token = jwt.encode(
        {
            'user': 'example_user',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expires in 1 hour
        },
        app.config['SECRET_KEY'],
        algorithm="HS256"
    )

    return jsonify({"token": token})


# Endpoint to get a recommendation (requires authentication)
@app.route('/recommend', methods=['GET'])
@token_required
def recommend():
    try:
        # Parse the request arguments into a RecommendRequest dataclass
        recommend_request = RecommendRequest(
            itemUrl=request.args.get('itemUrl'),
            itemTitle=request.args.get('itemTitle'),
            itemPrice=float(request.args.get('itemPrice'))
        )

        # Print values for debugging
        print("##############################################")
        print("URL received from frontend:\n", recommend_request.itemUrl)
        print("Product Title received from frontend:\n", recommend_request.itemTitle)
        print("Product price received from frontend:\n", recommend_request.itemPrice)

        # Validate required fields
        if not recommend_request.itemUrl:
            return jsonify({"error": "URL parameter is required"}), 400

        # Process recommendation logic here...

        # Return a successful response
        return jsonify({"message": "Recommendation generated", "data": asdict(recommend_request)})

    except (TypeError, ValueError) as e:
        return jsonify({"error": "Invalid input parameters", "details": str(e)}), 400
