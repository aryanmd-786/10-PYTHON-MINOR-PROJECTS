import tkinter as tk
from tkinter import messagebox
import json
import os


class TodoApp:

    def __init__(self, root):

        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("650x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#F3F4F6")

        self.file_name = "tasks.json"
        self.tasks = []

        # Load saved tasks
        self.load_tasks()

        # ================= HEADER =================

        header = tk.Frame(
            root,
            bg="#1E3A8A",
            height=90
        )
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="MY TO-DO LIST",
            font=("Arial", 24, "bold"),
            bg="#1E3A8A",
            fg="white"
        )
        title.pack(pady=25)

        # ================= INPUT SECTION =================

        input_frame = tk.Frame(
            root,
            bg="#F3F4F6"
        )
        input_frame.pack(
            fill="x",
            padx=30,
            pady=25
        )

        self.task_entry = tk.Entry(
            input_frame,
            font=("Arial", 13),
            bd=1,
            relief="solid"
        )
        self.task_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=10
        )

        add_button = tk.Button(
            input_frame,
            text="ADD TASK",
            font=("Arial", 11, "bold"),
            bg="#2563EB",
            fg="white",
            activebackground="#1D4ED8",
            activeforeground="white",
            bd=0,
            width=12,
            height=2,
            cursor="hand2",
            command=self.add_task
        )
        add_button.pack(
            side="right",
            padx=(10, 0)
        )

        # Enter key support
        self.task_entry.bind(
            "<Return>",
            lambda event: self.add_task()
        )

        # ================= TASK FRAME =================

        task_frame = tk.LabelFrame(
            root,
            text=" My Tasks ",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#1E3A8A",
            padx=15,
            pady=15
        )
        task_frame.pack(
            fill="both",
            expand=True,
            padx=30
        )

        # Listbox + scrollbar

        list_frame = tk.Frame(
            task_frame,
            bg="white"
        )
        list_frame.pack(
            fill="both",
            expand=True
        )

        scrollbar = tk.Scrollbar(
            list_frame
        )
        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.task_listbox = tk.Listbox(
            list_frame,
            font=("Arial", 13),
            bg="#F9FAFB",
            fg="#111827",
            selectbackground="#2563EB",
            selectforeground="white",
            activestyle="none",
            bd=0,
            highlightthickness=0,
            yscrollcommand=scrollbar.set
        )

        self.task_listbox.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.config(
            command=self.task_listbox.yview
        )

        # Double click to complete
        self.task_listbox.bind(
            "<Double-Button-1>",
            lambda event: self.complete_task()
        )

        # ================= TASK COUNT =================

        self.counter_label = tk.Label(
            root,
            text="Total Tasks: 0",
            font=("Arial", 11, "bold"),
            bg="#F3F4F6",
            fg="#4B5563"
        )
        self.counter_label.pack(
            pady=12
        )

        # ================= BUTTONS =================

        button_frame = tk.Frame(
            root,
            bg="#F3F4F6"
        )
        button_frame.pack(
            pady=(0, 25)
        )

        complete_button = tk.Button(
            button_frame,
            text="✓ Complete",
            font=("Arial", 10, "bold"),
            bg="#16A34A",
            fg="white",
            activebackground="#15803D",
            activeforeground="white",
            bd=0,
            width=14,
            height=2,
            cursor="hand2",
            command=self.complete_task
        )
        complete_button.grid(
            row=0,
            column=0,
            padx=5
        )

        delete_button = tk.Button(
            button_frame,
            text="Delete Task",
            font=("Arial", 10, "bold"),
            bg="#DC2626",
            fg="white",
            activebackground="#B91C1C",
            activeforeground="white",
            bd=0,
            width=14,
            height=2,
            cursor="hand2",
            command=self.delete_task
        )
        delete_button.grid(
            row=0,
            column=1,
            padx=5
        )

        clear_button = tk.Button(
            button_frame,
            text="Clear All",
            font=("Arial", 10, "bold"),
            bg="#F59E0B",
            fg="white",
            activebackground="#D97706",
            activeforeground="white",
            bd=0,
            width=14,
            height=2,
            cursor="hand2",
            command=self.clear_all
        )
        clear_button.grid(
            row=0,
            column=2,
            padx=5
        )

        # Display loaded tasks
        self.refresh_list()

    # ================= ADD TASK =================

    def add_task(self):

        task = self.task_entry.get().strip()

        if task == "":
            messagebox.showwarning(
                "Empty Task",
                "Please enter a task."
            )
            self.task_entry.focus()
            return

        self.tasks.append({
            "text": task,
            "completed": False
        })

        self.task_entry.delete(
            0,
            tk.END
        )

        self.save_tasks()
        self.refresh_list()

        self.task_entry.focus()

    # ================= COMPLETE TASK =================

    def complete_task(self):

        selected = self.task_listbox.curselection()

        if not selected:
            messagebox.showwarning(
                "No Task Selected",
                "Please select a task first."
            )
            return

        index = selected[0]

        # Toggle completion
        self.tasks[index]["completed"] = not self.tasks[index]["completed"]

        self.save_tasks()
        self.refresh_list()

    # ================= DELETE TASK =================

    def delete_task(self):

        selected = self.task_listbox.curselection()

        if not selected:
            messagebox.showwarning(
                "No Task Selected",
                "Please select a task first."
            )
            return

        index = selected[0]

        task_name = self.tasks[index]["text"]

        answer = messagebox.askyesno(
            "Delete Task",
            f'Do you want to delete "{task_name}"?'
        )

        if answer:

            del self.tasks[index]

            self.save_tasks()
            self.refresh_list()

    # ================= CLEAR ALL =================

    def clear_all(self):

        if not self.tasks:
            messagebox.showinfo(
                "No Tasks",
                "There are no tasks to clear."
            )
            return

        answer = messagebox.askyesno(
            "Clear All",
            "Are you sure you want to delete all tasks?"
        )

        if answer:

            self.tasks.clear()

            self.save_tasks()
            self.refresh_list()

    # ================= REFRESH LIST =================

    def refresh_list(self):

        self.task_listbox.delete(
            0,
            tk.END
        )

        completed = 0

        for task in self.tasks:

            if task["completed"]:

                display_text = "✓  " + task["text"]
                completed += 1

            else:

                display_text = "○  " + task["text"]

            self.task_listbox.insert(
                tk.END,
                display_text
            )

        total = len(self.tasks)

        self.counter_label.config(
            text=f"Total Tasks: {total}    |    Completed: {completed}"
        )

    # ================= SAVE TASKS =================

    def save_tasks(self):

        try:

            with open(
                self.file_name,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    self.tasks,
                    file,
                    indent=4
                )

        except Exception as error:

            messagebox.showerror(
                "Save Error",
                f"Could not save tasks.\n{error}"
            )

    # ================= LOAD TASKS =================

    def load_tasks(self):

        if not os.path.exists(self.file_name):
            self.tasks = []
            return

        try:

            with open(
                self.file_name,
                "r",
                encoding="utf-8"
            ) as file:

                self.tasks = json.load(file)

        except (json.JSONDecodeError, OSError):

            self.tasks = []


# ================= MAIN =================

if __name__ == "__main__":

    root = tk.Tk()

    app = TodoApp(root)

    root.mainloop()