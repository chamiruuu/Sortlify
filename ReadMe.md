# Sortlify

Sortlify is a lightweight file-sorting utility designed to help you quickly organize files by filtering based on user-specified names and file types. Built with CustomTkinter and Pillow, Sortlify provides a modern, dark-themed GUI for intuitive file management.

## Features

### Simple, Intuitive UI
- A clean, dark-themed interface built using CustomTkinter for a modern look.

### Flexible File Filtering
- Specify file names (one per line) and select file types to target specific files.

### Clipboard Integration
- Easily paste file names directly from your clipboard using the integrated paste button.

### Progress Tracking
- A real-time progress bar and on-screen notifications keep you informed during the sorting process.

### Undo Capability
- Quickly revert the last file operation if you need to correct any mistakes.

### Cross-Platform
- Works on Windows, macOS, and Linux (with Python and required libraries installed).

## Prerequisites

- Python 3.7+
- Required Libraries:
  - CustomTkinter
  - Pillow (PIL)
  - Tkinter (typically included with standard Python installations)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/chamiruuu/Sortlify.git
    cd Sortlify
    ```

2. Install dependencies:

    Use pip to install the required packages:

    ```bash
    pip install customtkinter Pillow
    ```

3. Ensure Resources are in Place:

    Make sure the `pasteicon.png` file is located in the repository’s root directory or the appropriate resources folder as referenced in the code.

4. Run the Application:

    Launch the application with:

    ```bash
    python script.py
    ```

## How It Works

### Select a Folder
Click the "Browse" button to choose the folder that contains the files you want to sort.

### Enter File Names
In the left panel, type the names (one per line) of the files you wish to process. You can also click the paste button (with the paste icon) to insert file names from your clipboard.

### Choose File Types
On selecting a folder, the app scans and displays the available file types. Check the boxes corresponding to the file types you want to filter. If none are selected, all file types will be processed.

### Select Action
Use the radio buttons to choose between Copy or Move:
- **Copy**: Duplicates the files into a subfolder.
- **Move**: Transfers the files into a subfolder.

### Process Files
Click the "Sortlify" button to begin processing. A new subfolder named "Sortlified" will be created within the selected folder, and files matching your criteria will be copied or moved accordingly.

### Undo Action
If you need to revert the last operation, simply click the "Undo" button to restore files to their original location.

### Reset Interface
Use the "Reset" button to clear all selections and inputs, allowing you to start a new sorting session.

## File Structure

- `script.py`: Main script that contains the application code.
- `pasteicon.png`: Icon used for the paste functionality in the GUI.
- (Other resource files, if any, should be included in the repository as needed.)

## Contributing

Contributions are welcome! If you find bugs or have ideas for improvements, please:
- Open an issue to discuss your suggestions.
- Submit a pull request with your proposed changes.

## License

This project is licensed under the MIT License.

## Acknowledgements

- CustomTkinter for the modern UI framework.
- Pillow for image processing support.
- Thanks to all contributors and users who help improve the project!