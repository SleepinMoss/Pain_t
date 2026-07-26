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

Go to the **Releases** tab, download the version for your operating system, extract it, and have fun!

Or should I say... pain.

### Linux

This app work on linux, but for some reason the color picker doesnt work on wayland. Worry not, it works on X11

After extracting the archive, you'll need to make the file executable.

```bash
cd path/to/file
chmod +x pain_t
```

Then run:

```bash
./pain_t
```

## Bugs?

If you find one, congratulations! You've discovered a feature I didn't know existed.

Seriously though, this is a personal project. Expect bugs, but don't expect me to fix them. Maybe I will. Maybe I won't.

Supports Linux, MacOS (have only been tested on Intel CPU Mac), and Windows. Doesn't support TempleOS currently though...
