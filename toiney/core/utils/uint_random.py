import struct
import sys
import os
import numpy as np
from decimal import Decimal
import datetime
import calendar



class Random:
    def __init__(self):
        pass

    def _rand(self, min_n, max_n):
        uint32 = np.iinfo(np.uint32)  # unsigned integer max: 4294967295
        num = uint32.max
        while num == uint32.max:
            random_bytes = struct.unpack("I", os.urandom(4))
            array = random_bytes[0]
            return int(round(Decimal(min_n) + Decimal(max_n - min_n) * Decimal(array) / Decimal(uint32.max)))

    def _int64_next(self, min_n, max_n):
        int64 = np.iinfo(np.int64)
        num = int64.max
        while num == int64.max:
            random_bytes = struct.unpack("q", os.urandom(8))
            array = random_bytes[0]
            return int(round(Decimal(min_n) + Decimal(max_n - min_n) * Decimal(array) / Decimal(9.2233720368547758E+18)))

    def rand_next(self, min_num, max_num):
        num = sys.float_info[0]  # max float size
        while num == 1.7976931348623157E+308:
            random_bytes = struct.unpack('d', os.urandom(8))[0]
            array = random_bytes
            return array
        return min_num + (max_num + min_num) * (num / sys.float_info[0])

    def birth_date(self, min_year, max_year):
        year = self._rand(min_year, max_year)
        month = self._rand(1, 12)
        result = (year, month, self._rand(calendar.monthrange(year, month)[0], calendar.monthrange(year, month)[1]))
        return result


if __name__ == '__main__':
    print(Random().birth_date(1997, 1999))  # testing purposes only

