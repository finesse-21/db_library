from PyQt6.QtWidgets import QApplication
from ui.login_window import LoginWindow
from ui.main_window import MainWindow

def main():
    app = QApplication([])

    login_window = LoginWindow()
    if login_window.exec():
        main_window = MainWindow(username=login_window.username, role=login_window.user_role)  # Pass username and role
        main_window.show()
        app.exec()

if __name__ == "__main__":
    main()