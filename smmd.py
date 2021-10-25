"""
Stream min/max detector with O(1) complexity
It check that center of window has minmal/maximal value of window
"""

from dataclasses import dataclass
import typing as t


@dataclass
class PositionalValue:
    position: float
    value: float


@dataclass
class StackRecord:
    pvalue: PositionalValue
    minimal: float
    maximal: float


class SMMD:
    def __init__(self, tail: int):
        """
        tail - size of left/right tails of window
        so window always has odd length
        """
        self.tail = tail
        self.maxlen = 2 * tail + 1
        self.stack1: t.List[StackRecord] = []  # first stack, new values come to here
        self.stack2: t.List[StackRecord] = []  # second stack, old values pop out from here

    def push(self, pv: PositionalValue) -> t.Optional[PositionalValue]:
        tmp = None
        if len(self.stack1) + len(self.stack2) == self.maxlen:
            tmp = self.pop()
        self._internal_push(1, pv)
        return tmp

    def pop(self) -> t.Optional[PositionalValue]:
        if len(self.stack2) == 0:
            # pump values from stack 1 to stack 2
            # it happens 1 times every 2*tail+1 pushes
            while len(self.stack1) > 0:
                rec = self.stack1.pop()
                self._internal_push(2, rec.pvalue)
        return self.stack2.pop().pvalue

    def _internal_push(self, istack: int, pv: PositionalValue):
        """
        Push value to certain stack and calculate min/max
        Every i-element known min/max for [0:i+1] part of stack
        i.e. last element of stack ALWAYS known min/max for entire stack
        """
        if istack == 1:
            if len(self.stack1) == 0:
                self.stack1.append(StackRecord(pv, pv.value, pv.value))
            else:
                self.stack1.append(StackRecord(pv,
                                               min(pv.value, self.stack1[-1].minimal),
                                               max(pv.value, self.stack1[-1].maximal)
                                               )
                                   )
        if istack == 2:
            if len(self.stack2) == 0:
                self.stack2.append(StackRecord(pv, pv.value, pv.value))
            else:
                self.stack2.append(StackRecord(pv,
                                               min(pv.value, self.stack2[-1].minimal),
                                               max(pv.value, self.stack2[-1].maximal)
                                               )
                                   )

    def is_center_mm(self) -> t.Tuple[t.Optional[PositionalValue], bool, bool]:
        """
        return tuple: value/None, True if current center is minimal, True if current center is maximal
        """
        if len(self.stack1) + len(self.stack2) < self.maxlen:
            return None, False, False
        mid = None
        ismin = True
        ismax = True
        isdif1 = False  # do we have a difference between min and max in stack1?
        isdif2 = False  # do we have a difference between min and max in stack2?
        if len(self.stack1) > self.tail:
            mid = self.stack1[-self.tail - 1].pvalue
        if len(self.stack2) > self.tail:
            mid = self.stack2[-self.tail - 1].pvalue
        if len(self.stack1) > 0:
            isdif1 = self.stack1[-1].minimal < self.stack1[-1].maximal
            ismin = ismin and (mid.value <= self.stack1[-1].minimal)
            ismax = ismax and (mid.value >= self.stack1[-1].maximal)
        if len(self.stack2) > 0:
            isdif2 = self.stack2[-1].minimal < self.stack2[-1].maximal
            ismin = ismin and (mid.value <= self.stack2[-1].minimal)
            ismax = ismax and (mid.value >= self.stack2[-1].maximal)
        return mid, ismin and (isdif1 or isdif2), ismax and (isdif1 or isdif2)
