# 🚀 Quick Start - Run on Port 5001

## Run the Application

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Run (will use port 5001 by default)
python3 run.py
```

## Access the Application

Open in browser: **http://localhost:5001**

## What You Should See

- Dark theme page (black/dark gray background)
- White text
- Login/Register tabs
- Forms ready to use

## If Page is Blank

1. **Check browser console** (F12 or Cmd+Option+I):
   - Look for errors in Console tab
   - Check Network tab - verify files load (200 status)

2. **Verify files are loading:**
   - `http://localhost:5001/` → Should show HTML
   - `http://localhost:5001/style.css` → Should show CSS
   - `http://localhost:5001/main.js` → Should show JavaScript

3. **Hard refresh:** `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows)

## Stop Server

Press `CTRL+C` in terminal

## Troubleshooting

- **Port 5001 in use?** The app will auto-switch to 5002, 5003, etc.
- **Still blank?** Check browser console for JavaScript errors
- **404 errors?** Make sure you're running from project root with venv activated

