# Echo-Check Backend API

Flask REST API with MongoDB and JWT authentication.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and fill in your values:
   - `MONGO_URI`: MongoDB connection string (default: `mongodb://localhost:27017/`)
   - `DB_NAME`: Database name (default: `echo_check`)
   - `JWT_SECRET`: Secret key for JWT tokens (change this!)
   - `FLASK_ENV`: Set to `development` for debug mode
   - `PORT`: Server port (default: 5000)

3. **Start MongoDB:**
   Make sure MongoDB is running on your system.

4. **Run the server:**
   ```bash
   python app.py
   ```
   Or:
   ```bash
   flask run
   ```

## API Endpoints

### Authentication

**POST /api/register**
```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com", "password": "password123"}'
```

**POST /api/login**
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com", "password": "password123"}'
```

### Contacts (Protected)

**GET /api/contacts**
```bash
curl -X GET http://localhost:5000/api/contacts \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**POST /api/contacts**
```bash
curl -X POST http://localhost:5000/api/contacts \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Emergency Contact", "phone": "+1234567890", "email": "contact@example.com"}'
```

**DELETE /api/contacts/<contact_id>**
```bash
curl -X DELETE http://localhost:5000/api/contacts/CONTACT_ID \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Trips (Protected)

**POST /api/trip**
```bash
curl -X POST http://localhost:5000/api/trip \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"destination": "New York", "interval_minutes": 60}'
```

**GET /api/trip/active**
```bash
curl -X GET http://localhost:5000/api/trip/active \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Check-ins (Protected)

**POST /api/checkin**
```bash
curl -X POST http://localhost:5000/api/checkin \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"trip_id": "TRIP_ID", "lat": 40.7128, "lng": -74.0060}'
```

### SOS (Protected)

**POST /api/sos**
```bash
curl -X POST http://localhost:5000/api/sos \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"lat": 40.7128, "lng": -74.0060, "reason": "Emergency situation"}'
```

### Utility (Protected)

**GET /api/scan_missed_checks**
```bash
curl -X GET http://localhost:5000/api/scan_missed_checks \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Database Collections

- `users`: User accounts
- `contacts`: Trusted contacts
- `trips`: Trip records
- `checkins`: Check-in history
- `sos_events`: SOS event logs

## Security Notes

- JWT tokens expire after 7 days
- All protected routes require `Authorization: Bearer <token>` header
- Passwords are hashed using bcrypt
- For production, use a strong `JWT_SECRET` and enable HTTPS

