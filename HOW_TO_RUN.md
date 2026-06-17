# 🚀 How to Run Echo-Check

## Quick Start (Easiest Method)

### Step 1: Navigate to Project Root
```bash
cd /Users/akilamanasa/Desktop/Echo-check
```

### Step 2: Activate Virtual Environment
```bash
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Run the Application
```bash
python3 run.py
```

**IMPORTANT:** Use `run.py`, NOT `app.py`!

That's it! The server will start automatically.

---

## Alternative Methods

### Method 1: Using run.py (Recommended)
```bash
# From project root directory
python3 run.py
```

This automatically:
- ✅ Detects and uses virtual environment
- ✅ Handles port conflicts (auto-switches to 5001, 5002, etc.)
- ✅ Shows helpful error messages

### Method 2: Direct Backend Run
```bash
# Make sure you're in project root, not backend folder
cd /Users/akilamanasa/Desktop/Echo-check
source venv/bin/activate
python backend/app.py
```

### Method 3: Using the Shell Script
```bash
./start.sh
```

---

## Common Issues & Solutions

### ❌ Error: "No module named 'bson'"

**Problem:** Not using virtual environment

**Solution:**
```bash
# Activate venv first
source venv/bin/activate

# Then run
python3 run.py
```

### ❌ Error: "can't open file 'app.py'"

**Problem:** Running from wrong directory or wrong file name

**Solution:**
```bash
# Make sure you're in project root
cd /Users/akilamanasa/Desktop/Echo-check

# Use run.py (not app.py)
python3 run.py
```

### ❌ Error: "Port 5000 is in use"

**Solution:** The app automatically switches to port 5001, 5002, etc.
Just use the port shown in the message (e.g., `http://localhost:5002`)

---

## Step-by-Step First Time Setup

1. **Navigate to project:**
   ```bash
   cd /Users/akilamanasa/Desktop/Echo-check
   ```

2. **Activate virtual environment:**
   ```bash
   source venv/bin/activate
   ```
   You should see `(venv)` appear in your prompt.

3. **Configure environment (if not done):**
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env with your MongoDB URI and JWT_SECRET
   cd ..
   ```

4. **Run the application:**
   ```bash
   python3 run.py
   ```

5. **Open in browser:**
   - Look for the message: `🚀 Starting Echo-Check server on http://0.0.0.0:XXXX`
   - Open: `http://localhost:XXXX` (replace XXXX with the port number)

---

## What You Should See

When running successfully, you'll see:
```
⚠️  Port 5000 is in use. Using port 5002 instead.
🚀 Starting Echo-Check server on http://0.0.0.0:5002
 * Serving Flask app 'backend.app'
 * Debug mode: off
 * Running on http://127.0.0.1:5002
Press CTRL+C to quit
```

Then open `http://localhost:5002` in your browser.

---

## Stop the Server

Press `CTRL+C` in the terminal where the server is running.

---

## Summary

**Always use this command:**
```bash
source venv/bin/activate
python3 run.py
```

This works from the project root directory and handles everything automatically!

