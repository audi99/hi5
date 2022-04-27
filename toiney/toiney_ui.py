import sys
import logging
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QAction
from quamash import QEventLoop
import asyncio

import sqlite3

from toiney.forms.main import Ui_MainWindow
from toiney.forms.config import ConfigWindow
from toiney.forms.account_form import Ui_account_form

import toiney.forms.gui as gui

from toiney.logs.func_wrappers_etc import wait_alt
from toiney.session import Session, main as runner
from toiney.core.models import Device

from datetime import datetime

device = Device()

accountManager = gui.Ui_dialog  # TODO: this is the account tab window, probably need to reimplement this


class QTextEditLogger(logging.Handler, QObject):
    sigLog = pyqtSignal(str)

    def __init__(self):
        logging.Handler.__init__(self)
        QObject.__init__(self)

    def emit(self, record):
        msg = str(self.format(record))
        self.sigLog.emit(msg)


# def asyncSlot(*args):
#     def real_decorator(fn):
#         @pyqtSlot(*args)
#         @functools.wraps(fn)
#         def wrapper(*args, **kwargs):
#             asyncio.ensure_future(fn(*args, **kwargs))
#
#         return wrapper
#
#     return real_decorator


class AccountManager(QtWidgets.QDialog, accountManager):
    def __init__(self, parent=None):
        super(AccountManager, self).__init__(parent)
        self.setupUi(self)
        self.show()
        self.database = sqlite3.connect('credentials.db')

        self.fileDialog = QtWidgets.QFileDialog(self)
        self.fileDialog.setNameFilter("Images (*.png *.jpg)")
        self.fileChosen = None

        self.photoBtn.clicked.connect(self.upload_photo)

        self.buttonBox.accepted.connect(self.call_register)
        self.ethnicityBox.addItems(self.ethnicity_list())
        self.session = Session()  # TODO: fix error about functions being unfilled

        # self.access_token = self.post_register()['access_token']  TODO: fix this

    def call_register(self, delay):
        asyncio.ensure_future(self.post_register(delay))

    async def post_register(self, delay):
        toiney = await self.session._api.register(
            firstName=str(self.firstName.text()),
            lastName=str(self.lastName.text()),
            birthYear=str(self.birthYear.text()),
            birthMonth=str(self.birthMonth.text()),
            birthDay=str(self.birthDay.text()),
            gender=str(self.genderBox.currentText()),
            ethnicity=str(self.ethnicityBox.currentText()),
            country=str(self.countryCode.currentText()),
            zipCode=str(self.zipCode.text()),
            email=str(self.email.text()),
            password=str(self.password.text())
        )
        await asyncio.sleep(delay)
        return toiney

    async def login(self):  # TODO: redo this completely. needs saved user data from SQL database
        sql_q = """SELECT email from user"""
        cur = self.database.cursor()
        data = cur.execute(sql_q).fetchall()  # fetch all emails

        for emails in data:
            await wait_alt(1, 3)
            email = emails[0]
            await self._session.login(email)

    async def upload_photo(self):
        dialog_style = self.fileDialog.DontUseNativeDialog
        dialog_style |= self.fileDialog.DontUseCustomDirectoryIcons

        # open file dialog and select img
        self.fileChosen, _ = self.fileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                             "JPEG (*.JPEG *.jpeg *.JPG *.jpg);; PNG (*.PNG *.png))", options=dialog_style)

        if self.fileChosen:
            return self.fileChosen
        else:
            self.photoPath.setText("No file was selected. Please select an image.")

    def chat(self):
        pass  # TODO: implement this

    async def location_list(self):
        country_list = []
        location_list = await Session().location()  # list of country codes
        locations = location_list
        for country in locations:
            country_list.append(country['countryCode'])
        self.countryCode.addItems(country_list)

    @classmethod
    def ethnicity_list(cls):
        ethnicityList = ['caucasian',
                         'asian',
                         'african',
                         'african_american',
                         'east_indian',
                         'hispanic',
                         'middle_eastern',
                         'native_person',
                         'pacific_islander',
                         'other']
        return ethnicityList


def current_time():
    now = datetime.now()  # current time
    currentTime = now.strftime('[%I:%M:%S]')
    return currentTime


class Form(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        if self.actionEvent_Log.isChecked():
            # console handler
            consoleHandler = QTextEditLogger()
            consoleHandler.setFormatter(logging.Formatter(
               ' %(asctime)s - %(name)s - %(levelname)s - %(message)s', current_time()))
            logging.getLogger().addHandler(consoleHandler)
            logging.getLogger().setLevel(logging.DEBUG)
            consoleHandler.sigLog.connect(self.consoleBox.appendPlainText)
            # creating file for log
            handler = logging.FileHandler('logs/debug.log')
            handler.setFormatter(logging.Formatter(
                ' %(asctime)s - %(name)s - %(levelname)s - %(message)s', current_time()))
            handler.setLevel(logging.DEBUG)
            logging.getLogger().addHandler(handler)

        self.action_account.triggered.connect(self.on_click)
        self.actionConfiguration.triggered.connect(self.config)
        self.acc_manager = None
        self.config_win = None
        self.start_btn = QAction(QIcon(
            'C:\\Users\\calib\\Documents\gui-stuff\\enable.png'), 'Run', self)
        self.toolBar.addAction(self.start_btn)
        self.start_btn.triggered.connect(self.fetch)   # TODO: this

    def fetch(self):
        asyncio.ensure_future(self.executor(['inbox'], login=True, loop=loop))

    async def executor(self, tasks, loop, login=False):
        return await runner(login=login, list_of_tasks=tasks, loop=loop)

    def config(self):
        self.config_win = ConfigWindow()

    def on_click(self):
        self.acc_manager = AccountManager()
        self.run_locations()

    def run_locations(self):
        # to run location_list() function
        asyncio.ensure_future(self.acc_manager.location_list(), loop=loop)

    def run_login(self):
        # login to account(s)
        asyncio.ensure_future(self.acc_manager.login(), loop=loop)


app = QtWidgets.QApplication(sys.argv)
loop = QEventLoop(app)
asyncio.set_event_loop(loop)  # NEW must set the event loop
app.setQuitOnLastWindowClosed(False)


if __name__ == '__main__':
    w = Form()
    w.show()
    #
    # tasks = []
    #
    # task = AccountManager()
    # tasks.append(task.location_list())
    #
    # loop.run_until_complete(asyncio.gather(*tasks))
    with loop:
        loop.run_forever()
