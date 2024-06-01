import Enigma as Eng

enigma = Eng.Enigma(5,3,2,5,24,11,2,4,24,2,None)
encryptedMessage = enigma.encrypt_decrypt("gjiid")
print(encryptedMessage)