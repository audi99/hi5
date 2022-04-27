from enum import Enum
from typing import TypeVar
from toiney.core.utils.uint_random import Random
import random


T = TypeVar('T')


class AbstractExtensions:
    def __init__(self):  # nothing to do here, may remove later
        self.Random = Random()
        pass

    def compare_enumerables(self, first: T, second: T) -> bool:  # TODO: maybe need to fix this
        # print(new)
        if len(first) != len(second):
            return False
        num = 0
        num2 = len(first) - 1
        i = num
        while i <= num2:
            if first[i] is not None or second[i] is not None:
                if first[i] is not None or second[i] is not None:
                    t = first[i]
                    print(t)
                    print(second[i])
                    if t == second[i]:
                        i += 1
                        continue
            return False
        return True

    def me(self, value: T) -> T:
        return value

    def shuffler(self, items=None):
        if items is None:
            items = []
        if items is not None:
            if len(items) <= 1:
                return
        random.shuffle(items)
        return items

    def try_take(self, appender=False, target=None) -> T:
        """
        :param appender:
        :param target:
        :return: target
        """
        if target is None:
            target = []
        t = ""
        if len(target) > 0:
            t = target[0]
            del target[0]
            if appender:
                target.append(t)
        return t

    def try_take_all(self, target=None) -> T:
        if target is None:
            target = []
        result: T = []
        if len(target) > 0:
            result = target
            target.clear()
        return result

    def try_add(self, value: T, target=None):
        if target is None:
            target = []
        target.append(value)


if __name__ == '__main__':
    first = ['hello', 'how are you', 'i\'m doing okay']
    second = ['hi', 'what\'s up?', 'nothing much, you?']
    pictures = []
    foo = AbstractExtensions().try_take(appender=False, target=pictures)
    print(foo)

