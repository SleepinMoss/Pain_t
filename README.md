# Pain_t

*A painful drawing app...*

## Screenshot

<img width="1366" height="711" alt="image" src="https://github.com/user-attachments/assets/8edfb457-23df-4721-ac4f-d1a1a7990179" />
Yes, I drew that!
Its not an original artwork. Link to the reference: https://pin.it/5hth0dZbp


## What in the world...

A few months ago, I started getting really into digital art. Then I had the completely delusional idea of making my own drawing app. It was supposed to be a quick little project. Yeah... it wasn't.

Instead, it turned into 480 lines of code and made me question every life decision that led me here. That's why **Pain_t** felt like the perfect name.

Also, I made the icon in Pain_t itself!

## Features

* Brush
* Eraser
* Color Picker
* Undo
* Redo
* Brush Stabilizer
* HSV Color Picker
* Export as PNG
* Import PNG, JPEG, and Pain_t JSON files
* Save as JSON to preserve stroke history, enabling Undo and Redo

## Keybinds

| Key      | Action              |
| -------- | ------------------- |
| B        | Brush               |
| E        | Eraser              |
| C        | Color Picker        |
| A        | Decrease Brush Size |
| D        | Increase Brush Size |
| Ctrl + Z | Undo                |
| Ctrl + Y | Redo                |

## Installation

Supports Windows, Linux, and MacOS. Doesn't support TempleOS though...

Go to the **Releases** tab, download the version for your operating system, extract it, and have fun!

Or should I say... pain.

### Linux

Doesn't supports Wayland. It works perfectly on X11 though!

### MacOS

Apologize for MacOS x86_64 (Intel Cpu) user. I have been trying to build it on Github, but doesn't seem to work. 
Instead, I will give you guys tutorial!

1. Install Python
2. Install Dependencies
3. Install PyInstaller
4. Install and unzip the source code
5. Open your terminal and go to the directory you installed the source code
6. Finally, paste this command:
```bash
pyinstaller --onefile --windowed --collect-all PIL --icon=assets/icon.icns --add-data "assets:assets" pain_t.py
```

## Bugs?

If you find one, congratulations! You've discovered a feature I didn't know existed.
