from PyQt6.QtWidgets import QMainWindow, QMessageBox, QWidget, QVBoxLayout, QLabel, QPushButton, QInputDialog, QHBoxLayout
from PyQt6.QtCore import Qt
from models.library_operations import get_books_on_loan, get_client_ids, get_largest_fine, get_client_fine, get_top_3_books_all_time
from ui.login_window import LoginWindow

class MainWindow(QMainWindow):
    def __init__(self, username, role):
        super().__init__()
        self.username = username
        self.role = role
        self.setWindowTitle("Библиотечная система управления")
        self.resize(800, 600)

        self.initUI()

    def initUI(self):
        self.set_initial_widget()
        self.apply_styles()

    def set_initial_widget(self):
        initial_widget = QWidget()
        layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        welcome_label = QLabel("Добро пожаловать в систему управления библиотекой!")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_layout.addWidget(welcome_label)

        self.username_label = QLabel(f"Пользователь: {self.username}")
        self.username_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        top_layout.addWidget(self.username_label)

        layout.addLayout(top_layout)

        if self.role == "admin":
            clients_button = QPushButton("Управление клиентами")
            clients_button.clicked.connect(self.show_clients)
            layout.addWidget(clients_button)

            books_button = QPushButton("Управление книгами")
            books_button.clicked.connect(self.show_books)
            layout.addWidget(books_button)

            book_types_button = QPushButton("Управление типами книг")
            book_types_button.clicked.connect(self.show_book_types)
            layout.addWidget(book_types_button)

            journal_button = QPushButton("Журнал выдачи книг")
            journal_button.clicked.connect(self.show_journal)
            layout.addWidget(journal_button)

            self.books_on_loan_button = QPushButton("Число книг на руках у клиента")
            self.books_on_loan_button.clicked.connect(self.show_books_on_loan)
            layout.addWidget(self.books_on_loan_button)

            self.largest_fine_button = QPushButton("Размер самого большого штрафа")
            self.largest_fine_button.clicked.connect(self.show_largest_fine)
            layout.addWidget(self.largest_fine_button)

            self.client_fine_button = QPushButton("Размер штрафа данного клиента")
            self.client_fine_button.clicked.connect(self.show_client_fine)
            layout.addWidget(self.client_fine_button)

            self.top_books_all_time_button = QPushButton("Три самые популярные книги за все время")
            self.top_books_all_time_button.clicked.connect(self.show_top_books_all_time)
            layout.addWidget(self.top_books_all_time_button)

            self.logout_button = QPushButton("Выйти")
            self.logout_button.setObjectName("logout_button")
            self.logout_button.clicked.connect(self.handle_logout)
            layout.addWidget(self.logout_button)
        else:
            QMessageBox.warning(self, "Доступ закрыт", "У вас нет прав доступа к этой системе")

        initial_widget.setLayout(layout)
        self.setCentralWidget(initial_widget)

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 16px;
                color: #333;
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
            QPushButton#logout_button {
                background-color: #B22222;  /* FireBrick color */
            }
            QPushButton#logout_button:hover {
                background-color: #CD5C5C;  /* IndianRed */
            }
            QPushButton#logout_button:pressed {
                background-color: #8B0000;  /* DarkRed */
            }
            QMessageBox, QInputDialog {
                background-color: #ffffff;  /* White background */
                color: #000000;  /* Black text */
            }
            QComboBox {
                background-color: #e0e0e0;  /* Light grey background for specific QComboBox */
                color: #000000;  /* Black text */
                font-size: 14px;
                padding: 0 15px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: #e0e0e0;  /* Light grey background for specific QComboBox */
                color: #000000;  /* Black text */
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QComboBox::item:selected {
                background-color: #6A5ACD;  /* SlateBlue color for selected item */
                color: #ffffff;  /* White text for selected item */
            }
            QComboBox::item {
                color: #000000;  /* Black text for all items */
            }
        """)

    def show_clients(self):
        from ui.clients_view import ClientsView
        self.clients_view = ClientsView(self)
        self.setCentralWidget(self.clients_view)

    def show_books(self):
        from ui.books_view import BooksView
        self.books_view = BooksView(self)
        self.setCentralWidget(self.books_view)

    def show_book_types(self):
        from ui.book_types_view import BookTypesView
        self.book_types_view = BookTypesView(self)
        self.setCentralWidget(self.book_types_view)

    def show_journal(self):
        from ui.journal_view import JournalView
        self.journal_view = JournalView(self)
        self.setCentralWidget(self.journal_view)

    def show_books_on_loan(self):
        client_ids = get_client_ids()
        client_id, ok = QInputDialog.getItem(self, "Выбор клиента", "Выберите ID клиента:", map(str, client_ids), 0, False)
        if ok and client_id:
            books_on_loan = get_books_on_loan(client_id)
            QMessageBox.information(self, "Число книг на руках у клиента", f"Число книг на руках у клиента: {books_on_loan}")

    def show_largest_fine(self):
        client_id, largest_fine = get_largest_fine()
        if client_id:
            QMessageBox.information(self, "Информация о штрафе", f"ID Клиента: {client_id}, Размер самого большого штрафа: {largest_fine}")

    def show_client_fine(self):
        client_ids = get_client_ids()
        client_id, ok = QInputDialog.getItem(self, "Выбор клиента", "Выберите ID клиента:", map(str, client_ids), 0, False)
        if ok and client_id:
            client_fine = get_client_fine(client_id)
            QMessageBox.information(self, "Размер штрафа данного клиента", f"Размер штрафа данного клиента: {client_fine}")

    def show_top_books_all_time(self):
        try:
            top_books = get_top_3_books_all_time()
            if top_books:
                top1_id, top1_count, top2_id, top2_count, top3_id, top3_count = top_books
                QMessageBox.information(self, "Tоп 3 популярных книг", f"1: {top1_id}, Количество выдач: {top1_count}\n2: {top2_id}, Количество выдач: {top2_count}\n3: {top3_id}, Количество выдач: {top3_count}")
            else:
                QMessageBox.information(self, "Tоп 3 популярных книг", "Нет информации")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка: {e}")

    def handle_logout(self):
        self.username = None
        self.role = None
        self.close()
        self.show_login_window()

    def show_login_window(self):
        login_window = LoginWindow()
        if login_window.exec():
            self.username = login_window.username
            self.role = login_window.user_role
            self.initUI()
            self.show()