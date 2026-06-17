"""
Utility functions for JWT authentication and database connection
"""
import jwt
import os
from functools import wraps
from flask import request, jsonify
from datetime import datetime, timedelta, timezone
from pymongo import MongoClient
from bson import ObjectId
from pathlib import Path
from dotenv import load_dotenv

# Load .env file if not already loaded
backend_env = Path(__file__).parent / '.env'
if backend_env.exists() and not os.getenv("JWT_SECRET"):
    load_dotenv(dotenv_path=backend_env, override=True)

# MongoDB connection
_db_client = None
_db_instance = None

def get_db():
    """Get MongoDB database connection with error handling"""
    global _db_client, _db_instance
    
    try:
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        db_name = os.getenv("DB_NAME", "echo_check")
        
        # Reuse connection if available
        if _db_client is None:
            _db_client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            # Test connection
            _db_client.admin.command('ping')
            _db_instance = _db_client[db_name]
            print(f"✅ Connected to MongoDB: {db_name}")
        
        return _db_instance
    
    except Exception as e:
        print(f"❌ MongoDB connection error: {e}")
        print("   Make sure MongoDB is running:")
        print("   - macOS: brew services start mongodb-community")
        print("   - Linux: sudo systemctl start mongod")
        print("   - Or check: mongosh")
        # Return a connection anyway (might work on retry)
        if _db_client is None:
            try:
                _db_client = MongoClient(mongo_uri, serverSelectionTimeoutMS=2000)
                _db_instance = _db_client[db_name]
            except:
                pass
        if _db_instance is None:
            raise Exception("MongoDB connection failed. Please start MongoDB.")
        return _db_instance

# JWT functions
def encode_jwt(user_id):
    """Generate JWT token for user"""
    secret = os.getenv("JWT_SECRET")
    if not secret:
        # For development, use a default (NOT SECURE FOR PRODUCTION)
        import warnings
        warnings.warn("JWT_SECRET not set. Using default for development only. Set JWT_SECRET in .env for production!")
        secret = "dev_secret_change_in_production"
        os.environ["JWT_SECRET"] = secret
    
    payload = {
        "user_id": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(days=7),
        "iat": datetime.now(timezone.utc)
    }
    return jwt.encode(payload, secret, algorithm="HS256")

def decode_jwt(token):
    """Decode and verify JWT token"""
    secret = os.getenv("JWT_SECRET")
    if not secret:
        # For development, use a default (NOT SECURE FOR PRODUCTION)
        import warnings
        warnings.warn("JWT_SECRET not set. Using default for development only. Set JWT_SECRET in .env for production!")
        secret = "dev_secret_change_in_production"
        os.environ["JWT_SECRET"] = secret
    
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def get_token_from_header():
    """Extract JWT token from Authorization header"""
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None
    try:
        token = auth_header.split(" ")[1]  # "Bearer <token>"
        return token
    except IndexError:
        return None

def require_auth(f):
    """Decorator to require JWT authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = get_token_from_header()
        if not token:
            return jsonify({"error": "Missing or invalid token"}), 401
        
        payload = decode_jwt(token)
        if not payload:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        # Add user_id to request context
        request.user_id = payload["user_id"]
        return f(*args, **kwargs)
    
    return decorated_function

def to_json_serializable(obj):
    """Convert MongoDB ObjectId and datetime to JSON serializable format"""
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {k: to_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [to_json_serializable(item) for item in obj]
    return obj

