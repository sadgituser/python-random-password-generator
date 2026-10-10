# Project imports
import json
import os
import random
import tkinter as tk
from pathlib import Path
from tkinter import colorchooser, filedialog, messagebox
from webbrowser import open_new_tab

THEMES = {
    "Forest": {
        "background": "#101820",
        "text": "#DCE8E2",
        "accent": "#83C9A5",
        "surface": "#1B2931",
    },

    "Matrix Green": {
            "background": "#000000",
            "text": "#00FF00",
            "accent": "#5F945F",
            "surface": "#000000",
    },

    "Matrix Blue": {
            "background": "#000000",
            "text": "#0000FF",
            "accent": "#151572",
            "surface": "#000000",
    },

    "Matrix Red": {
            "background": "#000000",
            "text": "#FF0000",
            "accent": "#682323",
            "surface": "#000000",
    },

    "Ocean": {
        "background": "#101923",
        "text": "#DDE8F2",
        "accent": "#83BDE0",
        "surface": "#1B2B3A",
    },

    "Desert": {
        "background": "#DDCA3A",
        "text": "#6D692E",
        "accent": "#E99444",
        "surface": "#A0CA3D",
    },

    "Light": {
        "background": "#F2F5F3",
        "text": "#24312A",
        "accent": "#267A55",
        "surface": "#E0E8E3",
    },

    "Dark": {
            "background": "#1F1F1F",
            "text": "#8A8A8A",
            "accent": "#70C9A2",
            "surface": "#2F3130",
    },
}
RAINBOW_COLORS = (
    "#83C9A5",
    "#83BDE0",
    "#A9A0D8",
    "#D59BC0",
    "#D99F88",
    "#C9B575",
)
TEXT_SCALES = {"Standard": 1.0, "Large": 1.25, "Extra large": 1.5}

# Set either path to a PNG, GIF, or other format supported by Tkinter PhotoImage.
# Relative paths are resolved from the folder containing this script.
ROOT_ICON_PATH = None
SETTINGS_ICON_PATH = None

DEFAULT_SETTINGS = {
    "length": 14,
    "use_uppercase": True,
    "use_numbers": True,
    "use_special": True,
    "memorable_text": "",
    "theme": "Matrix Green",
    "background_color": THEMES["Matrix Green"]["background"],
    "text_color": THEMES["Matrix Green"]["text"],
    "accent_color": THEMES["Matrix Green"]["accent"],
    "surface_color": THEMES["Matrix Green"]["surface"],
    "rainbow_mode": False,
    "text_size": "Standard",
}

APP_DATA_DIRECTORY = Path(os.environ.get("APPDATA") or Path.home())
SETTINGS_FILE = APP_DATA_DIRECTORY / "PasswordGenerator" / "settings.json"


def validate_color(value, name):
    if (
        not isinstance(value, str)
        or len(value) != 7
        or value[0] != "#"
        or any(character not in "0123456789abcdefABCDEF" for character in value[1:])
    ):
        raise ValueError(f"'{name}' must be a six-digit hexadecimal colour.")
    return value


def genpass(length, use_uppercase, use_numbers, use_special, memorable_text=""):
    characters = "abcdefghijklmnopqrstuvwxyz"
    if use_uppercase:
        characters += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if use_numbers:
        characters += "0123456789"
    if use_special:
        characters += "`¬!@#$%^&*()_+-=[]}{|;':,./<>?"

    if not isinstance(memorable_text, str):
        raise ValueError("Memorable text must be a string.")

    password_length = max(length, len(memorable_text))
    random_characters = "".join(
        random.choice(characters)
        for _ in range(password_length - len(memorable_text))
    )
    insertion_point = random.randint(0, len(random_characters))
    return (
        random_characters[:insertion_point]
        + memorable_text
        + random_characters[insertion_point:]
    )


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

    memorable_text = data.get("memorable_text", "")
    if not isinstance(memorable_text, str):
        raise ValueError("'memorable_text' must be a string.")
    settings["memorable_text"] = memorable_text

    theme = data.get("theme", DEFAULT_SETTINGS["theme"])
    if not isinstance(theme, str) or theme not in (*THEMES, "Custom"):
        raise ValueError("'theme' must be Forest, Ocean, Light, Matrix Colours, Desert or Custom.")
    settings["theme"] = theme

    for key in ("background_color", "text_color", "accent_color", "surface_color"):
        settings[key] = validate_color(data.get(key, DEFAULT_SETTINGS[key]), key)

    rainbow_mode = data.get("rainbow_mode", False)
    if type(rainbow_mode) is not bool:
        raise ValueError("'rainbow_mode' must be true or false.")
    settings["rainbow_mode"] = rainbow_mode

    text_size = data.get("text_size", DEFAULT_SETTINGS["text_size"])
    if not isinstance(text_size, str) or text_size not in TEXT_SCALES:
        raise ValueError("'text_size' must be Standard, Large, or Extra large.")
    settings["text_size"] = text_size

    return settings


def make_logo_icon(kind):
    image = tk.PhotoImage(width=32, height=32)
    background = "#101820"
    accent = "#83C9A5"
    image.put(background, to=(0, 0, 32, 32))

    if kind == "key":
        for y in range(7, 25):
            for x in range(4, 22):
                if (x - 13) ** 2 + (y - 16) ** 2 <= 81:
                    image.put(accent, to=(x, y))
        for y in range(12, 21):
            for x in range(10, 28):
                if x >= 18 or (x - 13) ** 2 + (y - 16) ** 2 >= 20:
                    image.put(accent, to=(x, y))
        for y in range(17, 23):
            for x in range(22, 25):
                image.put(background, to=(x, y))
    else:
        for y in range(5, 27):
            for x in range(5, 27):
                distance = (x - 16) ** 2 + (y - 16) ** 2
                if 65 <= distance <= 110 or (distance <= 150 and (x in (9, 22) or y in (9, 22))):
                    image.put(accent, to=(x, y))
        for y in range(12, 20):
            for x in range(12, 20):
                if 5 <= (x - 16) ** 2 + (y - 16) ** 2 <= 16:
                    image.put(background, to=(x, y))
    return image


def window_icon(window, icon_path, fallback, parent):
    if not icon_path:
        image = fallback
    else:
        path = Path(icon_path)
        if not path.is_absolute():
            path = Path(__file__).resolve().parent / path
        try:
            image = tk.PhotoImage(file=str(path))
        except tk.TclError as error:
            messagebox.showerror(
                "Could not load window icon",
                f"The icon file could not be loaded:\n{path}\n\n{error}",
                parent=parent,
            )
            image = fallback
    window.iconphoto(True, image)
    return image


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
    root.title("Python Password Generator")
    root.geometry("520x280+300+200")
    root.minsize(360, 220)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    icon_images = {
        "root": window_icon(
            root,
            ROOT_ICON_PATH,
            make_logo_icon("key"),
            root,
        ),
        "settings": None,
    }

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
    memorable_text_variable = tk.StringVar(
        value=initial_settings["memorable_text"]
    )
    theme_variable = tk.StringVar(value=initial_settings["theme"])
    background_color_variable = tk.StringVar(
        value=initial_settings["background_color"]
    )
    text_color_variable = tk.StringVar(value=initial_settings["text_color"])
    accent_color_variable = tk.StringVar(value=initial_settings["accent_color"])
    surface_color_variable = tk.StringVar(value=initial_settings["surface_color"])
    rainbow_variable = tk.BooleanVar(value=initial_settings["rainbow_mode"])
    text_size_variable = tk.StringVar(value=initial_settings["text_size"])

    settings_window = None
    about_window = None
    password_label = None
    about_heading = None
    font_widgets = []
    theme_menus = []
    rainbow_after_id = None
    password_animation_after_id = None
    rainbow_index = 0

    def register_font(widget, size, family="IBM Plex Mono"):
        font_widgets.append((widget, size, family))
        widget.configure(font=(family, size))
        return widget

    def apply_text_size():
        scale = TEXT_SCALES[text_size_variable.get()]
        for widget, size, family in font_widgets:
            if widget.winfo_exists():
                widget.configure(font=(family, max(8, round(size * scale))))
        dimensions = {
            "Standard": "520x280+300+200",
            "Large": "590x340+300+200",
            "Extra large": "650x390+300+200",
        }
        root.geometry(dimensions[text_size_variable.get()])
        if settings_window is not None and settings_window.winfo_exists():
            heights = {"Standard": 680, "Large": 740, "Extra large": 800}
            settings_window.geometry(
                f"520x{heights[text_size_variable.get()]}"
            )
        if about_window is not None and about_window.winfo_exists():
            dimensions = {
                "Standard": "520x480",
                "Large": "590x540",
                "Extra large": "650x600",
            }
            about_window.geometry(dimensions[text_size_variable.get()])

    def apply_theme():
        accent = accent_color_variable.get()
        if rainbow_variable.get():
            accent = RAINBOW_COLORS[rainbow_index]
        colors = {
            "background": background_color_variable.get(),
            "text": text_color_variable.get(),
            "accent": accent,
            "surface": surface_color_variable.get(),
        }

        def style_children(container):
            for widget in container.winfo_children():
                widget_class = widget.winfo_class()
                if widget_class in ("Frame", "Toplevel"):
                    widget.configure(bg=colors["background"])
                elif widget_class == "Label":
                    foreground = (
                        colors["accent"]
                        if widget in (password_label, about_heading)
                        else colors["text"]
                    )
                    widget.configure(
                        bg=colors["background"],
                        fg=foreground,
                    )
                elif widget_class == "Button":
                    widget.configure(
                        bg=colors["surface"],
                        fg=colors["text"],
                        activebackground=colors["accent"],
                        activeforeground=colors["background"],
                    )
                elif widget_class == "Entry":
                    widget.configure(
                        bg=colors["surface"],
                        fg=colors["text"],
                        insertbackground=colors["accent"],
                    )
                elif widget_class == "Scale":
                    widget.configure(
                        bg=colors["background"],
                        fg=colors["text"],
                        troughcolor=colors["surface"],
                        highlightbackground=colors["background"],
                        activebackground=colors["accent"],
                    )
                elif widget_class == "Checkbutton":
                    widget.configure(
                        bg=colors["background"],
                        fg=colors["text"],
                        selectcolor=colors["surface"],
                        activebackground=colors["background"],
                        activeforeground=colors["accent"],
                    )
                elif widget_class == "Menubutton":
                    widget.configure(
                        bg=colors["surface"],
                        fg=colors["text"],
                        activebackground=colors["accent"],
                        activeforeground=colors["background"],
                    )
                style_children(widget)

        root.configure(bg=colors["background"])
        style_children(root)
        if settings_window is not None and settings_window.winfo_exists():
            settings_window.configure(bg=colors["background"])
        if about_window is not None and about_window.winfo_exists():
            about_window.configure(bg=colors["background"])
            style_children(about_window)
        for menu_widget in theme_menus:
            menu_widget.configure(
                bg=colors["surface"],
                fg=colors["text"],
                activebackground=colors["accent"],
                activeforeground=colors["background"],
            )

    def apply_saved_theme():
        theme = theme_variable.get()
        if theme in THEMES:
            colors = THEMES[theme]
            background_color_variable.set(colors["background"])
            text_color_variable.set(colors["text"])
            accent_color_variable.set(colors["accent"])
            surface_color_variable.set(colors["surface"])
        apply_theme()

    def choose_color(variable, title):
        selected_color = colorchooser.askcolor(
            color=variable.get(),
            title=title,
            parent=settings_window,
        )[1]
        if selected_color:
            variable.set(selected_color)
            theme_variable.set("Custom")
            apply_theme()

    def cycle_rainbow():
        nonlocal rainbow_after_id, rainbow_index
        if not rainbow_variable.get():
            rainbow_after_id = None
            apply_theme()
            return
        rainbow_index = (rainbow_index + 1) % len(RAINBOW_COLORS)
        apply_theme()
        rainbow_after_id = root.after(4500, cycle_rainbow)

    def toggle_rainbow():
        nonlocal rainbow_after_id
        if rainbow_variable.get():
            if rainbow_after_id is None:
                cycle_rainbow()
        else:
            if rainbow_after_id is not None:
                root.after_cancel(rainbow_after_id)
                rainbow_after_id = None
            apply_theme()

    def theme_selected(selection):
        theme_variable.set(selection)
        apply_saved_theme()

    def text_size_selected(selection):
        text_size_variable.set(selection)
        apply_text_size()

    main_frame = tk.Frame(root, bg="#000000", padx=24, pady=24)
    main_frame.grid(row=0, column=0, sticky="nsew")
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=0)
    main_frame.rowconfigure(1, weight=1)

    heading = register_font(tk.Label(
        main_frame,
        text="Your password is:",
        bg="#000000",
        font=("IBM Plex Mono", 16),
    ), 16)
    heading.grid(row=0, column=0, pady=(0, 12))

    generated_password = tk.StringVar()
    password_label = register_font(tk.Label(
        main_frame,
        text="Click Generate Password to get started.",
        bg="#000000",
        font=("IBM Plex Mono", 14),
        wraplength=460,
        justify=tk.CENTER,
    ), 14)
    password_label.grid(row=1, column=0, sticky="nsew")
    password_label.bind(
        "<Configure>",
        lambda event: password_label.configure(wraplength=max(200, event.width - 16)),
    )

    def copy_password():
        password = generated_password.get()
        if not password:
            return
        try:
            root.clipboard_clear()
            root.clipboard_append(password)
            root.update()
        except tk.TclError as error:
            messagebox.showerror(
                "Could not copy password",
                str(error),
                parent=root,
            )

    copy_button = register_font(tk.Button(
        main_frame,
        text="Copy",
        command=copy_password,
        state=tk.DISABLED,
        bg="#000000",
        font=("IBM Plex Mono", 10),
    ), 10)
    copy_button.grid(row=1, column=1, padx=(12, 0))

    def generate_password():
        nonlocal password_animation_after_id
        password = genpass(
            length_variable.get(),
            uppercase_variable.get(),
            numbers_variable.get(),
            special_variable.get(),
            memorable_text_variable.get(),
        )
        animation_characters = (
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
            "0123456789!@#$%^&*"
        )
        animation_frames = random.randint(0, 100)
        animation_frame = 0

        copy_button.configure(state=tk.DISABLED)
        generate_button.configure(state=tk.DISABLED)
        password_label.configure(textvariable=generated_password)

        def animate_password():
            nonlocal animation_frame, password_animation_after_id
            animation_frame += 1
            revealed_characters = (
                len(password) * animation_frame // animation_frames
            )
            generated_password.set(
                password[:revealed_characters]
                + "".join(
                    random.choice(animation_characters)
                    for _ in range(len(password) - revealed_characters)
                )
            )

            if animation_frame == animation_frames:
                generated_password.set(password)
                copy_button.configure(state=tk.NORMAL)
                generate_button.configure(state=tk.NORMAL)
                password_animation_after_id = None
            else:
                password_animation_after_id = root.after(
                    50,
                    animate_password,
                )

        animate_password()

    generate_button = register_font(tk.Button(
        main_frame,
        text="Generate Password",
        command=generate_password,
        bg="#000000",
        font=("IBM Plex Mono", 12),
    ), 12)
    generate_button.grid(
        row=2,
        column=0,
        columnspan=2,
        sticky="ew",
        pady=(16, 0),
    )

    apply_saved_theme()
    apply_text_size()

    def current_settings():
        return {
            "length": length_variable.get(),
            "use_uppercase": uppercase_variable.get(),
            "use_numbers": numbers_variable.get(),
            "use_special": special_variable.get(),
            "memorable_text": memorable_text_variable.get(),
            "theme": theme_variable.get(),
            "background_color": background_color_variable.get(),
            "text_color": text_color_variable.get(),
            "accent_color": accent_color_variable.get(),
            "surface_color": surface_color_variable.get(),
            "rainbow_mode": rainbow_variable.get(),
            "text_size": text_size_variable.get(),
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

    def close_settings(save=True):
        nonlocal settings_window
        if settings_window is not None:
            if save:
                persist_settings()
            settings_window.destroy()
            settings_window = None
            theme_menus[:] = [
                menu_widget
                for menu_widget in theme_menus
                if menu_widget.winfo_exists()
            ]

    def show_settings():
        nonlocal settings_window
        if settings_window is not None and settings_window.winfo_exists():
            settings_window.lift()
            settings_window.focus_set()
            return

        settings_window = tk.Toplevel(root)
        settings_window.title("Password Generation Settings")
        settings_window.geometry("520x680")
        settings_window.minsize(420, 600)
        settings_window.configure(bg="#000000")
        settings_window.transient(root)
        settings_window.columnconfigure(0, weight=1)
        settings_window.protocol("WM_DELETE_WINDOW", close_settings)
        icon_images["settings"] = window_icon(
            settings_window,
            SETTINGS_ICON_PATH,
            make_logo_icon("gear"),
            settings_window,
        )

        settings_frame = tk.Frame(
            settings_window,
            bg="#000000",
            padx=24,
            pady=20,
        )
        settings_frame.grid(row=0, column=0, sticky="nsew")
        settings_frame.columnconfigure(0, weight=1)

        register_font(tk.Label(
            settings_frame,
            text="Password settings",
            bg="#000000",
            font=("IBM Plex Mono", 14),
        ), 14).grid(row=0, column=0, pady=(0, 12))

        register_font(tk.Label(
            settings_frame,
            text="Password length",
            bg="#000000",
            font=("IBM Plex Mono", 10),
        ), 10).grid(row=1, column=0, sticky="w")

        register_font(tk.Scale(
            settings_frame,
            from_=1,
            to=32,
            orient=tk.HORIZONTAL,
            variable=length_variable,
            bg="#000000",
            troughcolor="#333333",
            highlightbackground="#000000",
            font=("IBM Plex Mono", 9),
            showvalue=True,
        ), 9).grid(row=2, column=0, sticky="ew", pady=(0, 12))

        register_font(tk.Label(
            settings_frame,
            text="Word or phrase to include",
            bg="#000000",
            font=("IBM Plex Mono", 10),
        ), 10).grid(row=3, column=0, sticky="w")

        register_font(tk.Entry(
            settings_frame,
            textvariable=memorable_text_variable,
            bg="#111111",
            insertbackground="#00FF00",
            font=("Consolas", 11),
        ), 11, "Consolas").grid(row=4, column=0, sticky="ew", pady=(2, 12))

        for row, text, variable in (
            (5, "Include uppercase letters", uppercase_variable),
            (6, "Include numbers", numbers_variable),
            (7, "Include special characters", special_variable),
        ):
            register_font(tk.Checkbutton(
                settings_frame,
                text=text,
                variable=variable,
                bg="#000000",
                selectcolor="#222222",
                activebackground="#000000",
                font=("IBM Plex Mono", 10),
                anchor="w",
            ), 10).grid(row=row, column=0, sticky="ew")

        register_font(tk.Button(
            settings_frame,
            text="Save Settings",
            command=lambda: persist_settings(show_confirmation=True),
            bg="#000000",
            font=("IBM Plex Mono", 10),
        ), 10).grid(row=8, column=0, sticky="ew", pady=(18, 0))

        register_font(tk.Label(
            settings_frame,
            text="Settings are also saved when you close this window.",
            bg="#000000",
            font=("IBM Plex Mono", 8),
        ), 8).grid(row=9, column=0, pady=(10, 0))

        tk.Frame(
            settings_frame,
            height=2,
            bg="#333333",
        ).grid(row=10, column=0, sticky="ew", pady=(16, 10))

        register_font(tk.Label(
            settings_frame,
            text="Appearance",
            bg="#000000",
            font=("IBM Plex Mono", 13),
        ), 13).grid(row=11, column=0, sticky="w", pady=(0, 6))

        theme_menu = tk.OptionMenu(
            settings_frame,
            theme_variable,
            *THEMES,
            "Custom",
            command=theme_selected,
        )
        register_font(theme_menu, 10)
        register_font(theme_menu["menu"], 10)
        theme_menu.grid(row=12, column=0, sticky="ew")
        theme_menus.append(theme_menu["menu"])

        color_frame = tk.Frame(settings_frame, bg="#000000")
        color_frame.grid(row=13, column=0, sticky="ew", pady=(8, 4))
        for column in range(2):
            color_frame.columnconfigure(column, weight=1)
        for row, label, variable in (
            (0, "Background colour...", background_color_variable),
            (0, "Text colour...", text_color_variable),
            (1, "Accent colour...", accent_color_variable),
            (1, "Button colour...", surface_color_variable),
        ):
            column = 0 if label.startswith(("Background", "Accent")) else 1
            register_font(tk.Button(
                color_frame,
                text=label,
                command=lambda color_variable=variable, color_title=label: choose_color(
                    color_variable,
                    color_title.replace("...", ""),
                ),
                bg="#000000",
                font=("IBM Plex Mono", 9),
            ), 9).grid(row=row, column=column, sticky="ew", padx=3, pady=3)

        size_frame = tk.Frame(settings_frame, bg="#000000")
        size_frame.grid(row=14, column=0, sticky="ew", pady=(5, 0))
        size_frame.columnconfigure(1, weight=1)
        register_font(tk.Label(
            size_frame,
            text="Text size",
            bg="#000000",
            font=("IBM Plex Mono", 10),
        ), 10).grid(row=0, column=0, sticky="w", padx=(0, 12))
        size_menu = tk.OptionMenu(
            size_frame,
            text_size_variable,
            *TEXT_SCALES,
            command=text_size_selected,
        )
        register_font(size_menu, 10)
        register_font(size_menu["menu"], 10)
        size_menu.grid(row=0, column=1, sticky="ew")
        theme_menus.append(size_menu["menu"])

        register_font(tk.Checkbutton(
            settings_frame,
            text="Gentle rainbow accent (slow colour cycle)",
            variable=rainbow_variable,
            command=toggle_rainbow,
            bg="#000000",
            font=("IBM Plex Mono", 10),
            anchor="w",
        ), 10).grid(row=15, column=0, sticky="ew", pady=(8, 0))

        apply_theme()
        apply_text_size()

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
        memorable_text_variable.set(settings["memorable_text"])
        theme_variable.set(settings["theme"])
        background_color_variable.set(settings["background_color"])
        text_color_variable.set(settings["text_color"])
        accent_color_variable.set(settings["accent_color"])
        surface_color_variable.set(settings["surface_color"])
        rainbow_variable.set(settings["rainbow_mode"])
        text_size_variable.set(settings["text_size"])
        apply_theme()
        apply_text_size()
        toggle_rainbow()
        persist_settings()

    menu = tk.Menu(root)
    root.configure(menu=menu)
    theme_menus.append(menu)

    options_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Options", menu=options_menu)
    theme_menus.append(options_menu)
    options_menu.add_command(label="Save Configuration...", command=export_settings)
    options_menu.add_command(label="Open Configuration...", command=import_settings)
    options_menu.add_separator()
    options_menu.add_command(label="Exit", command=lambda: close_application())

    settings_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Settings", menu=settings_menu)
    theme_menus.append(settings_menu)
    settings_menu.add_command(
        label="Password Generation Settings...",
        command=show_settings,
    )

    def infopage():
        nonlocal about_window, about_heading
        if about_window is not None and about_window.winfo_exists():
            about_window.lift()
            about_window.focus_set()
            return

        about_window = tk.Toplevel(root)
        about_window.title("About Me")
        about_window.geometry("520x480+50+50")
        about_window.minsize(400, 360)
        about_window.transient(root)
        about_window.columnconfigure(0, weight=1)
        about_window.rowconfigure(0, weight=1)
        about_window.protocol(
            "WM_DELETE_WINDOW",
            close_about_page,
        )

        about_frame = tk.Frame(about_window, padx=28, pady=24)
        about_frame.grid(row=0, column=0, sticky="nsew")
        about_frame.columnconfigure(0, weight=1)

        about_heading = register_font(tk.Label(
            about_frame,
            text="About Me",
            font=("IBM Plex Mono", 18),
            justify=tk.CENTER,
        ), 18)
        about_heading.grid(row=0, column=0, pady=(0, 8))

        register_font(tk.Label(
            about_frame,
            text="I am Kavi Mistry - Maker/Hobbyist  :)",
            font=("IBM Plex Mono", 13),
            justify=tk.CENTER,
        ), 13).grid(row=1, column=0, pady=(0, 20))

        for row, title, details in (
            (2, "A little about me,", "I am alive (can you believe it!) and creating projects with Hackclub. I saw the Terra project (https://terra.hackclub.com) and decided to join it and this project was created for that reason. Still in school tho :( "),
            (4, "Interests", "I like making things  >:) such as little projects like these. I quite like coding and making things that other people will enjoy  :) "),
            (6, "Get in touch", "Click the 'Contact Me' button on the top menu to open a Mailto: link to my email address. You could also check out my GitHub at https://github.com/sadgituser and see my upcoming projects on there!"),
        ):
            register_font(tk.Label(
                about_frame,
                text=title,
                font=("IBM Plex Mono", 11),
                anchor="w",
                justify=tk.LEFT,
            ), 11).grid(row=row, column=0, sticky="ew", pady=(8, 2))
            details_label = register_font(tk.Label(
                about_frame,
                text=details,
                font=("IBM Plex Mono", 10),
                anchor="w",
                justify=tk.LEFT,
                wraplength=400,
            ), 10)
            details_label.grid(row=row + 1, column=0, sticky="ew")
            details_label.bind(
                "<Configure>",
                lambda event: event.widget.configure(
                    wraplength=max(180, event.width - 16)
                ),
            )

        register_font(tk.Button(
            about_frame,
            text="Close",
            command=close_about_page,
            font=("IBM Plex Mono", 10),
        ), 10).grid(row=8, column=0, sticky="ew", pady=(24, 0))

        apply_theme()
        apply_text_size()

    def close_about_page():
        nonlocal about_window, about_heading
        if about_window is not None:
            about_window.destroy()
            about_window = None
            about_heading = None


    help_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Help", menu=help_menu)
    theme_menus.append(help_menu)
    help_menu.add_command(
        label="About the Project",
        command=infopage,
    )
    help_menu.add_command(
        label="Contact Me (Your Default Email Service will be Opened)",
        command=lambda: open_new_tab("mailto:kavi@mistrypi.dev"),
    )

    def prompt_generate_password():
        tk.messagebox.showwarning(title="Password?", message="Are you going to generate a password? If not then CLOSE ME!!")
        root.after(random.randint(60000, 600000), prompt_generate_password)

    def close_application():
        close_settings(save=False)
        if rainbow_after_id is not None:
            root.after_cancel(rainbow_after_id)
        if password_animation_after_id is not None:
            root.after_cancel(password_animation_after_id)
        persist_settings()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", close_application)
    apply_theme()
    apply_text_size()
    if rainbow_variable.get():
        toggle_rainbow()
    prompt_generate_password()
    prompt_generate_password
    root.mainloop()


if __name__ == "__main__":
    main()

