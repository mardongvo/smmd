from unittest import TestCase
from smmd import SMMD, PositionalValue


def saw_wave(amin: int, amax: int, half_period: int):
    buffer = []
    while True:
        if len(buffer) == 0:
            for i in range(half_period):
                buffer.append(amin + (amax - amin) * i / half_period)
            for i in range(half_period):
                buffer.append(amax - (amax - amin) * i / half_period)
        yield buffer.pop()


def saw_wave2(amin: int, amax: int, half_period: int):
    buffer = []
    while True:
        if len(buffer) == 0:
            # with two min/max
            for i in range(half_period):
                buffer.append(amin + (amax - amin) * i / (half_period-1))
            for i in range(half_period):
                buffer.append(amax - (amax - amin) * i / (half_period-1))
        yield buffer.pop()


class TestSMMD(TestCase):
    def test_is_center_mm1(self):
        det = SMMD(10)
        gen = saw_wave(0, 1, 15)  # min/max in 14,29,44...
        mins = []
        maxs = []
        for pos in range(61):
            v = next(gen)
            det.push(PositionalValue(pos, v))
            pv, ismin, ismax = det.is_center_mm()
            if ismin:
                mins.append(pv.position)
            if ismax:
                maxs.append(pv.position)
        self.assertListEqual(mins, [29], "minimals are not equal")
        self.assertListEqual(maxs, [14, 44], "maximals are not equal")

    def test_is_center_mm2(self):
        det = SMMD(10)
        gen = saw_wave2(0, 1, 15)  # min/max in 14,29,30,44...
        mins = []
        maxs = []
        for pos in range(61):
            v = next(gen)
            det.push(PositionalValue(pos, v))
            pv, ismin, ismax = det.is_center_mm()
            if ismin:
                mins.append(pv.position)
            if ismax:
                maxs.append(pv.position)
        self.assertListEqual(mins, [29, 30], "minimals are not equal")
        self.assertListEqual(maxs, [14, 15, 44, 45], "maximals are not equal")
