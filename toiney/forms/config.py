from toiney.forms.configuration import Ui_Dialog
from toiney.forms.addaccount import Ui_Dialog as add_account
from toiney.core.utils.uint_random import Random
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QTableWidgetItem
import sys
import sqlite3


sys._excepthook = sys.excepthook


def exception_hook(exctype, value, traceback):
    # print error & traceback
    print(exctype, value, traceback)
    # call normal exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = exception_hook


class ConfigWindow(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.show()

        self.pushButton_22.clicked.connect(self.add_account)
        self.pushButton_23.clicked.connect(self.edit_account)

        self.fileDialog = QtWidgets.QFileDialog(self)
        self.fileDialog.setNameFilter("Text Document (*.txt)")
        self.fileChosen = None

        self.emailPath_btn_3.clicked.connect(self.openFile)
        self.checkBox_3.clicked.connect(self.gui_state)
        self.treeWidget.clicked.connect(self.on_click)
        self.tree = self.treeWidget

        self.db = sqlite3.connect('../credentials.db')  # TODO: change this later or error will raise cuz of path

        self.stackedWidget.setCurrentIndex(0)
        self.tableWidget.resizeColumnToContents(0)  # checkbox column goes here
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        self.bg_fill()

        self.pushButton_23.setEnabled(False)
        self.tableWidget.clicked.connect(self.enabler)

    def on_click(self):
        item = self.tree.currentItem()  # item in qtreewidget
        text = item.text(0)  # text of item selected in qtreewidget
        if str(text) == 'General':
            self.stackedWidget.setCurrentIndex(0)
            self.bg_fill()
        if str(text) == 'Networking':
            self.stackedWidget.setCurrentIndex(1)
            self.bg_fill()
        if str(text) == 'Connection':  # TODO: this
            self.bg_fill()
        if str(text) == 'Account':
            self.stackedWidget.setCurrentIndex(2)
            self.bg_fill()
        if str(text) == 'Registration':
            self.stackedWidget.setCurrentIndex(3)
            self.bg_fill()

    def enabler(self):  # exists just to re-enable the edit button
        if len(self.tableWidget.selectedItems()) > 0:
            self.pushButton_23.setEnabled(True)
        else:
            self.pushButton_23.setEnabled(False)

    def add_account(self):
        add = AddAccount(self)
        if add.exec_():
            try:
                self.set_values(add.add_item())  # function that adds items to table
            finally:
                pass
                # self.set_db()  # function that adds items from table to database

    def edit_account(self):
        edit = EditAccount(self, data=self.edit_items())
        if edit.exec_():
            try:
                self.set_values(edit.edit_set(), caller='edit')
            finally:
                pass
            # self.set_db()  # TODO: may remove this later not sure

    def bg_fill(self):
        page = self.stackedWidget.currentWidget()
        page.setAutoFillBackground(True)
        palette = page.palette()
        palette.setColor(page.backgroundRole(), QtCore.Qt.white)
        page.setPalette(palette)

    def gui_state(self):  # TODO: object names changed, change this asap
        if self.checkBox_3.isChecked():
            self.radioButton_5.setEnabled(True)
            self.radioButton_6.setEnabled(True)
            self.label_14.setEnabled(True)
            self.label_15.setEnabled(True)
            self.label_16.setEnabled(True)
            self.label_17.setEnabled(True)
            self.label_18.setEnabled(True)
            self.spinBox_12.setEnabled(True)
            self.spinBox_13.setEnabled(True)
            self.spinBox_14.setEnabled(True)
            self.emailPath_btn_3.setEnabled(True)
            self.pushButton_22.setEnabled(True)
            self.pushButton_24.setEnabled(True)
            self.pushButton_25.setEnabled(True)
            self.line_6.setEnabled(True)
            self.checkBox_4.setEnabled(True)
            self.checkBox_10.setEnabled(True)
            self.tableWidget.setEnabled(True)
            self.gridFrame_5.setEnabled(True)
        else:
            self.radioButton_5.setEnabled(False)
            self.radioButton_6.setEnabled(False)
            self.label_14.setEnabled(False)
            self.label_15.setEnabled(False)
            self.label_16.setEnabled(False)
            self.label_17.setEnabled(False)
            self.label_18.setEnabled(False)
            self.spinBox_12.setEnabled(False)
            self.spinBox_13.setEnabled(False)
            self.spinBox_14.setEnabled(False)
            self.emailPath_btn_3.setEnabled(False)
            self.pushButton_22.setEnabled(False)
            self.pushButton_23.setEnabled(False)
            self.pushButton_24.setEnabled(False)
            self.pushButton_25.setEnabled(False)
            self.line_6.setEnabled(False)
            self.checkBox_4.setEnabled(False)
            self.checkBox_10.setEnabled(False)
            self.tableWidget.setEnabled(False)
            self.gridFrame_5.setEnabled(False)

    def set_values(self, tuplex, caller=None):
        if caller is None:
            self.tableWidget.insertRow(self.tableWidget.rowCount())

        tuplex = list(tuplex)

        x, y = tuplex[3]
        birth = x + '-' + y
        looking_for = None
        if isinstance(tuplex[5], list):
            if 1 < len(tuplex[5]) < 3:
                f, d = tuplex[5]  # friendship, dating, chat
                looking_for = f + ', ' + d
            elif len(tuplex[5]) > 2:
                f, d, c = tuplex[5]
                looking_for = f + ', ' + d + ', ' + c
            elif len(tuplex[5]) == 1:
                f = tuplex[5]
                looking_for = f[0]

        tuplex.pop(3)
        tuplex.pop(4)
        tuplex.insert(3, birth)
        tuplex.append(looking_for)
        chkbox_widget = QtWidgets.QWidget()
        chkbox = QtWidgets.QCheckBox()
        layoutCheckBox = QtWidgets.QHBoxLayout(chkbox_widget)
        layoutCheckBox.addWidget(chkbox)
        layoutCheckBox.setAlignment(Qt.AlignCenter)
        layoutCheckBox.setContentsMargins(0, 0, 0, 0, )
        self.tableWidget.setCellWidget(self.tableWidget.rowCount() - 1, 0, chkbox_widget)
        if caller == 'edit':
            num = 1
            for x in range(len(tuplex)):
                self.tableWidget.setItem(self.tableWidget.currentRow(), num, QTableWidgetItem(tuplex[x]))
                num += 1
        else:
            i = 1
            for x in range(int(len(tuplex))):
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, i, QTableWidgetItem(tuplex[x]))
                i += 1

            self.label_15.setText('Total Registrations: {}'.format(self.tableWidget.rowCount()))

    def edit_items(self):
        try:
            item_list = []
            items_selected = self.tableWidget.selectedItems()
            for item in items_selected:
                value = item.text()
                item_list.append(value)
            return item_list
        except Exception:
            pass

    def set_db(self):
        first_name = [self.tableWidget.item(row, 0).text() for row in range(self.tableWidget.rowCount())]
        last_name = [self.tableWidget.item(row, 1).text() for row in range(self.tableWidget.rowCount())]
        password = [self.tableWidget.item(row, 2).text() for row in range(self.tableWidget.rowCount())]
        birthday = [self.tableWidget.item(row, 3).text() for row in range(self.tableWidget.rowCount())]
        gender = [self.tableWidget.item(row, 4).text() for row in range(self.tableWidget.rowCount())]
        looking_for = [self.tableWidget.item(row, 5).text() for row in range(self.tableWidget.rowCount())]

        cur = self.db.cursor()
        for i in range(0, len(first_name)):
            cur.execute("INSERT INTO registration (first_name,last_name,password,birthday,gender,looking_for) "
                        "VALUES (?,?,?,?,?,?)", (first_name[i],
                                                 last_name[i],
                                                 password[i],
                                                 birthday[i],
                                                 gender[i],
                                                 looking_for[i]
                                                 ))
        self.db.commit()

    def openFile(self):

        # open file dialog and select img
        self.fileChosen, _ = self.fileDialog.getOpenFileName(self, "Locate email list...", "",
                                                             "Text Document (*.txt)")

        if self.fileChosen:
            self.lineEdit_3.setText(self.fileChosen)
        else:
            self.lineEdit_3.setText("No file was selected. Please select a valid path.")


class EditAccount(QtWidgets.QDialog, add_account):
    def __init__(self, parent=None, data=None):
        super(EditAccount, self).__init__(parent)
        if data is None:
            data = []
        self.setupUi(self)
        self.show()
        self.setWindowTitle('Edit Registration')

        try:
            self.data = data  # should be a list

            self.first_name = self.data[0]
            self.last_name = self.data[1]
            self.password = self.data[2]
            self.birthday = self.data[3]
            self.gender = self.data[4]
            self.looking_for = []

            self.buttonBox.rejected.connect(self.reject)
            # self.accepted.connect(self.edit)
            self.original()
            self.edit_set()

            self.radioButton.toggled.connect(lambda: self.btnstate(self.radioButton))
            self.radioButton_2.toggled.connect(lambda: self.btnstate(self.radioButton_2))
        except Exception as e:
            print(e)
            if self.data is None:
                print('No account was selected.')

    def original(self):
        self.lineEdit.setText(self.first_name)
        self.lineEdit_2.setText(self.last_name)
        self.lineEdit_3.setText(self.password)
        self.spinBox_2.setValue(int(self.birthday[0]))
        self.spinBox.setValue(int(self.birthday[1]))
        if self.gender == 'F':
            self.radioButton_2.setChecked(True)
        else:
            self.radioButton.setChecked(True)
        looking_for = self.data[5].split(' ')
        for val in looking_for:
            if val.startswith('F'):
                self.listWidget.item(0).setCheckState(QtCore.Qt.Checked)
            elif val.startswith('D'):
                self.listWidget.item(1).setCheckState(QtCore.Qt.Checked)
            elif val.startswith('C'):
                self.listWidget.item(2).setCheckState(QtCore.Qt.Checked)

    def btnstate(self, b):
        if b.text() == 'Male':
            if b.isChecked() is True:
                b.setChecked(True)
            else:
                pass
        if b.text() == 'Female':
            if b.isChecked() is True:
                b.setChecked(True)
            else:
                pass

    def edit_set(self):
        self.first_name = self.lineEdit.text()
        self.last_name = self.lineEdit_2.text()
        self.password = self.lineEdit_3.text()
        self.birthday = self.spinBox_2.text(), self.spinBox.text()
        if self.radioButton.isChecked():
            self.gender = 'M'
        else:
            self.gender = 'F'

        for index in range(self.listWidget.count()):
            if self.listWidget.item(index).checkState() == QtCore.Qt.Checked:
                self.looking_for.append(self.listWidget.item(index).text())
        return self.first_name, self.last_name, self.password, self.birthday, self.gender, self.looking_for

    def edit(self):
        print(self.data)


class AddAccount(QtWidgets.QDialog, add_account):
    def __init__(self, parent=None):
        super(AddAccount, self).__init__(parent)
        self.setupUi(self)
        self.show()

        self.setWindowTitle('Add Registration')
        self.first_name = None
        self.last_name = None
        self.password = None
        self.birthday = []
        self.gender = None
        self.looking_for = []

        self.buttonBox.rejected.connect(self.reject)
        # self.accepted.connect(self.add_item)

    def shuffle_birthday(self, args):
        minyear, maxyear = args
        try:
            return Random().birth_date(int(minyear), int(maxyear))[0]
        except Exception as e:
            raise e

    def add_item(self):
        self.first_name = self.lineEdit.text()
        self.last_name = self.lineEdit_2.text()
        self.password = self.lineEdit_3.text()
        self.birthday = self.spinBox_2.text(), self.spinBox.text()
        if self.radioButton.isChecked():
            self.gender = 'M'
        else:
            self.gender = 'F'

        for index in range(self.listWidget.count()):
            if self.listWidget.item(index).checkState() == QtCore.Qt.Checked:
                self.looking_for.append(self.listWidget.item(index).text())
        return self.first_name, self.last_name, self.password, self.birthday, self.gender, self.looking_for


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = ConfigWindow()
    w.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting...")
