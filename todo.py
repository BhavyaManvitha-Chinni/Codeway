import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

class ToDoListApp:
    def __init__(self, master):
        self.master = master
        self.master.title("To-Do List App")
        
        # Connect to SQLite database
        self.conn = sqlite3.connect("todo_list.db")
        self.cursor = self.conn.cursor()
        
        # Create tasks table if not exists
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS tasks (
                                id INTEGER PRIMARY KEY,
                                title TEXT NOT NULL,
                                description TEXT,
                                priority INTEGER DEFAULT 0,
                                due_date TEXT,
                                completed INTEGER DEFAULT 0
                                )""")
        
        self.tasks = []
        self.load_tasks()
        self.create_widgets()
    
    def create_widgets(self):
        self.task_listbox = tk.Listbox(self.master, width=50, height=15)
        self.task_listbox.grid(row=0, column=0, padx=10, pady=10, columnspan=3)
        
        self.add_button = tk.Button(self.master, text="Add Task", command=self.add_task)
        self.add_button.grid(row=1, column=0, padx=5, pady=5)
        
        self.edit_button = tk.Button(self.master, text="Edit Task", command=self.edit_task)
        self.edit_button.grid(row=1, column=1, padx=5, pady=5)
        
        self.delete_button = tk.Button(self.master, text="Delete Task", command=self.delete_task)
        self.delete_button.grid(row=1, column=2, padx=5, pady=5)
        
        self.refresh_listbox()
    
    def load_tasks(self):
        self.tasks = []
        self.cursor.execute("SELECT * FROM tasks")
        rows = self.cursor.fetchall()
        for row in rows:
            self.tasks.append(row)
    
    def refresh_listbox(self):
        self.load_tasks()
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "Completed" if task[5] else "Active"
            self.task_listbox.insert(tk.END, f"{task[1]} - {status}")
    
    def add_task(self):
        self.add_edit_window("Add Task")
    
    def edit_task(self):
        if not self.task_listbox.curselection():
            messagebox.showwarning("Warning", "Please select a task to edit.")
            return
        selected_index = self.task_listbox.curselection()[0]
        task_id = self.tasks[selected_index][0]
        self.add_edit_window("Edit Task", task_id)
    
    def delete_task(self):
        if not self.task_listbox.curselection():
            messagebox.showwarning("Warning", "Please select a task to delete.")
            return
        selected_index = self.task_listbox.curselection()[0]
        task_id = self.tasks[selected_index][0]
        self.cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        self.conn.commit()
        self.refresh_listbox()
    
    def add_edit_window(self, mode, task_id=None):
        window = tk.Toplevel(self.master)
        window.title(mode)
        
        tk.Label(window, text="Title:").grid(row=0, column=0, padx=5, pady=5)
        title_entry = tk.Entry(window, width=40)
        title_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(window, text="Description:").grid(row=1, column=0, padx=5, pady=5)
        description_entry = tk.Text(window, width=40, height=5)
        description_entry.grid(row=1, column=1, padx=5, pady=5)
        
        if mode == "Edit Task":
            task = self.cursor.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
            title_entry.insert(tk.END, task[1])
            description_entry.insert(tk.END, task[2])
        
        def save_task():
            title = title_entry.get()
            description = description_entry.get("1.0", tk.END)
            if mode == "Add Task":
                self.cursor.execute("INSERT INTO tasks (title, description) VALUES (?, ?)", (title, description))
            elif mode == "Edit Task":
                self.cursor.execute("UPDATE tasks SET title=?, description=? WHERE id=?", (title, description, task_id))
            self.conn.commit()
            self.refresh_listbox()
            window.destroy()
        
        save_button = tk.Button(window, text="Save", command=save_task)
        save_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        
        cancel_button = tk.Button(window, text="Cancel", command=window.destroy)
        cancel_button.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

root = tk.Tk()
app = ToDoListApp(root)
root.mainloop()
