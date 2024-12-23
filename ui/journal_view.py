from PyQt6.QtWidgets import QMessageBox, QPushButton, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QWidget, QComboBox, QDialog, QLabel, QLineEdit, QDialogButtonBox, QFormLayout, QHeaderView, QFileDialog
from datetime import datetime, timedelta
from models.library_operations import update_journal_entry, get_book_type_and_count, add_journal_entry, fetch_journal_entries, delete_journal_entry, get_client_ids, get_book_ids, get_journal_entry_ids, update_journal_return

class JournalView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Журнал библиотекаря")
        self.resize(600, 400)

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "ID Клиента", "ID Книги", "Дата выдачи", "Выдано до", "Дата возврата"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Добавить запись")
        self.add_button.clicked.connect(self.add_entry)
        button_layout.addWidget(self.add_button)

        self.delete_button = QPushButton("Удалить запись")
        self.delete_button.clicked.connect(self.delete_entry)
        button_layout.addWidget(self.delete_button)

        self.update_button = QPushButton("Обновить запись")
        self.update_button.clicked.connect(self.update_entry)
        button_layout.addWidget(self.update_button)

        self.return_button = QPushButton("Оформить возврат")
        self.return_button.clicked.connect(self.add_return)
        button_layout.addWidget(self.return_button)

        self.report_button = QPushButton("Создать отчет")
        self.report_button.clicked.connect(self.create_report)
        layout.addWidget(self.report_button)

        self.back_button = QPushButton("Назад")
        self.back_button.setObjectName("back_button")
        self.back_button.clicked.connect(self.go_back)
        button_layout.addWidget(self.back_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)
        self.apply_styles()
        self.load_journal_entries()

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

    def load_journal_entries(self):
        entries = fetch_journal_entries()
        entries.sort(key=lambda x: x[0])
        self.table.setRowCount(len(entries))

        for row_idx, (entry_id, client_id, book_id, date_beg, date_end, date_ret) in enumerate(entries):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(entry_id)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(str(client_id)))
            self.table.setItem(row_idx, 2, QTableWidgetItem(str(book_id)))
            self.table.setItem(row_idx, 3, QTableWidgetItem(str(date_beg)))
            self.table.setItem(row_idx, 4, QTableWidgetItem(str(date_end)))
            self.table.setItem(row_idx, 5, QTableWidgetItem(str(date_ret)))

    def add_entry(self):
        client_ids = get_client_ids()
        book_ids = get_book_ids()

        if not client_ids or not book_ids:
            QMessageBox.critical(self, "Ошибка", "Не удалось загрузить список клиентов или книг")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить запись")
        layout = QVBoxLayout(dialog)

        layout.addWidget(QLabel("Выберите ID Клиента:"))
        client_combo = QComboBox()
        client_combo.addItems(map(str, client_ids))
        layout.addWidget(client_combo)

        layout.addWidget(QLabel("Выберите ID Книги:"))
        book_combo = QComboBox()
        book_combo.addItems(map(str, book_ids))
        layout.addWidget(book_combo)

        add_button = QPushButton("Добавить")
        add_button.clicked.connect(dialog.accept)
        layout.addWidget(add_button)

        if not dialog.exec():
            return

        client_id = client_combo.currentText()
        book_id = book_combo.currentText()
        date_beg = datetime.now().strftime("%Y-%m-%d")

        book_type, book_cnt = get_book_type_and_count(book_id)
        if book_cnt == 0:
            QMessageBox.critical(self, "Ошибка", "Книг нет в наличии")
            return

        if book_type == 1:
            date_end = datetime.strptime(date_beg, "%Y-%m-%d") + timedelta(days=60)
        elif book_type == 2:
            date_end = datetime.strptime(date_beg, "%Y-%m-%d") + timedelta(days=21)
        elif book_type == 3:
            date_end = datetime.strptime(date_beg, "%Y-%m-%d") + timedelta(days=7)
        else:
            date_end = None

        if date_end:
            date_end = date_end.strftime("%Y-%m-%d")

        date_ret = None

        try:
            add_journal_entry(client_id, book_id, date_beg, date_end, date_ret)
        except Exception as e:
            if "Client already has 10 or more books issued" in str(e):
                QMessageBox.critical(self, "Ошибка", "У данного клиента уже взято 10 книг")
            else:
                QMessageBox.critical(self, "Ошибка", f"Ошибка добавления записи журнала: {e}")
        self.load_journal_entries()

    def delete_entry(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            return

        entry_id = int(self.table.item(selected_row, 0).text())

        error_message = delete_journal_entry(entry_id)
        if error_message:
            QMessageBox.critical(self, "Ошибка", error_message)
        self.load_journal_entries()

    def update_entry(self):
        client_ids = get_client_ids()
        book_ids = get_book_ids()
        selected_row = self.table.currentRow()
        if selected_row < 0:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Обновить запись")
        layout = QFormLayout(dialog)
        entry_id = int(self.table.item(selected_row, 0).text())

        client_combo = QComboBox()
        client_combo.addItems(map(str, client_ids))
        client_combo.setCurrentText(self.table.item(selected_row, 1).text())
        layout.addRow("Выберите ID Клиента:", client_combo)

        book_combo = QComboBox()
        book_combo.addItems(map(str, book_ids))
        book_combo.setCurrentText(self.table.item(selected_row, 2).text())
        layout.addRow("Выберите ID Книги:", book_combo)

        date_beg_input = QLineEdit(self.table.item(selected_row, 3).text())
        layout.addRow("Дата выдачи:", date_beg_input)

        date_end_input = QLineEdit(self.table.item(selected_row, 4).text())
        layout.addRow("Дата окончания выдачи:", date_end_input)

        date_ret_input = QLineEdit(self.table.item(selected_row, 5).text())
        layout.addRow("Дата возврата:", date_ret_input)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            update_journal_entry(entry_id, client_combo.currentText(), book_combo.currentText(), date_beg_input.text(),
                                 date_end_input.text(), date_ret_input.text())
            self.load_journal_entries()

    def add_return(self):
        entry_ids = get_journal_entry_ids()
        if not entry_ids:
            QMessageBox.critical(self, "Ошибка", "Не удалось загрузить список записей журнала")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить возврат")
        layout = QVBoxLayout(dialog)

        entry_id_combo = QComboBox()
        entry_id_combo.addItems(map(str, entry_ids))
        layout.addWidget(QLabel("ID Записи в журнале:"))
        layout.addWidget(entry_id_combo)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        entry_id = entry_id_combo.currentText()

        date_ret = datetime.now().strftime("%Y-%m-%d")

        update_journal_return(entry_id, date_ret=date_ret)
        self.load_journal_entries()

    def create_report(self):
        try:
            file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить отчет", "", "Text Files (*.txt)")
            if file_path:
                with open(file_path, "w") as file:
                    headers = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
                    file.write("\t".join(headers) + "\n")

                    for row in range(self.table.rowCount()):
                        row_data = []
                        for column in range(self.table.columnCount()):
                            item = self.table.item(row, column)
                            if item is not None:
                                row_data.append(item.text())
                        file.write("\t".join(row_data) + "\n")
                QMessageBox.information(self, "Отчет", "Отчет успешно создан.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при создании отчета: {e}")

    def go_back(self):
        self.main_window.set_initial_widget()