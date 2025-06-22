import tkinter as tk
from tkinter import ttk
import irsdk
import time
import threading

class TelemetryViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("iCrashRewind - Moniteur vitesse/surface (réel)")

        self.tree = ttk.Treeview(root, columns=("car", "name", "speed", "surface"), show='headings')
        self.tree.heading("car", text="CarIdx")
        self.tree.heading("name", text="Driver")
        self.tree.heading("speed", text="Vitesse (km/h)")
        self.tree.heading("surface", text="Surface")

        self.tree.pack(fill='both', expand=True)
        self.ir = irsdk.IRSDK()
        self.ir.startup()
        self.running = True

        self.player_idx = None
        self.drivers = []

        self.update_thread = threading.Thread(target=self.update_loop, daemon=True)
        self.update_thread.start()

    def update_loop(self):
        while self.running and self.ir.is_connected:
            try:
                if self.player_idx is None:
                    self.player_idx = self.ir['PlayerCarIdx']
                    self.drivers = self.ir['DriverInfo']['Drivers']

                surfaces = self.ir['CarIdxTrackSurface']
                vel_x = self.ir['CarIdxLocalVelX']
                vel_y = self.ir['CarIdxLocalVelY']
                vel_z = self.ir['CarIdxLocalVelZ']

                self.tree.delete(*self.tree.get_children())

                for driver in self.drivers:
                    idx = driver['CarIdx']
                    if idx == self.player_idx:
                        continue
                    name = driver['UserName']

                    try:
                        vx = vel_x[idx]
                        vy = vel_y[idx]
                        vz = vel_z[idx]
                        speed_mps = (vx ** 2 + vy ** 2 + vz ** 2) ** 0.5
                        speed_kmh = speed_mps * 3.6
                    except:
                        speed_kmh = 0

                    if speed_kmh > 400 or speed_kmh < 0:
                        speed_kmh = 0

                    surface = surfaces[idx] if idx < len(surfaces) else -1
                    self.tree.insert('', 'end', values=(
                        idx,
                        name,
                        f"{speed_kmh:.1f}",
                        surface
                    ))
            except Exception as e:
                print("Erreur:", e)

            time.sleep(0.5)

    def stop(self):
        self.running = False

if __name__ == "__main__":
    root = tk.Tk()
    app = TelemetryViewer(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (app.stop(), root.destroy()))
    root.mainloop()
