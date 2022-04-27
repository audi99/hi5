import sys
import threading
from threading import Thread
import threading
from toiney.logs.func_wrappers_etc import event
from toiney.core.models.geolocation import Geolocation
from toiney.core.models.photoset import Photoset
from PyQt5.QtWidgets import QTableWidget


class Controller:  # TODO: this
    def __init__(self, locations=Geolocation, photosets=Photoset):
        self.tasks = []  # threading tasks
        self._disposedValue: bool = False
        self._stop_tasks = threading.Event()  # call this to cancel all tasks. threading.Event() is False by default

        self._account = None  # TODO: this
        self.locations = locations()
        self.photosets = photosets(path='C:/Users/calib/PycharmProjects/hi5/toiney/photosets', photos='Photos').importer()

    @event
    def started(self):
        """Called when event has started."""

    @event
    def completed(self):
        """Called when event has completed."""

    def dispose(self, disposing: bool):
        if not self._disposedValue and disposing:
            if self.tasks is not None and len(self.tasks) > 0:
                try:
                    self.tasks.clear()
                finally:
                    pass

    def cancel(self):
        self._stop_tasks.set()


if __name__ == '__main__':
    photosets = Controller().photosets
    print(photosets)
