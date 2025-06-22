import irsdk
import time

class ReplayController:
    def __init__(self, ir):
        self.ir = ir
        self.last_call_time = 0

    def rewind_to(self, session_num, session_time_seconds, car_idx):
        now = time.time()
        if now - self.last_call_time < 2:
            return
        self.last_call_time = now

        ms = int(max(session_time_seconds - 5, 0) * 1000)
        self.ir.replay_set_play_speed(0)
        time.sleep(0.1)
        self.ir.replay_search_session_time(session_num, ms)
        time.sleep(0.1)
        self.ir.cam_switch_pos(car_idx,0 )  # switch to the car
        self.ir.cam_set_state(irsdk.CameraState.cam_tool_active)
        self.ir.replay_set_play_speed(1)