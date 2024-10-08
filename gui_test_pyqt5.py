import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QScrollArea, QCheckBox, QPushButton, QFormLayout

class ScrollableWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Scrollable Checkbox List')
        self.setGeometry(100, 100, 300, 400)

        # Main layout
        layout = QVBoxLayout(self)

        # Scroll Area
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        # Widget that holds the list
        container_widget = QWidget()
        scroll_area.setWidget(container_widget)

        # Form layout for checkboxes
        self.form_layout = QFormLayout(container_widget)

        # Add checkboxes
        self.checkboxes = []
        elements = ['Element 1', 'Element 2', 'Element 3', 'Element 4', 'Element 5']
        for element in elements:
            checkbox = QCheckBox(element)
            checkbox.setChecked(True)  # Set default as checked
            self.checkboxes.append(checkbox)
            self.form_layout.addWidget(checkbox)

        # Add Remove Button
        remove_button = QPushButton('Remove Unchecked Items')
        remove_button.clicked.connect(self.remove_unchecked_items)
        layout.addWidget(remove_button)

    def remove_unchecked_items(self):
        # Remove unchecked items from the form layout
        for checkbox in self.checkboxes[:]:
            if not checkbox.isChecked():
                self.form_layout.removeWidget(checkbox)
                checkbox.deleteLater()
                self.checkboxes.remove(checkbox)

        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ScrollableWindow()
    window.show()
    sys.exit(app.exec_())
