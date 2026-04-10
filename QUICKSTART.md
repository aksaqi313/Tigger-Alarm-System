# 🚀 Quick Start Guide

## Water Level Alarm System - Python Version

This guide will get you up and running in less than 5 minutes!

---

## Option 1: Automatic Setup (Easiest)

### For Windows (Batch File)

1. Open File Explorer and navigate to:
   ```
   c:\Users\Azhar Khan\Desktop\Alram tigger code
   ```

2. Double-click **`run.bat`**
   - This will automatically:
     - Check if Python is installed
     - Create a virtual environment
     - Install dependencies
     - Start the server
     - Open your browser

3. Your browser will open to `http://localhost:5000` automatically

4. Press `Ctrl+C` in the Command Prompt to stop the server

---

### For Windows (PowerShell)

1. Open PowerShell

2. Navigate to the project directory:
   ```powershell
   cd "c:\Users\Azhar Khan\Desktop\Alram tigger code"
   ```

3. Run the PowerShell script:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
   .\run.ps1
   ```

4. Your browser will open automatically

---

## Option 2: Manual Setup (More Control)

### Step 1: Open Command Prompt or PowerShell

Navigate to the project directory:
```powershell
cd "c:\Users\Azhar Khan\Desktop\Alram tigger code"
```

### Step 2: Create Virtual Environment (Optional but Recommended)

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 4: Run the Application

```powershell
python app.py
```

You should see:
```
============================================================
Water Level Alarm System - Python Application
============================================================

Starting server...
Open your browser and navigate to: http://localhost:5000

API Endpoints:
  GET  /api/state          - Get current system state
  POST /api/select         - Select alarm level
  POST /api/trigger        - Trigger alarm
  POST /api/reset          - Reset system
  GET  /api/logs           - Get alarm logs
  POST /api/clear-logs     - Clear all logs

Press Ctrl+C to stop the server
============================================================
```

### Step 5: Open Your Browser

Go to: **http://localhost:5000**

---

## Using the Application

### 1. Select an Alarm Level
   - Click **LOW** (Yellow) for low priority
   - Click **MED** (Orange) for medium priority
   - Click **HIGH** (Red) for high priority

### 2. Trigger the Alarm
   - Click **▶ ACTIVATE ALARM** button
   - Timer will count down from 30 seconds
   - Red indicator light turns on
   - Event is logged

### 3. Monitor
   - Watch real-time sensor readings
   - View all events in the log table
   - Check SW12 relay status

---

## File Structure

```
Alram tigger code/
├── run.bat                 ← Double-click to run (Windows)
├── run.ps1                 ← PowerShell startup script
├── app.py                  ← Python Flask backend
├── requirements.txt        ← Python dependencies
├── PYTHON_README.md        ← Full documentation
├── QUICKSTART.md          ← This file
│
├── static/
│   └── index.html         ← Web interface
│
└── water_alarm_system.html ← Original HTML (reference)
```

---

## Python Requirements

- **Python 3.7** or higher
- **Flask 2.3.2**
- **Werkzeug 2.3.6**

All dependencies are in `requirements.txt` and installed automatically.

---

## Troubleshooting

### Python Not Found
**Error:** `'python' is not recognized as an internal or external command`

**Solution:**
1. Install Python from https://www.python.org/
2. IMPORTANT: Check "Add Python to PATH" during installation
3. Restart Command Prompt/PowerShell after installing

### Port 5000 Already in Use
**Error:** `OSError: [WinError 10048] Only one usage of each socket address`

**Solution:**
Edit `app.py` line ~400 and change:
```python
app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5001)
                                                            ^^^^
```

Then restart and go to http://localhost:5001

### Can't Connect to Server
**Error:** Browser says "Can't reach localhost:5000"

**Solution:**
1. Make sure the Flask server is running in your terminal
2. Check that you're using `http://` (not `https://`)
3. Make sure nothing else is using port 5000
4. Try a different browser

### Blank Page or No Updates
**Solution:**
1. Press `Ctrl+Shift+Delete` to clear browser cache
2. Refresh the page with `Ctrl+R`
3. Check browser console (Press F12) for errors

---

## Key Differences from HTML Version

| Feature | HTML Version | Python Version |
|---------|-------------|-----------------|
| State Management | JavaScript in browser | Python backend (thread-safe) |
| Data Persistence | Session only (lost on refresh) | Server persists during runtime |
| Performance | Single-threaded | Multi-threaded backend |
| Scalability | Single user | Ready for multi-user (future) |
| API | Internal JavaScript | RESTful API endpoints |
| Deployment | Static file server | Flask web server |

---

## Next Steps

- Read **`PYTHON_README.md`** for detailed documentation
- Check API endpoints: `http://localhost:5000/api/state`
- Explore the code in `app.py`
- Modify sensor values or alarm duration as needed

---

## Support

For issues:
1. Check the **Troubleshooting** section above
2. Read **`PYTHON_README.md`** for detailed info
3. Check Flask console output for error messages
4. Open browser Developer Tools (F12) for JavaScript errors

---

**Ready to go?**
→ Run `run.bat` (Windows) or `python app.py` and enjoy! 🎉
