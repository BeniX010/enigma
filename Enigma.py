class Rotor:
    def __init__(self,permutation,notch):
        self.__permutation = permutation
        self.__notch = notch
        self.__ringPosition = -1
        self.__position = -1
    
    def getPermutation(self):
        return self.__permutation

    def getNotch(self):
        return self.__notch
    
    def getPosition(self):
        return self.__position
    
    def getRingPosition(self):
        return self.__ringPosition
    
    def setRingPosition(self, input):
        ringPosition = int(input)
        if ringPosition < 1 or ringPosition > 26:
            raise ValueError("Invalid Input! Position can only be set from 1 to 26!")
        self.__ringPosition = ringPosition-1
    
    def setPosition(self,input):
        position = int(input)
        if position < 1 or position > 26:
            raise ValueError("Invalid Input! Position can only be set from 1 to 26!")
        self.__position = position-1
    
    def step(self):
        self.__position = (self.__position + 1) % 26

class Enigma:
    wheels = [Rotor([4,10,12,5,11,6,3,16,21,25,13,19,14,22,24,7,23,20,18,15,0,8,1,17,2,9],16),
              Rotor([0,9,3,10,18,8,17,20,23,1,11,7,22,19,12,2,16,6,25,13,15,24,5,21,14,4],4),
              Rotor([1,3,5,7,9,11,2,15,17,19,23,21,25,13,24,4,8,22,6,0,10,12,20,18,16,14],21),
              Rotor([4,18,14,21,15,25,9,0,24,16,20,8,17,7,23,11,13,5,19,6,10,3,2,12,22,1],9),
              Rotor([21,25,1,17,6,8,19,24,20,15,18,3,13,7,11,23,0,22,12,9,16,14,5,4,2,10],25)]
    
    ukws = [[4,9,12,25,0,11,24,23,21,1,22,5,2,17,16,20,14,13,19,18,15,8,10,7,6,3],
            [24,17,20,7,16,18,11,3,15,23,13,6,14,10,12,8,4,1,5,25,2,22,21,9,0,19],
            [5,21,15,9,8,0,14,24,4,3,17,25,23,22,6,2,19,10,20,16,18,1,13,12,7,11]]

    def __init__(self,wheel1: int,wheel2: int,wheel3: int,position1: int,position2: int,position3: int,ringPosition1: int,ringPosition2: int,ringPosition3: int,ukw: int,plugboard: list):
        self.__wheel1 = self.wheels[wheel1-1]
        self.__wheel2 = self.wheels[wheel2-1]
        self.__wheel3 = self.wheels[wheel3-1]
        self.__wheel1.setPosition(position1)
        self.__wheel2.setPosition(position2)
        self.__wheel3.setPosition(position3)
        self.__wheel1.setRingPosition(ringPosition1)
        self.__wheel2.setRingPosition(ringPosition2)
        self.__wheel3.setRingPosition(ringPosition3)
        self.__ukw = self.ukws[ukw-1]
        self.__plugboard = plugboard
    
    def encrypt_decrypt(self,argument):
        message = str(argument)
        message = message.upper()
        result = ""
        for letter in message:
            letterValue = ord(letter) - 65

            if letterValue < 0 or letterValue > 25:
                raise ValueError("Invalid Letter! The Input can only contain the Letter A-Z!")

            if self.__wheel1.getNotch() == self.__wheel1.getPosition():

                if self.__wheel2.getNotch == self.__wheel2.getPosition():
                    self.__wheel3.step()

                self.__wheel2.step()

            self.__wheel1.step()

            if  self.__plugboard is not None:
                letterValue = self.__plugboard[letterValue]
            
            positionChange1 = (self.__wheel1.getPosition()-self.__wheel1.getRingPosition()) % 26
            letterValue = (letterValue+positionChange1) % 26
            letterValue = (self.__wheel1.getPermutation()[letterValue]-positionChange1) % 26
            
            positionChange2 = (self.__wheel2.getPosition()-self.__wheel2.getRingPosition()) % 26
            letterValue = (letterValue+positionChange2) % 26
            letterValue = (self.__wheel2.getPermutation()[letterValue]-positionChange2) % 26

            positionChange3 = (self.__wheel3.getPosition()-self.__wheel3.getRingPosition()) % 26
            letterValue = (letterValue+positionChange3) % 26
            letterValue = (self.__wheel3.getPermutation()[letterValue]-positionChange3) % 26

            letterValue = self.__ukw[letterValue]
            
            letterValue = (letterValue+positionChange3) % 26
            letterValue = (self.__wheel3.getPermutation().index(letterValue) - positionChange3) % 26

            letterValue = (letterValue+positionChange2) % 26
            letterValue = (self.__wheel2.getPermutation().index(letterValue) - positionChange2) % 26

            letterValue = (letterValue+positionChange1) % 26   
            letterValue = (self.__wheel1.getPermutation().index(letterValue) - positionChange1) % 26

            if  self.__plugboard is not None:
                letterValue = self.__plugboard[letterValue]
            
            #print(chr(letterValue+65))
            result += chr(letterValue+65)
        return result


enigma = Enigma(5,3,2,5,24,11,2,4,24,2,None)
encryptedMessage = enigma.encrypt_decrypt("gjiid")
print(encryptedMessage)