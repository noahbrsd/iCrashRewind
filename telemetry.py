import irsdk
import time

class TelemetryMonitor:
    def __init__(self):
        self.ir = irsdk.IRSDK()
        self.ir.startup()
        self.last_track_surfaces = {}
        self.last_speed = {}
        self.player_idx = self.ir['PlayerCarIdx']
        self.drivers = self.ir['DriverInfo']['Drivers']

    def is_connected(self):
        return self.ir.is_connected

    def get_new_incidents(self):
        incidents = []
        try:
            surfaces = self.ir['CarIdxTrackSurface']
            speeds = self.ir['CarIdxEstTime'] if 'CarIdxEstTime' in self.ir.var_headers_names else None
            session_time = self.ir['SessionTime']

            for driver in self.drivers:
                idx = driver['CarIdx']
                if idx == self.player_idx:
                    continue  # ignore self
                name = driver['UserName']

                prev_surface = self.last_track_surfaces.get(idx, 3)  # default: on_track
                prev_speed = self.last_speed.get(idx, 100)  # assume moving
                curr_surface = surfaces[idx]

                # speed_mps = self.ir['CarIdxRPM'][idx] / 10 if 'CarIdxRPM' in self.ir.var_headers_names else 3000
                # kmh = speed_mps * 3.6

                try:
                    vel_x = self.ir['CarIdxLocalVelX'][idx]
                    vel_y = self.ir['CarIdxLocalVelY'][idx]
                    vel_z = self.ir['CarIdxLocalVelZ'][idx]
                    speed_mps = (vel_x ** 2 + vel_y ** 2 + vel_z ** 2) ** 0.5
                except:
                    speed_mps = 30  # fallback

                kmh = speed_mps * 3.6

                self.last_track_surfaces[idx] = curr_surface
                self.last_speed[idx] = kmh

                # OFFTRACK
                if prev_surface == 3 and curr_surface == 0:
                    incidents.append({
                        'car_idx': idx,
                        'driver_name': name,
                        'time': session_time,
                        'type': 'Off-track'
                    })

                # CRASH (vitesse très basse + offtrack)
                if curr_surface != -1 and kmh < 30:
                    incidents.append({
                        'car_idx': idx,
                        'driver_name': name,
                        'time': session_time,
                        'type': 'Crash'
                    })
        except:
            pass

        return incidents

    def get_ir(self):
        return self.ir
