A simple, keyboard-navigable TV app launcher built with Python and Pygame. This project provides a graphical user interface (GUI) for launching applications, with a grid-based menu system, customizable app list, and a form to add new apps.
Features

    Grid-Based Navigation: Navigate a grid of app buttons using arrow keys (UP, DOWN, LEFT, RIGHT).
    App Launching: Launch applications by selecting a button and pressing ENTER.
    Add New Apps: Add new apps via a form (Name, Image, Cmd) that saves to a JSON file.
    Customizable Background: Set a 1920x1080 background image for a sleek TV-like interface.
    Wrapping Navigation: Seamlessly wrap around the grid (top-to-bottom, left-to-right).
    Transparent Menus: Semi-transparent menus for a modern look.

Screenshots
Main Menu <!-- Add screenshots if when available -->
Add App Form
Requirements

    Python 3.6+
    Pygame: For rendering the GUI.
    JetBrains Mono Nerd Font: For text rendering (optional, replace with any font).

Install dependencies:
bash

pip install pygame

Installation

    Clone the Repository:
    bash

    git clone https://github.com/MasterTut/launcher.git
    cd launcher

    Set Up the Font:
        The project uses /usr/share/fonts/TTF/JetBrainsMonoNLNerdFontPropo-Regular.ttf.
        If this font isn’t available, update launcher_ui.py to use a different font:
        python

        self.font = pygame.font.Font(None, 30)  # Use default system font

    Prepare the Background:
        Place a 1920x1080 background image named background.png in the project root.
        Update main.py if the path differs:
        python

        background_image = pygame.image.load("path/to/background.png").convert()

    Prepare App Icons:
        The apps.json file references app icons (e.g., ./Assets/addApp.png).
        Ensure the Assets directory exists with the required images, or update apps.json paths.
    Run the Launcher:
    bash

    python main.py

Usage

    Navigation:
        Use UP, DOWN, LEFT, RIGHT to move the selection between app buttons.
        Navigation wraps around the grid (e.g., moving down from the bottom row goes to the top).
    Launch an App:
        Select an app button and press ENTER to run its command (defined in apps.json).
    Add a New App:
        Select the "AddApp" button and press ENTER.
        A form appears with fields for Name, Image, and Cmd.
        Navigate fields with UP/DOWN, press ENTER to edit a field, type, and press ENTER again to finish.
        Select "Submit" and press ENTER to save the new app to apps.json.
    Exit:
        Press ESC to exit the launcher or return to the main menu from the add app form.

Project Structure

launcher/
│
├── main.py              # Entry point, sets up Pygame and runs the main loop
├── launcher_ui.py       # Core UI classes (Menu, Button, TextField, Selection) and functions
├── apps.json            # JSON file storing app data (name, image, command)
├── background.png       # Background image (1920x1080)
├── Assets/              # Directory for app icons
│   ├── addApp.png
│   ├── testing.png
│   └── ...
└── README.md            # Project documentation

apps.json Format
The apps.json file stores the list of apps displayed in the launcher. Example:
json

{
  "apps": [
    {
      "name": "binary",
      "image": "./Assets/logo.png",
      "cmd": "program to launch from terminal"
    },
    {
      "name": "librewolf",
      "image": "./Assets/librewolf.png",
      "cmd": "librewolf"
    }
  ]
}

    name: Display name of the app.
    image: Path to the app’s icon (256x256 recommended).
    cmd: Command to run when the app is launched (e.g., librewolf).

Customization

    Background: Replace background.png with your own 1920x1080 image.
    App Icons: Add new icons to the Assets directory and update apps.json.
    Menu Layout:
        Adjust Menu positions and sizes in main.py (e.g., appsMenu, sideMenu, addAppMenu).
        Modify buttons_per_row in launcher_ui.importApps to change the grid layout.
    Styling:
        Update colors, fonts, and transparency in launcher_ui.py (e.g., Button.display, updateMenus).

Known Issues

    Font Dependency: If the specified font isn’t found, update the font path in launcher_ui.py.
    Command Security: The Button.onclickFunction uses subprocess.call with shell=True, which can be a security risk if cmd is user-controlled. Consider sanitizing inputs or using shell=False.

Contributing
Contributions are welcome! To contribute:

    Fork the repository.
    Create a new branch (git checkout -b feature/your-feature).
    Make your changes and commit (git commit -m "Add your feature").
    Push to your branch (git push origin feature/your-feature).
    Open a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.
Acknowledgments

    Built with Pygame.
    Inspired by modern TV app launcher interfaces.

Notes on the README

    Logo/Screenshots: I included placeholders for a logo and screenshots. If you have images, add them to the project and update the paths.
    License: I assumed an MIT License, but you can change it to your preferred license (e.g., GPL, Apache).
    Security Warning: I noted the shell=True issue in Button.onclickFunction, as it’s a potential vulnerability if cmd comes from untrusted input.

Adding the README

    Create a file named README.md in your project root.
    Copy the above content into README.md.
    Customize as needed (e.g., add screenshots, update paths, add a license file).

Let me know if you’d like to adjust any sections or add more details!
