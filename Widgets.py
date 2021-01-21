import tkinter as tk

class BasicWidget:
    def __init__(self, master, text, row, column):
        self.master = master
        self.text = text
        self.row = row
        self.column = column
        self.label = tk.Label(self.master, text = self.text)
        self.label.grid(row = self.row, column = self.column,
                        padx=5, pady=5, sticky="we")
        self.entryVar = tk.StringVar()
        self.entry = tk.Entry(self.master, textvariable = self.entryVar)
        self.entry.grid(row=self.row, column = self.column,
                        padx=5, pady=5, sticky="we")
