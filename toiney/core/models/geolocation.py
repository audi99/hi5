from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QApplication

import sys
import pathlib


class Table(QTableWidget):  # TODO: maybe need to change this inheritance, etc
    def __init__(self, parent=None):
        super(Table, self).__init__(parent)
        self.setColumnCount(4)
        self.insertRow(self.rowCount())


class Geolocation:
    def __init__(self, name="", zipcode="", latitude="", longitude=""):
        self._name = name
        self._zipcode = zipcode
        self._latitude = latitude
        self._longitude = longitude

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        try:
            pass
            # self.table.setItem(self.table.rowCount() - 1, 0, QTableWidgetItem(value))
        except Exception:
            pass

    @property
    def zipcode(self):
        return self._zipcode

    @zipcode.setter
    def zipcode(self, value):
        self._zipcode = value
        try:
            pass
            # self.table.setItem(self.table.rowCount() - 1, 1, QTableWidgetItem(value))
        except Exception:
            pass

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        value = "%.4f" % value
        self._latitude = value
        try:
            float(value)
            # self.table.setItem(self.table.rowCount() - 1, 2, QTableWidgetItem(value))
        except ValueError:
            pass
            # return "Invalid latitude value."

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        value = "%.4f" % value
        self._longitude = value
        try:
            float(value)
            # self.table.setItem(self.table.rowCount() - 1, 3, QTableWidgetItem(value))
        except ValueError:
            pass
            # return "Invalid longitude value."

    def _coordinates(self):
        try:
            file = pathlib.Path(__file__).parent
            # the file var will work if func is called from same location as coordinates.txt
            with open(file/'coordinates.txt', 'r') as coords:
                locations = coords.readlines()
            return locations
        except Exception as e:
            file = '../../coordinates.txt'
            with open(file, 'r') as coords:
                locations = coords.readlines()
            return locations

    def parse(self, value=None):
        if value is None:
            value = self._coordinates()
        if '|' not in value:
            return None
        array = value.split("|")
        if len(array) != 4 or any(s in array for s in array) is None:
            return None
        if not all(x in array for x in [array[0], array[1]]):
            return None

        return Geolocation(array[0], array[1], array[2], array[3])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Geolocation().parse()
    sys.exit(app.exec_())


