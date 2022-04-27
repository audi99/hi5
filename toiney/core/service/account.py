import threading
from toiney.constants import device
from toiney.core.models.emailaddress import EmailAddress
from toiney.core.models.photoset import Photoset
from toiney.core.models.geolocation import Geolocation
from datetime import datetime


class AtomicInteger:
    """ Custom Atomic Integer class """
    def __init__(self, value=0):
        self._value = value
        self._lock = threading.Lock()

    def inc(self):
        with self._lock:
            self._value += 1
            return self._value

    def dec(self):
        with self._lock:
            self._value -= 1
            return self._value

    @property
    def value(self):
        with self._lock:
            return self._value

    @value.setter
    def value(self, v):
        with self._lock:
            self._value = v


class Account:  # TODO: this
    def __init__(self, email=EmailAddress, photoset=Photoset, interlocked=AtomicInteger, geolocation=Geolocation):
        self._state = None  # TODO: this
        self.device = device
        self.email = email
        self.photoset = photoset
        self.interlocked = interlocked()
        self.logged_in: bool = None
        self.member_id = None  # TODO: add this
        self.status = "Awaiting further instruction."
        self.next_allowable_usage = None  # TODO: reimplement the logic for this, prob won't work like idb's
        self.geolocation = geolocation()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def device_header(self):
        return ','.join(['android', self.device.device_id,
                         ':'.join(['1480', '1480'])])

    def set_online(self, register: bool=False):  # TODO: this, probably wont work just copying idb :sob:
        if register:  # testing out custom atomic integer class
            self.interlocked.inc()  # TODO: add shit here

    def reset(self, full: bool=True):
        if full:
            # not needed afaik, but for thoroughness i added this from idb's source code
            pass
        self.logged_in = False
        self.member_id = None

    def wake(self):
        self.status = "Awaiting further instruction."
        self.next_allowable_usage = datetime.now()
        # TODO: add await call here maybe

    def work(self):  # TODO: this
        pass


if __name__ == '__main__':
    print(Account().device_header)
