# ✅ Port Conflict Fixed

## Problem
Error: "Port 5000 is in use" when running `backend/app.py` directly.

## Solution

### 1. ✅ Improved Port Handling
- Default port changed to **5001** (instead of 5000)
- Automatic port conflict detection
- Tries alternative ports: 5001, 5002, 8000, 8080, 3000
- Better error messages with troubleshooting tips

### 2. ✅ Command Line Port Support
You can now specify a port:
```bash
python backend/app.py --port=8000
```

## How to Run

### Recommended: Use `run.py`
```bash
cd /Users/akilamanasa/Desktop/Echo-check
source venv/bin/activate
python3 run.py
```

### Alternative: Run `app.py` directly
```bash
cd /Users/akilamanasa/Desktop/Echo-check
source venv/bin/activate
python3 backend/app.py
```

### With Custom Port
```bash
python3 backend/app.py --port=8000
```

## Fix Port 5000 Conflict

If port 5000 is in use (often by macOS AirPlay Receiver):

### Option 1: Let it auto-select another port
The app will automatically try port 5001, 5002, 8000, etc.

### Option 2: Disable AirPlay Receiver (macOS)
1. System Preferences → General
2. AirDrop & Handoff
3. Turn off "AirPlay Receiver"

### Option 3: Kill the process on port 5000
```bash
# Find process
lsof -ti:5000

# Kill it (replace PID with actual process ID)
kill -9 588
```

## Status: ✅ FIXED

Port handling improved. The app will automatically use an available port if the default is busy.


