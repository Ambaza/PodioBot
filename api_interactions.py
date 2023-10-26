import requests
import requests
import logging
import time

logging.basicConfig(level=logging.ERROR)
BASE_URL = 'https://api.podio.com/'
base_url = BASE_URL

class APIInteractions:
    def __init__(self, base_url, access_token, client_id, client_secret):
        self.base_url = base_url
        self.access_token = access_token
        self.client_id = client_id
        self.client_secret = client_secret
        
    @staticmethod
    def get_access_token(client_id, client_secret, username, password):
        auth_url = BASE_URL + 'oauth/token'
        response = requests.post(auth_url, data={
            'grant_type': 'password',
            'client_id': client_id,
            'client_secret': client_secret,
            'username': username,
            'password': password
        })

        if response.status_code == 200:
            return response.json()['access_token']
        else:
            return None
        
    @staticmethod
    def get_organizations(access_token):
        orgs_url = base_url + 'org'
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(orgs_url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return []

    @staticmethod
    def get_workspaces(access_token, org_id):
        workspaces_url = base_url + f'org/{org_id}/space/'
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(workspaces_url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return []

    @staticmethod
    def get_apps_in_workspace(access_token, space_id, include_inactive=False):
        endpoint = f"app/space/{space_id}/"
        params = {
            "include_inactive": str(include_inactive).lower()
        }
        headers = {'Authorization': f'Bearer {access_token}'}

        response = requests.get(base_url + endpoint, params=params, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return []

    @staticmethod
    def get_app_dependencies(access_token, app_id):
        endpoint = f"app/{app_id}/dependencies/"
        headers = {'Authorization': f'Bearer {access_token}'}

        response = requests.get(base_url + endpoint, headers=headers)
        if response.status_code == 200:
            dependencies = response.json().get('apps', [])
            return dependencies
        else:
            return []

    @staticmethod
    def get_app_fields(access_token, app_id):
        endpoint = f"app/{app_id}"
        headers = {'Authorization': f'Bearer {access_token}'}

        response = requests.get(base_url + endpoint, headers=headers)
        if response.status_code == 200:
            app_data = response.json()
            fields = app_data.get('fields', [])
            return fields
        else:
            return []

    @staticmethod
    def create_new_workspace(token, org_id, workspace_name):
        endpoint = 'space/'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        data = {
            'org_id': org_id,
            'name': workspace_name
        }

        response = requests.post(BASE_URL + endpoint, json=data, headers=headers)
        if response.status_code == 200:
            return response.json().get('space_id')
        else:
            return None

    @staticmethod
    def create_new_app(self, token, workspace_id, app_type, app_name, item_name, app_icon, standard_layout, app_description, instruction):
        endpoint = 'app/'  # Définir le point d'accès pour créer une application
        headers = {'Authorization': f'Bearer {token}'}  # Définir les en-têtes avec le jeton d'accès

        # Définir la configuration de l'application comme un dictionnaire
        app_config = {
            "type": app_type,
            "name": app_name,
            "item_name": item_name,
            "icon": app_icon,
            "default_view": standard_layout,
            "description": app_description,
            "usage": instruction
        }

        # Define the fields as a list of dictionaries
        fields = [
            {
                "type": "date",
                "external_id": "meeting_time",
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
                "external_id": "meeting_participants",
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
                "external_id": "meeting_location",
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
                "external_id": "meeting_agenda",
                "config": {
                    "label": "Meeting agenda",
                    "description": "The topics to be discussed in the meeting",
                    "delta": 3,
                    "settings": {
                        "size": []
                    },
                }
            }
        ]

        data = {
            'space_id': workspace_id,
            'config': app_config,
            'fields': fields
        }
        # app_url = f'https://api.podio.com/app/'

        response = requests.post(BASE_URL + endpoint, json=data, headers=headers)
        
        if response.status_code == 400:
            new_app_id = response.json().get('app_id')
            print(new_app_id)
            return new_app_id
        else:
            return None

        # Introduce a 10-second delay
        time.sleep(10)


    @staticmethod
    def install_the_app(token, app_id, workspace_id):
        endpoint = f'app/{app_id}/install'
        headers = {'Authorization': f'Bearer {token}'}

        data = {
            "space_id": workspace_id
        }

        response = requests.post(BASE_URL + endpoint, json=data, headers=headers)
        if response.status_code == 200:
            return True
        else:
            return False
