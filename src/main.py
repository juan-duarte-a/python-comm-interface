from comm_interface.ml_comm import CommInterface, Actions
import time

comm_test: bool = False

if comm_test:
    comm: CommInterface = CommInterface(0, True)
    comm.connect(test=True)
    duration: float = time.time()
    comm.communicate_test(5000)
    duration = time.time() - duration
    comm.send_action(Actions.END)
    comm.close_comm()
    print("Prueba de velocidad de conexión finalizada.")
    print("Duración total del test:", duration)

time_factor: float = 1 / 3 + 0.0
turning_mode: int = 1

comm: CommInterface = CommInterface(latency=0.005*time_factor, verbose_option=True)
comm.connect()

if turning_mode == 0 and not comm_test:
    while True:
        time.sleep(1)
        # for i in range(1000):
        #     comm.distance_from_center()
        #     time.sleep(1)
        print(comm.state_parameters)
        comm.send_action(Actions.RUN)
        time.sleep(3.1440718173980713 * time_factor)
        comm.send_action(Actions.TURN_RIGHT)
        print(comm.state_parameters)
        time.sleep(0.49595141410827637 * time_factor)
        comm.send_action(Actions.TURN_RIGHT)
        print(comm.state_parameters)
        time.sleep(0.5039870738983154 * time_factor)
        comm.send_action(Actions.TURN_RIGHT)
        print(comm.state_parameters)
        time.sleep(1.5199060440063477 * time_factor)
        comm.send_action(Actions.TURN_RIGHT)
        print(comm.state_parameters)
        time.sleep(0.46399545669555664 * time_factor)
        comm.send_action(Actions.TURN_RIGHT)
        print(comm.state_parameters)
        time.sleep(0.42399120330810547 * time_factor)
        comm.send_action(Actions.TURN_RIGHT)
        print(comm.state_parameters)
        time.sleep(3.8480470180511475 * time_factor)
        comm.send_action(Actions.TURN_LEFT)
        print(comm.state_parameters)
        time.sleep(0.35996508598327637 * time_factor)
        comm.send_action(Actions.TURN_LEFT)
        print(comm.state_parameters)
        time.sleep(0.32782840728759766 * time_factor)
        comm.send_action(Actions.TURN_LEFT)
        print(comm.state_parameters)
        time.sleep(0.3361194133758545 * time_factor)
        comm.send_action(Actions.TURN_LEFT)
        print(comm.state_parameters)
        time.sleep(0.3039357662200928 * time_factor)
        comm.send_action(Actions.TURN_LEFT)
        print(comm.state_parameters)
        time.sleep(0.3280210494995117 * time_factor)
        comm.send_action(Actions.TURN_LEFT)
        print(comm.state_parameters)
        time.sleep(1.8318979740142822 * time_factor)
        comm.send_action(Actions.TURN_RIGHT)
        print(comm.state_parameters)
        time.sleep(0.5199811458587646 * time_factor)
        comm.send_action(Actions.TURN_RIGHT)
        print(comm.state_parameters)
        time.sleep(0.45592355728149414 * time_factor)
        comm.send_action(Actions.TURN_RIGHT)
        print(comm.state_parameters)
        time.sleep(0.5039677619934082 * time_factor)
        comm.send_action(Actions.TURN_RIGHT)
        print(comm.state_parameters)
        time.sleep(0.5520195960998535 * time_factor)
        comm.send_action(Actions.TURN_RIGHT)
        print(comm.state_parameters)
        time.sleep(0.4078669548034668 * time_factor)
        comm.send_action(Actions.TURN_RIGHT)
        print(comm.state_parameters)
        time.sleep(3.7441139221191406 * time_factor)
        comm.send_action(Actions.TURN_RIGHT)
        print(comm.state_parameters)
        time.sleep(0.41591882705688477 * time_factor)
        comm.send_action(Actions.TURN_RIGHT)
        print(comm.state_parameters)
        time.sleep(0.7360262870788574 * time_factor)
        comm.send_action(Actions.TURN_RIGHT)
        print(comm.state_parameters)
        time.sleep(2.551975727081299 * time_factor)
        comm.send_action(Actions.TURN_RIGHT)
        print(comm.state_parameters)
        time.sleep(0.40778303146362305 * time_factor)
        comm.send_action(Actions.TURN_RIGHT)
        print(comm.state_parameters)
        time.sleep(0.4001486301422119 * time_factor)
        comm.send_action(Actions.TURN_RIGHT)
        print(comm.state_parameters)
        time.sleep(0.8719604015350342 * time_factor)
        comm.send_action(Actions.TURN_LEFT)
        print(comm.state_parameters)
        time.sleep(0.46390652656555176 * time_factor)
        comm.send_action(Actions.TURN_LEFT)
        print(comm.state_parameters)
        time.sleep(0.4559016227722168 * time_factor)
        comm.send_action(Actions.TURN_LEFT)
        print(comm.state_parameters)
        time.sleep(0.7760920524597168 * time_factor)
        comm.send_action(Actions.TURN_RIGHT)
        print(comm.state_parameters)
        time.sleep(0.4559178352355957 * time_factor)
        comm.send_action(Actions.TURN_RIGHT)
        print(comm.state_parameters)
        time.sleep(0.4240138530731201 * time_factor)
        comm.send_action(Actions.TURN_RIGHT)
        print(comm.state_parameters)
        time.sleep(1)
        # break
elif turning_mode == 1 and not comm_test:
    while True:
        while True:
            print(comm.state_parameters)    # Revisión de estado inicial.
            time.sleep(1)
            comm.send_action(Actions.GEAR_UP)
            print(comm.state_parameters)
            time.sleep(1.1354331970214844 * time_factor)
            if comm.state_parameters["done"]:
                print("Done!")
                break
            comm.send_action(Actions.GEAR_UP)
            print(comm.state_parameters)
            time.sleep(1.2402265071868896 * time_factor)
            if comm.state_parameters["done"]:
                print("Done!")
                break
            comm.send_action(Actions.GEAR_DOWN)
            print(comm.state_parameters)
            time.sleep(0.6876347064971924 * time_factor)
            if comm.state_parameters["done"]:
                print("Done!")
                break
            comm.send_action(Actions.TURN_RIGHT)
            print(comm.state_parameters)
            time.sleep(0.7918345928192139 * time_factor)
            if comm.state_parameters["done"]:
                print("Done!")
                break
            comm.send_action(Actions.CENTER_WHEEL)
            print(comm.state_parameters)
            time.sleep(0.45648622512817383 * time_factor)
            if comm.state_parameters["done"]:
                print("Done!")
                break
            comm.send_action(Actions.GEAR_UP)
            print(comm.state_parameters)
            time.sleep(0.927941083908081 * time_factor)
            if comm.state_parameters["done"]:
                print("Done!")
                break
            comm.send_action(Actions.TURN_RIGHT)
            print(comm.state_parameters)
            time.sleep(1.1115915775299072 * time_factor)
            if comm.state_parameters["done"]:
                print("Done!")
                break
            comm.send_action(Actions.CENTER_WHEEL)
            print(comm.state_parameters)
            time.sleep(0.816058874130249 * time_factor)
            if comm.state_parameters["done"]:
                print("Done!")
                break
            comm.send_action(Actions.TURN_LEFT)
            print(comm.state_parameters)
            time.sleep(0.10382843017578125 * time_factor)
            if comm.state_parameters["done"]:
                print("Done!")
                break
            comm.send_action(Actions.CENTER_WHEEL)
            print(comm.state_parameters)
            time.sleep(0.9924483299255371 * time_factor)
            if comm.state_parameters["done"]:
                print("Done!")
                break
            comm.send_action(Actions.GEAR_DOWN)
            print(comm.state_parameters)
            time.sleep(1.4159784317016602 * time_factor)
            if comm.state_parameters["done"]:
                print("Done!")
                break
            comm.send_action(Actions.TURN_LEFT)
            print(comm.state_parameters)
            time.sleep(1.607478380203247 * time_factor)
            if comm.state_parameters["done"]:
                print("Done!")
                break
            comm.send_action(Actions.CENTER_WHEEL)
            print(comm.state_parameters)
            time.sleep(1.0323925018310547 * time_factor)
            if comm.state_parameters["done"]:
                print("Done!")
                break
            comm.send_action(Actions.TURN_LEFT)
            print(comm.state_parameters)
            time.sleep(0.11151957511901855 * time_factor)
            if comm.state_parameters["done"]:
                print("Done!")
                break
            comm.send_action(Actions.CENTER_WHEEL)
            print(comm.state_parameters)
            time.sleep(1.0081548690795898 * time_factor)
            if comm.state_parameters["done"]:
                print("Done!")
                break
            comm.send_action(Actions.TURN_RIGHT)
            print(comm.state_parameters)
            time.sleep(0.8399081230163574 * time_factor)
            if comm.state_parameters["done"]:
                print("Done!")
                break
            comm.send_action(Actions.CENTER_WHEEL)
            print(comm.state_parameters)
            time.sleep(1.1281981468200684 * time_factor)
            if comm.state_parameters["done"]:
                print("Done!")
                break
            comm.send_action(Actions.TURN_RIGHT)
            print(comm.state_parameters)
            time.sleep(0.8955626487731934 * time_factor)
            if comm.state_parameters["done"]:
                print("Done!")
                break
            comm.send_action(Actions.CENTER_WHEEL)
            print(comm.state_parameters)
            time.sleep(0.5123169422149658 * time_factor)
            if comm.state_parameters["done"]:
                print("Done!")
                break
            comm.send_action(Actions.GEAR_UP)
            print(comm.state_parameters)
            time.sleep(2.520219564437866 * time_factor)
            if comm.state_parameters["done"]:
                print("Done!")
                break
            comm.send_action(Actions.TURN_RIGHT)
            print(comm.state_parameters)
            time.sleep(0.8315355777740479 * time_factor)
            if comm.state_parameters["done"]:
                print("Done!")
                break
            comm.send_action(Actions.CENTER_WHEEL)
            print(comm.state_parameters)
            time.sleep(0.38446593284606934 * time_factor)
            if comm.state_parameters["done"]:
                print("Done!")
                break
            comm.send_action(Actions.TURN_RIGHT)
            print(comm.state_parameters)
            time.sleep(0.19951438903808594 * time_factor)
            if comm.state_parameters["done"]:
                print("Done!")
                break
            comm.send_action(Actions.CENTER_WHEEL)
            print(comm.state_parameters)
            time.sleep(1.1524112224578857 * time_factor)
            if comm.state_parameters["done"]:
                print("Done!")
                break
            comm.send_action(Actions.GEAR_DOWN)
            print(comm.state_parameters)
            time.sleep(0.7200107574462891 * time_factor)
            if comm.state_parameters["done"]:
                print("Done!")
                break
            comm.send_action(Actions.TURN_RIGHT)
            print(comm.state_parameters)
            time.sleep(0.7112476825714111 * time_factor)
            if comm.state_parameters["done"]:
                print("Done!")
                break
            comm.send_action(Actions.CENTER_WHEEL)
            print(comm.state_parameters)
            time.sleep(1.384526014328003 * time_factor)
            if comm.state_parameters["done"]:
                print("Done!")
                break
            comm.send_action(Actions.TURN_LEFT)
            print(comm.state_parameters)
            time.sleep(0.72774338722229 * time_factor)
            if comm.state_parameters["done"]:
                print("Done!")
                break
            comm.send_action(Actions.CENTER_WHEEL)
            print(comm.state_parameters)
            time.sleep(1.2605715274810791 * time_factor)
            if comm.state_parameters["done"]:
                print("Done!")
                break
            comm.send_action(Actions.TURN_RIGHT)
            print(comm.state_parameters)
            time.sleep(0.7993309497833252 * time_factor)
            if comm.state_parameters["done"]:
                print("Done!")
                break
            comm.send_action(Actions.CENTER_WHEEL)
            print(comm.state_parameters)
            time.sleep(0.55 * time_factor)
