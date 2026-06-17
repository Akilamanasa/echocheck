# Port Handling - Automatic Port Selection

## Problem Solved

Port 5000 is often in use on macOS by AirPlay Receiver, causing the error:
```
Address already in use
Port 5000 is in use by another program
```

## Solution Implemented

The application now automatically detects if port 5000 is in use and tries alternative ports:
- 5001
- 5002
- 8000
- 8080
- 3000

## How It Works

1. **Automatic Detection**: Checks if the requested port is available
2. **Auto-Fallback**: If port 5000 is busy, automatically tries alternative ports
3. **Clear Messages**: Shows which port is being used and why

## Usage

### Default (Auto Port Selection)
```bash
python3 run.py
# Will use port 5000 if available, or automatically switch to 5001, 5002, etc.
```

### Specify Custom Port
```bash
# Via command line
python3 run.py --port=3000

# Or just the number
python3 run.py 3000

# Via environment variable
export PORT=3000
python3 run.py
```

### Via .env File
```bash
# In backend/.env
PORT=3000
```

## Frontend Configuration

If the backend uses a different port, update `frontend/main.js`:

```javascript
const API_BASE_URL = 'http://localhost:5001/api';  // Change 5001 to your port
```

Or use environment detection (if you add a config endpoint).

## Disable AirPlay Receiver (macOS)

If you want to use port 5000 specifically:

1. Open **System Preferences** (or **System Settings** on newer macOS)
2. Go to **General** → **AirDrop & Handoff**
3. Turn off **AirPlay Receiver**

Then restart the application.

## Example Output

When port 5000 is in use:
```
⚠️  Port 5000 is in use. Using port 5001 instead.
   To use a specific port: python run.py --port=YOUR_PORT
   Note: Port 5000 is often used by macOS AirPlay Receiver.
   To disable: System Preferences → General → AirDrop & Handoff → AirPlay Receiver
🚀 Starting Echo-Check server on http://0.0.0.0:5001
```

## Status

✅ Port conflict handling implemented
✅ Automatic port selection working
✅ Clear error messages and instructions
✅ Multiple ways to specify custom port

