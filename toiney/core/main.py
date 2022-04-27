from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from toiney.toiney_ui import Form
import os
import os.path
import datetime


class Main(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.fileDialog = QFileDialog(self)

    def initUI(self):
        pass
        # self.show()

    def browseOpenFile(self,
                       dialogTitle="",
                       defaultPath="",
                       filters=str("Text Document (*.txt)|.txt|All Files (*.*)|*.*")):

        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                   filter=filters)
        if file_name:
            return file_name

    def browseSaveFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,
                                                  "QFileDialog.getSaveFileName()",
                                                  "",
                                                  "All Files (*);;Text Files (*.txt)",
                                                  options=options)
        if fileName:
            print(fileName)

    def browseDirectory(self, title="", selectedPath=""):
        # open file dialog and select img
        self.fileChosen = self.fileDialog.getExistingDirectory(self, "Select Directory")

        if self.fileChosen:
            return self.fileChosen
        else:
            self.photoPath.setText("No file was selected. Please select a folder.")

    def getImages(self, pic_dir=""):
        for img in os.listdir(pic_dir):
            if img.endswith('.jpg') or img.endswith('.jpeg') or img.endswith('png'):
                return img

    def updateEvents(self, sender=None, text=""):
        text2 = "[{0}]".format(str(datetime.datetime.now().strftime("[%I:%M:%S]")))
        if sender is None:
            text2 += "Core. "
        elif isinstance(sender, Form):
            text2 += "UI, "





