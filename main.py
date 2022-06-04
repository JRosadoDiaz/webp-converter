import converter
import os
import sys

from filetype import FileType as FT
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QFileDialog, QPlainTextEdit, QCheckBox, QMessageBox, QComboBox, QPushButton, QApplication, QMainWindow, QLabel, QWidget, QLineEdit


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        windowSize = QSize(320, 280)
        self.setMinimumSize(windowSize)
        self.setWindowTitle("Webp Converter")
        self.setFixedSize(windowSize)

        self.verifyCheck = False
        self.UiComponents()

        self.show()

    def UiComponents(self):
        self.directoryLabel = QLabel(self)
        self.directoryLabel.setText('Folder Directory:')
        self.directoryLabel.move(20, 10)

        # self.directorySelection = QFileDialog().getExistingDirectory(self, "Choose Directory")
        self.directoryLine = QLineEdit(self)
        self.directoryLine.textChanged.connect(
            self.verifyDirectory)
        self.directoryLine.move(20, 35)
        self.directoryLine.resize(220, 25)

        self.directoryButton = QPushButton('Folder...', self)
        self.directoryButton.move(240, 35)
        self.directoryButton.resize(60, 25)
        self.directoryButton.pressed.connect(self.dirButton)

        self.directoryStatusLabel = QLabel(self)
        self.directoryStatusLabel.move(20, 60)
        self.directoryStatusLabel.resize(280, 20)

        self.fileTypeSelection = QComboBox(self)
        self.fileTypeSelection.move(20, 85)
        self.fileTypeSelection.resize(280, 25)
        self.populateComboBox()

        self.deleteOption = QCheckBox("Delete after convert?", self)
        self.deleteOption.move(20, 107)
        self.deleteOption.resize(280, 32)

        self.convertLog = QPlainTextEdit(self)
        self.convertLog.setReadOnly(True)
        self.convertLog.move(20, 135)
        self.convertLog.resize(280, 100)

        self.startButton = QPushButton('Start', self)
        self.startButton.clicked.connect(self.startConversion)
        self.startButton.move(200, 240)
        self.startButton.resize(100, 32)
        self.startButton.setDisabled(True)

    def dirButton(self):
        dir = QFileDialog().getExistingDirectory(self, "Choose Directory")
        print(dir)
        self.directoryLine.setText(dir)

    def populateComboBox(self):
        for item in FT:
            self.fileTypeSelection.addItem(item.name)

    def toggleButton(self, value):
        self.startButton.setDisabled(not value)

    def verifyDirectory(self, text):
        if len(text) == 0:
            self.directoryStatusLabel.setText('')
            self.verifyCheck = False
            return

        try:
            files = converter.scanFiles(text)
            if len(files) > 0:
                self.verifyCheck = True
                self.directoryStatusLabel.setStyleSheet("color: black")
                self.directoryStatusLabel.setText(
                    "Files Found: " + str(len(files)))
            else:
                self.verifyCheck = False
                self.directoryStatusLabel.setStyleSheet("color: red")
                self.directoryStatusLabel.setText("No files found")
        except Exception as e:
            self.verifyCheck = False
            self.directoryStatusLabel.setStyleSheet("color: red")
            self.directoryStatusLabel.setText("Error: Directory not found")

        self.toggleButton(self.verifyCheck)

    def startConversion(self):
        files = []
        if self.verifyCheck:
            files = self.findFiles()
            self.convertLog.insertPlainText(
                "Begining Conversion on " + self.directoryLine.text() + "\n")
            if self.deleteOption.isChecked():
                confirmBox = QMessageBox.question(self,
                                                  'Delete Files?',
                                                  'Do you want to delete files?',
                                                  QMessageBox.Yes | QMessageBox.No,
                                                  QMessageBox.No)

                if confirmBox == QMessageBox.Yes:
                    for item in files:
                        converter.convert(self.directoryLine.text(),
                                          item, FT[self.fileTypeSelection.currentText()])
                        self.convertLog.insertPlainText(
                            "Deleting " + item + "\n")
                        converter.deleteFile(
                            self.directoryLine.text(), item)

                    self.convertLog.insertPlainText("Conversions Finished!\n")

                else:
                    self.convertLog.insertPlainText(
                        "Conversion cancelled...\n")
            else:
                newFolderMessage = QMessageBox()
                newFolderMessage.setWindowTitle("Files will be moved")
                newFolderMessage.setText(
                    "Converted files will move to folder named WEBP within the directory.\nFolder will be made if none exist")
                newFolderMessage.exec_()

                files = self.findFiles()
                for item in files:
                    self.convertLog.insertPlainText("Moving " + item + "\n")
                    converter.convert(self.directoryLine.text(),
                                      item, FT[self.fileTypeSelection.currentText()])
                    converter.moveFile(self.directoryLine.text(), item)
                    self.convertLog.insertPlainText("Files Moved to " +
                                                    self.directoryLine.text() + '/WEBP\n')
                self.convertLog.insertPlainText("Conversions Finished!\n")

            self.convertLog.verticalScrollBar().setValue(
                self.convertLog.verticalScrollBar().maximum())
            self.verifyCheck = False

    def findFiles(self):
        temp = []
        for filename in os.listdir(self.directoryLine.text()):
            if filename.endswith(".webp"):
                temp.append(filename)

        return temp


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    sys.exit(app.exec_())
