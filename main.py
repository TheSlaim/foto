from PyQt5 import QtWidgets, QtGui
from ui import Ui_MainWindow
import sys
import os

class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.image_folder = None

        self.ui.pushButton.clicked.connect(self.load_images)

        # Налаштування моделі для QListView
        self.model = QtGui.QStandardItemModel()
        self.ui.listView.setModel(self.model)

    def load_images(self):
        # Відкрити діалог для вибору папки
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Виберіть папку з фотографіями")

        if folder:  # Якщо вибрано папку
            self.image_folder = folder
            self.display_images()

    def display_images(self):
        # Очищення списку
        self.model.clear()

        # Допустимі формати зображень
        valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']

        for file_name in os.listdir(self.image_folder):
            if any(file_name.lower().endswith(ext) for ext in valid_extensions):
                # Додати зображення до моделі QListView
                item = QtGui.QStandardItem(file_name)
                item.setEditable(False)
                self.model.appendRow(item)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindows = MainApp()
    mainWindows.show()
    sys.exit(app.exec_())