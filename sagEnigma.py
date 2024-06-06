import sys

r"""
Enigma

<Paragraph description>

EXAMPLES::

<Lots and lots of examples>

AUTHORS:

- YOUR NAME (2024-06-06): initial version

"""


# ****************************************************************************
#       Copyright (C) 2024 YOUR NAME <your email>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  https://www.gnu.org/licenses/
# ****************************************************************************

class Rotor:
    r"""
    An object representing a rotor of the enigma.

    INPUT:

    - ``permutation`` -- list[integer]; the permutation of the letters for this rotor
    - ``notch`` -- integer; sets the required amount of steps before rotating
    - ``initial_position`` -- integer; sets the position at which the rotor will start
    - ``offset`` -- integer; also known as ring position

    """

    def __init__(self, permutation: list[int], notch: int, initial_position: int, offset: int):
        self._position = initial_position - 1
        self._notch = notch
        self._permutation = permutation
        self._offset = offset - 1

    def _process_letter_forward(self, letter: str, rotate: bool) -> (str, bool):
        r"""
        Private function which allows a rotor to process a single letter when moving through the enigma,
        towards the reflector

        INPUT:

        - ``letter`` -- string; the letter to be processed
        - ``rotate`` -- boolean; indicates whether the next rotor should rotate

        OUTPUT: a tuple containing the processed letter and whether the rotor rotated or not
        """
        letter_value = ord(letter) - 65
        next_rotate: bool = False

        if letter_value < 0 or letter_value > 25:
            raise ValueError("Invalid letter: Input can only contain letters a - z.")

        if rotate:
            self._position = (self._position + 1) % 26

        if self._position == self._notch:
            next_rotate: bool = True

        current_offset = (self._position - self._offset) % 26
        print(f'offset: {current_offset}')
        letter_value = (letter_value + current_offset) % 26
        letter_value = (self._permutation[letter_value] - current_offset) % 26

        return chr(letter_value + 65), next_rotate

    def _process_letter_backward(self, letter: str) -> str:
        r"""
        Private function which allows a rotor to process a single letter when moving through the enigma,
        after passing the reflector

        INPUT:

        - ``letter`` -- string; letter to be processed

        OUTPUT: processed letter
        """
        letter_value = ord(letter) - 65

        if letter_value < 0 or letter_value > 25:
            raise ValueError("Invalid letter: Input can only contain letters a - z.")

        current_offset = (self._position - self._offset) % 26
        print(f'offset: {current_offset}')
        letter_value = (letter_value + current_offset) % 26
        letter_value = (self._permutation.index(letter_value) - current_offset) % 26

        return chr(letter_value + 65)


class Reflector:
    r"""
    A special rotor that misses the key thing of one: the rotating. After going through the rotors in one direction,
    the electric signal gets reflected at the Reflector after which it passes the rotors again.
    In short: the reflector is a static permutation.

    INPUT:

    - ``permutation`` -- list[integer]; permutation to be used in the reflector which must have a length of 26

    EXAMPLES:

    Creating own Reflector ::
        sage: R =
            Reflector([24, 17, 20, 7, 16, 18, 11, 3, 15, 23, 13, 6, 14, 10, 12, 8, 4, 1, 5, 25, 2, 22, 21, 9, 0, 19])

    Using it in the enigma ::
        sage: E = Enigma([A, B, C], R)
    """

    def __init__(self, permutation: list[int]):
        if len(permutation) != 26:
            raise ValueError("Permutation must have a length of 26")
        self._permutation = permutation

    def _process_letter(self, letter: str) -> str:
        r"""
        Private function to permutate a given letter

        INPUT:

        - ``letter`` -- string; letter to be processed

        OUTPUT: processed letter
        """
        letter_value = ord(letter) - 65

        if letter_value < 0 or letter_value > 25:
            raise ValueError("Invalid letter: Input can only contain letters a - z.")

        letter_value = self._permutation[letter_value]

        return chr(letter_value + 65)


class Enigma:
    r"""
    An object representing the Enigma. Purpose is to encrypt and decrypt texts.

    INPUT:

    - ``rotors`` -- list[Rotor]; a list of rotors to be used in this enigma

    """

    def __init__(self, rotors: list[Rotor], reflector: Reflector):
        self.rotors = rotors
        self.reflector = reflector

    def en_de_crypt(self, text):
        r"""
        Encrypts or decrypts a text.

        INPUT:

        - ``text`` -- string; The text to be processed by this enigma

        OUTPUT: the encrypted or decrypted text

        EXAMPLES:

        TESTS::

        """
        result = ""
        message = str(text).upper()

        for letter in message:
            predecessor_tuple: (str, bool) = letter, True

            for rotor in self.rotors:
                print(predecessor_tuple)
                predecessor_tuple = rotor._process_letter_forward(predecessor_tuple[0], predecessor_tuple[1])

            print(predecessor_tuple)
            predecessor_tuple = reflector._process_letter(predecessor_tuple[0]), False

            for rotor in reversed(self.rotors):
                print(predecessor_tuple)
                predecessor_tuple = rotor._process_letter_backward(predecessor_tuple[0]), False

            print(predecessor_tuple)
            print("-----------------")
            result += predecessor_tuple[0]

        return result


class EnigmaFactory:
    r"""
    Factory for creating (semi-) realistic Enigmas. Choose from real reflectors and rotors.

    EXAMPLES:

    TESTS::

    """
    def __init__(self):
        self._wheels = [[4, 10, 12, 5, 11, 6, 3, 16, 21, 25, 13, 19, 14, 22, 24, 7, 23, 20, 18, 15, 0, 8, 1, 17, 2, 9],
                        [0, 9, 3, 10, 18, 8, 17, 20, 23, 1, 11, 7, 22, 19, 12, 2, 16, 6, 25, 13, 15, 24, 5, 21, 14, 4],
                        [1, 3, 5, 7, 9, 11, 2, 15, 17, 19, 23, 21, 25, 13, 24, 4, 8, 22, 6, 0, 10, 12, 20, 18, 16, 14],
                        [4, 18, 14, 21, 15, 25, 9, 0, 24, 16, 20, 8, 17, 7, 23, 11, 13, 5, 19, 6, 10, 3, 2, 12, 22, 1],
                        [21, 25, 1, 17, 6, 8, 19, 24, 20, 15, 18, 3, 13, 7, 11, 23, 0, 22, 12, 9, 16, 14, 5, 4, 2, 10]]
        self._notches = [16, 4, 21, 9, 25]
        self._reflectors = [
            [4, 9, 12, 25, 0, 11, 24, 23, 21, 1, 22, 5, 2, 17, 16, 20, 14, 13, 19, 18, 15, 8, 10, 7, 6, 3],
            [24, 17, 20, 7, 16, 18, 11, 3, 15, 23, 13, 6, 14, 10, 12, 8, 4, 1, 5, 25, 2, 22, 21, 9, 0, 19],
            [5, 21, 15, 9, 8, 0, 14, 24, 4, 3, 17, 25, 23, 22, 6, 2, 19, 10, 20, 16, 18, 1, 13, 12, 7, 11]]

    def create(self, rotors: list[(int, int, int)], reflector: int) -> Enigma:
        r"""
        Function to create an Enigma with predefined rotors and reflectors.

        INPUT:

        - ``rotors`` -- list[(integer, integer, integer)]; List of integer tuples with the first integer indicating
          which rotor to use (I to V), the second integer sets the initial position of the rotor and the third integer
          indicating the ring position

        - ``reflector`` -- integer; Sets on of the three (3) predefined reflectors

        OUTPUT: Enigma with predefined settings

        EXAMPLES:

        This example shows the creation of a realistic enigma ::

            sage: F = EnigmaFactory()
            sage: A = F.create([(5, 5, 2), (3, 24, 4), (2, 11, 24)], 2)

        Nobody will stop you from having more than necessary rotors ::
            sage: F = EnigmaFactory()
            sage: B = F.create([(1, 2, 3), (2, 3, 4), (3, 4, 5), (4, 5, 6), (5, 6, 7), (3, 3, 3), (1, 1, 1)], 1)

        TESTS::

        """
        if len(rotors) < 0:
            raise ValueError("Enigma must have a rotor")

        if reflector - 1 < 0 or reflector - 1 > 2:
            raise ValueError("There are only 3 predefined reflectors.")
        reflector_ = Reflector(self._reflectors[reflector])

        rotor_list: list[Rotor] = []
        for r in rotors:
            if r[0] - 1 < 0 or r[0] - 1 > 4:
                raise ValueError("There are only 5 predefined rotors.")

            rotor_list.append(Rotor(self._wheels[r[0] - 1], self._notches[r[0] - 1], r[1], r[2]))

        return Enigma(rotor_list, reflector_)


r1 = Rotor([21, 25, 1, 17, 6, 8, 19, 24, 20, 15, 18, 3, 13, 7, 11, 23, 0, 22, 12, 9, 16, 14, 5, 4, 2, 10], 25, 5, 2)
r2 = Rotor([1, 3, 5, 7, 9, 11, 2, 15, 17, 19, 23, 21, 25, 13, 24, 4, 8, 22, 6, 0, 10, 12, 20, 18, 16, 14], 21, 24, 4)
r3 = Rotor([0, 9, 3, 10, 18, 8, 17, 20, 23, 1, 11, 7, 22, 19, 12, 2, 16, 6, 25, 13, 15, 24, 5, 21, 14, 4], 4, 11, 24)
reflector = Reflector([24, 17, 20, 7, 16, 18, 11, 3, 15, 23, 13, 6, 14, 10, 12, 8, 4, 1, 5, 25, 2, 22, 21, 9, 0, 19])
enigma = Enigma([r1, r2, r3], reflector)
print(enigma.en_de_crypt(sys.argv[1]))
