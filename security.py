import numpy as np
from random import choices, choice
from string import (
    ascii_lowercase,
    ascii_uppercase,
    punctuation,
    digits
)


def create_password(length: int=16) -> str:
    password_fragment = choices((ascii_uppercase, ascii_lowercase, punctuation, digits), weights=(1, 3, 2, 1), k=length)
    password = ""
    for random_character in password_fragment:
        password += choice(random_character)
    return password


class Hash:
    __slots__ = "aes", "__key"

    def __init__(self, key) -> None:
        self.aes = AES()
        self.__key = key

    def cypher(self, password: str) -> str:
        return self.aes.encode(password, self.__key)

    def inverse_cypher(self, password: str) -> str:
        return self.aes.decode(password, self.__key)


class AES:
    __slots__ = "__roundKey", "__state"
    Rows = 4
    BitsNumber = 4
    Rounds = 10
    SBox = np.array([
        0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
        0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
        0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
        0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
        0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
        0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
        0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
        0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
        0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
        0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
        0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
        0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
        0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16], dtype=np.uint8)
    InvSBox = np.array([
        0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
        0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
        0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
        0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
        0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
        0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
        0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
        0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
        0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
        0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
        0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
        0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
        0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
        0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
        0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
        0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d], dtype=np.uint8)
    RCon = np.array([0x1, 0x2, 0x4, 0x8, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36], dtype=np.uint8)
    
    def encode(self, password: str, key: bytes) -> str:
        assert len(password) == 16, KeyException("Password lenght is not equal 16")
        self.__state = np.frombuffer(bytearray(password.encode("ASCII")), dtype=np.dtype((np.uint8, (4,))))

        assert len(key) == 16, KeyException("Key lenght is not equal 16")
        self._expend_key(key)

        self._encode_state()
        self.__roundKey = None

        encoded_password = ''.join(chr(c) for c in self.__state.flatten())
        self.__state = None
        
        return encoded_password
    
    def decode(self, password: str, key: bytes)  -> str:
        assert len(password) == 16, KeyException("Password lenght is not equal 16")
        self.__state = np.frombuffer(bytearray([ord(c) for c in password]), dtype=np.dtype((np.uint8, (4,))))

        assert len(key) == 16, KeyException("Key lenght is not equal 16")
        self._expend_key(key)

        self._decode_state()
        self.__roundKey = None
        
        decoded_password = ''.join(chr(c) for c in self.__state.flatten())
        self.__state = None

        return decoded_password

    def _encode_state(self) -> None:
        self._add_round_key(0)

        for round in range(1, self.Rounds):
            self._sub_bytes()
            self._shitf_rows()
            self._mix_columns()
            self._add_round_key(round)
        
        self._sub_bytes()
        self._shitf_rows()
        self._add_round_key(self.Rounds)
    
    def _decode_state(self) -> None:
        self._add_round_key(self.Rounds)
        self._inv_shitf_rows()
        self._inv_sub_bytes()

        for round in range(self.Rounds-1, 0, -1):
            self._add_round_key(round)
            self._inv_mix_columns()
            self._inv_shitf_rows()
            self._inv_sub_bytes()
        
        self._add_round_key(0)

    def _expend_key(self, key: bytes) -> None:
        self.__roundKey = list(key)
        for i in range(self.BitsNumber, self.Rows * (self.Rounds+1)):
            k = (i - 1) * 4
            temp = [self.__roundKey[k+j] for j in range(4)]

            if i % self.BitsNumber == 0:
                # RotWord()
                temp = [temp[j%4] for j in range(1, 5)]
                # SubWord()
                temp = [self.SBox[temp[j]] for j in range(4)]

                temp[0] ^= self.RCon[i//self.BitsNumber-1]

            k = (i - self.BitsNumber) * 4 
            self.__roundKey += [self.__roundKey[k+j]^temp[j] for j in range(4)]
        self.__roundKey = np.array(self.__roundKey, dtype=np.uint8)

    def _shitf_rows(self) -> None:
        for i in range(1, 4):
            self.__state[i] = np.array([self.__state[i][(j + i)%4] for j in range(4)], dtype=np.uint8)
    
    def _inv_shitf_rows(self) -> None:
        for i in range(1, 4):
            self.__state[i] = np.array([self.__state[i][(j - i)%4] for j in range(4)], dtype=np.uint8)

    @staticmethod
    def _mul2(x: np.uint8) -> np.uint8:
        """
        x : 0000 0000 | 8 bits
        2x = (x * 2) +
            if x>>7 == 1: 27
            else        :  0
        """
        return (x<<1) ^ (((x>>7) & 1) * 0x1b)
    
    @staticmethod
    def _mul3(x: np.uint8) -> np.uint8:
        """3x = 2x + x"""
        return AES._mul2(x) ^ x

    def _mix_columns(self) -> None:
        for i in range(4):
            a, b, c, d = self.__state[: ,i]
            self.__state[0][i] = self._mul2(a) ^ self._mul3(b) ^ c ^ d # 2a + 3b +  c +  d
            self.__state[1][i] = a ^ self._mul2(b) ^ self._mul3(c) ^ d #  a + 2b + 3c +  d
            self.__state[2][i] = a ^ b ^ self._mul2(c) ^ self._mul3(d) #  a +  b + 2c + 3d
            self.__state[3][i] = self._mul3(a) ^ b ^ c ^ self._mul2(d) # 3a +  b +  c + 2d
    
    def _mul_9(self, x: np.uint8) -> np.uint8:
        """9x = (((2x) * 2) * 2) + x"""
        return     x ^ self._mul2(self._mul2(self._mul2(x)))

    def _mul11(self, x: np.uint8) -> np.uint8:
        """11x = ((((2x) * 2) + x) * 2) + x"""
        return x ^ self._mul2(x ^ self._mul2(self._mul2(x)))
    
    def _mul13(self, x: np.uint8) -> np.uint8:
        """13x = ((((2x) + x) * 2) * 2) + x"""
        return x ^ self._mul2(self._mul2(x ^ self._mul2(x)))
    
    def _mul14(self, x: np.uint8) -> np.uint8:
        """14x = ((((2x) + x) * 2) + x) * 2"""
        return self._mul2(x ^ self._mul2(x ^ self._mul2(x)))

    def _inv_mix_columns(self) -> None:
        for i in range(4):
            a, b, c, d = self.__state[: ,i]
            self.__state[0][i] = self._mul14(a) ^ self._mul11(b) ^ self._mul13(c) ^ self._mul_9(d) # 14a + 11b + 13c +  9d
            self.__state[1][i] = self._mul_9(a) ^ self._mul14(b) ^ self._mul11(c) ^ self._mul13(d) #  9a + 14b + 11c + 13d
            self.__state[2][i] = self._mul13(a) ^ self._mul_9(b) ^ self._mul14(c) ^ self._mul11(d) # 13a +  9b + 14c + 11d
            self.__state[3][i] = self._mul11(a) ^ self._mul13(b) ^ self._mul_9(c) ^ self._mul14(d) # 11a + 13b +  9c + 14d

    def _sub_bytes(self) -> None:
        for i in range(4):
            for j in range(4):
                self.__state[i][j] = self.SBox[self.__state[i][j]]

    
    def _inv_sub_bytes(self) -> None:
        for i in range(4):
            for j in range(4):
                self.__state[i][j] = self.InvSBox[self.__state[i][j]]
    
    def _add_round_key(self, round: int) -> None:
        for i in range(4):
            for j in range(4):
                self.__state[i][j] ^= self.__roundKey[round*self.Rows*4 + i*self.Rows + j]


class KeyException(Exception):
    pass
