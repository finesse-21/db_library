from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
from PyQt6.QtCore import Qt
from models.authentication import authenticate_user, register_user

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Авторизация")
        self.resize(400, 200)

        self.initUI()
        self.apply_styles()

    def initUI(self):
        layout = QVBoxLayout()

        welcome_label = QLabel("Добро пожаловать в систему управления библиотекой!")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Логин")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        button_layout = QHBoxLayout()
        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.handle_login)
        button_layout.addWidget(self.login_button)

        self.register_button = QPushButton("Регистрация")
        self.register_button.clicked.connect(self.handle_registration)
        button_layout.addWidget(self.register_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def apply_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 16px;
                color: #333;
            }
            QLineEdit {
                font-size: 14px;
                background-color: #e6e6e6;
                color: #333;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
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
            QPushButton#cancel_button {
                background-color: #B22222;  /* FireBrick color */
            }
            QPushButton#cancel_button:hover {
                background-color: #CD5C5C;  /* IndianRed */
            }
            QPushButton#cancel_button:pressed {
                background-color: #8B0000;  /* DarkRed */
            }
        """)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        role, message = authenticate_user(username, password)
        if role:
            QMessageBox.information(self, "Авторизация", message)
            self.username = username
            self.user_role = role
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка", message)

    def handle_registration(self):
        username = self.username_input.text()
        password = self.password_input.text()

        success, message = register_user(username, password)
        if success:
            QMessageBox.information(self, "Регистрация", message)
        else:
            QMessageBox.warning(self, "Ошибка", message)