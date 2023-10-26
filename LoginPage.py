from PyQt5.QtWidgets import  QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
from api_interactions import APIInteractions
from WorkspaceAppDisplay import WorkspaceAppDisplay

background_color = "#F2E8CF"
text_color = "#101010"
window_width = 1200
window_height = 600

class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.access_token = None
        self.organizations = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title_label = QLabel("Podio Bot")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font: bold 16px 'Arial Rounded MT Bold';")
        layout.addWidget(title_label)

        self.setGeometry(100, 100, window_width, window_height)
        self.setStyleSheet(
            f"background-color: {background_color}; color: {text_color}; font-family: Arial;"
            f"font-size: 14px;"
        )

        self.client_id_input = QLineEdit()
        self.client_secret_input = QLineEdit()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.login)

        layout.addWidget(QLabel("Client ID:"))
        layout.addWidget(self.client_id_input)
        layout.addWidget(QLabel("Client Secret:"))
        layout.addWidget(self.client_secret_input)
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)
        self.setWindowTitle("Podio App Login")

    def login(self):
        self.access_token = APIInteractions.get_access_token(
            self.client_id_input.text(), self.client_secret_input.text(),
            self.username_input.text(), self.password_input.text()
        )

        if self.access_token:
            self.organizations = APIInteractions.get_organizations(self.access_token)
            if self.organizations:
                self.show_second_page()

    def show_second_page(self):
        self.second_page = WorkspaceAppDisplay(self.access_token, self.organizations)
        self.second_page.show()
        self.hide()
