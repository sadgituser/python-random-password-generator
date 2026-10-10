# Python Random Password Generator

A customizable desktop password generator built using Python and Tkinter.


## Screenshots


First Screenshot:

![Screenshot of the Password Generation App screen](/Assets/photo1.png)


Second Screenshot:

![Screenshot of the Password Generation App with a Password on](/Assets/photo2.png)


Third Screenshot:

![Sceenshot of the Password Generation App Settings](/Assets/photo3.png)


Fourth Screenshot:

![Screenshotof the About Me page](/Assets/photo4.png)


## Usage

Launch `password_generator.exe`. Go to **Settings > Password Generation Settings** to configure your password length, character options, or add a custom word/phrase to include, then click **Generate Password** or the **Enter Key** (does not always work) on the main screen. Characters scroll through each position before the completed password appears. If your custom phrase exceeds the chosen length, the password will automatically expand to fit it. You can copy the generated password straight to your clipboard with the **Copy** button.

Your settings save automatically whenever you close the app or the settings window, though you can also force an immediate save via **Save Settings**. To back up or load specific setups, use **Options > Save Configuration** and **Options > Open Configuration** to export or import your settings as a JSON file.
Use **Randomise Settings** in the settings window to shuffle the password length, character options, preset theme, and rainbow toggle. It leaves your text size and included word/phrase unchanged and does not create custom colours.

## Appearance

Head to **Settings > Password Generation Settings** under the **Appearance** section to customize the interface. You can pick from built-in color themes (Forest, Ocean, Matrix Colours, Desert), toggle between Light and Dark modes, or manually set custom colors for the background, text, accents, and buttons. Enabling **Gentle rainbow accent** slowly rotates through soft accent colors across key elements like the generated password display. For better accessibility, you can also switch to **Large** or **Extra large** text size.

Custom themes and UI choices are saved alongside your general preferences and included in JSON config exports. Older settings files remain compatible and will fall back to default values for any new options.

### Storage Location
Settings are saved automatically to `%APPDATA%\PasswordGenerator\settings.json` on Windows, or within a `PasswordGenerator` folder in your user home directory on Linux and macOS.

Made for the [Hackclub Terra](https://terra.hackclub.com) project for [Hackclub](https://hackclub.com).



![Hackclub Flag](/Assets/photo5.png) ![Hackclub Terra Fox](/Assets/photo6.png)