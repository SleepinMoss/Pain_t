import tkinter as tk
import colorsys, json
from tkinter import *
from tkinter import filedialog, messagebox
from pathlib import Path
from PIL import ImageGrab, Image, ImageTk

root = tk.Tk()
root.title("Pain_t")
root.geometry("1080x720")

theme = {
    "bgCol":"#232323",
    "panelCol":"#090A0B",
    "buttonCol":"#232323",
    "textCol":"#E9E9E9",
    "accent":"#2F5BA8"
}
shortcut = {
    "pen":"<b>",
    "eraser":"<e>",
    "colPick":"<c>",
    "undo":"<Control-z>",
    "redo":"<Control-y>",
    "incSize":"<d>",
    "decSize":"<a>",
}

root.config(background=theme["bgCol"])

lPanel = tk.Frame(root, width=60, height=300, bg=theme["bgCol"])
lPanel.pack(padx=15, pady=15, side=tk.LEFT)
canframe = tk.Frame(root)
canframe.pack(side=tk.LEFT, expand=True)
canvas = Canvas(canframe, width=600, height=600, background="#ffffff")
canvas.pack(anchor=tk.CENTER)
rPanel = tk.Frame(root, width=300, height=720, bg=theme["bgCol"])
rPanel.pack(padx=15, pady=15, side=tk.RIGHT)

lastX = 0
lastY = 0
stabX = 0
stabY = 0
brushCol = "#000000"
penCol = "#000000"
brushSize = 5
lines = {}
curLine = 0
stabilize = 5
hue = 0
saturation = 0
value = 0
sizeStep = 1
curTool = 0
showOpt = 0

def rClick(event):
    global stabX
    stabX = event.x

def incSize(event):
    global brushSize
    brushSize += sizeStep
    if brushSize >= 200:
        brushSize = 200
    sizeShow.config(text=brushSize)

def decSize(event):
    global brushSize
    brushSize -= sizeStep
    if brushSize <= 1:
        brushSize = 1
    sizeShow.config(text=brushSize)

def eraser(event=None):
    global brushCol, penCol, curTool
    curTool = 1
    penCol = brushCol
    brushCol = "#ffffff"
    penButton.config(bg=theme["panelCol"])
    colButton.config(bg=theme["panelCol"])
    erButton.config(bg=theme["accent"])

def pen(event=None):
    global brushCol, curTool
    curTool = 0
    brushCol = penCol
    print(lines,curLine)
    penButton.config(bg=theme["accent"])
    colButton.config(bg=theme["panelCol"])
    erButton.config(bg=theme["panelCol"])

def click(event):
    global lastX, lastY, lines, curLine, stabX, stabY, curTool
    if brushCol == 0:
        takeColor(event)
        curTool = 0
        penButton.config(bg=theme["accent"])
        colButton.config(bg=theme["panelCol"])
        erButton.config(bg=theme["panelCol"])
        return
    else:
        if curLine != len(lines):
            delLines = len(lines) - curLine
            while delLines != 0:
                del lines[next(reversed(lines))]
                delLines -= 1
        curLine += 1
        lines[curLine] = []
        stabX, stabY = event.x, event.y
        lastX, lastY = stabX, stabY

def draw(event):
    global lastX, lastY, stabilize, stabX, stabY, lines, brushCol, burshSize
    lastX, lastY = stabX, stabY
    stabX += (event.x - stabX) / stabilize
    stabY += (event.y - stabY) / stabilize

    canvas.create_line(stabX, stabY, lastX, lastY, smooth=True, width=brushSize, fill=brushCol, capstyle=ROUND)

    lines[curLine].append([brushCol,brushSize,stabX,stabY,lastX,lastY])

def colPick(event=None):
    global brushCol, curTool
    curTool = 2
    brushCol = 0
    penButton.config(bg=theme["panelCol"])
    colButton.config(bg=theme["accent"])
    erButton.config(bg=theme["panelCol"])

def takeColor(event):
    global image, brushCol
    x = canvas.winfo_rootx() + event.x
    y = canvas.winfo_rooty() + event.y
    image = ImageGrab.grab((x, y, x + 1, y + 1))
    brushCol = image.getpixel((0, 0))
    brushCol = turnToHex(brushCol[0], brushCol[1], brushCol[2])
    color.config(bg=brushCol)
    hexToHSV()
    hueSlider.set(hue * 100)
    satSlider.set(saturation * 100)
    valSlider.set(value * 100)

def turnToHex(r, g, b):
    return f"#{r:02X}{g:02X}{b:02X}"

# I gave up on the redo system. ChatGPT rewrote it lol

def redrawCanvas():
    canvas.delete("all")
    for lineNum in range(1, curLine + 1):
        for segment in lines[lineNum]:
            if segment[0] != "image":
                canvas.create_line(
                    segment[2],
                    segment[3],
                    segment[4],
                    segment[5],
                    smooth=True,
                    width=segment[1],
                    fill=segment[0],
                    capstyle=ROUND
                )
            else:
                img = Image.open(segment[1])
                img.thumbnail((600, 600))
                importedImg = ImageTk.PhotoImage(img)
                if not hasattr(redrawCanvas, "images"):
                    redrawCanvas.images = []
                redrawCanvas.images.append(importedImg)
                canvas.create_image(
                    0,
                    0,
                    anchor="nw",
                    image=importedImg
                )

def undo(event=None):
    global curLine
    if curLine > 0:
        curLine -= 1
    redrawCanvas()

def redo(event=None):
    global curLine
    if curLine < len(lines):
        curLine += 1
    redrawCanvas()

def hsvToHex(event):
    global hue, saturation, value, brushCol
    hue = hueSlider.get() / 100
    saturation = satSlider.get() / 100
    value = valSlider.get() / 100
    r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)
    brushCol = turnToHex(r, g, b)
    color.config(bg=brushCol)
    colorLabel.config(text=brushCol)

def hexToHSV(event=None):
    global hue, saturation, value
    col = brushCol.lstrip("#")
    r, g, b = tuple(int(col[i:i+2], 16) for i in (0, 2, 4))
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    hue, saturation, value = colorsys.rgb_to_hsv(r, g, b)

def export(event=None):
    global showOpt
    settingsFrame.place_forget()
    showOpt = 0
    optButton.config(bg=theme["panelCol"])
    root.update()
    x = canvas.winfo_rootx()
    y = canvas.winfo_rooty()
    x1 = x + canvas.winfo_width()
    y1 = y + canvas.winfo_height()
    img = ImageGrab.grab(bbox=(x, y, x1, y1))
    filePath = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG Image", "*.png")],
        title = "Export Image..."
    )
    if filePath:
        img.save(filePath)
        messagebox.showinfo("Information","Image exported succesfully!")

def save(event=None):
    global showOpt
    settingsFrame.place_forget()
    showOpt = 0
    optButton.config(bg=theme["panelCol"])
    filePath = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json")],
        title = "Save Pain_t file (JSON)..."
    )
    if filePath:
        with open(filePath, "w") as f:
            json.dump(lines, f, )
        messagebox.showinfo("Information","JSON file saved!")

def impImage(event=None):
    global showOpt
    settingsFrame.place_forget()
    showOpt = 0
    optButton.config(bg=theme["panelCol"])
    global lines, curLine, importedImg
    fileTypes=[("JSON", "*.json"),("PNG", "*.png"),("JPEG", "*.jpeg")]
    selectedType = tk.StringVar()
    filepath = filedialog.askopenfilename(
        title="Select image or saved Pain_t (JSON) file...",
        filetypes = fileTypes,
        typevariable=selectedType
    )
    if not filepath:
        return
    try:
        if selectedType.get() != "JSON":
            img = Image.open(filepath)
            img.thumbnail((600,600))
            importedImg = ImageTk.PhotoImage(img)
            if curLine != len(lines):
                delLines = len(lines) - curLine
                while delLines != 0:
                    del lines[next(reversed(lines))]
                    delLines -= 1
            curLine += 1
            lines[curLine] = []
            lines[curLine].append(["image",filepath])
            curLine = len(lines)
            redrawCanvas()
        else:
            with open(filepath, "r", encoding="utf-8") as file:
                lines = json.load(file)
            lines = {int(k): v for k, v in lines.items()}
            curLine = len(lines)
            redrawCanvas()
    except json.JSONDecodeError:
        messagebox.showerror("Error", "The selected file is not a valid JSON.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")

def settings(event=None):
    global showOpt
    if showOpt == 0:
        settingsFrame.place(relx=0.5, rely=0.5, anchor="center")
        settingsFrame.lift()
        showOpt = 1
        optButton.config(bg=theme["accent"])
    else:
        settingsFrame.place_forget()
        showOpt = 0
        optButton.config(bg=theme["panelCol"])

canvas.bind("<Button-1>", click)
canvas.bind("<Button-3>", rClick)
canvas.bind("<B1-Motion>", draw)
canvas.bind("<Button-2>", takeColor)
root.bind(shortcut["incSize"], incSize)
root.bind(shortcut["decSize"], decSize)
root.bind(shortcut["eraser"], eraser)
root.bind(shortcut["pen"], pen)
root.bind(shortcut["colPick"], colPick)
root.bind(shortcut["undo"], undo)
root.bind(shortcut["redo"], redo)

import sys
if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent
assetsDir = BASE_DIR
imgPath = assetsDir / "assets" / "br.png"
pilImg = Image.open(imgPath)
pilImg = pilImg.resize((20, 20))
brIco = ImageTk.PhotoImage(pilImg)
imgPath = assetsDir / "assets" / "er.png"
pilImg = Image.open(imgPath)
pilImg = pilImg.resize((20, 20))
erIco = ImageTk.PhotoImage(pilImg)
imgPath = assetsDir / "assets" / "pick.png"
pilImg = Image.open(imgPath)
pilImg = pilImg.resize((20, 20))
pickIco = ImageTk.PhotoImage(pilImg)
imgPath = assetsDir / "assets" / "undo.png"
pilImg = Image.open(imgPath)
pilImg = pilImg.resize((20, 20))
undoIco = ImageTk.PhotoImage(pilImg)
imgPath = assetsDir / "assets" / "redo.png"
pilImg = Image.open(imgPath)
pilImg = pilImg.resize((20, 20))
redoIco = ImageTk.PhotoImage(pilImg)
imgPath = assetsDir / "assets" / "settings.png"
pilImg = Image.open(imgPath)
pilImg = pilImg.resize((20, 20))
optIco = ImageTk.PhotoImage(pilImg)

settingsFrame = tk.Frame(root, bg=theme["panelCol"], width=500, height=800)
settingsFrame2 = tk.Frame(settingsFrame, bg=theme["panelCol"])
settingsFrame2.pack(padx=20, pady=20)
optLabel = tk.Label(settingsFrame2, text="============= Settings =============", bg=theme["panelCol"], fg=theme["textCol"], font=("sans_serif", 15, "bold"))
optLabel.pack()
expButton = tk.Button(settingsFrame2, command=export, text="Export", bg=theme["panelCol"], fg=theme["textCol"], borderwidth=0, highlightthickness=0, relief="flat")
expButton.pack()
impButton = tk.Button(settingsFrame2, command=impImage, text="Import", bg=theme["panelCol"], fg=theme["textCol"], borderwidth=0, highlightthickness=0, relief="flat")
impButton.pack()
saveButton = tk.Button(settingsFrame2, command=save, text="Save", bg=theme["panelCol"], fg=theme["textCol"], borderwidth=0, highlightthickness=0, relief="flat")
saveButton.pack()

optFrame = tk.Frame(lPanel, bg=theme["panelCol"])
optFrame.pack(pady=15)
optButton = tk.Button(optFrame, command=settings, image=optIco, bg=theme["panelCol"], borderwidth=0, highlightthickness=0, highlightcolor=theme["bgCol"], relief="flat", width=25, height=25)
optButton.pack(padx=8, pady=8, expand=False)

toolFrame = tk.Frame(lPanel, bg=theme["panelCol"])
toolFrame.pack()
penButton = tk.Button(toolFrame, command=pen, image=brIco, bg=theme["panelCol"], borderwidth=0, highlightthickness=0, highlightcolor=theme["bgCol"], relief="flat", width=25, height=25)
penButton.pack(padx=8, pady=8, expand=False)
erButton = tk.Button(toolFrame, command=eraser, image=erIco, bg=theme["panelCol"], borderwidth=0, highlightthickness=0, highlightcolor=theme["bgCol"], relief="flat", width=25, height=25)
erButton.pack(padx=8, pady=8, expand=False)
colButton = tk.Button(toolFrame, command=colPick, image=pickIco, bg=theme["panelCol"], borderwidth=0, highlightthickness=0, highlightcolor=theme["bgCol"], relief="flat", width=25, height=25)
colButton.pack(padx=8, pady=8, expand=False)
undoButton = tk.Button(toolFrame, command=undo, image=undoIco, bg=theme["panelCol"], borderwidth=0, highlightthickness=0, highlightcolor=theme["bgCol"], relief="flat", width=25, height=25)
undoButton.pack(padx=8, pady=8, expand=False)
redoButton = tk.Button(toolFrame, command=redo, image=redoIco, bg=theme["panelCol"], borderwidth=0, highlightthickness=0, highlightcolor=theme["bgCol"], relief="flat", width=25, height=25)
redoButton.pack(padx=8, pady=8, expand=False)

penButton.config(bg=theme["accent"])
colButton.config(bg=theme["panelCol"])
erButton.config(bg=theme["panelCol"])

colorFrame2 = tk.Frame(rPanel, bg=theme["panelCol"])
colorFrame2.pack(padx=15, pady=15)
colorFrame = tk.Frame(colorFrame2, bg=theme["panelCol"])
colorFrame.pack(padx=15, pady=15)
color = Canvas(colorFrame, width=120, height=120, background=brushCol)
color.pack()
colorLabel = tk.Label(colorFrame, text=brushCol, fg=theme["textCol"], bg=theme["panelCol"])
colorLabel.pack()
hueFrame = tk.Frame(colorFrame, bg=theme["panelCol"])
hueFrame.pack()
hueLabel = tk.Label(hueFrame, text="H", fg=theme["textCol"], bg=theme["panelCol"])
hueLabel.pack(side=LEFT, padx=5)
hueSlider = tk.Scale(hueFrame, from_=0, to=100, orient='horizontal', command=hsvToHex, length=145, bg=theme["panelCol"], bd=0, troughcolor=theme["bgCol"], highlightthickness=0, fg=theme["textCol"], width=16, showvalue=0, sliderlength=12)
hueSlider.pack()
satFrame = tk.Frame(colorFrame, bg=theme["panelCol"])
satFrame.pack()
satLabel = tk.Label(satFrame, text="S", fg=theme["textCol"], bg=theme["panelCol"])
satLabel.pack(side=LEFT, padx=5)
satSlider = tk.Scale(satFrame, from_=0, to=100, orient='horizontal', command=hsvToHex, length=145, bg=theme["panelCol"], bd=0, troughcolor=theme["bgCol"], highlightthickness=0, fg=theme["textCol"], width=16, showvalue=0, sliderlength=12)
satSlider.pack()
valFrame = tk.Frame(colorFrame, bg=theme["panelCol"])
valFrame.pack()
valLabel = tk.Label(valFrame, text="V", fg=theme["textCol"], bg=theme["panelCol"])
valLabel.pack(side=LEFT, padx=5)
valSlider = tk.Scale(valFrame, from_=0, to=100, orient='horizontal', command=hsvToHex, length=145, bg=theme["panelCol"], bd=0, troughcolor=theme["bgCol"], highlightthickness=0, fg=theme["textCol"], width=16, showvalue=0, sliderlength=12)
valSlider.pack()

brushFrame2 = tk.Frame(rPanel ,bg=theme["panelCol"])
brushFrame2.pack(padx=15, pady=15)
brushFrame = tk.Frame(brushFrame2 ,bg=theme["panelCol"])
brushFrame.pack(padx=15, pady=15)

def sizeIncr(event=None):
    global brushSize
    brushSize += 1
    if brushSize >= 200:
        brushSize = 200
    sizeShow.config(text=brushSize)

def sizeDecr(event=None):
    global brushSize
    brushSize -= 1
    if brushSize <= 0:
        brushSize = 0
    sizeShow.config(text=brushSize)

sizeFrame = tk.Frame(brushFrame, bg=theme["panelCol"])
sizeFrame.pack()
sizeLabel = tk.Label(sizeFrame, text="Brush Size: ", fg=theme["textCol"], bg=theme["panelCol"], width=12)
sizeLabel.pack(side=LEFT)
sizeShow = tk.Label(sizeFrame, text=brushSize, fg=theme["textCol"], bg=theme["bgCol"], width=3)
sizeShow.pack(side=LEFT)
sizeDec = tk.Button(sizeFrame, command=sizeDecr, text="-", fg=theme["textCol"], bg=theme["bgCol"], borderwidth=0, highlightthickness=0, relief="flat")
sizeDec.pack(side=LEFT)
sizeInc = tk.Button(sizeFrame, command=sizeIncr, text="+", fg=theme["textCol"], bg=theme["bgCol"], borderwidth=0, highlightthickness=0, relief="flat")
sizeInc.pack(side=LEFT)

def stabIncr(event=None):
    global stabilize
    stabilize += 1
    if stabilize >= 20:
        stabilize = 20
    stabShow.config(text=stabilize)

def stabDecr(event=None):
    global stabilize
    stabilize -= 1
    if stabilize <= 1:
        stabilize = 1
    stabShow.config(text=stabilize)

stabFrame = tk.Frame(brushFrame, bg=theme["panelCol"])
stabFrame.pack()
stabLabel = tk.Label(stabFrame, text="Stabilizer: ", fg=theme["textCol"], bg=theme["panelCol"], width=12)
stabLabel.pack(side=LEFT)
stabShow = tk.Label(stabFrame, text=stabilize, fg=theme["textCol"], bg=theme["bgCol"], width=3)
stabShow.pack(side=LEFT)
stabDec = tk.Button(stabFrame, command=stabDecr, text="-", fg=theme["textCol"], bg=theme["bgCol"], borderwidth=0, highlightthickness=0, relief="flat")
stabDec.pack(side=LEFT)
stabInc = tk.Button(stabFrame, command=stabIncr, text="+", fg=theme["textCol"], bg=theme["bgCol"], borderwidth=0, highlightthickness=0, relief="flat")
stabInc.pack(side=LEFT)

def stepIncr(event=None):
    global sizeStep
    sizeStep += 1
    if sizeStep >= 10:
        sizeStep = 10
    stepShow.config(text=sizeStep)

def stepDecr(event=None):
    global sizeStep
    sizeStep -= 1
    if sizeStep <= 1:
        sizeStep = 1
    stepShow.config(text=sizeStep)

stepFrame = tk.Frame(brushFrame, bg=theme["panelCol"])
stepFrame.pack()
stepLabel = tk.Label(stepFrame, text="Size Step: ", fg=theme["textCol"], bg=theme["panelCol"], width=12)
stepLabel.pack(side=LEFT)
stepShow = tk.Label(stepFrame, text=sizeStep, fg=theme["textCol"], bg=theme["bgCol"], width=3)
stepShow.pack(side=LEFT)
stepDec = tk.Button(stepFrame, command=stepDecr, text="-", fg=theme["textCol"], bg=theme["bgCol"], borderwidth=0, highlightthickness=0, relief="flat")
stepDec.pack(side=LEFT)
stepInc = tk.Button(stepFrame, command=stepIncr, text="+", fg=theme["textCol"], bg=theme["bgCol"], borderwidth=0, highlightthickness=0, relief="flat")
stepInc.pack(side=LEFT)

root.mainloop()
