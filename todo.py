import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import time
import random

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")

        # Configure style for ttk elements
        style = ttk.Style()
        style.configure("TFrame", background="white")
        style.configure("TLabel", font=('Helvetica', 12), background="white")
        style.configure("TButton", font=('Helvetica', 12), padding=5)
        style.configure("TEntry", font=('Helvetica', 14))

        # Larger panel using Frame
        main_frame = ttk.Frame(root, style="TFrame")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Falling stars animation using Canvas
        self.canvas = tk.Canvas(main_frame, width=root.winfo_reqwidth(), height=root.winfo_reqheight(), bg="black")
        self.canvas.pack(expand=True, fill=tk.BOTH)

        self.stars = []
        for _ in range(400):  # Increased the number of stars
            x = random.randint(0, root.winfo_reqwidth())
            y = random.randint(0, root.winfo_reqheight())
            self.stars.append(self.canvas.create_text(x, y, text="*", fill="white"))

        self.date_label = ttk.Label(main_frame, text=self.get_current_date(), style="TLabel")
        self.date_label.pack(pady=10)

        self.clock_label = ttk.Label(main_frame, text="", style="TLabel")
        self.clock_label.pack(pady=10)

        # Make the task panel a larger frame
        task_panel = ttk.Frame(main_frame, style="TFrame")
        task_panel.pack(expand=True, fill=tk.BOTH)

        # Use a Tkinter Listbox for displaying tasks
        self.task_listbox = tk.Listbox(task_panel, selectbackground="blue", selectmode=tk.SINGLE, font=('Helvetica', 14))
        self.task_listbox.pack(side=tk.TOP, padx=10, pady=10, expand=True, fill=tk.BOTH)
        self.task_listbox.bind("<ButtonRelease-1>", self.on_task_click)  # Bind click event

        entry_frame = ttk.Frame(task_panel, style="TFrame")  # Separate frame for entry boxes and labels
        entry_frame.pack(side=tk.TOP, pady=10, fill=tk.BOTH)

        task_label = ttk.Label(entry_frame, text="Task:", style="TLabel")
        task_label.pack(side=tk.LEFT, padx=10)
        self.task_entry = ttk.Entry(entry_frame, font=('Helvetica', 14))
        self.task_entry.pack(side=tk.LEFT, padx=10)

        deadline_label = ttk.Label(entry_frame, text="Deadline:", style="TLabel")
        deadline_label.pack(side=tk.LEFT, padx=10)
        self.deadline_entry = ttk.Entry(entry_frame, font=('Helvetica', 14), width=10)
        self.deadline_entry.pack(side=tk.LEFT, padx=10)

        button_frame = ttk.Frame(task_panel, style="TFrame")
        button_frame.pack(side=tk.TOP, pady=10, fill=tk.BOTH)

        add_task_button = ttk.Button(button_frame, text="Add Task", command=self.add_task, style="TButton")
        add_task_button.pack(side=tk.LEFT, padx=10)

        remove_task_button = ttk.Button(button_frame, text="Remove Task", command=self.remove_task, style="TButton")
        remove_task_button.pack(side=tk.LEFT, padx=10)

        # Bind mouse events for drag-and-drop
        self.task_listbox.bind("<ButtonPress-1>", self.on_start_drag)
        self.task_listbox.bind("<B1-Motion>", self.on_drag_motion)

        self.task_counter = 1  # Initialize the task counter
        self.update_clock()  # Update the clock initially
        self.update_clock_interval = 1000  # Update the clock every second
        self.root.after(self.update_clock_interval, self.update_clock_periodic)

        # Variables for drag-and-drop
        self.drag_data = {"x": 0, "y": 0, "item": None}

        # Schedule the star animation
        self.root.after(100, self.move_stars)

        # Load tasks from file
        self.load_tasks()
        
    def move_stars(self):
        for star in self.stars:
            dx = random.randint(-5, 5)
            dy = random.randint(-5, 5)
            self.canvas.move(star, dx, dy)
        # Reschedule the movement
        self.root.after(100, self.move_stars)

    def get_current_date(self):
        return datetime.now().strftime("%Y-%m-%d")

    def update_clock(self):
        current_time = time.strftime("%H:%M:%S")
        self.clock_label.config(text=current_time)

    def update_clock_periodic(self):
        self.update_clock()
        self.root.after(self.update_clock_interval, self.update_clock_periodic)

    def add_task(self):
        task = self.task_entry.get().strip()  # Remove leading/trailing spaces
        deadline = self.deadline_entry.get().strip()  # Remove leading/trailing spaces
        if task:
            # Include the task number, task, and deadline when adding to the listbox
            task_with_number_and_date = f"{self.task_counter}. {task} (Deadline: {deadline})"
            self.task_listbox.insert(tk.END, task_with_number_and_date)
            self.renumber_tasks()
            self.save_tasks()
            self.task_entry.delete(0, tk.END)
            self.deadline_entry.delete(0, tk.END)
            self.task_counter += 1  # Increment the task counter
        else:
            messagebox.showwarning("Input Error", "Task cannot be empty!")

    def remove_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            self.task_listbox.delete(selected_index)
            self.renumber_tasks()
            self.save_tasks()

    def on_start_drag(self, event):
        # Get the item under the cursor
        self.drag_data["item"] = self.task_listbox.nearest(event.y)

    def on_drag_motion(self, event):
        # Move the item under the cursor to the new position
        new_index = self.task_listbox.nearest(event.y)
        if new_index != self.drag_data["item"]:
            task = self.task_listbox.get(self.drag_data["item"])
            self.task_listbox.delete(self.drag_data["item"])
            self.task_listbox.insert(new_index, task)
            self.renumber_tasks()
            self.save_tasks()
            self.drag_data["item"] = new_index

    def on_task_click(self, event):
        # Change color when a task is clicked
        task_index = self.task_listbox.nearest(event.y)
        self.task_listbox.selection_clear(0, tk.END)
        self.task_listbox.selection_set(task_index)
        self.task_listbox.activate(task_index)
        self.task_listbox.itemconfig(task_index, {'bg': 'blue', 'fg': 'black'})

    def renumber_tasks(self):
        # Update task numbers based on their new order
        tasks = self.task_listbox.get(0, tk.END)
        self.task_listbox.delete(0, tk.END)
        for i, task in enumerate(tasks, start=1):
            task_text = task.split('.', 1)[1].lstrip()  # Remove leading spaces
            self.task_listbox.insert(tk.END, f"{i}. {task_text}")


        # Save the updated tasks to the file
        self.save_tasks()

    def save_tasks(self):
        tasks = self.task_listbox.get(0, tk.END)
        with open("tasks.txt", "w") as file:
            for task_with_number_and_date in tasks:
                # Extract task and deadline, removing leading/trailing spaces
                task_with_number_and_date = task_with_number_and_date.strip()
                file.write(task_with_number_and_date + "\n")

    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as file:
                tasks = file.read().splitlines()
                for task_with_number_and_date in tasks:
                    self.task_listbox.insert(tk.END, task_with_number_and_date)
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
