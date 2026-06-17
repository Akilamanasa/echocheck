"""
Echo-Check Flask Backend API
MongoDB + JWT Authentication
"""
import sys
from pathlib import Path

# Add project root to path if running directly
if __name__ == "__main__" or Path(__file__).parent.name == "backend":
    project_root = Path(__file__).parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone
from bson import ObjectId
from passlib.context import CryptContext
from backend.utils import get_db, encode_jwt, require_auth, to_json_serializable

# Load environment variables
# Try to load from backend/.env first, then project root
backend_env = Path(__file__).parent / '.env'
if backend_env.exists():
    load_dotenv(dotenv_path=backend_env)
else:
    load_dotenv()  # Try project root

# Initialize Flask app
project_root = Path(__file__).parent.parent
frontend_path = project_root / 'frontend'

app = Flask(__name__)
# Enable CORS with proper configuration
CORS(app, 
     resources={r"/api/*": {"origins": "*"}},
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ==================== AUTH ENDPOINTS ====================

@app.route("/api/register", methods=["POST"])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request data"}), 400
            
        name = data.get("name", "").strip()
        email = data.get("email", "").strip().lower()
        password = data.get("password", "").strip()
        
        # Validation
        if not name or not email or not password:
            return jsonify({"error": "Name, email, and password are required"}), 400
        
        if len(password) < 6:
            return jsonify({"error": "Password must be at least 6 characters"}), 400
        
        # Test database connection
        try:
            db = get_db()
            # Test connection by pinging
            db.client.admin.command('ping')
        except Exception as db_error:
            return jsonify({
                "error": "Database connection failed",
                "details": str(db_error),
                "help": "Make sure MongoDB is running. Check terminal for connection details."
            }), 503
        
        users = db.users
        
        # Check if email already exists
        if users.find_one({"email": email}):
            return jsonify({"error": "Email already registered"}), 409
        
        # Hash password and create user
        hashed_password = pwd_context.hash(password)
        user_doc = {
            "name": name,
            "email": email,
            "password": hashed_password,
            "createdAt": datetime.now(timezone.utc)
        }
        
        result = users.insert_one(user_doc)
        user_id = str(result.inserted_id)
        
        print(f"✅ User registered: {email} (ID: {user_id})")
        
        return jsonify({
            "message": "User registered successfully",
            "user_id": user_id
        }), 201
    
    except Exception as e:
        print(f"❌ Registration error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Registration failed: {str(e)}"}), 500

@app.route("/api/login", methods=["POST"])
def login():
    """Login and get JWT token"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request data"}), 400
            
        email = data.get("email", "").strip().lower()
        password = data.get("password", "").strip()
        
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400
        
        # Test database connection
        try:
            db = get_db()
            # Test connection by pinging
            db.client.admin.command('ping')
        except Exception as db_error:
            return jsonify({
                "error": "Database connection failed",
                "details": str(db_error),
                "help": "Make sure MongoDB is running. Check terminal for connection details."
            }), 503
        
        user = db.users.find_one({"email": email})
        
        if not user:
            print(f"❌ Login failed: User not found - {email}")
            return jsonify({"error": "Invalid credentials"}), 401
        
        # Verify password
        if not pwd_context.verify(password, user["password"]):
            print(f"❌ Login failed: Invalid password for - {email}")
            return jsonify({"error": "Invalid credentials"}), 401
        
        # Generate JWT token
        token = encode_jwt(str(user["_id"]))
        
        print(f"✅ User logged in: {email} (ID: {user['_id']})")
        
        return jsonify({
            "token": token,
            "user": {
                "id": str(user["_id"]),
                "name": user["name"],
                "email": user["email"]
            }
        }), 200
    
    except Exception as e:
        print(f"❌ Login error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Login failed: {str(e)}"}), 500

# ==================== CONTACTS ENDPOINTS ====================

@app.route("/api/contacts", methods=["GET"])
@require_auth
def get_contacts():
    """Get all contacts for authenticated user"""
    try:
        db = get_db()
        contacts = list(db.contacts.find({"userId": request.user_id}))
        return jsonify(to_json_serializable(contacts)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/contacts", methods=["POST"])
@require_auth
def add_contact():
    """Add a new trusted contact"""
    try:
        data = request.get_json()
        name = data.get("name", "").strip()
        phone = data.get("phone", "").strip()
        email = data.get("email", "").strip().lower() or None
        
        if not name or not phone:
            return jsonify({"error": "Name and phone are required"}), 400
        
        db = get_db()
        contact_doc = {
            "userId": request.user_id,
            "name": name,
            "phone": phone,
            "email": email,
            "createdAt": datetime.now(timezone.utc)
        }
        
        result = db.contacts.insert_one(contact_doc)
        contact_doc["_id"] = result.inserted_id
        
        return jsonify(to_json_serializable(contact_doc)), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/contacts/<contact_id>", methods=["DELETE"])
@require_auth
def delete_contact(contact_id):
    """Delete a contact (only if it belongs to user)"""
    try:
        db = get_db()
        result = db.contacts.delete_one({
            "_id": ObjectId(contact_id),
            "userId": request.user_id
        })
        
        if result.deleted_count == 0:
            return jsonify({"error": "Contact not found or unauthorized"}), 404
        
        return jsonify({"message": "Contact deleted successfully"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== TRIP ENDPOINTS ====================

@app.route("/api/trip", methods=["POST"])
@require_auth
def create_trip():
    """Create a new trip (closes any existing active trip)"""
    try:
        data = request.get_json()
        destination = data.get("destination", "").strip()
        interval_minutes = int(data.get("interval_minutes", 60))
        
        if not destination:
            return jsonify({"error": "Destination is required"}), 400
        
        if interval_minutes < 1:
            return jsonify({"error": "Interval must be at least 1 minute"}), 400
        
        db = get_db()
        trips = db.trips
        
        # Close any existing active trip
        now = datetime.now(timezone.utc)
        trips.update_many(
            {"userId": request.user_id, "status": "active"},
            {"$set": {"status": "closed", "closedAt": now}}
        )
        
        # Create new trip
        next_check_due = now + timedelta(minutes=interval_minutes)
        trip_doc = {
            "userId": request.user_id,
            "destination": destination,
            "intervalMinutes": interval_minutes,
            "startedAt": now,
            "nextCheckDue": next_check_due,
            "status": "active"
        }
        
        result = trips.insert_one(trip_doc)
        trip_doc["_id"] = result.inserted_id
        
        return jsonify(to_json_serializable(trip_doc)), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/trip/active", methods=["GET"])
@require_auth
def get_active_trip():
    """Get active trip for user"""
    try:
        db = get_db()
        trip = db.trips.find_one({
            "userId": request.user_id,
            "status": "active"
        })
        
        if not trip:
            return jsonify({"error": "No active trip found"}), 404
        
        return jsonify(to_json_serializable(trip)), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== CHECK-IN ENDPOINTS ====================

@app.route("/api/checkin", methods=["POST"])
@require_auth
def checkin():
    """Record a check-in and update trip next check due time"""
    try:
        data = request.get_json()
        trip_id = data.get("trip_id")
        lat = data.get("lat")
        lng = data.get("lng")
        
        if not trip_id or lat is None or lng is None:
            return jsonify({"error": "trip_id, lat, and lng are required"}), 400
        
        db = get_db()
        
        # Verify trip belongs to user and is active
        trip = db.trips.find_one({
            "_id": ObjectId(trip_id),
            "userId": request.user_id,
            "status": "active"
        })
        
        if not trip:
            return jsonify({"error": "Trip not found or not active"}), 404
        
        # Record check-in
        checkin_doc = {
            "tripId": ObjectId(trip_id),
            "userId": request.user_id,
            "lat": float(lat),
            "lng": float(lng),
            "checkedInAt": datetime.now(timezone.utc)
        }
        db.checkins.insert_one(checkin_doc)
        
        # Update trip next check due time
        now = datetime.now(timezone.utc)
        next_check_due = now + timedelta(minutes=trip["intervalMinutes"])
        db.trips.update_one(
            {"_id": ObjectId(trip_id)},
            {"$set": {"nextCheckDue": next_check_due}}
        )
        
        return jsonify({
            "message": "Check-in recorded",
            "nextCheckDue": next_check_due.isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== SOS ENDPOINT ====================

@app.route("/api/sos", methods=["POST"])
@require_auth
def sos():
    """Create SOS event and return WhatsApp links for contacts"""
    try:
        data = request.get_json()
        lat = data.get("lat")
        lng = data.get("lng")
        
        if lat is None or lng is None:
            return jsonify({"error": "lat and lng are required"}), 400
        
        db = get_db()
        
        # Get user info
        user = db.users.find_one({"_id": ObjectId(request.user_id)})
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Get user's contacts
        contacts = list(db.contacts.find({"userId": request.user_id}))
        
        # Create SOS event
        sos_doc = {
            "userId": request.user_id,
            "lat": float(lat),
            "lng": float(lng),
            "createdAt": datetime.now(timezone.utc)
        }
        db.sos_events.insert_one(sos_doc)
        
        # Generate WhatsApp links
        map_link = f"https://maps.google.com/?q={lat},{lng}"
        message_text = (
            f"🚨 SOS Alert from {user.get('name', 'User')} 🚨\n\n"
            f"Location: {map_link}\n"
            f"\nPlease help immediately!"
        )
        
        from urllib.parse import quote
        encoded_message = quote(message_text)
        
        wa_links = []
        for contact in contacts:
            phone = contact.get("phone", "").strip()
            if phone:
                # Remove any non-digit characters for phone number
                clean_phone = "".join(filter(str.isdigit, phone))
                # Ensure phone number has country code (if it doesn't start with +, assume it needs one)
                # For now, use the number as-is - user should provide full number with country code
                if clean_phone:
                    # WhatsApp requires phone number in international format without + or 00
                    wa_link = f"https://wa.me/{clean_phone}?text={encoded_message}"
                    wa_links.append({
                        "phone": clean_phone,
                        "name": contact.get("name", "Contact"),
                        "link": wa_link
                    })
        
        return jsonify({
            "map_link": map_link,
            "wa_links": wa_links,
            "contacts": to_json_serializable(contacts),
            "message": "SOS event created"
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== ADMIN/UTILITY ENDPOINTS ====================

@app.route("/api/scan_missed_checks", methods=["GET"])
@require_auth
def scan_missed_checks():
    """Get trips where nextCheckDue < now and status == 'active' for user"""
    try:
        db = get_db()
        now = datetime.now(timezone.utc)
        
        missed_trips = list(db.trips.find({
            "userId": request.user_id,
            "status": "active",
            "nextCheckDue": {"$lt": now}
        }))
        
        return jsonify(to_json_serializable(missed_trips)), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== HEALTH CHECK ====================

@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok"}), 200

# ==================== FRONTEND ROUTES ====================
# Note: These routes must be registered AFTER API routes to avoid conflicts

@app.route("/")
def index():
    """Serve the frontend SPA"""
    from flask import send_from_directory
    return send_from_directory(str(frontend_path), 'index.html')

# Serve static files explicitly (CSS, JS, etc.)
@app.route("/style.css")
def serve_css():
    from flask import send_from_directory, Response
    response = send_from_directory(str(frontend_path), 'style.css')
    response.headers['Content-Type'] = 'text/css; charset=utf-8'
    return response

@app.route("/main.js")
def serve_js():
    from flask import send_from_directory, Response
    response = send_from_directory(str(frontend_path), 'main.js')
    response.headers['Content-Type'] = 'application/javascript; charset=utf-8'
    return response

# Catch-all for SPA routing (must be last)
@app.route("/<path:path>")
def serve_frontend(path):
    """Serve frontend static files or SPA fallback"""
    from flask import send_from_directory
    # Don't serve API routes
    if path.startswith('api/'):
        return jsonify({"error": "Not found"}), 404
    
    # Check if it's a static file
    file_path = frontend_path / path
    if file_path.exists() and file_path.is_file():
        return send_from_directory(str(frontend_path), path)
    else:
        # For SPA routing, serve index.html for any non-API path
        return send_from_directory(str(frontend_path), 'index.html')

# ==================== RUN APP ====================

if __name__ == "__main__":
    import socket
    
    # Get port from environment, command line, or default to 5001
    port = int(os.getenv("PORT", 5001))
    if len(sys.argv) > 1:
        if sys.argv[1].startswith('--port='):
            port = int(sys.argv[1].split('=')[1])
        elif sys.argv[1].isdigit():
            port = int(sys.argv[1])
    
    # Check if port is available, try alternatives if not
    def is_port_available(port_num):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('127.0.0.1', port_num))
                return True
            except OSError:
                return False
    
    original_port = port
    if not is_port_available(port):
        # Try alternative ports
        for alt_port in [5001, 5002, 8000, 8080, 3000]:
            if is_port_available(alt_port):
                port = alt_port
                print(f"⚠️  Port {original_port} is in use. Using port {port} instead.")
                print("   To use a specific port: python backend/app.py --port=YOUR_PORT")
                if original_port == 5000:
                    print("   Note: Port 5000 is often used by macOS AirPlay Receiver.")
                    print("   To disable: System Preferences → General → AirDrop & Handoff → AirPlay Receiver")
                break
        else:
            print(f"❌ Error: Port {original_port} is in use and no alternative ports available.")
            print("   Please specify a different port: python backend/app.py --port=YOUR_PORT")
            print(f"   Or stop the process using port {original_port}")
            print("   Recommended: Use 'python3 run.py' instead for better port handling")
            if original_port == 5000:
                print("   On macOS: Disable AirPlay Receiver in System Preferences")
            sys.exit(1)
    
    debug = os.getenv("FLASK_ENV") == "development"
    print(f"🚀 Starting Echo-Check server on http://0.0.0.0:{port}")
    print(f"   Open in browser: http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug)
