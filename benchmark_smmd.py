"""
Benchmark to show O(1) complexity

sample results:
10   	8.560999870300293
100  	8.523000001907349
1000 	8.79699993133545
10000	8.781999826431274
100000	8.099999904632568

10   	8.560999870300293
100  	8.523000001907349
1000 	8.79699993133545
10000	8.781999826431274
100000	8.099999904632568

"""

from smmd import SMMD, PositionalValue
import time


def saw_wave(amin: int, amax: int, half_period: int):
    buffer = []
    for i in range(half_period):
        buffer.append(amin + (amax - amin) * i / half_period)
    for i in range(half_period):
        buffer.append(amax - (amax - amin) * i / half_period)
    pos = 0
    while True:
        if pos == len(buffer):
            pos = 0
        yield buffer[pos]
        pos += 1


for tailsize in [10, 100, 1000, 10000, 100000]:
    det = SMMD(tailsize)
    gen = saw_wave(0, 1, tailsize-1)
    start = time.time()
    for pos in range(1000000):
        v = next(gen)
        det.push(PositionalValue(pos, v))
        det.is_center_mm()
    end = time.time()
    print("{tailsize:<5}\t{time}".format(tailsize=tailsize, time=end - start))
