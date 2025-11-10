'''
Is it too much to ask for basic utilities these days?
'''
import sys, os
import tkinter as tk
from tkinter import filedialog, messagebox, font, ttk
import subprocess

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")

        self.file_path = None  # keep track of the currently open file
        self._reset_title()

        # Create menu bar
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        # File menu
        file_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", command=self.save_as)
        file_menu.add_command(label="Save To", command=self.save_to)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Font configuration
        self.font_size = 12
        self.available_fonts = sorted(font.families())
        self.current_font_family = tk.StringVar(value="Consolas")
        self.text_font = font.Font(family=self.current_font_family.get(), size=self.font_size)

        # Font menu
        font_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="Font", menu=font_menu)
        font_menu.add_command(label="Increase Size", command=self.increase_font, accelerator="Ctrl+=")
        font_menu.add_command(label="Decrease Size", command=self.decrease_font, accelerator="Ctrl+-")

        # Font Dropdown
        self.font_box = ttk.Combobox(root, textvariable=self.current_font_family, values=self.available_fonts, state="readonly")
        # self.font_box.pack(side="top", fill="x") # Uncomment for font menu
        self.font_box.bind("<<ComboboxSelected>>", self.change_font)

        # Text area
        self.text_area = tk.Text(self.root, wrap="word", undo=True)
        self.text_area.pack(fill="both", expand=True)
        self.text_area.configure(font=self.text_font, tabs=(20,))

        # Scrollbar
        scroll = tk.Scrollbar(self.text_area)
        scroll.pack(side="right", fill="y")
        self.text_area.config(yscrollcommand=scroll.set)
        scroll.config(command=self.text_area.yview)

        # Keyboard shortcuts
        self.root.bind("<Control-s>", lambda event: self.save_file())
        self.root.bind("<Control-o>", lambda event: self.open_file())
        self.root.bind("<Control-n>", lambda event: self.new_file())
        self.root.bind("<Control-equal>", lambda event: self.increase_font())
        self.root.bind("<Control-minus>", lambda event: self.decrease_font())
        
        # Tested on MacOS, not sure if it'll throw errors on Windows. Will test soon
        self.root.bind("<Command-s>", lambda event: self.save_file())
        self.root.bind("<Command-o>", lambda event: self.open_file())
        self.root.bind("<Command-n>", lambda event: self.new_file())
        self.root.bind("<Command-equal>", lambda event: self.increase_font())
        self.root.bind("<Command-minus>", lambda event: self.decrease_font())

    def new_file(self):
        subprocess.Popen([sys.executable, os.path.abspath(__file__)])

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            self._load(file_path)
            self._change_context(file_path)

    def save_file(self):
        if self.file_path:
            self._save_to(self.file_path)
        else:
            self.save_as()

    def save_as(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            self._save_to(file_path)
            self._change_context(file_path)

    def save_to(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            self._save_to(file_path)

    def _save_to(self, file_path):
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(self.text_area.get(1.0, "end-1c"))

    def _load(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, content)

    def _change_context(self, file_path):
        self.file_path = file_path
        self._reset_title()

    def _reset_title(self):
        self.root.title(f"Classic Text Editor - {os.path.basename(self.file_path or 'Untitled')}")

    def change_font(self, event=None):
        new_font = self.current_font_family.get()
        self.text_font.configure(family=new_font)

    def increase_font(self):
        self.font_size += 2
        self.text_font.configure(size=self.font_size)

    def decrease_font(self):
        if self.font_size > 6:
            self.font_size -= 2
            self.text_font.configure(size=self.font_size)

if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditor(root)
    root.mainloop()
