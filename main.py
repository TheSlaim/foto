from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from ui import Ui_MainWindow
from PIL import Image, ImageEnhance
import os

class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.image_folder = None
        self.current_image_path = None  # Шлях до вибраного зображення
        self.image = None  # Об'єкт PIL.Image

        self.ui.pushButton.clicked.connect(self.load_images)
        self.ui.listView.clicked.connect(self.load_selected_image)
        self.ui.pushButton_2.clicked.connect(self.rotate_left)
        self.ui.pushButton_3.clicked.connect(self.rotate_right)
        self.ui.pushButton_4.clicked.connect(self.mirror_image)
        self.ui.pushButton_5.clicked.connect(self.sharpen_image)
        self.ui.pushButton_6.clicked.connect(self.to_grayscale)
        # self.ui.pushButton_7.clicked.connect(self.adjust_color)

        # Налаштування моделі для QListView
        self.model = QtGui.QStandardItemModel()
        self.ui.listView.setModel(self.model)

    def load_images(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Виберіть папку з фотографіями")

        if folder:
            self.image_folder = folder
            self.display_images()

    def display_images(self):
        self.model.clear()
        valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']

        for file_name in os.listdir(self.image_folder):
            if any(file_name.lower().endswith(ext) for ext in valid_extensions):
                item = QtGui.QStandardItem(file_name)
                item.setEditable(False)
                self.model.appendRow(item)

    def load_selected_image(self, index):
        file_name = self.model.itemFromIndex(index).text()
        self.current_image_path = os.path.join(self.image_folder, file_name)
        self.image = Image.open(self.current_image_path)
        self.display_image()

    def display_image(self):
        if self.image:
            try:
                # Конвертація PIL.Image у QPixmap через QImage
                image_data = self.image.convert("RGBA")
                data = image_data.tobytes("raw", "RGBA")
                qimage = QtGui.QImage(data, image_data.width, image_data.height, QtGui.QImage.Format_RGBA8888)
                pixmap = QPixmap.fromImage(qimage)

                # Обмеження розмірів зображення до розмірів головного вікна
                max_width = self.width() - 140
                max_height = self.height() - 80
                pixmap = pixmap.scaled(max_width, max_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

                # Створення QLabel, якщо ще не створено
                if not hasattr(self, "image_label"):
                    self.image_label = QtWidgets.QLabel(self.ui.widget_2)
                    self.image_label.setAlignment(Qt.AlignCenter)
                    self.image_label.setScaledContents(False)

                # Встановлюємо відмасштабоване зображення
                self.image_label.setPixmap(pixmap)

                # Центруємо зображення у віджеті та масштабуємо QLabel під розміри зображення
                self.ui.widget_2.setFixedSize(pixmap.width(), pixmap.height())
                self.image_label.setGeometry(80, 40, pixmap.width(), pixmap.height())
                self.image_label.show()

            except Exception as e:
                print(f"Error displaying image: {e}")

    def save_image(self):
        if self.image and self.current_image_path:
            self.image.save(self.current_image_path)

    def rotate_left(self):
        if self.image:
            self.image = self.image.rotate(90, expand=True)
            self.display_image()
            self.save_image()

    def rotate_right(self):
        if self.image:
            self.image = self.image.rotate(-90, expand=True)
            self.display_image()
            self.save_image()

    def mirror_image(self):
        if self.image:
            self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
            self.display_image()
            self.save_image()

    def sharpen_image(self):
        if self.image:
            enhancer = ImageEnhance.Sharpness(self.image)
            self.image = enhancer.enhance(2.0)
            self.display_image()
            self.save_image()

    def to_grayscale(self):
        if self.image:
            self.image = self.image.convert("L")
            self.display_image()
            self.save_image()

    def adjust_color(self):
        if self.image:
            enhancer = ImageEnhance.Color(self.image)
            self.image = enhancer.enhance(1,5)
            self.display_image()
            self.save_image()



if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainApp()
    mainWindow.show()
    sys.exit(app.exec_())