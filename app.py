"""
Water Level Alarm System - Python Backend with Flask
Converts the HTML-based alarm system to a Python web application
"""

from flask import Flask, jsonify, request, send_from_directory
from datetime import datetime
import random
import threading
import time
import json
import os

app = Flask(__name__, static_folder='static', static_url_path='')

# ─────────────────────────────────────────────
# ALARM SYSTEM STATE (Core Logic)
# ─────────────────────────────────────────────
class WaterAlarmSystem:
    def __init__(self):
        # State variables (mirrors CRBasic Public variables)
        self.alarm_select = 0
        self.alarm_trigger = 0
        self.prev_trigger = 0
        self.active_alarm = 0
        self.alarm_timer = 0
        self.alarm_type = "NORMAL"
        self.alarm_message = ""
        self.radar_distance = 5.5
        self.water_level = 0.0
        self.ptemp = 25.0
        self.batt_volts = 12.6
        
        # Configuration
        self.alarm_duration = 30
        self.reference_height = 10.0
        
        # Logging
        self.log_entries = []
        self.max_logs = 1000
        
        # Threading
        self.running = False
        self.scan_thread = None
        self.lock = threading.Lock()
    
    def update_sensors(self):
        """Simulate sensor readings with random walk"""
        self.radar_distance = round(
            self.radar_distance + (random.random() - 0.5) * 0.04, 3
        )
        self.radar_distance = max(5.0, min(9.5, self.radar_distance))
        self.water_level = round(self.reference_height - self.radar_distance, 3)
        self.ptemp = round(25.0 + (random.random() - 0.5) * 0.2, 2)
        self.batt_volts = round(12.6 + (random.random() - 0.5) * 0.04, 3)
    
    def scan_loop(self):
        """Main CRBasic scan loop (runs every 1 second)"""
        with self.lock:
            # STEP 1: Update sensor readings
            self.update_sensors()
            
            # STEP 2: Show AlarmType from AlarmSelect when idle
            if self.active_alarm == 0 and self.alarm_timer == 0:
                type_map = {0: "NORMAL", 1: "LOW", 2: "MEDIUM", 3: "HIGH"}
                self.alarm_type = type_map.get(self.alarm_select, "NORMAL")
            
            # STEP 3: Lock AlarmTrigger + AlarmSelect while alarm is running
            if self.alarm_timer > 0:
                self.alarm_trigger = 1
                if self.alarm_select != self.active_alarm:
                    self.alarm_select = self.active_alarm
                    self.alarm_message = "Alarm are all ready active"
            
            # STEP 4: AlarmTrigger clicked but AlarmSelect = 0 → block + warn
            if (self.alarm_trigger == 1 and self.prev_trigger == 0 and
                self.alarm_select == 0 and self.alarm_timer == 0):
                self.alarm_trigger = 0
                self.alarm_message = "Please Select AlarmSelect"
                self.add_log("WARN")
            
            # STEP 5: New alarm start
            if (self.alarm_trigger == 1 and self.prev_trigger == 0 and
                self.active_alarm == 0 and self.alarm_timer == 0 and
                self.alarm_select > 0):
                self.active_alarm = self.alarm_select
                self.alarm_timer = self.alarm_duration
                self.alarm_message = ""
                type_map = {1: "LOW", 2: "MEDIUM", 3: "HIGH"}
                self.alarm_type = type_map.get(self.active_alarm, "NORMAL")
                self.add_log("START")
            
            # STEP 6: AlarmType update while alarm is running
            if self.active_alarm > 0 and self.alarm_timer > 0:
                type_map = {1: "LOW", 2: "MEDIUM", 3: "HIGH"}
                self.alarm_type = type_map.get(self.active_alarm, "NORMAL")
            
            # STEP 7: 30-second countdown
            if self.alarm_timer > 0:
                self.alarm_timer -= 1
                if self.alarm_timer <= 0:
                    self.alarm_timer = 0
                    self.active_alarm = 0
                    self.alarm_select = 0
                    self.alarm_trigger = 0
                    self.prev_trigger = 0
                    self.alarm_type = "NORMAL"
                    self.alarm_message = ""
                    self.add_log("END")
            
            # STEP 8: Save PrevTrigger
            self.prev_trigger = self.alarm_trigger
    
    def select_alarm(self, level):
        """User selects an alarm level"""
        with self.lock:
            if self.alarm_timer > 0:
                self.alarm_message = "Alarm are all ready active"
                return {"error": "Alarm already active"}
            
            self.alarm_select = level
            self.alarm_message = ""
            type_map = {1: "LOW", 2: "MEDIUM", 3: "HIGH"}
            self.alarm_type = type_map.get(level, "NORMAL")
            return {"success": True}
    
    def trigger_alarm(self):
        """User triggers the alarm"""
        with self.lock:
            if self.alarm_timer > 0:
                self.alarm_message = "Alarm are all ready active"
                return {"error": "Alarm already active"}
            
            if self.alarm_select == 0:
                self.alarm_message = "Please Select AlarmSelect"
                return {"error": "Please select alarm level first"}
            
            self.alarm_trigger = 1
            self.alarm_message = ""
            return {"success": True}
    
    def add_log(self, event):
        """Add entry to alarm log"""
        now = datetime.now()
        ts = now.strftime('%H:%M:%S') + f'.{now.microsecond // 1000:03d}'
        
        entry = {
            'id': time.time() * 1000 + random.random(),
            'ts': ts,
            'event': event,
            'type': self.alarm_type,
            'active': self.active_alarm,
            'timer': self.alarm_timer,
            'select': self.alarm_select,
            'trigger': self.alarm_trigger,
            'msg': self.alarm_message,
            'wl': f"{self.water_level:.3f}",
            'rd': f"{self.radar_distance:.3f}",
            'pt': f"{self.ptemp:.2f}",
            'bv': f"{self.batt_volts:.3f}"
        }
        
        self.log_entries.insert(0, entry)
        if len(self.log_entries) > self.max_logs:
            self.log_entries.pop()
    
    def get_state(self):
        """Return current system state"""
        with self.lock:
            return {
                'alarm_select': self.alarm_select,
                'alarm_trigger': self.alarm_trigger,
                'active_alarm': self.active_alarm,
                'alarm_timer': self.alarm_timer,
                'alarm_type': self.alarm_type,
                'alarm_message': self.alarm_message,
                'water_level': self.water_level,
                'radar_distance': self.radar_distance,
                'ptemp': self.ptemp,
                'batt_volts': self.batt_volts,
                'log_entries': self.log_entries
            }
    
    def start(self):
        """Start the scan loop in background thread"""
        if not self.running:
            self.running = True
            self.scan_thread = threading.Thread(target=self._run_loop, daemon=True)
            self.scan_thread.start()
    
    def _run_loop(self):
        """Background loop that runs scan_loop every 1 second"""
        while self.running:
            self.scan_loop()
            time.sleep(1)
    
    def stop(self):
        """Stop the scan loop"""
        self.running = False

# ─────────────────────────────────────────────
# Initialize the alarm system
# ─────────────────────────────────────────────
alarm_system = WaterAlarmSystem()

# ─────────────────────────────────────────────
# Flask Routes
# ─────────────────────────────────────────────

@app.route('/')
def index():
    """Serve the main HTML file"""
    return send_from_directory('static', 'index.html')

@app.route('/api/state', methods=['GET'])
def get_state():
    """Get current system state"""
    return jsonify(alarm_system.get_state())

@app.route('/api/select', methods=['POST'])
def select_alarm():
    """Select an alarm level (1=LOW, 2=MEDIUM, 3=HIGH)"""
    data = request.get_json()
    level = data.get('level', 0)
    result = alarm_system.select_alarm(level)
    return jsonify(result)

@app.route('/api/trigger', methods=['POST'])
def trigger_alarm():
    """Trigger the selected alarm"""
    result = alarm_system.trigger_alarm()
    return jsonify(result)

@app.route('/api/reset', methods=['POST'])
def reset_system():
    """Reset the alarm system"""
    with alarm_system.lock:
        alarm_system.alarm_select = 0
        alarm_system.alarm_trigger = 0
        alarm_system.active_alarm = 0
        alarm_system.alarm_timer = 0
        alarm_system.alarm_type = "NORMAL"
        alarm_system.alarm_message = ""
    return jsonify({"success": True})

@app.route('/api/logs', methods=['GET'])
def get_logs():
    """Get all alarm log entries"""
    with alarm_system.lock:
        return jsonify({"logs": alarm_system.log_entries})

@app.route('/api/clear-logs', methods=['POST'])
def clear_logs():
    """Clear all log entries"""
    with alarm_system.lock:
        alarm_system.log_entries = []
    return jsonify({"success": True})

# ─────────────────────────────────────────────
# Error Handlers
# ─────────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Server error"}), 500

# ─────────────────────────────────────────────
# Startup and Shutdown
# ─────────────────────────────────────────────

@app.before_request
def before_request():
    """Initialize system on first request"""
    if not alarm_system.running:
        alarm_system.start()

def shutdown():
    """Shutdown the system"""
    alarm_system.stop()

if __name__ == '__main__':
    try:
        print("=" * 60)
        print("Water Level Alarm System - Python Application")
        print("=" * 60)
        print("\nStarting server...")
        print("Open your browser and navigate to: http://localhost:5000")
        print("\nAPI Endpoints:")
        print("  GET  /api/state          - Get current system state")
        print("  POST /api/select         - Select alarm level")
        print("  POST /api/trigger        - Trigger alarm")
        print("  POST /api/reset          - Reset system")
        print("  GET  /api/logs           - Get alarm logs")
        print("  POST /api/clear-logs     - Clear all logs")
        print("\nPress Ctrl+C to stop the server")
        print("=" * 60 + "\n")
        
        app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        shutdown()
        print("\n\nServer stopped.")
