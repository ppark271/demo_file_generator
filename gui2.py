import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QHBoxLayout
from PyQt5.QtGui import QPixmap

class FileImageInputWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('File and Image Input')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout(self)

        # File input section
        file_layout = QHBoxLayout()
        self.file_label = QLabel("No file selected")
        file_button = QPushButton("Select File")
        file_button.clicked.connect(self.select_file)
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(file_button)
        layout.addLayout(file_layout)

        # Image input section
        image_layout = QVBoxLayout()
        self.image_label = QLabel("No image selected")
        self.image_label.setFixedSize(200, 200)  # Set the size of the image display area
        self.image_label.setStyleSheet("border: 1px solid black;")  # Add a border to the image label
        image_button = QPushButton("Select Image")
        image_button.clicked.connect(self.select_image)
        image_layout.addWidget(self.image_label)
        image_layout.addWidget(image_button)
        layout.addLayout(image_layout)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)")
        if file_path:
            self.file_label.setText(file_path)

    def select_image(self):
        image_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.bmp)")
        if image_path:
            pixmap = QPixmap(image_path)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size()))  # Resize to fit the label size

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileImageInputWindow()
    window.show()
    sys.exit(app.exec_())
