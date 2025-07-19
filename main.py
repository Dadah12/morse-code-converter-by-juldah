import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import winsound
import threading
import time

# Morse Code Dictionary
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.',
    'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..',
    'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-',
    'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..',
    '9': '----.', ' ': '/', '.': '.-.-.-',
    ',': '--..--', '?': '..--..', '!': '-.-.--'
}
REVERSE_DICT = {v: k for k, v in MORSE_CODE_DICT.items()}

sample_phrases = [
    "I'm not lazy, I'm on energy-saving mode.",
    "Why don’t scientists trust atoms? Because they make up everything!",
    "I told my computer I needed a break, and now it won’t stop sending me Kit-Kats.",
    "I'm on a seafood diet. I see food and I eat it.",
    "I'm reading a book about anti-gravity. It's impossible to put down!",
    "Parallel lines have so much in common. It’s a shame they’ll never meet.",
    "I would lose weight, but I hate losing.",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "I’m great at multitasking. I can waste time, be unproductive, and procrastinate all at once.",
    "I asked the librarian if the library had books on paranoia. She whispered, 'They're right behind you.'"
]

DOT_DURATION = 100
DASH_DURATION = 300
FREQ = 750


def play_morse_sound(code):
    def play():
        for symbol in code:
            if symbol == '.':
                winsound.Beep(FREQ, DOT_DURATION)
            elif symbol == '-':
                winsound.Beep(FREQ, DASH_DURATION)
            elif symbol == ' ':
                time.sleep(0.1)
            elif symbol == '/':
                time.sleep(0.3)
    threading.Thread(target=play).start()


def text_to_morse():
    text = input_text.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Empty input", "Please enter text to convert.")
        return

    result = []
    for char in text:
        upper_char = char.upper()
        if upper_char in MORSE_CODE_DICT:
            result.append(MORSE_CODE_DICT[upper_char])
        else:
            result.append('?')

    output = ' '.join(result)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, output)
    input_text.delete("1.0", tk.END)

    if play_sound.get():
        play_morse_sound(output)


def morse_to_text():
    code = input_text.get("1.0", tk.END).strip()
    if not code:
        messagebox.showwarning("Empty input", "Please enter Morse code to convert.")
        return

    try:
        words = code.split(' / ')
        result = []
        for word in words:
            letters = word.strip().split()
            decoded = ''.join(REVERSE_DICT.get(l, '?') for l in letters)
            result.append(decoded)
        final_text = ' '.join(result)

        if not preserve_case.get():
            final_text = final_text.upper()

        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, final_text)
    except:
        output_text.insert(tk.END, "Invalid Morse code input.")
    input_text.delete("1.0", tk.END)


def copy_result():
    result = output_text.get("1.0", tk.END).strip()
    if result:
        app.clipboard_clear()
        app.clipboard_append(result)
        messagebox.showinfo("Copied", "Output copied to clipboard!")


def save_to_file():
    result = output_text.get("1.0", tk.END).strip()
    if not result:
        messagebox.showwarning("No Output", "There's nothing to save.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(result)
        messagebox.showinfo("Saved", f"File saved to:\n{file_path}")


def load_sample(event):
    selected = sample_combo.get()
    input_text.delete("1.0", tk.END)
    input_text.insert(tk.END, selected)


def toggle_theme():
    if dark_mode.get():
        bg = "#1e1e1e"
        fg = "#ffffff"
        entry_bg = "#2b2b2b"
        # Fix checkbox color sa dark mode
        # Find all checkbuttons and update colors
        for widget in app.winfo_children():
            if isinstance(widget, tk.Checkbutton):
                widget.configure(bg=bg, fg=fg, selectcolor=bg, activebackground=bg, activeforeground=fg)
    else:
        bg = "#f0f0f0"
        fg = "#000000"
        entry_bg = "#ffffff"
        for widget in app.winfo_children():
            if isinstance(widget, tk.Checkbutton):
                widget.configure(bg=bg, fg=fg, selectcolor=bg, activebackground=bg, activeforeground=fg)

    app.configure(bg=bg)
    for widget in app.winfo_children():
        if isinstance(widget, (tk.Label)):
            widget.configure(bg=bg, fg=fg)
        elif isinstance(widget, tk.Text):
            widget.configure(bg=entry_bg, fg=fg, insertbackground=fg)
        elif isinstance(widget, tk.Button):
            widget.configure(bg=entry_bg, fg=fg)
    output_text.configure(bg=entry_bg, fg=fg)


# GUI setup
app = tk.Tk()
app.title("Morse Code Converter by Juldah")

dark_mode = tk.BooleanVar(value=True)
preserve_case = tk.BooleanVar(value=True)
play_sound = tk.BooleanVar(value=True)

# Theme toggle
tk.Checkbutton(app, text="Dark Mode 🌙", variable=dark_mode, command=toggle_theme).pack(anchor='w', padx=10)

# Dropdown
tk.Label(app, text="Sample Phrases:").pack()
sample_combo = ttk.Combobox(app, values=sample_phrases, width=45, state="readonly")
sample_combo.pack()
sample_combo.bind("<<ComboboxSelected>>", load_sample)

# Input
tk.Label(app, text="\nInput Text or Morse Code:").pack()
input_text = tk.Text(app, height=5, width=60)
input_text.pack(padx=10, pady=5)

# Checkboxes
tk.Checkbutton(app, text="Preserve Case (for text output)", variable=preserve_case).pack()
tk.Checkbutton(app, text="Play Morse Sound", variable=play_sound).pack()

# Buttons
tk.Button(app, text="Convert to Morse", command=text_to_morse).pack(pady=2)
tk.Button(app, text="Convert to Text", command=morse_to_text).pack(pady=2)

# Output
tk.Label(app, text="Output:").pack()
output_text = tk.Text(app, height=5, width=60)
output_text.pack(padx=10, pady=5)

# Copy and Save
tk.Button(app, text="Copy Output", command=copy_result).pack(pady=2)
tk.Button(app, text="Save Output to .txt", command=save_to_file).pack(pady=3)

# Initial theme setup
toggle_theme()

app.mainloop()
