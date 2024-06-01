import Enigma as Eng
import threading
from queue import Queue


# initial setup, we know this translates to hello
enigma = Eng.Enigma(5, 3, 2, 5, 2, 2, 2, 4, 4, 2, None)
enigma2 = Eng.Enigma(1, 2, 2, 1, 2, 1, 1, 2, 2, 2,None)
encryptedMessage = enigma2.encrypt_decrypt("fuytv")
print(encryptedMessage)

# break the code without plugboard, we are trying to brutefore it by going through all possible configurations
# Value is one more than the actual max number since range is excluding
# for testing purposes I lowered the numbers, otherwise it will take ages to execute
MAX_WHEEL_VAL = 3#6
MAX_POSITION_VAL = 3 #27
MAX_UKW_VAL = 3#4
PLUGBOARD = None
found = False
# found_lock = threading.Lock()
found_config = threading.Event()
crib = "HALLO"
encrypted_word = "fuytv"
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
                                            [wheel1, wheel2,wheel3, position1, position2,position3, ringPosition1, ringPosition2, ringPosition3, ukw])


# tasks of the thread
def get_se_germans():
    try:
        while not tasks.empty():
            enigma_config = tasks.get()
            wheel_1, wheel_2, wheel_3, position_1, position_2,position_3, ring_position_1, ring_position_2, ring_position_3, ukw_in = enigma_config
            threaded_enigma = Eng.Enigma(wheel_1, wheel_2, wheel_3, position_1, position_2,position_3, ring_position_1, ring_position_2, ring_position_3, ukw_in, PLUGBOARD)
            decrypted_text = threaded_enigma.encrypt_decrypt(encrypted_word)
            if decrypted_text == crib:
                print(f"Decrypted Message: {decrypted_text}")
                print(f"One possible setting of the Day: {enigma_config} go get those Fritzes!")
            tasks.task_done()
    except Exception as e:
        print(e)


for _ in range(16):
    threading.Thread(target=get_se_germans).start()

tasks.join()
