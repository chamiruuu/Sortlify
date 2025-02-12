import sys
import os
import shutil
import threading
import time
import customtkinter as ctk
from PIL import Image
from tkinter import filedialog, messagebox

def resource_path(relative_path):
    """Get the absolute path to a resource. Works for dev and PyInstaller."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS during runtime
        base_path = sys._MEIPASS
    except AttributeError:
        # If not in a PyInstaller bundle, use the current directory
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Set the dark appearance mode.
ctk.set_appearance_mode("dark")

class FileSorterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sortlify")
        self.geometry("1000x700")  # Default size for larger screens.
        self.minsize(800, 600)  # Minimum window size
        self.geometry("800x600")  # Ensure the window opens at the minimum size.
        self.selected_folder = None
        self.last_action = None  # Store the last action for undo
        self.create_widgets()

    def create_widgets(self):
        # Create a main container frame that splits the window into two columns.
        self.main_frame = ctk.CTkFrame(self, fg_color="#0d0d0d")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=0)  # Left: fixed for file names
        self.main_frame.grid_columnconfigure(1, weight=1)  # Right: expands
        self.main_frame.grid_rowconfigure(0, weight=1)

        # ===== Left Frame: File Names Input =====
        self.left_frame = ctk.CTkFrame(self.main_frame, width=250, fg_color="#1a1a1a")
        self.left_frame.grid(row=0, column=0, sticky="ns", padx=(10, 10), pady=10)  # Added extra padding to the left (20px)
        self.left_frame.grid_propagate(False)  # Keeps a fixed width

        # Label and Paste Button in the same row
        self.names_label_frame = ctk.CTkFrame(self.left_frame, fg_color="#1a1a1a")
        self.names_label_frame.pack(anchor="nw", fill="x", padx=10, pady=(10, 5))
        self.names_label = ctk.CTkLabel(self.names_label_frame, text="File Names (one per line):")
        self.names_label.pack(side="left", padx=(0, 5), pady=5)

        # Paste Button with an icon
        self.paste_icon = ctk.CTkImage(
            light_image=Image.open(resource_path("pasteicon.png")),  # Correct path for PyInstaller
            size=(20, 20)  # Set the desired size of the icon
        )
        self.paste_button = ctk.CTkButton(
            self.names_label_frame,
            image=self.paste_icon,
            text="",
            width=30,
            height=30,
            command=self.paste_from_clipboard,
            fg_color="#0073e6",  # Normal color
            hover_color="#333333",  # Hover color
            border_width=1.5,  # Add border width
            border_color="#333333"  # Add border color
        )
        self.paste_button.pack(side="right", padx=(5, 0), pady=5)

        # Textbox for entering file names
        self.names_textbox = ctk.CTkTextbox(self.left_frame)
        self.names_textbox.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Line count label
        self.line_count_label = ctk.CTkLabel(self.left_frame, text="File names: 0", anchor="w", font=("Courier", 10))
        self.line_count_label.pack(anchor="sw", padx=10, pady=(0, 10))

        # Bind the textbox to update line count on key release
        self.names_textbox.bind("<KeyRelease>", self.update_line_count)

        # ===== Right Frame: Folder, File Types, Action, Buttons, etc. =====
        self.right_frame = ctk.CTkFrame(self.main_frame, fg_color="#0d0d0d")
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 0), pady=10)
        self.right_frame.grid_columnconfigure(0, weight=1)

        # --- Folder Selection Section ---
        self.folder_frame = ctk.CTkFrame(self.right_frame, corner_radius=8, fg_color="#1a1a1a")
        self.folder_frame.pack(fill="x", padx=10, pady=(0, 10))
        self.folder_label = ctk.CTkLabel(self.folder_frame, text="Select Folder:")
        self.folder_label.pack(side="left", padx=10, pady=10)
        self.folder_button = ctk.CTkButton(self.folder_frame, text="Browse", command=self.select_folder, fg_color="#0073e6")
        self.folder_button.pack(side="left", padx=10, pady=10)

        # Folder path display styled like a code block.
        self.folder_path_var = ctk.StringVar(value="No folder selected")
        self.folder_path_display = ctk.CTkLabel(
            self.folder_frame,
            textvariable=self.folder_path_var,
            anchor="w",
            font=("Courier", 10),
            fg_color="#2b2b2b",  # Slightly lighter block background
            corner_radius=4,
            padx=10, pady=5
        )
        self.folder_path_display.pack(side="left", fill="x", expand=True, padx=10, pady=10)

        # --- Dynamic File Types Section ---
        self.file_types_frame = ctk.CTkFrame(self.right_frame, corner_radius=8, fg_color="#1a1a1a")
        self.file_types_frame.pack(fill="both", padx=10, pady=(5, 10))
        # This section will be populated when a folder is selected.
        self.file_type_vars = {}

        # --- Action Selection Section (Copy/Move) ---
        self.action_frame = ctk.CTkFrame(self.right_frame, corner_radius=8, fg_color="#1a1a1a")
        self.action_frame.pack(fill="x", padx=10, pady=(5, 10))
        self.action_label = ctk.CTkLabel(self.action_frame, text="Action:")
        self.action_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.action_var = ctk.StringVar(value="copy")
        self.radio_copy = ctk.CTkRadioButton(self.action_frame, text="Copy", variable=self.action_var, value="copy", fg_color="#0073e6")
        self.radio_move = ctk.CTkRadioButton(self.action_frame, text="Move", variable=self.action_var, value="move", fg_color="#0073e6")
        self.radio_copy.grid(row=0, column=1, padx=10, pady=10)
        self.radio_move.grid(row=0, column=2, padx=10, pady=10)
        self.action_frame.grid_columnconfigure(3, weight=1)

        # --- Buttons Section: Process (Sort), Reset & Undo ---
        self.button_frame = ctk.CTkFrame(self.right_frame, corner_radius=8, fg_color="#1a1a1a")
        self.button_frame.pack(fill="x", padx=10, pady=(5, 10))
        self.process_button = ctk.CTkButton(self.button_frame, text="Sortlify", command=self.process_files, fg_color="#0073e6")
        self.process_button.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        self.reset_button = ctk.CTkButton(self.button_frame, text="Reset", command=self.reset_ui, fg_color="#0073e6")
        self.reset_button.grid(row=0, column=1, padx=20, pady=10, sticky="ew")
        self.undo_button = ctk.CTkButton(self.button_frame, text="Undo", command=self.undo_last_action, fg_color="#0073e6")
        self.undo_button.grid(row=0, column=2, padx=20, pady=10, sticky="ew")
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)
        self.button_frame.grid_columnconfigure(2, weight=1)

        # --- Progress Indicator Section ---
        self.progress_frame = ctk.CTkFrame(self.right_frame, corner_radius=8, fg_color="#1a1a1a")
        self.progress_frame.pack(fill="x", padx=10, pady=(5, 10))
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", padx=10, pady=10)

        # --- Notification Section ---
        self.notification_label = ctk.CTkLabel(self.right_frame, text="", font=ctk.CTkFont(size=14))
        self.notification_label.pack(pady=(5, 10))

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.selected_folder = folder
            self.folder_path_var.set(folder)
            self.update_file_types()

    def update_file_types(self):
        # Clear any previous file type checkboxes.
        for widget in self.file_types_frame.winfo_children():
            widget.destroy()
        self.file_type_vars = {}
        if self.selected_folder:
            try:
                files = [f for f in os.listdir(self.selected_folder)
                         if os.path.isfile(os.path.join(self.selected_folder, f))]
            except Exception as e:
                messagebox.showerror("Error", f"Could not list files in folder: {str(e)}")
                return
            exts = set()
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext:
                    exts.add(ext)
            exts = sorted(exts)
            if not exts:
                label = ctk.CTkLabel(self.file_types_frame, text="No file types found in this folder.")
                label.pack(padx=10, pady=10)
            else:
                # Create a scrollable frame for file types.
                scrollable_frame = ctk.CTkScrollableFrame(self.file_types_frame, fg_color="#1a1a1a")
                scrollable_frame.pack(fill="both", expand=True, padx=10, pady=5)
                label = ctk.CTkLabel(scrollable_frame, text="Select File Types:")
                label.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))
                # Arrange checkboxes in a grid layout.
                row, col = 1, 0
                max_cols = 4  # Maximum number of columns for file type checkboxes.
                for idx, ext in enumerate(exts):
                    var = ctk.BooleanVar(value=False)
                    self.file_type_vars[ext] = var
                    cb = ctk.CTkCheckBox(scrollable_frame, text=ext, variable=var)
                    cb.grid(row=row, column=col, sticky="w", padx=10, pady=5)
                    # Update grid position.
                    col += 1
                    if col >= max_cols:
                        col = 0
                        row += 1

    def reset_ui(self):
        self.selected_folder = None
        self.folder_path_var.set("No folder selected")
        # Clear dynamic file types.
        for widget in self.file_types_frame.winfo_children():
            widget.destroy()
        self.file_type_vars = {}
        # Clear file names textbox.
        self.names_textbox.delete("1.0", "end")
        self.action_var.set("copy")
        self.progress_bar.set(0)
        self.notification_label.configure(text="")
        # Reset line count
        self.line_count_label.configure(text="File names: 0")

    def process_files(self):
        if not self.selected_folder:
            messagebox.showerror("Error", "Please select a folder first!")
            return

        # Check if the names_textbox is empty
        names_input = self.names_textbox.get("1.0", "end").strip()
        if not names_input:
            messagebox.showerror("Error", "No file names provided. Please enter file names.")
            return

        # Build the list of file extensions based on user selections.
        selected_extensions = []
        if self.file_type_vars:
            for ext, var in self.file_type_vars.items():
                if var.get():
                    selected_extensions.append(ext)

        # If no checkboxes are selected, process all files.
        if not selected_extensions:
            selected_extensions = None

        # Read file names from the textbox (one per line).
        names_input = names_input.splitlines()
        names_set = {name.strip() for name in names_input if name.strip()}
        action = self.action_var.get()  # Either "copy" or "move"

        # Run file processing in a separate thread.
        threading.Thread(
            target=self.process_files_thread,
            args=(selected_extensions, names_set, action),
            daemon=True
        ).start()

    def process_files_thread(self, selected_extensions, names_set, action):
        folder = self.selected_folder
        try:
            all_files = [f for f in os.listdir(folder)
                         if os.path.isfile(os.path.join(folder, f))]
        except Exception as e:
            self.show_notification(f"Error reading folder: {str(e)}", error=True)
            return
        files_to_process = []
        skipped_names = set(names_set)  # Start with all input names as skipped.
        for file in all_files:
            ext = os.path.splitext(file)[1].lower()
            if selected_extensions is None or ext in selected_extensions:
                if names_set:
                    base_name = os.path.splitext(file)[0]
                    if base_name in names_set:
                        files_to_process.append(file)
                        skipped_names.discard(base_name)  # Remove from skipped if found.
                else:
                    files_to_process.append(file)
        total_files = len(files_to_process)
        if total_files == 0:
            self.show_notification("No files matched the criteria.", error=True)
            return

        # Create a destination subfolder.
        dest_folder = os.path.join(folder, "Sortlified")  # Changed folder name to "Sortlified"
        os.makedirs(dest_folder, exist_ok=True)

        processed_files = 0
        for idx, file in enumerate(files_to_process):
            src_path = os.path.join(folder, file)
            dest_path = os.path.join(dest_folder, file)
            base, ext = os.path.splitext(file)
            counter = 1
            while os.path.exists(dest_path):
                dest_path = os.path.join(dest_folder, f"{base}_{counter}{ext}")
                counter += 1
            try:
                if action == "copy":
                    shutil.copy2(src_path, dest_path)
                elif action == "move":
                    shutil.move(src_path, dest_path)
                processed_files += 1
            except Exception as e:
                self.show_notification(f"Error processing {file}: {str(e)}", error=True)
            progress = (idx + 1) / total_files
            self.progress_bar.set(progress)
            time.sleep(0.1)  # Simulate processing time

        # Prepare the summary message.
        skipped_count = len(skipped_names)  # Count of names not found in the folder.
        summary_message = (
            f"Process complete!\n"
            f"{action.capitalize()}: {processed_files} | Skipped: {skipped_count}"
        )
        self.show_notification(summary_message)
        self.last_action = (selected_extensions, names_set, action, files_to_process)  # Store the last action for undo
        time.sleep(1)
        self.progress_bar.set(0)

    def undo_last_action(self):
        if not self.last_action:
            messagebox.showinfo("Info", "No action to undo.")
            return
        selected_extensions, names_set, action, files_to_process = self.last_action
        folder = self.selected_folder
        dest_folder = os.path.join(folder, "Sortlified")  # Changed folder name to "Sortlified"
        for file in files_to_process:
            dest_path = os.path.join(dest_folder, file)
            if os.path.exists(dest_path):
                try:
                    if action == "copy":
                        os.remove(dest_path)
                    elif action == "move":
                        shutil.move(dest_path, folder)
                except Exception as e:
                    self.show_notification(f"Error undoing {file}: {str(e)}", error=True)
        self.show_notification("Last action undone.")
        self.last_action = None  # Clear the last action after undo

    def show_notification(self, message, error=False):
        color = "red" if error else "green"
        self.notification_label.configure(text=message, text_color=color)
        self.after(5000, lambda: self.notification_label.configure(text=""))

    def update_line_count(self, event=None):
        """Update the line count label based on the content of the names_textbox."""
        content = self.names_textbox.get("1.0", "end").strip()
        line_count = len(content.splitlines())
        self.line_count_label.configure(text=f"File names: {line_count}")

    def paste_from_clipboard(self):
        """Paste text from the clipboard into the names_textbox."""
        try:
            clipboard_content = self.clipboard_get()
            self.names_textbox.insert("end", clipboard_content)
            self.update_line_count()  # Update the line count after pasting
        except Exception as e:
            messagebox.showerror("Error", f"Failed to paste from clipboard: {str(e)}")

if __name__ == "__main__":
    app = FileSorterApp()
    app.mainloop()