from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QWidget, QDialog, QLineEdit, QDialogButtonBox, QPushButton, QFormLayout, QMessageBox
from models.library_operations import fetch_book_types, add_book_type, delete_book_type, update_book_type
from PyQt6.QtGui import QIntValidator

class BookTypesView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Типы книг")
        self.resize(600, 400)

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Type", "Fine", "Day Count"])
        layout.addWidget(self.table)

        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Добавить тип")
        self.add_button.clicked.connect(self.add_type)
        button_layout.addWidget(self.add_button)

        self.delete_button = QPushButton("Удалить тип")
        self.delete_button.clicked.connect(self.delete_type)
        button_layout.addWidget(self.delete_button)

        self.update_button = QPushButton("Обновить тип")
        self.update_button.clicked.connect(self.update_type)
        button_layout.addWidget(self.update_button)

        self.back_button = QPushButton("Назад")
        self.back_button.setObjectName("back_button")
        self.back_button.clicked.connect(self.go_back)
        button_layout.addWidget(self.back_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)
        self.apply_styles()
        self.load_book_types()

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 16px;
                color: #333;
            }
            QTableWidget {
                background-color: #ffffff;
                alternate-background-color: #f9f9f9;
                color: #000000;
                gridline-color: #cccccc;
            }
            QHeaderView::section {
                background-color: #6A5ACD;
                color: white;
                font-size: 14px;
                padding: 5px;
            }
            QLineEdit {
                font-size: 14px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #e6e6e6;
                color: #333;
            }
            QPushButton {
                font-size: 14px;
                padding: 10px;
                background-color: #6A5ACD;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #836FFF;
            }
            QPushButton:pressed {
                background-color: #483D8B;
            }
            QPushButton#back_button {
                background-color: #B22222;
            }
            QPushButton#back_button:hover {
                background-color: #CD5C5C;
            }
            QPushButton#back_button:pressed {
                background-color: #8B0000;
            }
        """)

    def load_book_types(self):
        types = fetch_book_types()
        self.table.setRowCount(len(types))

        for row_idx, (type_id, type_name, fine, day_count) in enumerate(types):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(type_id)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(type_name))
            self.table.setItem(row_idx, 2, QTableWidgetItem(str(fine)))
            self.table.setItem(row_idx, 3, QTableWidgetItem(str(day_count)))

    def update_type(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Обновить тип")
        layout = QFormLayout(dialog)
        type_id = int(self.table.item(selected_row, 0).text())

        type_input = QLineEdit(self.table.item(selected_row, 1).text())
        layout.addRow("Тип:", type_input)

        fine_input = QLineEdit(self.table.item(selected_row, 2).text())
        fine_input.setValidator(QIntValidator())
        layout.addRow("Штраф:", fine_input)

        day_count_input = QLineEdit(self.table.item(selected_row, 3).text())
        day_count_input.setValidator(QIntValidator())
        layout.addRow("Количество дней:", day_count_input)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            type_name = type_input.text()
            fine = int(fine_input.text())
            day_count = int(day_count_input.text())
            update_book_type(type_id, type_name, fine, day_count)
            self.load_book_types()

    def delete_type(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            return

        type_id = int(self.table.item(selected_row, 0).text())
        delete_book_type(type_id)
        self.load_book_types()

    def add_type(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить тип")
        layout = QFormLayout(dialog)

        type_input = QLineEdit()
        layout.addRow("Тип:", type_input)

        fine_input = QLineEdit()
        fine_input.setValidator(QIntValidator())
        layout.addRow("Штраф:", fine_input)

        day_count_input = QLineEdit()
        day_count_input.setValidator(QIntValidator())
        layout.addRow("Количество дней:", day_count_input)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            type_name = type_input.text()
            fine = int(fine_input.text())
            day_count = int(day_count_input.text())
            add_book_type(type_name, fine, day_count)
            self.load_book_types()

    def go_back(self):
        self.main_window.set_initial_widget()