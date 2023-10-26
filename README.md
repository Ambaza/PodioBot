# PodioBot

PodioBot is a Python application that allows you to interact with the Podio API, create workspaces, apps, and manage your data on the Podio platform. This README provides an overview of the application's structure, features, and how to use it.

## Table of Contents

- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

This section will guide you on how to set up and use the PodioBot application.

### Prerequisites

To run PodioBot, you need to have the following prerequisites:

- Python 3
- PyQt5 library
- Podio API credentials (Client ID, Client Secret)
- Podio user credentials (Username, Password)

### Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/podiobot.git
   ```

2. Navigate to the project folder:

   ```bash
   cd podiobot
   ```

3. Install the required Python dependencies:

   ```bash
   pip install PyQt5
   ```

4. Update the configuration:

   Open `config.py` and provide your Podio API credentials (Client ID, Client Secret) and user credentials (Username, Password).

### Usage

Run the PodioBot application:

```bash
python main.py
```

This will launch the application's graphical user interface (GUI). You can interact with the GUI to create workspaces, apps, and manage your Podio data.

## Documentation

For more detailed information on the application structure and how to customize or extend its functionality, refer to the code documentation and comments in the source files.

- `main.py`: The main entry point of the application.
- `LoginPage.py`: Handles user authentication and provides access to the main workspace display.
- `WorkspaceAppDisplay.py`: Displays workspaces, apps, and allows you to create new workspaces and apps.
- `PandasModel.py`: Provides a model for displaying data in the GUI using PyQt5.
- `AppCreationPage.py`: Allows you to create new apps in a selected workspace.
- `api_interactions.py`: Contains functions for interacting with the Podio API.

## Contributing

If you would like to contribute to this project, feel free to open issues or pull requests. We welcome any contributions that improve the application's functionality or usability.

## Authors
This project was developed by AMBAZA KIMANUKA Armand.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
