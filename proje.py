from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import os
from datetime import datetime
import shutil


class FileEditGUİ(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(400, 100)
        self.setWindowTitle("Klasörleyici")

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setText("")

        self.FileButon = QPushButton(self)
        self.FileButon.setText("Gözat...")

        self.label = QLabel(self)
        self.label.setText("Klasörleme Ölçütü")

        self.buton = QPushButton(self)
        self.buton.setText("Klasörle")

        self.comboBox = QComboBox(self)
        self.comboBox.addItems(["Yıl", "Yıl-Ay", "Yıl-Ay-Gün"])

        self.uyariAksiyonu = QAction(self)
        self.uyariAksiyonu.setText("Uyarı")

        self.uyariAksiyonu.triggered.connect(self.uyariKutusuGoster)

        layout = QGridLayout()
        layout.addWidget(self.lineEdit, 0, 0)
        layout.addWidget(self.FileButon, 0, 1)
        layout.addWidget(self.label, 1, 0)
        layout.addWidget(self.comboBox, 2, 0)
        layout.addWidget(self.buton, 3, 0)

        self.setLayout(layout)

        self.file = FileEdit()

        self.FileButon.clicked.connect(self.gozat)
        self.buton.clicked.connect(self.hangiCombobox)
        self.buton.clicked.connect(self.klasorle)

    def uyariKutusuGoster(self):
        QMessageBox.warning(self, "Uyarı", "Lütfen  geçerli bir dizin seçin")

    def hangiCombobox(self):
        if self.comboBox.currentIndex() == 0:
            self.file.choose = '%Y'
        elif self.comboBox.currentIndex() == 1:
            self.file.choose = '%Y-%m'
        elif self.comboBox.currentIndex() == 2:
            self.file.choose = '%Y-%m-%d'

    def gozat(self):
        dosya = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.lineEdit.setText(dosya)
        try:
            self.file.main_directory = self.lineEdit.text() + "/"

        except:
            self.uyariKutusuGoster()

    def klasorle(self):
        if os.path.isdir(self.file.main_directory):
            self.file.get_folder_path(self.file.main_directory)
            self.file.create_dir()
        else:
            self.uyariKutusuGoster()

class FileEdit:
    def __init__(self):
        self.file_path = []
        self.main_directory = ""
        self.choose = ""

    def last_motified_time(self, path, choose):
        file_stat = os.stat(path)
        last_motified_time = datetime.fromtimestamp(int(file_stat.st_mtime)).strftime(choose)
        return last_motified_time

    def create_dir(self):
        for i in self.file_path:
            full_path = self.main_directory + self.last_motified_time(i, self.choose)
            if not os.path.exists(full_path):
                os.mkdir(full_path)
            shutil.move(i, full_path)

    def get_folder_path(self, main_directory):
        for i in os.listdir(main_directory):
            if os.path.isfile(main_directory + i):
                self.file_path.append(main_directory + i)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileEditGUİ()
    window.show()
    app.exec_()

