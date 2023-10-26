import logging
from PyQt5.QtWidgets import QWidget, QProgressBar, QMessageBox, QListWidget, QListWidgetItem, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTextEdit, QComboBox
from PyQt5.QtCore import Qt
import requests
from api_interactions import APIInteractions


BASE_URL = 'https://api.podio.com/'

background_color = "#F2E8CF"
text_color = "#101010"
window_width = 1200
window_height = 600


class AppCreationPage(QWidget):
    def __init__(self, access_token, workspaces, return_function, podio_client):
        super().__init__()
        self.podio_client = podio_client
        self.access_token = access_token
        self.workspaces = workspaces
        self.return_function = return_function
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title_label = QLabel("Podio Bot - Create App")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font: bold 16px 'Arial Rounded MT Bold';")
        layout.addWidget(title_label)

        self.setGeometry(100, 100, window_width, window_height)
        self.setStyleSheet(
            f"background-color: {background_color}; color: {text_color}; font-family: Arial;"
            f"font-size: 14px;"
        )

        # Add input fields for app creation details (type, name, description, etc.)
        self.workspace_input = QComboBox()
        self.workspace_input.addItems([workspace['name'] for workspace in self.workspaces])  # Use the stored workspaces data

        self.app_type_input = QComboBox()
        self.app_type_input.addItems(["meeting", "standard", "contact"])  # Corrected values
        self.app_name_input = QLineEdit()
        self.item_name_input = QLineEdit()
        self.app_icon_input = QLineEdit()
        self.standard_layout_input = QComboBox()
        self.standard_layout_input.addItems(['stream', 'table', 'badge', 'table-new', 'calendar', 'card'])  # Corrected values
        self.app_description_input = QTextEdit()
        self.instruction_input = QTextEdit()

        # Validation button
        self.validate_button = QPushButton("Validate")
        self.validate_button.clicked.connect(self.create_my_app)

        self.cancel_button = QPushButton("Cancel the process")
        self.cancel_button.clicked.connect(self.create_my_app)

        layout.addWidget(QLabel("Select Workspace:"))
        layout.addWidget(self.workspace_input)
        layout.addWidget(QLabel("App Type:"))
        layout.addWidget(self.app_type_input)
        layout.addWidget(QLabel("App Name:"))
        layout.addWidget(self.app_name_input)
        layout.addWidget(QLabel("Item Name:"))
        layout.addWidget(self.item_name_input)
        layout.addWidget(QLabel("App Icon:"))
        layout.addWidget(self.app_icon_input)
        layout.addWidget(QLabel("Standard Layout:"))
        layout.addWidget(self.standard_layout_input)
        layout.addWidget(QLabel("App Description:"))
        layout.addWidget(self.app_description_input)
        layout.addWidget(QLabel("Instruction for creating an item:"))
        layout.addWidget(self.instruction_input)
        layout.addWidget(self.validate_button)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)  # Définir le layout comme le layout du widget


    def create_my_app(self):
        selected_workspace_name = self.workspace_input.currentText()
        workspace_id = None
        for workspace in self.workspaces:
            if workspace['name'] == selected_workspace_name:
                workspace_id = workspace['space_id']
                break

        if workspace_id:
            app_type = self.app_type_input.currentText()
            app_name = self.app_name_input.text()
            item_name = self.item_name_input.text()
            app_icon = self.app_icon_input.text()
            # Check if the required fields have non-empty values
            if not app_name:
                print("App Name is required and cannot be empty.")
                return

            if not item_name:
                print("Item Name is required and cannot be empty.")
                return

            if not app_icon:
                print("App Icon is required and cannot be empty.")
                return

            # Use the selected_standard_layout variable here
            selected_standard_layout = self.standard_layout_input.currentText()

            app_description = self.app_description_input.toPlainText()
            instruction = self.instruction_input.toPlainText()

            # app_id = APIInteractions.create_new_app(self.access_token, workspace_id, app_type, app_name, item_name, app_icon, standard_layout, app_description, instruction)
            app_id = self.create_new_app(self.access_token, workspace_id, app_type, app_name, item_name, app_icon, selected_standard_layout, app_description, instruction)

            if app_id:
                self.install_the_app(self.access_token, app_id, workspace_id)


    def install_the_app(self, token, app_id, workspace_id):
        endpoint = f'app/{app_id}/install'  # Définir le point d'accès pour installer une application
        headers = {'Authorization': f'Bearer {token}'}  # Définir les en-têtes avec le jeton d'accès

        data = {
            "space_id": workspace_id  # Donner l'identifiant de l'espace de travail où installer l'application
        }

        response = requests.post(BASE_URL + endpoint, json=data, headers=headers)  # Faire une requête POST à l'API Podio avec les données et les en-têtes
        if response.status_code == 400:  # Si la requête a réussi
            return True
        else:
            return False

    def create_new_app(self, token, workspace_id, app_type, app_name, item_name, app_icon, selected_standard_layout, app_description, instruction):
        endpoint = 'app/'  # Endpoint for creating a new app
        headers = {'Authorization': f'Bearer {token}'}  # Headers with the access token

        # Define the configuration of the app
        app_config = {
            "type": app_type,
            "name": app_name,
            "item_name": item_name,
            "description": app_description,
            "usage": instruction,
            "icon": app_icon,
            "default_view": selected_standard_layout
        }

        # Define the fields for the app
        fields = [
            {
                "type": "date",
                "config": {
                    "label": "Meeting time",
                    "description": "The date and time of the meeting",
                    "delta": 0,
                    "settings": {
                        "time": True
                    },
                    "mapping": "meeting_time",
                    "required": True
                }
            },
            {
                "type": "contact",
                "config": {
                    "label": "Meeting participants",
                    "description": "The people who are attending the meeting",
                    "delta": 1,
                    "settings": {
                        "type": ["user", "space"]
                    },
                    "mapping": "meeting_participants",
                    "required": True
                }
            },
            {
                "type": "location",
                "config": {
                    "label": "Meeting location",
                    "description": "The place where the meeting is held",
                    "delta": 2,
                    "mapping": "meeting_location",
                    "required": True
                }
            },
            {
                "type": "text",
                "config": {
                    "label": "Meeting agenda",
                    "description": "The topics to be discussed in the meeting",
                    "delta": 3,
                    "settings": {
                        "size": []
                    },
                    "mapping": "meeting_agenda",
                    "required": True
                }
            }
        ]

        # Define the data to be sent in the request
        data = {
            'space_id': workspace_id,
            'config': app_config,
            'fields': fields
        }

        response = requests.post(BASE_URL + endpoint, json=data, headers=headers)

        if response.status_code == 200:
            new_app_id = response.json().get('app_id')
            return new_app_id
        else:
            print("Error creating the app:", response.text)
            return None




class ReuseApps(QWidget):
    def __init__(self, access_token, space_id, app_id, fields):
        super().__init__()
        self.access_token = access_token
        self.workspaces = space_id
        self.apps = app_id
        self.fields = fields
        self.init_ui()

    

    def init_ui(self):
        layout = QVBoxLayout()

        title_label = QLabel("Podio Bot - Create App")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font: bold 16px 'Arial Rounded MT Bold';")
        layout.addWidget(title_label)

        self.setGeometry(100, 100, window_width, window_height)
        self.setStyleSheet(
            f"background-color: {background_color}; color: {text_color}; font-family: Arial;"
            f"font-size: 14px;"
        )

        # Step 1: Display Available Workspaces
        layout.addWidget(QLabel("Select Destination Workspace:"))
        self.destination_workspace_input = QComboBox()
        self.destination_workspace_input.addItems([workspace['name'] for workspace in self.workspaces])

        layout.addWidget(self.destination_workspace_input)

        # Step 1: Display Available Workspaces
        layout.addWidget(QLabel("Select Workspace:"))
        self.workspace_input = QComboBox()
        self.workspace_input.addItems([workspace['name'] for workspace in self.workspaces])
        self.workspace_input.currentIndexChanged.connect(self.on_workspace_selected)  # Connect to the handler

        layout.addWidget(self.workspace_input)
           


        # Step 2: Display Available Apps
        layout.addWidget(QLabel("Select Apps to Copy:"))
        self.app_list = QListWidget()
        for apps in self.apps:
            item = QListWidgetItem(apps['name'], self.apps)
            item.setData(Qt.UserRole, self.apps['app_id'])  # Store the app ID as user data
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.apps.addItem(item)

        layout.addWidget(self.app_list)

        # Step 3: Display App Fields with Checkboxes
        layout.addWidget(QLabel("Select Fields to Copy:"))
        self.app_field_list = QListWidget()
        for fields in self.app_field:
            item = QListWidgetItem(fields['label'], self.app_field_list)
            item.setData(Qt.UserRole, fields['id'])  # Store the field ID as user data
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.app_field_list.addItem(item)

        layout.addWidget(self.app_field_list)
 
        # Step 4: Add a Progress Bar
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        # Step 5: Add Validation and Copy Buttons
        self.validate_button = QPushButton("Validate and Copy")
        self.validate_button.clicked.connect(self.validate_and_copy_app)
        layout.addWidget(self.validate_button)

        self.cancel_button = QPushButton("Cancel the process")
        self.cancel_button.clicked.connect(self.cancel_copy_app)
        layout.addWidget(self.cancel_button)

        # App Information Text
        self.app_info_text = QTextEdit()
        self.app_info_text.setReadOnly(True)
        layout.addWidget(self.app_info_text)

        self.setLayout(layout)

    def validate_and_copy_app(self):
        if not self.validate_selection():
            return

        selected_apps = [item.data(Qt.UserRole) for item in self.apps_input.selectedItems()]
        selected_fields = self.get_selected_fields()
        selected_destination_workspace = self.destination_workspace_input.currentText()

        total_apps = len(selected_apps)
        progress = 0

        for app_id in selected_apps:
            try:
                # Fetch the destination workspace ID based on the selected name
                destination_workspace_id = self.APIInteractions.get_workspace_id(selected_destination_workspace)

                # Copy the app and fields here, using the destination workspace ID
                new_app_id = self.APIInteractions.copy_app_to_workspace(app_id, destination_workspace_id)
                self.APIInteractions.copy_fields_to_app(selected_fields, new_app_id)

                # Now, you can use the logic from PodioAppMarketShare to install the copied app
                share_id = app_id  # Assuming app_id is equivalent to share_id
                self.api_interactions.install_the_app(share_id, destination_workspace_id)

            except Exception as e:
                # Log the error
                logging.error(f"Error copying app {app_id}: {str(e)}")

            # Update progress
            progress += 1
            self.progress_bar.setValue((progress / total_apps) * 100)

    def validate_selection(self):
            selected_workspace = self.workspace_input.currentText()
            selected_apps = [item.data(Qt.UserRole) for item in self.apps_input.selectedItems()]
            selected_destination_workspace = self.destination_workspace_input.currentText()

            if not selected_workspace:
                QMessageBox.warning(self, "Validation Error", "Please select a workspace.")
                return False

            if not selected_apps:
                QMessageBox.warning(self, "Validation Error", "Please select at least one app to copy.")
                return False

            if not selected_destination_workspace:
                QMessageBox.warning(self, "Validation Error", "Please select a destination workspace.")
                return False

            return True

    def update_app_list(self, app_data):
        self.apps_input.clear()  # Clear the list widget
        for app in app_data:
            item = QListWidgetItem(app['name'], self.apps_input)
            item.setData(Qt.UserRole, app['app_id'])  # Store the app ID as user data
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.apps_input.addItem(item)

    def on_workspace_selected(self):
        # This method is called when the user selects a workspace.
        # Fetch the app data for the selected workspace and update the app list.
        selected_workspace = self.workspace_input.currentText()
        app_data = self.api_interactions.get_apps_in_workspace(self.access_token, self.space_id)  # Replace workspace_id with the actual ID
        self.update_app_list(app_data)

    def get_selected_fields(self):
        selected_fields = [item.data(Qt.UserRole) for item in self.app_field_input.selectedItems()]
        return selected_fields

    def cancel_copy_app(self):
        self.close()

    def install_the_app(self):
        return
