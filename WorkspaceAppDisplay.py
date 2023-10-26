import pandas as pd
from PyQt5.QtWidgets import QTableView, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt, QAbstractTableModel
from api_interactions import APIInteractions
from WorkspaceCreationPage import WorkspaceCreationPage
from AppCreationPage import AppCreationPage, ReuseApps

background_color = "#F2E8CF"
text_color = "#101010"
window_width = 1200
window_height = 600

class WorkspaceAppDisplay(QWidget):
    def __init__(self, access_token, organizations):
        super().__init__()
        self.access_token = access_token
        self.organizations = organizations
        self.workspaces = []  # Initialize an empty list for workspaces
        self.podio_client = []
        self.apps_data = []
        self.app_field_data = []
        self.base_url = []
        self.client_id = []
        self.client_secret = []
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

        self.table_view = QTableView()

        data = self.fetch_data()
        data_frame = pd.DataFrame(data)
        model = pandasModel(data_frame)
        self.table_view.setModel(model)

        layout.addWidget(self.table_view)

        self.create_workspace_button = QPushButton("Create New Workspace")
        self.create_workspace_button.clicked.connect(self.show_workspace_creation_page)
        
        self.create_app_button = QPushButton("Create New App")
        self.create_app_button.clicked.connect(self.show_app_creation_page)

        self.reuse_app_button = QPushButton("Add Apps in a specific WorkSpace")
        self.reuse_app_button.clicked.connect(self.add_apps_page)

        layout.addWidget(self.create_workspace_button)
        layout.addWidget(self.create_app_button)
        layout.addWidget(self.reuse_app_button)

        self.setLayout(layout)

    def fetch_data(self):
        all_data = []
        for org in self.organizations:
            workspaces = APIInteractions.get_workspaces(self.access_token, org['org_id'])
            self.workspaces.extend(workspaces)  # Store the fetched workspaces

            for workspace in workspaces:
                apps = APIInteractions.get_apps_in_workspace(self.access_token, workspace['space_id'])
                
                if not apps:  # If no apps in the workspace, add a placeholder entry
                    all_data.append({
                        "Organization": org['name'],
                        "Org ID": org['org_id'],
                        "Workspace": workspace['name'],
                        "Space ID": workspace['space_id'],
                        "App": "No Apps",  # Placeholder
                        "App ID": None,
                        "Dependencies": ""
                    })
                else:
                    for app in apps:
                        dependencies = APIInteractions.get_app_dependencies(self.access_token, app['app_id'])
                        dependency_names = ', '.join([dependency['name'] for dependency in dependencies])
                        app_data = {
                            "Organization": org['name'],
                            "Org ID": org['org_id'],
                            "Workspace": workspace['name'],
                            "Space ID": workspace['space_id'],
                            "App": app['config']['name'],
                            "App ID": app['app_id'],
                            "Dependencies": dependency_names
                        }
                        all_data.append(app_data)
        return all_data

    def show_workspace_creation_page(self):
        self.hide()
        self.workspace_creation_page = WorkspaceCreationPage(self.access_token, self.organizations, self.show_previous_page)
        self.workspace_creation_page.show()

    def show_app_creation_page(self):
        self.hide()
        self.app_creation_page = AppCreationPage(self.access_token, self.workspaces, self.show_previous_page, self.podio_client)
        self.app_creation_page.show()

    def add_apps_page(self):
        self.hide()
        # Make sure you pass 'apps' and 'app_field' arguments here
        self.app_creation_page = ReuseApps(self.access_token, self.workspaces, self.show_previous_page, self.podio_client, self.apps_data, self.app_field_data, self.base_url, self.client_id, self.client_secret)
        self.app_creation_page.show()

    def show_previous_page(self):
        self.show()


class pandasModel(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return str(self._data.iloc[index.row(), index.column()])
        return None

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._data.columns)

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return str(self._data.columns[section])
        return None
