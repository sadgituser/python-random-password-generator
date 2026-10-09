# Project imports
import json
import os
import random
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox
from webbrowser import open_new_tab


DEFAULT_SETTINGS = {
    "length": 16,
    "use_uppercase": True,
    "use_numbers": True,
    "use_special": True,
}

APP_DATA_DIRECTORY = Path(os.environ.get("APPDATA") or Path.home())
SETTINGS_FILE = APP_DATA_DIRECTORY / "PasswordGenerator" / "settings.json"


def genpass(length, use_uppercase, use_numbers, use_special):
    characters = "abcdefghijklmnopqrstuvwxyz"
    if use_uppercase:
        characters += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if use_numbers:
        characters += "0123456789"
    if use_special:
        characters += "`¬!@#$%^&*()_+-=[]}{|;':,./<>?"

    return "".join(random.choice(characters) for _ in range(length))


def validate_settings(data):
    if not isinstance(data, dict):
        raise ValueError("Settings must be a JSON object.")

    length = data.get("length")
    if type(length) is not int or not 1 <= length <= 32:
        raise ValueError("Password length must be a whole number from 1 to 32.")

    settings = {"length": length}
    for key in ("use_uppercase", "use_numbers", "use_special"):
        if type(data.get(key)) is not bool:
            raise ValueError(f"'{key}' must be true or false.")
        settings[key] = data[key]

    return settings


def read_settings(path):
    with Path(path).open(encoding="utf-8") as settings_file:
        return validate_settings(json.load(settings_file))


def write_settings(path, settings):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as settings_file:
        json.dump(settings, settings_file, indent=2)
        settings_file.write("\n")


def main():
    root = tk.Tk()
    root.title("Password Generator")
    root.geometry("520x280+300+200")
    root.minsize(360, 220)
    root.configure(bg="#000000")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    try:
        initial_settings = read_settings(SETTINGS_FILE)
    except FileNotFoundError:
        initial_settings = DEFAULT_SETTINGS.copy()
    except (OSError, json.JSONDecodeError, ValueError) as error:
        messagebox.showerror(
            "Could not load settings",
            f"Default settings will be used.\n\n{error}",
            parent=root,
        )
        initial_settings = DEFAULT_SETTINGS.copy()

    length_variable = tk.IntVar(value=initial_settings["length"])
    uppercase_variable = tk.BooleanVar(value=initial_settings["use_uppercase"])
    numbers_variable = tk.BooleanVar(value=initial_settings["use_numbers"])
    special_variable = tk.BooleanVar(value=initial_settings["use_special"])

    main_frame = tk.Frame(root, bg="#000000", padx=24, pady=24)
    main_frame.grid(row=0, column=0, sticky="nsew")
    main_frame.columnconfigure(0, weight=1)
    main_frame.rowconfigure(1, weight=1)

    heading = tk.Label(
        main_frame,
        text="Your password:",
        bg="#000000",
        fg="#00FF00",
        font=("Comic Sans MS", 16),
    )
    heading.grid(row=0, column=0, pady=(0, 12))

    password_label = tk.Label(
        main_frame,
        text="Open Settings to choose options and generate a password.",
        bg="#000000",
        fg="#00FF00",
        font=("Consolas", 14),
        wraplength=460,
        justify=tk.CENTER,
    )
    password_label.grid(row=1, column=0, sticky="nsew")
    password_label.bind(
        "<Configure>",
        lambda event: password_label.configure(wraplength=max(200, event.width - 16)),
    )

    settings_window = None

    def current_settings():
        return {
            "length": length_variable.get(),
            "use_uppercase": uppercase_variable.get(),
            "use_numbers": numbers_variable.get(),
            "use_special": special_variable.get(),
        }

    def persist_settings(show_confirmation=False):
        try:
            write_settings(SETTINGS_FILE, current_settings())
        except OSError as error:
            messagebox.showerror(
                "Could not save settings",
                f"Settings could not be saved to:\n{SETTINGS_FILE}\n\n{error}",
                parent=root,
            )
            return False

        if show_confirmation:
            messagebox.showinfo(
                "Settings saved",
                "Your settings have been saved.",
                parent=root,
            )
        return True

    def generate_password():
        password_label.configure(
            text=genpass(
                length_variable.get(),
                uppercase_variable.get(),
                numbers_variable.get(),
                special_variable.get(),
            )
        )

    def close_settings(save=True):
        nonlocal settings_window
        if settings_window is not None:
            if save:
                persist_settings()
            settings_window.destroy()
            settings_window = None

    def show_settings():
        nonlocal settings_window
        if settings_window is not None and settings_window.winfo_exists():
            settings_window.lift()
            settings_window.focus_set()
            return

        settings_window = tk.Toplevel(root)
        settings_window.title("Password Generation Settings")
        settings_window.geometry("420x400")
        settings_window.minsize(360, 360)
        settings_window.configure(bg="#000000")
        settings_window.transient(root)
        settings_window.columnconfigure(0, weight=1)
        settings_window.protocol("WM_DELETE_WINDOW", close_settings)

        settings_frame = tk.Frame(
            settings_window,
            bg="#000000",
            padx=24,
            pady=20,
        )
        settings_frame.grid(row=0, column=0, sticky="nsew")
        settings_frame.columnconfigure(0, weight=1)

        tk.Label(
            settings_frame,
            text="Password settings",
            bg="#000000",
            fg="#00FF00",
            font=("Comic Sans MS", 14),
        ).grid(row=0, column=0, pady=(0, 12))

        tk.Label(
            settings_frame,
            text="Password length",
            bg="#000000",
            fg="#00FF00",
            font=("Comic Sans MS", 10),
        ).grid(row=1, column=0, sticky="w")

        tk.Scale(
            settings_frame,
            from_=1,
            to=32,
            orient=tk.HORIZONTAL,
            variable=length_variable,
            bg="#000000",
            fg="#00FF00",
            troughcolor="#333333",
            highlightbackground="#000000",
            activebackground="#00FF00",
            font=("Comic Sans MS", 9),
            showvalue=True,
        ).grid(row=2, column=0, sticky="ew", pady=(0, 12))

        for row, text, variable in (
            (3, "Include uppercase letters", uppercase_variable),
            (4, "Include numbers", numbers_variable),
            (5, "Include special characters", special_variable),
        ):
            tk.Checkbutton(
                settings_frame,
                text=text,
                variable=variable,
                bg="#000000",
                fg="#00FF00",
                selectcolor="#222222",
                activebackground="#000000",
                activeforeground="#00FF00",
                font=("Comic Sans MS", 10),
                anchor="w",
            ).grid(row=row, column=0, sticky="ew")

        tk.Button(
            settings_frame,
            text="Generate Password",
            command=generate_password,
            bg="#000000",
            fg="#00FF00",
            activebackground="#00FF00",
            activeforeground="#000000",
            font=("Comic Sans MS", 12),
        ).grid(row=6, column=0, sticky="ew", pady=(18, 8))

        tk.Button(
            settings_frame,
            text="Save Settings",
            command=lambda: persist_settings(show_confirmation=True),
            bg="#000000",
            fg="#00FF00",
            activebackground="#00FF00",
            activeforeground="#000000",
            font=("Comic Sans MS", 10),
        ).grid(row=7, column=0, sticky="ew")

        tk.Label(
            settings_frame,
            text="Settings are also saved when you close this window.",
            bg="#000000",
            fg="#00FF00",
            font=("Comic Sans MS", 8),
        ).grid(row=8, column=0, pady=(10, 0))

    def export_settings():
        filename = filedialog.asksaveasfilename(
            parent=root,
            title="Save Configuration",
            defaultextension=".json",
            filetypes=(("JSON files", "*.json"), ("All files", "*.*")),
        )
        if not filename:
            return

        try:
            write_settings(filename, current_settings())
        except OSError as error:
            messagebox.showerror(
                "Could not save configuration",
                str(error),
                parent=root,
            )
        else:
            messagebox.showinfo(
                "Configuration saved",
                "Your configuration has been saved.",
                parent=root,
            )

    def import_settings():
        filename = filedialog.askopenfilename(
            parent=root,
            title="Open Configuration",
            filetypes=(("JSON files", "*.json"), ("All files", "*.*")),
        )
        if not filename:
            return

        try:
            settings = read_settings(filename)
        except (OSError, json.JSONDecodeError, ValueError) as error:
            messagebox.showerror(
                "Could not open configuration",
                str(error),
                parent=root,
            )
            return

        length_variable.set(settings["length"])
        uppercase_variable.set(settings["use_uppercase"])
        numbers_variable.set(settings["use_numbers"])
        special_variable.set(settings["use_special"])
        persist_settings()

    menu = tk.Menu(root)
    root.configure(menu=menu)

    options_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Options", menu=options_menu)
    options_menu.add_command(label="Save Configuration...", command=export_settings)
    options_menu.add_command(label="Open Configuration...", command=import_settings)
    options_menu.add_separator()
    options_menu.add_command(label="Exit", command=lambda: close_application())

    settings_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Settings", menu=settings_menu)
    settings_menu.add_command(
        label="Password Generation Settings...",
        command=show_settings,
    )

    help_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(
        label="About the Project",
        command=lambda: open_new_tab(
            "https://github.com/kavim/python-random-password-generator"
        ),
    )
    help_menu.add_command(
        label="Contact Me",
        command=lambda: open_new_tab("mailto:kavi@mistrypi.dev"),
    )

    def close_application():
        close_settings(save=False)
        persist_settings()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", close_application)
    root.mainloop()


if __name__ == "__main__":
    main()
