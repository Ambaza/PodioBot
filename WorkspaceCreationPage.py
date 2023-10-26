from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
from api_interactions import APIInteractions

background_color = "#F2E8CF"
text_color = "#101010"
window_width = 1200
window_height = 600

class WorkspaceCreationPage(QWidget):
    def __init__(self, access_token, organizations, return_to_previous_page_callback):
        super().__init__()
        self.access_token = access_token
        self.organizations = organizations
        self.return_to_previous_page_callback = return_to_previous_page_callback  # Renamed variable
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title_label = QLabel("Podio Bot - Create Workspace")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font: bold 16px 'Arial Rounded MT Bold';")
        layout.addWidget(title_label)

        self.setGeometry(100, 100, window_width, window_height)
        self.setStyleSheet(
            f"background-color: {background_color}; color: {text_color}; font-family: Arial;"
            f"font-size: 14px;"
        )
        
        self.workspace_name_label = QLabel("Enter the name of the new workspace:")
        self.workspace_name_input = QLineEdit()
        self.create_workspace_button = QPushButton("Create Workspace")
        self.create_workspace_button.clicked.connect(self.create_workspace)

        self.back_button = QPushButton("Back to Workspace and App Tab")
        self.back_button.clicked.connect(self.return_to_previous_page_callback)  # Updated method name

        layout.addWidget(self.workspace_name_label)
        layout.addWidget(self.workspace_name_input)
        layout.addWidget(self.create_workspace_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def create_workspace(self):
        new_workspace_name = self.workspace_name_input.text()
        org = self.organizations[0]  # Assuming only one organization
        new_workspace_id = APIInteractions.create_new_workspace(self.access_token, org['org_id'], new_workspace_name)

        if new_workspace_id:
            self.return_to_previous_page_callback()  # Updated method name

    def return_to_previous_page_callback(self):
        self.return_to_previous_page_callback()  # Use the provided method to return to the previous page
