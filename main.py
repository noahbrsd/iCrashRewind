import tkinter as tk
from telemetry import TelemetryMonitor
from replay import ReplayController
from gui import IncidentGUI
import threading
import time

def run_monitor(monitor, gui, replay_ctrl):
    while monitor.is_connected():
        incidents = monitor.get_new_incidents()
        for inc in incidents:
            gui.add_incident(inc)
        time.sleep(0.3)

def main():
    try:
        monitor = TelemetryMonitor()
    except RuntimeError as e:
        print(f"Erreur: {e}")
        return

    replay_ctrl = ReplayController(monitor.get_ir())

    def on_replay(car_idx, timestamp_str):
        minutes, seconds = map(float, timestamp_str.split(':'))
        session_time = minutes * 60 + seconds
        session_num = monitor.get_ir()['SessionNum']
        replay_ctrl.rewind_to(session_num, session_time, car_idx)

    root = tk.Tk()
    root.title("iCrashRewind - Incident Tracker")
    gui = IncidentGUI(root, on_replay)

    thread = threading.Thread(target=run_monitor, args=(monitor, gui, replay_ctrl), daemon=True)
    thread.start()
    root.mainloop()

if __name__ == '__main__':
    main()
