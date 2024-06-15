from sagEnigma import Enigma
import threading
from queue import Queue


# implementation for Enigma 1 and without a plugboard as of now
class Bombe:
    def __init__(self, max_wheel_val, max_position_val, max_reflector_val, crib, encrypted_word):
        self.max_wheel_val = max_wheel_val
        self.max_position_val = max_position_val
        self.max_reflector_val = max_reflector_val
        self.crib = crib
        self.encrypted_word = encrypted_word
        self.tasks = Queue()
        self.fill_tasks()

    def fill_tasks(self):
        for wheel1 in range(1, self.max_wheel_val):
            for wheel2 in range(1, self.max_wheel_val):
                for wheel3 in range(1, self.max_wheel_val):
                    for position1 in range(1, self.max_position_val):
                        for position2 in range(1, self.max_position_val):
                            for position3 in range(1, self.max_position_val):
                                for offset1 in range(1, self.max_position_val):
                                    for offset2 in range(1, self.max_position_val):
                                        for offset3 in range(1, self.max_position_val):
                                            for reflector in range(1, self.max_reflector_val):
                                                self.tasks.put(
                                                    [wheel1, wheel2, wheel3, position1, position2, position3,
                                                     offset1, offset2, offset3, reflector])

    def get_se_germans(self):
        try:
            while not self.tasks.empty():
                enigma_config = self.tasks.get()
                wheel_1, wheel_2, wheel_3, position_1, position_2, position_3, offset1, offset2, offset3, reflector = enigma_config
                threaded_enigma = Enigma.create([wheel_1, wheel_2, wheel_3], [position_1, position_2, position_3],
                                                [offset1, offset2, offset3], reflector)
                decrypted_text = threaded_enigma.en_de_crypt(self.encrypted_word)
                if decrypted_text == self.crib:
                    print(f"Decrypted Message: {decrypted_text}")
                    print(f"One possible setting of the Day: {enigma_config} go get those Fritzes!\n")
                self.tasks.task_done()
        except Exception as e:
            print(e)

    def crack(self):
        for _ in range(16):
            threading.Thread(target=self.get_se_germans).start()
        self.tasks.join()


# The correct max_wheel_val = 6, max_position_val = 27, max_ukw_val = 4
# I lowered them for testing purposes, feel free to create a new bombe with the actual values
bomber = Bombe(3, 3, 3, "HALLO", "fuytv")
bomber.crack()
