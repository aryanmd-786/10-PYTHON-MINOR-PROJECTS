import tkinter as tk


class Calculator:
    def __init__(self, root):
        self.root = root

        # Window settings
        self.root.title("Modern Calculator")
        self.root.geometry("380x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#111827")

        self.expression = ""

        # ---------------- DISPLAY ----------------
        self.display = tk.Entry(
            root,
            font=("Segoe UI", 30, "bold"),
            bg="#1F2937",
            fg="white",
            insertbackground="white",
            justify="right",
            bd=0,
            relief="flat"
        )

        self.display.pack(
            fill="x",
            padx=20,
            pady=(30, 20),
            ipady=25
        )

        # ---------------- BUTTON FRAME ----------------
        button_frame = tk.Frame(
            root,
            bg="#111827"
        )
        button_frame.pack(
            expand=True,
            fill="both",
            padx=15,
            pady=10
        )

        # Button layout
        buttons = [
            ["AC", "⌫", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "−"],
            ["1", "2", "3", "+"],
            ["00", "0", ".", "="]
        ]

        for row in range(5):
            button_frame.rowconfigure(row, weight=1)

        for column in range(4):
            button_frame.columnconfigure(column, weight=1)

        # Create buttons
        for row, button_row in enumerate(buttons):
            for column, text in enumerate(button_row):

                # Special colors
                if text == "AC":
                    bg = "#DC2626"
                    hover = "#EF4444"

                elif text == "=":
                    bg = "#2563EB"
                    hover = "#3B82F6"

                elif text in ["÷", "×", "−", "+", "%"]:
                    bg = "#374151"
                    hover = "#4B5563"

                else:
                    bg = "#1F2937"
                    hover = "#374151"

                button = tk.Button(
                    button_frame,
                    text=text,
                    font=("Segoe UI", 18, "bold"),
                    bg=bg,
                    fg="white",
                    activebackground=hover,
                    activeforeground="white",
                    bd=0,
                    relief="flat",
                    cursor="hand2",
                    command=lambda value=text: self.button_click(value)
                )

                button.grid(
                    row=row,
                    column=column,
                    padx=6,
                    pady=6,
                    sticky="nsew"
                )

        # Keyboard support
        self.root.bind("<Key>", self.keyboard_input)

    # ---------------- BUTTON FUNCTION ----------------
    def button_click(self, value):

        if value == "AC":
            self.clear()

        elif value == "⌫":
            self.backspace()

        elif value == "=":
            self.calculate()

        elif value == "÷":
            self.add_value("/")

        elif value == "×":
            self.add_value("*")

        elif value == "−":
            self.add_value("-")

        elif value == "%":
            self.add_value("%")

        else:
            self.add_value(value)

    # ---------------- ADD VALUE ----------------
    def add_value(self, value):
        self.expression += str(value)

        self.display.delete(0, tk.END)
        self.display.insert(0, self.expression)

    # ---------------- CLEAR ----------------
    def clear(self):
        self.expression = ""
        self.display.delete(0, tk.END)

    # ---------------- BACKSPACE ----------------
    def backspace(self):
        self.expression = self.expression[:-1]

        self.display.delete(0, tk.END)
        self.display.insert(0, self.expression)

    # ---------------- CALCULATE ----------------
    def calculate(self):
        try:
            if not self.expression:
                return

            result = eval(self.expression)

            # Remove unnecessary .0
            if isinstance(result, float) and result.is_integer():
                result = int(result)

            self.expression = str(result)

            self.display.delete(0, tk.END)
            self.display.insert(0, self.expression)

        except ZeroDivisionError:
            self.show_error("Cannot divide by zero")

        except Exception:
            self.show_error("Invalid Expression")

    # ---------------- ERROR ----------------
    def show_error(self, message):
        self.expression = ""

        self.display.delete(0, tk.END)
        self.display.insert(0, message)

        self.root.after(1500, self.clear)

    # ---------------- KEYBOARD ----------------
    def keyboard_input(self, event):

        key = event.char

        if key in "0123456789.+-*/%":
            self.add_value(key)

        elif event.keysym == "Return":
            self.calculate()

        elif event.keysym == "BackSpace":
            self.backspace()

        elif event.keysym == "Escape":
            self.clear()


# ---------------- MAIN PROGRAM ----------------
root = tk.Tk()

calculator = Calculator(root)

root.mainloop()