# Sortlify

Sortlify is a simple yet powerful file sorting utility that allows you to quickly copy or move files based on user-specified file names and file types. Built with CustomTkinter and Pillow, this application provides an intuitive, modern GUI for organizing your files.

## Features

### User-Friendly Interface
- A sleek, dark-themed interface built with CustomTkinter.

### Flexible File Sorting
- Filter and sort files by entering file names (one per line) and selecting file types.

### Clipboard Support
- Easily paste file names from your clipboard using the integrated paste button.

### Progress & Notifications
- Visual progress bar and on-screen notifications inform you as the process runs.

### Undo Functionality
- Quickly revert the last file operation if needed.

### Cross-Platform Compatibility
- Works on Windows, macOS, and Linux (with Python and necessary dependencies installed).

## Prerequisites

- Python 3.7 or higher
- Required packages:
  - CustomTkinter
  - Pillow (PIL)
  - Tkinter (typically included with Python)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/sortlify.git
    cd sortlify
    ```

2. Install dependencies:

    Use pip to install the required packages:

    ```bash
    pip install customtkinter Pillow
    ```

3. Run the application:

    ```bash
    python script.py
    ```

    (Make sure the [pasteicon.png](http://_vscodecontentref_/1) file is located in the same directory or in the appropriate resources folder.)

## How It Works

### Folder Selection
Click the "Browse" button to choose the folder containing the files you want to sort.

### Enter File Names
In the left panel, enter file names (one per line) that you wish to process. You can also click the paste button (with a paste icon) to insert file names from your clipboard.

### Select File Types (Optional)
The application dynamically lists available file types from the selected folder. Check the file types you want to filter on; if none are selected, all file types will be processed.

### Choose the Action
Decide whether to Copy or Move the files using the radio buttons.

### Sort Files
Click the "Sortlify" button. The app will create a subfolder called "Sortlified" in your selected folder and begin processing. A progress bar and notifications keep you updated on the operation’s status.

### Undo Last Action
If necessary, click the "Undo" button to revert the last file operation.

### Reset
The "Reset" button clears all inputs and selections, allowing you to start fresh.

## File Structure

- [script.py](http://_vscodecontentref_/2): The main Python script that runs the application.
- [pasteicon.png](http://_vscodecontentref_/3): Icon used for the paste button.
- (Additional resource files if any.)

## Contributing

Contributions are welcome! If you have suggestions, bug fixes, or enhancements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.

## Acknowledgements

- Built using [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- Icon image courtesy of its respective creator