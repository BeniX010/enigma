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
    An object representing a rotor of the enigma. The rotor of the enigma 
    permutates each letter that passes through it. It rotates after the 
    preceeding wheel has rotated a fixed amount of times.

    INPUT:

    - ``permutation`` -- list[integer]; the permutation of the letters for this 
      rotor, must have a length of 26
    - ``notch`` -- integer; sets the position at which the rotor will cause the 
      following rotor to rotate, must be a integer between 0 and 25
    - ``initial_position`` -- integer; sets the position at which the rotor 
      will start, must be a integer between 1 and 26
    - ``offset`` -- integer; also known as ring position

    EXAMPLES::

        sage: r = Rotor([21, 25, 1, 17, 6, 8, 19, 24, 20, 15, 18, 3, 13, 7, 11, 
        ....: 23, 0, 22, 12, 9, 16, 14, 5, 4, 2, 10], 25, 5, 2)
        sage: r
        Rotor with current position 5, permutation [21, 25, 1, 17, 6, 8, 19, 
        24, 20, 15, 18, 3, 13, 7, 11, 23, 0, 22, 12, 9, 16, 14, 5, 4, 2, 10], 
        initial position 5, offset 2 and notch 25
        

    The permutation used in the rotor needs to have a length of exactly 26::

        sage: r = Rotor([21, 25, 1, 17, 6, 8, 19, 24, 20, 15, 18, 3, 13, 7, 11, 
        ....: 23, 0, 22, 12, 9, 16, 14)
        Traceback (most recent call last):
        ...
        ValueError: Permutation must have a length of 26
        sage: r = Rotor([21, 25, 1, 17, 6, 8, 19, 24, 20, 15, 18, 3, 13, 7, 11, 
        ....: 23, 0, 22, 12, 9, 16, 14, 12, 11, 10, 9, 8, 7)
        Traceback (most recent call last):
        ...
        ValueError: Permutation must have a length of 26
        
    The notch must be a integer between 0 and 25::

        sage: r = Rotor([21, 25, 1, 17, 6, 8, 19, 24, 20, 15, 18, 3, 13, 7, 11, 
        sage: 23, 0, 22, 12, 9, 16, 14, 5, 4, 2, 10], 50, 5, 2)
        Traceback (most recent call last):
        ...
        ValueError: Notch must be a integer between 0 and 25
        sage: r = Rotor([21, 25, 1, 17, 6, 8, 19, 24, 20, 15, 18, 3, 13, 7, 11, 
        ....: 23, 0, 22, 12, 9, 16, 14, 5, 4, 2, 10], -1, 5, 2)
        Traceback (most recent call last):
        ...
        ValueError: Notch must be a integer between 0 25

    The initial position of the rotor must be a integer between 1 and 26::

        sage: r = Rotor([21, 25, 1, 17, 6, 8, 19, 24, 20, 15, 18, 3, 13, 7, 11, 
        ....: 23, 0, 22, 12, 9, 16, 14, 5, 4, 2, 10], 25, 0, 2)
        Traceback (most recen call last):
        ...
        ValueError: Initial position must be a integer between 1 and 26
        sage: r = Rotor([21, 25, 1, 17, 6, 8, 19, 24, 20, 15, 18, 3, 13, 7, 11, 
        ....: 23, 0, 22, 12, 9, 16, 14, 5, 4, 2, 10], 25, 30, 2)
        Traceback (most recen call last):
        ...
        ValueError: Initial position must be a integer between 1 and 26

    .. NOTE::

        Every value inside the permutation must be between 0 and 25
    """

    def __init__(self, permutation: list[int], notch: int, initial_position: int, offset: int):
        r"""
        Initializes the ``Rotor`` class. See the class :class:`Rotor` for full 
        documentation on the input of this initialization method.
        """

        if len(permutation) != 26:
            raise ValueError("Permutation must have a length of 26")
        if notch > 26 or notch < 1:
            raise ValueError("Notch must be a integer between 0 and 25")
        if initial_position > 25 or initial_position < 0:
            raise ValueError("Initial position must be a integer between 1 and "
                             "26")
        self._position = initial_position - 1
        self._initial_position = initial_position - 1
        self._notch = notch
        self._permutation = permutation
        self._offset = offset - 1

    def _process_letter_forward(self, letter: str, rotate: bool) -> tuple[str, bool]:
        r"""
        Private function which allows a rotor to process a single letter when 
        moving towards the reflector of the enigma

        INPUT:

        - ``letter`` -- string; the letter to be processed
        - ``rotate`` -- boolean; indicates whether the rotor should rotate

        OUTPUT: a tuple of

        - the processed `letter`
        - a boolean indicating whether the next rotor should rotate, this 
          happens when the current `position` of the rotor equals the `notch`

        EXAMPLES::

            sage: r = Rotor([21, 25, 1, 17, 6, 8, 19, 24, 20, 15, 18, 3, 13, 7, 
            ....: 11, 23, 0, 22, 12, 9, 16, 14, 5, 4, 2, 10], 25, 5, 2)
            sage: r._process_letter_forward("B", False)
            ('D', False)

        Can only process letters A - Z::

            sage: r._process_letter_forward("1", False)
            Traceback (most recent call last):
            ...
            ValueError: Invalid letter: Input can only contain letters A - Z

        Letters need to be uppercase::

            sage: r._process_letter_forward("a", False)
            Traceback (most recent call last):
            ...
            ValueError: Invalid letter: Input can only contain letters A - Z
        """

        letter_value = ord(letter) - 65
        next_rotate: bool = False

        if letter_value < 0 or letter_value > 25:
            raise ValueError(
                "Invalid letter: Input can only contain letters A - Z")

        if rotate:
            self._position = (self._position + 1) % 26

        if self._position == self._notch:
            next_rotate: bool = True

        current_offset = (self._position - self._offset) % 26
        letter_value = (letter_value + current_offset) % 26
        letter_value = (self._permutation[letter_value] - current_offset) % 26

        return chr(letter_value + 65), next_rotate

    def _process_letter_backward(self, letter: str) -> str:
        r"""
        Private function which allows a rotor to process a single letter when 
        moving through the enigma,
        after passing the reflector.

        INPUT:

        - ``letter`` -- string; letter to be processed

        OUTPUT: processed letter

        EXAMPLES::

            sage: r = Rotor([21, 25, 1, 17, 6, 8, 19, 24, 20, 15, 18, 3, 13, 7, 
            ....: 11, 23, 0, 22, 12, 9, 16, 14, 5, 4, 2, 10], 25, 5, 2)
            sage: r._process_letter_backward("B")
            U

        Can only process letters A - Z::

            sage: r._process_letter_backward("1")
            Traceback (most recent call last):
            ...
            ValueError: Invalid letter: Input can only contain letters A - Z

        Letters need to be uppercase::

            sage: r._process_letter_backward("a")
            Traceback (most recent call last):
            ...
            ValueError: Invalid letter: Input can only contain letters A - Z
        """

        letter_value = ord(letter) - 65

        if letter_value < 0 or letter_value > 25:
            raise ValueError(
                "Invalid letter: Input can only contain letters A - Z")

        current_offset = (self._position - self._offset) % 26
        letter_value = (letter_value + current_offset) % 26
        letter_value = (self._permutation.index(
            letter_value) - current_offset) % 26

        return chr(letter_value + 65)
    
    def __repr__(self) -> str:
        r"""
        Return the string representation of ``self``.

        EXAMPLES::

            sage: r = Rotor([21, 25, 1, 17, 6, 8, 19, 24, 20, 15, 18, 3, 13, 7, 
            ....: 11, 23, 0, 22, 12, 9, 16, 14, 5, 4, 2, 10], 25, 5, 2)
            sage: r
            Rotor with current position 5, permutation [21, 25, 1, 17, 6, 8, 
            19, 24, 20, 15, 18, 3, 13, 7, 11, 23, 0, 22, 12, 9, 16, 14, 5, 4, 
            2, 10], initial position 5, offset 2 and notch 25
        """

        msg = ("Rotor with current position {1}, permutation {2}, "
               "initial position {3}, offset {4} and notch {5}")
        return msg.format(self._position + 1, self._permutation, 
                          self._initial_position + 1, self._offset + 1, 
                          self._notch)


class Reflector:
    r"""
    A special rotor that misses the key thing of one: the rotating, which makes
    it a simple permutation.

    This class fulfills the purpose of the needed reflector inside the enigma
    but can also act as the plugboard since the technical requirements are
    the same.
    In the case of being the actual reflector it gets used once a letter has
    passed every rotor for the first time, reflecting it back to the rotors
    after which the letter passes every rotor again.
    In the case of being the plugboard it gets used twice. Once before entering
    the first rotor and once after being reflected and passing the first rotor
    again.
    In both cases it permutates the passing letter.

    INPUT:

    - ``permutation`` -- list[integer]; permutation to be used in the reflector 
    which must have a length of 26

    EXAMPLES::

        sage: r = Reflector([24, 17, 20, 7, 16, 18, 11, 3, 15, 23, 13, 6, 14, 
        ....: 10, 12, 8, 4, 1, 5, 25, 2, 22, 21, 9, 0, 19])
        sage: r
        Permutation acting as a reflector or plugboard with permutation: [24, 
        17, 20, 7, 16, 18, 11, 3, 15, 23, 13, 6, 14, 10, 12, 8, 4, 1, 5, 25, 2,
        22, 21, 9, 0, 19]

    The reflector/plugboard needs to have a length of exactly 26::

        sage: r = Reflector([24, 17, 20, 7, 16, 18, 11, 3, 15, 23, 13, 6, 14, 
        ....: 10, 12, 8, 4, 1, 5, 25, 2, 22, 21])
        Traceback (most recent call last):
        ...
        ValueError: Permutation must have a length of 26
        sage: p = Reflector([24, 17, 20, 7, 16, 18, 11, 3, 15, 23, 13, 6, 14, 
        ....: 10, 12, 8, 4, 1, 5, 25, 2, 22, 21, 9, 0, 19, 2, 1 , 1])
        Traceback (most recent call last):
        ...
        ValueError: Permutation must have a length of 26

    .. NOTE::

        Every value inside the permutation must be between 0 and 25
    """

    def __init__(self, permutation: list[int]):
        r"""
        Initializes the ``Reflector`` class. See the class :class:`Reflector` 
        for full documentation on the input of this initialization method.
        """

        if len(permutation) != 26:
            raise ValueError("Permutation must have a length of 26")
        self._permutation = permutation

    def _process_letter(self, letter: str) -> str:
        r"""
        Private function to permutate a given letter

        INPUT:

        - ``letter`` -- string; letter to be processed

        OUTPUT: processed letter

        EXAMPLES::

            sage: r = Reflector([24, 17, 20, 7, 16, 18, 11, 3, 15, 23, 13, 6, 
            ....: 14, 10, 12, 8, 4, 1, 5, 25, 2, 22, 21, 9, 0, 19])
            sage: r._process_letter('A')
            'Y'
            
        Can only process letters A - Z::

            sage: r._process_letter('1')
            Traceback (most recent call last):
            ...
            ValueError: Invalid letter: Input can only contain letters A - Z

        Letters need to be uppercase::

            sage: r._process_letter('a')
            Traceback (most recent call last):
            ...
            ValueError: Invalid letter: Input can only contain letters A - Z
        """

        letter_value = ord(letter) - 65

        if letter_value < 0 or letter_value > 25:
            raise ValueError(
                "Invalid letter: Input can only contain letters A - Z")

        letter_value = self._permutation[letter_value]

        return chr(letter_value + 65)
    
    def __repr__(self) -> str:
        r"""
        Return the string representation of ``self``.

        EXAMPLES::

            sage: r = Reflector([24, 17, 20, 7, 16, 18, 11, 3, 15, 23, 13, 6, 
            ....: 14, 10, 12, 8, 4, 1, 5, 25, 2, 22, 21, 9, 0, 19])
            sage: r
            Permutation acting as a reflector or plugboard with permutation: 
            [24, 17, 20, 7, 16, 18, 11, 3, 15, 23, 13, 6, 14, 10, 12, 8, 4, 1, 
            5, 25, 2, 22, 21, 9, 0, 19]
        """

        msg = ("Permutation acting as a reflector or plugboard with "
               "permutation: {1}")
        return msg.format(self._permutation)


class Enigma:
    r"""
    An object representing the Enigma. The enigma is used to encrypt and
    decrypt messages.
    To decrypt a message a enigma with the same settings as the one used to
    encrypt the message is needed.

    INPUT:

    - ``rotors`` -- list[Rotor]; a list of rotors to be used in this enigma
    - ``reflector`` -- Reflector; the reflector to be used in this enigma
    - ``plugboard`` -- Reflector (default: `None`); optional plugboard to use
      in this enigma

    EXAMPLES::

        sage: a = Rotor([21, 25, 1, 17, 6, 8, 19, 24, 20, 15, 18, 3, 13,
        ....: 7, 11, 23, 0, 22, 12, 9, 16, 14, 5, 4, 2, 10], 25, 5, 2)
        sage: b = Rotor([1, 3, 5, 7, 9, 11, 2, 15, 17, 19, 23, 21, 25, 13, 
        ....: 24, 4, 8, 22, 6, 0, 10, 12, 20, 18, 16, 14], 21, 24, 4)
        sage: c = Rotor([0, 9, 3, 10, 18, 8, 17, 20, 23, 1, 11, 7, 22, 19, 
        ....: 12, 2, 16, 6, 25, 13, 15, 24, 5, 21, 14, 4], 4, 11, 24)
        sage: d = Reflector([24, 17, 20, 7, 16, 18, 11, 3, 15, 23, 13, 6, 
        ....: 14, 10, 12, 8, 4, 1, 5, 25, 2, 22, 21, 9, 0, 19])
        sage: e = Enigma([a, b, c], d, None)
        sage: e
        Enigma with rotors [[21, 25, 1, 17, 6, 8, 19, 24, 20, 15, 18, 3, 
        13, 7, 11, 23, 0, 22, 12, 9, 16, 14, 5, 4, 2, 10], [1, 3, 5, 7, 9,
        11, 2, 15, 17, 19, 23, 21, 25, 13, 24, 4, 8, 22, 6, 0, 10, 12, 20, 
        18, 16, 14], [0, 9, 3, 10, 18, 8, 17, 20, 23, 1, 11, 7, 22, 19, 
        12, 2, 16, 6, 25, 13, 15, 24, 5, 21, 14, 4]], reflector [24, 17, 
        20, 7, 16, 18, 11, 3, 15, 23, 13, 6, 14, 10, 12, 8, 4, 1, 5, 25, 2, 
        22, 21, 9, 0, 19] and plugboard None

    .. NOTE::

        To use predefined rotors and reflectors see :class:`EnigmaFactory`
    """

    def __init__(self, rotors: list[Rotor], reflector: Reflector, 
                 plugboard: Reflector = None):
        r"""
        Initializes the ``Enigma`` class. See the class :class:`Enigma` for
        full documentation on the input of this initialization method.
        """

        self._rotors = rotors
        self._reflector = reflector
        self._plugboard = plugboard

    def en_de_crypt(self, text):
        r"""
        Processes the `text` which results in receiving a encrypted or
        decrypted text.
        To decrypt a text, a enigma is needed with the same starting settings
        as the enigma used to encrypt the text.

        INPUT:

        - ``text`` -- string; The text to be processed by this enigma, can only
        contain letters A - Z

        OUTPUT: the encrypted or decrypted text

        EXAMPLES::

            sage: a = Rotor([21, 25, 1, 17, 6, 8, 19, 24, 20, 15, 18, 3, 13,
            ....: 7, 11, 23, 0, 22, 12, 9, 16, 14, 5, 4, 2, 10], 25, 5, 2)
            sage: b = Rotor([1, 3, 5, 7, 9, 11, 2, 15, 17, 19, 23, 21, 25, 13, 
            ....: 24, 4, 8, 22, 6, 0, 10, 12, 20, 18, 16, 14], 21, 24, 4)
            sage: c = Rotor([0, 9, 3, 10, 18, 8, 17, 20, 23, 1, 11, 7, 22, 19, 
            ....: 12, 2, 16, 6, 25, 13, 15, 24, 5, 21, 14, 4], 4, 11, 24)
            sage: d = Reflector([24, 17, 20, 7, 16, 18, 11, 3, 15, 23, 13, 6, 
            ....: 14, 10, 12, 8, 4, 1, 5, 25, 2, 22, 21, 9, 0, 19])
            sage: e = Enigma([a, b, c], d, None)
            sage: e.en_de_crypt("HELLO")
            GCIID

        The text can not contain any other character than the letters A - Z::

            sage: e.en_de_crypt("HELLO HOW ARE YOU")
            Traceback (most recent call last):
            ...
            ValueError: Invalid letter: Input can only contain letters A - Z

        However, lowercase letters are automatically converted to uppercase
        letters::

            sage: e.en_de_crypt("hellohowareyou")
            CUNIWXNYWUXNXZ
        """

        result = ""
        message = str(text).upper()

        for letter in message:
            predecessor_tuple: tuple[str, bool] = letter, True

            for rotor in self._rotors:
                predecessor_tuple = rotor._process_letter_forward(
                    predecessor_tuple[0], predecessor_tuple[1])

            predecessor_tuple = self._reflector._process_letter(
                predecessor_tuple[0]), False

            for rotor in reversed(self._rotors):
                predecessor_tuple = rotor._process_letter_backward(
                    predecessor_tuple[0]), False

            result += predecessor_tuple[0]

        return result
    
    def __repr__(self) -> str:
        r"""
        Return the string representation of ``self``.

        EXAMPLES::

            sage: a = Rotor([21, 25, 1, 17, 6, 8, 19, 24, 20, 15, 18, 3, 13,
            ....: 7, 11, 23, 0, 22, 12, 9, 16, 14, 5, 4, 2, 10], 25, 5, 2)
            sage: b = Rotor([1, 3, 5, 7, 9, 11, 2, 15, 17, 19, 23, 21, 25, 13, 
            ....: 24, 4, 8, 22, 6, 0, 10, 12, 20, 18, 16, 14], 21, 24, 4)
            sage: c = Rotor([0, 9, 3, 10, 18, 8, 17, 20, 23, 1, 11, 7, 22, 19, 
            ....: 12, 2, 16, 6, 25, 13, 15, 24, 5, 21, 14, 4], 4, 11, 24)
            sage: d = Reflector([24, 17, 20, 7, 16, 18, 11, 3, 15, 23, 13, 6, 
            ....: 14, 10, 12, 8, 4, 1, 5, 25, 2, 22, 21, 9, 0, 19])
            sage: e = Enigma([a, b, c], d, None)
            sage: e
            Enigma with rotors [[21, 25, 1, 17, 6, 8, 19, 24, 20, 15, 18, 3, 
            13, 7, 11, 23, 0, 22, 12, 9, 16, 14, 5, 4, 2, 10], [1, 3, 5, 7, 9,
            11, 2, 15, 17, 19, 23, 21, 25, 13, 24, 4, 8, 22, 6, 0, 10, 12, 20, 
            18, 16, 14], [0, 9, 3, 10, 18, 8, 17, 20, 23, 1, 11, 7, 22, 19, 
            12, 2, 16, 6, 25, 13, 15, 24, 5, 21, 14, 4]], reflector [24, 17, 
            20, 7, 16, 18, 11, 3, 15, 23, 13, 6, 14, 10, 12, 8, 4, 1, 5, 25, 2, 
            22, 21, 9, 0, 19] and plugboard None
        """

        msg = ("Enigma with rotors: {0}, reflector {1} and plugboard {2}")
        return msg.format(self._rotors, self._reflector, self._plugboard)


class EnigmaFactory:
    r"""
    Factory for creating (semi-) realistic Enigmas. Choose from real reflectors and rotors.

    EXAMPLES:

    TESTS::

    """

    def __init__(self):
        self._wheels = [[4, 10, 12, 5, 11, 6, 3, 16, 21, 25, 13, 19, 14, 22, 24, 7, 23, 20, 18, 15, 0, 8, 1, 17, 2, 9],
                        [0, 9, 3, 10, 18, 8, 17, 20, 23, 1, 11, 7, 22, 19,
                            12, 2, 16, 6, 25, 13, 15, 24, 5, 21, 14, 4],
                        [1, 3, 5, 7, 9, 11, 2, 15, 17, 19, 23, 21, 25, 13,
                            24, 4, 8, 22, 6, 0, 10, 12, 20, 18, 16, 14],
                        [4, 18, 14, 21, 15, 25, 9, 0, 24, 16, 20, 8, 17,
                            7, 23, 11, 13, 5, 19, 6, 10, 3, 2, 12, 22, 1],
                        [21, 25, 1, 17, 6, 8, 19, 24, 20, 15, 18, 3, 13, 7, 11, 23, 0, 22, 12, 9, 16, 14, 5, 4, 2, 10]]
        self._notches = [16, 4, 21, 9, 25]
        self._reflectors = [
            [4, 9, 12, 25, 0, 11, 24, 23, 21, 1, 22, 5, 2, 17,
                16, 20, 14, 13, 19, 18, 15, 8, 10, 7, 6, 3],
            [24, 17, 20, 7, 16, 18, 11, 3, 15, 23, 13, 6, 14,
                10, 12, 8, 4, 1, 5, 25, 2, 22, 21, 9, 0, 19],
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

            rotor_list.append(
                Rotor(self._wheels[r[0] - 1], self._notches[r[0] - 1], r[1], r[2]))

        return Enigma(rotor_list, reflector_)


r1 = Rotor([21, 25, 1, 17, 6, 8, 19, 24, 20, 15, 18, 3, 13, 7,
           11, 23, 0, 22, 12, 9, 16, 14, 5, 4, 2, 10], 25, 5, 2)
r2 = Rotor([1, 3, 5, 7, 9, 11, 2, 15, 17, 19, 23, 21, 25, 13, 24,
           4, 8, 22, 6, 0, 10, 12, 20, 18, 16, 14], 21, 24, 4)
r3 = Rotor([0, 9, 3, 10, 18, 8, 17, 20, 23, 1, 11, 7, 22, 19, 12,
           2, 16, 6, 25, 13, 15, 24, 5, 21, 14, 4], 4, 11, 24)
reflector = Reflector([24, 17, 20, 7, 16, 18, 11, 3, 15, 23,
                      13, 6, 14, 10, 12, 8, 4, 1, 5, 25, 2, 22, 21, 9, 0, 19])
enigma = Enigma([r1, r2, r3], reflector)
print(enigma.en_de_crypt(sys.argv[1]))
