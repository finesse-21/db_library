from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QHBoxLayout, QMessageBox, QHeaderView
from models.library_operations import fetch_clients, add_client, update_client, delete_client
import PyQt6.QtGui as QtGui
import PyQt6.QtCore as QtCore

class ClientsView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Управление клиентами")
        self.resize(800, 600)
        self.apply_styles()

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Имя", "Фамилия", "Отчество", "Серия паспорта", "Номер паспорта"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        self.load_clients()

        form_layout = QHBoxLayout()
        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("Имя")
        form_layout.addWidget(self.first_name_input)
        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Фамилия")
        form_layout.addWidget(self.last_name_input)
        self.father_name_input = QLineEdit()
        self.father_name_input.setPlaceholderText("Отчество")
        form_layout.addWidget(self.father_name_input)

        # Поле "Серия паспорта" (только цифры, максимум 4 символа)
        self.passport_seria_input = QLineEdit()
        self.passport_seria_input.setPlaceholderText("Серия паспорта")
        seria_validator = QtGui.QRegularExpressionValidator(QtCore.QRegularExpression(r"\d{0,4}"))
        self.passport_seria_input.setValidator(seria_validator)
        form_layout.addWidget(self.passport_seria_input)

        # Поле "Номер паспорта" (только цифры, максимум 6 символов)
        self.passport_number_input = QLineEdit()
        self.passport_number_input.setPlaceholderText("Номер паспорта")
        number_validator = QtGui.QRegularExpressionValidator(QtCore.QRegularExpression(r"\d{0,6}"))
        self.passport_number_input.setValidator(number_validator)
        form_layout.addWidget(self.passport_number_input)

        layout.addLayout(form_layout)

        self.add_button = QPushButton("Добавить клиента")
        self.add_button.clicked.connect(self.add_client)
        layout.addWidget(self.add_button)

        self.update_button = QPushButton("Обновить данные")
        self.update_button.clicked.connect(self.update_client)
        layout.addWidget(self.update_button)

        self.delete_button = QPushButton("Удалить клиента")
        self.delete_button.clicked.connect(self.delete_client)
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
                background-color: #ffffff;  /* White background */
                alternate-background-color: #f9f9f9;  /* Light grey for alternate rows */
                color: #000000;  /* Black text */
                gridline-color: #cccccc;  /* Light grey grid lines */
            }
            QHeaderView::section {
                background-color: #6A5ACD;  /* SlateBlue color */
                color: white;  /* White text */
                font-size: 14px;
                padding: 5px;
            }
            QLineEdit {
                font-size: 14px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #e6e6e6;  /* Light grey background */
                color: #333;  /* Dark grey text */
            }
            QPushButton {
                font-size: 14px;
                padding: 10px;
                background-color: #6A5ACD;  /* SlateBlue color */
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #836FFF;  /* MediumSlateBlue */
            }
            QPushButton:pressed {
                background-color: #483D8B;  /* DarkSlateBlue */
            }
            QPushButton#back_button {
                background-color: #B22222;  /* FireBrick color */
            }
            QPushButton#back_button:hover {
                background-color: #CD5C5C;  /* IndianRed */
            }
            QPushButton#back_button:pressed {
                background-color: #8B0000;  /* DarkRed */
            }
            QComboBox {
                background-color: #ffffff;  /* White background */
                color: #333;  /* Dark grey text */
                font-size: 14px;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
        """)

    def load_clients(self):
        clients = fetch_clients()
        clients.sort(key=lambda x: x[0])
        self.table.setRowCount(len(clients))
        for row_idx, (client_id, first_name, last_name, father_name, passport_seria, passport_number) in enumerate(
                clients):
            self.table.setItem(row_idx, 0, self.create_centered_item(str(client_id)))
            self.table.setItem(row_idx, 1, self.create_centered_item(str(first_name)))
            self.table.setItem(row_idx, 2, self.create_centered_item(str(last_name)))
            self.table.setItem(row_idx, 3, self.create_centered_item(str(father_name)))
            self.table.setItem(row_idx, 4, self.create_centered_item(str(passport_seria)))
            self.table.setItem(row_idx, 5, self.create_centered_item(str(passport_number)))

    def create_centered_item(self, text):
        item = QTableWidgetItem(text)
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        return item

    def add_client(self):

        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        father_name = self.father_name_input.text()
        passport_seria = self.passport_seria_input.text()
        passport_number = self.passport_number_input.text()

        if not first_name or not last_name or not passport_seria or not passport_number:
            QMessageBox.critical(self, "Ошибка", "Все поля должны быть заполнены.")
            return

        try:
            add_client(first_name, last_name, father_name, passport_seria, passport_number)
            self.load_clients()
            QMessageBox.information(self, "Успех", "Клиент успешно добавлен.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", "Пользователь с данной серией и номером паспорта уже существует.")

    def update_client(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            client_id = int(self.table.item(selected_row, 0).text())
            first_name = self.first_name_input.text()
            last_name = self.last_name_input.text()
            father_name = self.father_name_input.text()
            passport_seria = self.passport_seria_input.text()
            passport_number = self.passport_number_input.text()
            update_client(client_id, first_name, last_name, father_name, passport_seria, passport_number)
            self.load_clients()

    def delete_client(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            client_id = int(self.table.item(selected_row, 0).text())
            delete_client(client_id)
            self.load_clients()

    def go_back(self):
        self.main_window.set_initial_widget()