from pynput.keyboard import Key, Listener
from comm_interface.ml_comm import CommInterface, Actions
import time


class MLRacingKeyRegister:

    comm = CommInterface()
    comm.connect()
    time_start: float = 0

    def on_press(self, key):
        pass

    def on_release(self, key):
        if key == Key.esc:
            # Stop listener
            self.comm.close_comm()
            return False
        elif key == Key.up:
            if self.time_start == 0:
                self.time_start = time.time()
            print(f"time.sleep({time.time() - self.time_start})")
            print("comm.send_action(Actions.RUN)")
            self.comm.send_action(Actions.RUN)
        elif key == Key.down:
            print(f"time.sleep({time.time() - self.time_start})")
            print("comm.send_action(Actions.STOP)")
            self.time_start = time.time()
            self.comm.send_action(Actions.STOP)
        elif key == Key.left:
            print(f"time.sleep({time.time() - self.time_start})")
            print("comm.send_action(Actions.TURN_LEFT)")
            self.time_start = time.time()
            self.comm.send_action(Actions.TURN_LEFT)
        elif key == Key.right:
            print(f"time.sleep({time.time() - self.time_start})")
            print("comm.send_action(Actions.TURN_RIGHT)")
            self.time_start = time.time()
            self.comm.send_action(Actions.TURN_RIGHT)

    # Collect events until released
    def collect_events(self):
        with Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()


ml_key_register = MLRacingKeyRegister()
ml_key_register.collect_events()
