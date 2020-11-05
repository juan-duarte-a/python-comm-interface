from comm_interface.ml_comm import CommInterface, Actions

comm: CommInterface = CommInterface()
comm.connect()
comm.communicate_test(100)
comm.send_action(Actions.END)
comm.close_comm()
print("Finished!")
