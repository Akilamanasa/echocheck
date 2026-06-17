# 🚀 How to Run Echo-Check - CORRECT COMMANDS

## ✅ CORRECT Way to Run

```bash
# 1. Make sure you're in the project root directory
cd /Users/akilamanasa/Desktop/Echo-check

# 2. Activate virtual environment
source venv/bin/activate

# 3. Run the application (use run.py, NOT app.py)
python3 run.py
```

## ❌ WRONG Commands (Don't Use These)

```bash
❌ python3 app.py          # File doesn't exist in root
❌ python app.py            # File doesn't exist in root
❌ python3 backend/app.py      # Works but not recommended
```

## Why Use `run.py`?

- ✅ Automatically uses virtual environment
- ✅ Handles port conflicts
- ✅ Creates .env file if missing
- ✅ Shows helpful error messages
- ✅ Properly loads environment variables

## Quick Reference

**Always use:**
```bash
source venv/bin/activate
python3 run.py
```

**From project root directory:**
```bash
/Users/akilamanasa/Desktop/Echo-check/
```

## What You'll See

```
🚀 Starting Echo-Check server on http://0.0.0.0:5001
 * Running on http://127.0.0.1:5001
```

Then open: **http://localhost:5001**

