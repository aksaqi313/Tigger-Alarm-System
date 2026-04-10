# Water Level Alarm System - Python Web App

## Overview

This is a Python Flask-based conversion of the original HTML Water Level Alarm System. It provides a real-time monitoring and control system for water level alarms with a beautiful cyber-themed user interface.

## Features

✅ **Real-time Monitoring** - Live sensor readings update every second
✅ **Alarm Control** - Select and trigger 3 alarm levels (LOW, MEDIUM, HIGH)
✅ **30-Second Alarm Duration** - Automatic countdown timer with visual arc
✅ **Sensor Simulation** - Realistic sensor data with random walk algorithm
  - Water Level (meters)
  - Radar Distance (meters)
  - Panel Temperature (°C)
  - Battery Voltage (V)
✅ **Alarm Logging** - Complete event log with timestamps (max 1000 entries)
✅ **SW12 Relay Output** - Visual indicator for siren/light activation
✅ **Responsive Design** - Works on desktop and mobile devices
✅ **Multi-threaded Backend** - Thread-safe state management

## Architecture

### Backend (Python Flask)
- `app.py` - Main Flask application with the WaterAlarmSystem class
- **State Management** - Thread-safe alarm state with locking mechanism
- **Scan Loop** - Runs every 1 second to update sensors and process logic
- **API Endpoints** - RESTful API for frontend communication

### Frontend (HTML/CSS/JavaScript)
- `static/index.html` - UI with real-time polling
- **CSS** - Cyber-themed styling with animations and glows
- **JavaScript** - Fetch API to communicate with Python backend

## System Architecture

```
┌─────────────────────────────────────────┐
│   Flask Web Server (localhost:5000)     │
├─────────────────────────────────────────┤
│  WaterAlarmSystem Class (Thread-safe)   │
│  ├─ State Variables                     │
│  ├─ Sensor Simulation                   │
│  ├─ Scan Loop (1 sec interval)         │
│  └─ Alarm Logic                         │
├─────────────────────────────────────────┤
│  RESTful API Endpoints                  │
│  ├─ /api/state      (GET)              │
│  ├─ /api/select     (POST)             │
│  ├─ /api/trigger    (POST)             │
│  ├─ /api/reset      (POST)             │
│  ├─ /api/logs       (GET)              │
│  └─ /api/clear-logs (POST)             │
├─────────────────────────────────────────┤
│  HTML/CSS/JavaScript Frontend           │
│  └─ Polls /api/state every 500ms       │
└─────────────────────────────────────────┘
```

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Steps

1. **Navigate to the project directory:**
   ```powershell
   cd "c:\Users\Azhar Khan\Desktop\Alram tigger code"
   ```

2. **Create a virtual environment (optional but recommended):**
   ```powershell
   python -m venv venv
   venv\Scripts\Activate.ps1
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

## Running the Application

### Start the Flask Server

```powershell
python app.py
```

### Output:
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

### Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage Guide

### Alarm Selection
1. Click one of the three alarm buttons: **LOW**, **MED**, or **HIGH**
2. The selected alarm type is displayed with color coding:
   - 🟨 **LOW** (Yellow)
   - 🟧 **MEDIUM** (Orange)
   - 🔴 **HIGH** (Red)

### Triggering the Alarm
1. Select an alarm level first
2. Click the **"▶ ACTIVATE ALARM"** button
3. The alarm will run for 30 seconds with a countdown timer
4. The SW12 relay indicator will turn red/on
5. The event will be logged automatically

### Real-Time Monitoring
- **Water Level** - Current water depth in meters
- **Radar Distance** - Distance measurement in meters
- **Panel Temperature** - Enclosure temperature in °C
- **Battery Voltage** - System power supply in volts

### Alarm Log
The log table shows all events with:
- Timestamp (HH:MM:SS.mmm format)
- Event type (START, END, WARN)
- Alarm type active
- Active alarm level
- Timer countdown
- All sensor readings

## API Documentation

### GET /api/state
Returns the current system state.

**Response:**
```json
{
  "alarm_select": 0,
  "alarm_trigger": 0,
  "active_alarm": 0,
  "alarm_timer": 0,
  "alarm_type": "NORMAL",
  "alarm_message": "",
  "water_level": 4.567,
  "radar_distance": 5.433,
  "ptemp": 25.15,
  "batt_volts": 12.582,
  "log_entries": [...]
}
```

### POST /api/select
Select an alarm level (1-3).

**Request Body:**
```json
{
  "level": 1
}
```

**Response:**
```json
{
  "success": true
}
// or
{
  "error": "Alarm already active"
}
```

### POST /api/trigger
Trigger the selected alarm.

**Response:**
```json
{
  "success": true
}
// or
{
  "error": "Please select alarm level first"
}
```

### POST /api/reset
Reset the entire alarm system.

**Response:**
```json
{
  "success": true
}
```

### GET /api/logs
Get all alarm log entries.

**Response:**
```json
{
  "logs": [
    {
      "id": 1712748300000.123,
      "ts": "14:35:20.123",
      "event": "START",
      "type": "HIGH",
      "active": 3,
      "timer": 30,
      "select": 3,
      "trigger": 1,
      "msg": "",
      "wl": "4.567",
      "rd": "5.433",
      "pt": "25.15",
      "bv": "12.582"
    }
  ]
}
```

### POST /api/clear-logs
Clear all alarm log entries.

**Response:**
```json
{
  "success": true
}
```

## Configuration

Edit the `WaterAlarmSystem` class in `app.py` to change:

```python
self.alarm_duration = 30          # Alarm duration in seconds
self.reference_height = 10.0      # Reference water height in meters
self.max_logs = 1000              # Maximum log entries to keep
```

## Troubleshooting

### Port Already in Use
If port 5000 is already in use:
```python
# Edit app.py, change the port
app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5001)
```

### Connection Refused
- Make sure the Flask server is running
- Check that you're accessing http://localhost:5000 (not https)
- Verify no firewall is blocking port 5000

### UI Not Updating
- Check browser console for JavaScript errors (F12)
- Verify the Flask API endpoints are responding (check Network tab)
- Try clearing browser cache (Ctrl+Shift+Delete)

## Project Structure

```
Alram tigger code/
├── app.py                  # Python Flask backend
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── water_alarm_system.html # Original HTML (reference)
└── static/
    └── index.html         # Updated HTML frontend
```

## Performance

- **Update Rate:** 500ms (frontend polls backend)
- **Scan Loop:** 1000ms (backend processes state)
- **Max Logs:** 1000 entries
- **Thread Safety:** Uses threading.Lock() for state protection
- **Memory Usage:** Minimal (~10-20 MB typical)

## Future Enhancements

- 📊 Historical data visualization
- 📧 Email/SMS notifications
- 💾 Database integration for persistent logs
- 🔐 User authentication and authorization
- 📱 Mobile app (React Native/Flutter)
- 🌐 Multi-client support with WebSockets
- 📈 Advanced sensor calibration
- ⚙️ Configuration dashboard

## License

This is a converted educational project. Use freely.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation
3. Check Flask console output for errors
4. Inspect browser developer tools (F12)

---

**Last Updated:** April 2026
**Backend:** Python 3.7+ with Flask
**Frontend:** HTML5 + CSS3 + JavaScript (Fetch API)
