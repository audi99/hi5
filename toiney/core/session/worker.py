import sys
import datetime
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from toiney.core.session.controller import Controller
from toiney.core.service.account import Account
from toiney.core.extensions.abstractextensions import AbstractExtensions

try_take = AbstractExtensions().try_take


class Worker:
    def __init__(self, controller=Controller(), account=Account()):
        self._status = "Awaiting further instruction."
        self.controller = controller
        self._account = account
        self._enabled: bool = None  # TODO: probably change, not sure

    @property
    def account(self):
        return self._account

    @account.setter
    def account(self, value):
        self._account = value

    @property
    def enabled(self) -> bool:
        return self._enabled

    def handle_get_geolocation(self) -> bool:
        if self._account is None:
            return False
        self.account.geolocation = try_take(self.controller.locations.parse())
        if self._account.geolocation is not None:
            return self.account.geolocation

    def handle_get_photoset(self) -> bool:
        if self.account is None:
            return False
        self.account.photoset = try_take(self.controller.photosets)
        if self.account.photoset is not None:
            return self.account.photoset


if __name__ == '__main__':
    work = Worker()
    print(work.handle_get_photoset())

