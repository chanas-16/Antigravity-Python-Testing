# Basic styling constants for Tkinter

BG_COLOR = "#f4f4f9"
FG_COLOR = "#333333"
PRIMARY_COLOR = "#1a1a1a" # Soft black
PRIMARY_FG = "#ffffff"
ERROR_COLOR = "#d9534f"
SUCCESS_COLOR = "#5cb85c"

FONT_TITLE = ("Helvetica", 24, "bold")
FONT_HEADER = ("Helvetica", 16, "bold")
FONT_NORMAL = ("Helvetica", 12)
FONT_SMALL = ("Helvetica", 10)

def configure_window(window):
    window.configure(bg=BG_COLOR)

def get_frame_style():
    return {"bg": BG_COLOR}

def get_label_style(font=FONT_NORMAL):
    return {"bg": BG_COLOR, "fg": FG_COLOR, "font": font}

def get_button_style(bg=PRIMARY_COLOR):
    return {
        "bg": bg,
        "fg": PRIMARY_FG,
        "font": FONT_NORMAL,
        "activebackground": "#333333",
        "activeforeground": PRIMARY_FG,
        "relief": "flat",
        "padx": 10,
        "pady": 5,
        "cursor": "hand2"
    }

def get_entry_style():
    return {"font": FONT_NORMAL, "relief": "solid", "bd": 1}
