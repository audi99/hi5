from PyQt5 import QtCore, QtWidgets
import sys
from toiney.forms.account_form import Ui_account_form


class AccountManager(QtWidgets.QWidget, Ui_account_form):
    def __init__(self, parent=None):
        super(AccountManager, self).__init__(parent)
        self.setupUi(self)
        self.show()
        self.setWindowTitle('Account Manager')

        self.pushButton_22.clicked


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = AccountManager()
    w.show()
    sys.exit(app.exec_())
