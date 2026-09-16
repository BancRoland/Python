from enum import Enum

class RESISTORS(Enum):
    CONST_RES_39D8 = 0x1000
    CONST_RES_39D4 = 0x0800
    CONST_RES_39D2 = 0x0400
    CONST_RES_39A = 0x0200
    CONST_RES_39B = 0x0100
    CONST_RES_68 = 0x0080
    CONST_RES_120 = 0x0040
    CONST_RES_150 = 0x0020
    CONST_RES_270 = 0x0010
    CONST_RES_560 = 0x0008
    CONST_RES_1000 = 0x0004
    CONST_RES_2200 = 0x0002
    CONST_RES_3900 = 0x0001
    CONST_RES_INF = 0x0000

    # put lookup table OUTSIDE of enum members
    _resistor_values_table = {
        CONST_RES_39D8: 39/8,
        CONST_RES_39D4: 39/4,
        CONST_RES_39D2: 39/2,
        CONST_RES_39A: 39,
        CONST_RES_39B: 39,
        CONST_RES_68: 68,
        CONST_RES_120: 120,
        CONST_RES_150: 150,
        CONST_RES_270: 270,
        CONST_RES_560: 560,
        CONST_RES_1000: 1000,
        CONST_RES_2200: 2200,
        CONST_RES_3900: 3900,
        CONST_RES_INF: 10**12
    }

    @classmethod
    def get_resistor_code_from_resistance(cls, target_resistance: float):
        return [code for code, value in cls._resistor_values_table.items() if value == target_resistance]


print(RESISTORS.get_resistor_code_from_resistance(68))
