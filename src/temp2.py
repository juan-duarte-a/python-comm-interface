from pynput.keyboard import Key, Listener
from comm_interface.ml_comm import CommInterface, Actions
import time


class MLRacingKeyRegister:

    comm = CommInterface()
    comm.connect()
    time_start: float = 0
    pressed: bool = False

    def on_press(self, key):
        if not self.pressed:
            if key == Key.up:
                print(f"time.sleep({time.time() - self.time_start} * time_factor)")
                print("comm.send_action(Actions.GEAR_UP)")
                self.time_start = time.time()
                self.comm.send_action(Actions.GEAR_UP)
            elif key == Key.down:
                print(f"time.sleep({time.time() - self.time_start} * time_factor)")
                print("comm.send_action(Actions.GEAR_DOWN)")
                self.time_start = time.time()
                self.comm.send_action(Actions.GEAR_DOWN)
            elif key == Key.left:
                print(f"time.sleep({time.time() - self.time_start} * time_factor)")
                print("comm.send_action(Actions.TURN_LEFT)")
                self.time_start = time.time()
                self.comm.send_action(Actions.TURN_LEFT)
            elif key == Key.right:
                print(f"time.sleep({time.time() - self.time_start} * time_factor)")
                print("comm.send_action(Actions.TURN_RIGHT)")
                self.time_start = time.time()
                self.comm.send_action(Actions.TURN_RIGHT)
            self.pressed = True

    def on_release(self, key):
        if key == Key.esc:
            # Stop listener
            self.comm.close_comm()
            return False
        elif key == Key.left:
            print(f"time.sleep({time.time() - self.time_start} * time_factor)")
            print("comm.send_action(Actions.CENTER_WHEEL)")
            self.time_start = time.time()
            self.comm.send_action(Actions.CENTER_WHEEL)
        elif key == Key.right:
            print(f"time.sleep({time.time() - self.time_start} * time_factor)")
            print("comm.send_action(Actions.CENTER_WHEEL)")
            self.time_start = time.time()
            self.comm.send_action(Actions.CENTER_WHEEL)
        self.pressed = False

    # Collect events until released
    def collect_events(self):
        with Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()


ml_key_register = MLRacingKeyRegister()
ml_key_register.collect_events()
