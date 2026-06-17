# Frontend Testing Guide

## If the page appears black:

The CSS uses a dark theme (`background: #1a1a1a`), so a dark page is expected. However, you should see:
- White text
- Login/Register forms
- Buttons and UI elements

## To verify files are loading:

1. **Open browser console** (F12 or Cmd+Option+I)
2. **Check Network tab** - verify these files load with 200 status:
   - `http://localhost:5002/` (index.html)
   - `http://localhost:5002/style.css`
   - `http://localhost:5002/main.js`

3. **Check Console tab** for JavaScript errors

## Quick Test URLs:

- `http://localhost:5002/` - Main page
- `http://localhost:5002/style.css` - Should show CSS code
- `http://localhost:5002/main.js` - Should show JavaScript code
- `http://localhost:5002/api/health` - Should return `{"status":"ok"}`

## Common Issues:

1. **404 on CSS/JS**: Routes not serving static files correctly
2. **CORS errors**: Backend CORS not configured (already fixed)
3. **JavaScript errors**: Check browser console
4. **Blank page**: JavaScript might be failing silently

## Expected Appearance:

- Dark gray/black background (#1a1a1a)
- White text (#ffffff)
- Blue accent buttons (#4a9eff)
- Login/Register tabs at top
- Forms with input fields

If you see a completely black page with NO text or UI elements, the CSS or JS isn't loading.

