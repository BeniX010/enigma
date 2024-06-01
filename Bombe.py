import Enigma as Eng
import threading
from queue import Queue

# initial setup, we know this translates to hello
enigma = Eng.Enigma(5, 3, 2, 5, 24, 11, 2, 4, 24, 2, None)
encryptedMessage = enigma.encrypt_decrypt("gjiid")
print(encryptedMessage)

# break the code without plugboard, we are trying to brutefore it by going through all possible configurations
# Value is one more than the actual max number since range is excluding
MAX_WHEEL_VAL = 6
MAX_POSITION_VAL = 27
MAX_UKW_VAL = 4
PLUGBOARD = None

crib = "gjiid"
tasks = Queue()
# fill the queue with tasks
for wheel1 in range(1, MAX_WHEEL_VAL):
    for wheel2 in range(1, MAX_WHEEL_VAL):
        for wheel3 in range(1, MAX_WHEEL_VAL):
            for position1 in range(1, MAX_POSITION_VAL):
                for position2 in range(1, MAX_POSITION_VAL):
                    for position3 in range(1, MAX_POSITION_VAL):
                        for ringPosition1 in range(1, MAX_POSITION_VAL):
                            for ringPosition2 in range(1, MAX_POSITION_VAL):
                                for ringPosition3 in range(1, MAX_POSITION_VAL):
                                    for ukw in range(1, MAX_UKW_VAL):
                                        tasks.put(
                                            [wheel1, wheel2, position1, position2, ringPosition1, ringPosition2, ukw])


# tasks of the thread
def printIt():
    while not tasks.empty():
        print(tasks.get())
        tasks.task_done()


for _ in range(10):
    threading.Thread(target=printIt).start()

tasks.join()
