# Python Random Password Generator

A customizable desktop password generator built using Python and Tkinter.


## Screenshots

![Screenshot of the password gen screen](Assets\photo1.png)
![Screenshot of the password gen with a password on](Assets\photo2.png)
![Sceenshot of the password gen settings](Assets\photo3.png)


## Usage

Launch `password_generator.exe`. Go to **Settings > Password Generation Settings** to configure your password length, character options, or add a custom word/phrase to include, then click **Generate Password** on the main screen. Characters scroll through each position before the completed password appears. If your custom phrase exceeds the chosen length, the password will automatically expand to fit it. You can copy the generated password straight to your clipboard with the **Copy** button.

Your settings save automatically whenever you close the app or the settings window, though you can also force an immediate save via **Save Settings**. To back up or load specific setups, use **Options > Save Configuration** and **Options > Open Configuration** to export or import your settings as a JSON file.

## Appearance

Head to **Settings > Password Generation Settings** under the **Appearance** section to customize the interface. You can pick from built-in color themes (Forest, Ocean, Matrix Colours, Desert), toggle between Light and Dark modes, or manually set custom colors for the background, text, accents, and buttons. Enabling **Gentle rainbow accent** slowly rotates through soft accent colors across key elements like the generated password display. For better accessibility, you can also switch to **Large** or **Extra large** text size.

Custom themes and UI choices are saved alongside your general preferences and included in JSON config exports. Older settings files remain compatible and will fall back to default values for any new options.

### Custom Window Icons
The app comes with built-in icons for the main window (key) and settings window (gear). To use custom icons, update `ROOT_ICON_PATH` and `SETTINGS_ICON_PATH` near the top of `password_generator.py` with your image paths (PNG, GIF, or any format supported by Tkinter's `PhotoImage`). Relative paths resolve relative to the script directory.

### Storage Location
Settings are saved automatically to `%APPDATA%\PasswordGenerator\settings.json` on Windows, or within a `PasswordGenerator` folder in your user home directory on Linux and macOS.

Made for the [Terra](terra.hackclub.com) project.
