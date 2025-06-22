import irsdk

class TelemetryMonitor:
    def __init__(self):
        self.ir = irsdk.IRSDK()
        self.ir.startup()
        self.last_incident_counts = {}
        self.player_car_idx = self.ir['PlayerCarIdx']

    def is_connected(self):
        return self.ir.is_connected

    def get_new_incidents(self):
        incidents = []
        for car_idx in range(64):  # max 64 cars in ir race
            if car_idx == self.player_car_idx:
                continue
            try:
                current_count = self.ir[f'CarIdxIncidentCount'][car_idx]
                last_count = self.last_incident_counts.get(car_idx, 0)
                if current_count > last_count:
                    delta = current_count - last_count
                    time_stamp = self.ir['SessionTime']
                    name = self.ir['DriverInfo']['Drivers'][car_idx]['UserName']
                    type_ = self.get_incident_type(delta)
                    incidents.append({
                        'car_idx': car_idx,
                        'driver_name': name,
                        'time': time_stamp,
                        'type': type_
                    })
                    self.last_incident_counts[car_idx] = current_count
            except:
                continue
        return incidents

    def get_incident_type(self, delta):
        if delta == 1:
            return 'Off-track'
        elif delta == 2:
            return 'Crash'
        elif delta >= 4:
            return 'Crash w/ car'
        return 'Unknown'
