from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QHBoxLayout, QLabel, QComboBox, QMessageBox, QHeaderView
from models.library_operations import fetch_books, add_book, update_book, delete_book, get_book_type_ids
import PyQt6.QtGui as QtGui
import PyQt6.QtCore as QtCore

class BooksView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Управление книгами")
        self.resize(800, 600)
        self.apply_styles()

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Количество", "ID Типа Редкости"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        self.load_books()

        form_layout = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Название")
        form_layout.addWidget(self.name_input)

        self.count_input = QLineEdit()
        self.count_input.setPlaceholderText("Количество")
        count_validator = QtGui.QRegularExpressionValidator(QtCore.QRegularExpression(r"\d{0,4}"))
        self.count_input.setValidator(count_validator)
        form_layout.addWidget(self.count_input)

        form_layout.addWidget(QLabel("Тип редкости:"))
        self.type_id_input = QComboBox()
        self.type_id_input.setObjectName("type_id_input")
        self.type_id_input.addItems(map(str, get_book_type_ids()))
        form_layout.addWidget(self.type_id_input)

        layout.addLayout(form_layout)

        self.add_button = QPushButton("Добавить книгу")
        self.add_button.clicked.connect(self.add_book)
        layout.addWidget(self.add_button)

        self.update_button = QPushButton("Обновить данные")
        self.update_button.clicked.connect(self.update_book)
        layout.addWidget(self.update_button)

        self.delete_button = QPushButton("Удалить книгу")
        self.delete_button.clicked.connect(self.delete_book)
        layout.addWidget(self.delete_button)

        self.back_button = QPushButton("Назад")
        self.back_button.setObjectName("back_button")
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

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
            QComboBox {
                background-color: #e0e0e0;  
                color: #000000; 
                font-size: 14px;
                padding: 0 15px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: #e0e0e0; 
                color: #000000; 
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QComboBox::item:selected {
                background-color: #6A5ACD; 
                color: #ffffff; 
            }
            QComboBox::item {
                color: #000000; 
            }
            QComboBox#type_id_input {
                background-color: #e0e0e0;
                color: #000000; 
            }
        """)

    def load_books(self):
        books = fetch_books()
        books.sort(key=lambda x: x[0])
        self.table.setRowCount(len(books))
        for row_idx, (book_id, name, cnt, type_id) in enumerate(books):
            self.table.setItem(row_idx, 0, self.create_centered_item(str(book_id)))
            self.table.setItem(row_idx, 1, self.create_centered_item(str(name)))
            self.table.setItem(row_idx, 2, self.create_centered_item(str(cnt)))
            self.table.setItem(row_idx, 3, self.create_centered_item(str(type_id)))

    def create_centered_item(self, text):
        item = QTableWidgetItem(text)
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        return item

    def add_book(self):
        name = self.name_input.text()
        count = self.count_input.text()
        type_id = self.type_id_input.currentText()

        if not name or not count or not type_id:
            QMessageBox.critical(self, "Ошибка", "Все поля должны быть заполнены.")
            return

        try:
            add_book(name, count, type_id)
            self.load_books()
            QMessageBox.information(self, "Успех", "Книга успешно добавлена.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", "Произошла ошибка при добавлении книги.")

    def update_book(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            book_id = int(self.table.item(selected_row, 0).text())
            name = self.name_input.text()
            count = self.count_input.text()
            type_id = self.type_id_input.currentText()
            update_book(book_id, name, count, type_id)
            self.load_books()

    def delete_book(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            book_id = int(self.table.item(selected_row, 0).text())
            delete_book(book_id)
            self.load_books()

    def go_back(self):
        self.main_window.set_initial_widget()