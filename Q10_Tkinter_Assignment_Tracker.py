"""
Q10 - Tkinter Assignment Tracker with File Persistence
"""
import tkinter as tk
from tkinter import ttk, messagebox
import csv
import json
import os

DATA_FILE = "assignments.json"

# Load existing data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# Save data
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Export to CSV
def export_csv(data):
    with open("assignments.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Enrollment", "Name", "Assignment", "Status", "Marks", "Remarks"])
        for record in data:
            writer.writerow([record["enrollment"], record["name"], record["assignment"],
                             record["status"], record["marks"], record["remarks"]])
    messagebox.showinfo("Export", "Data exported to assignments.csv")

# GUI Application
class AssignmentTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Assignment Tracker")

        self.data = load_data()

        # Widgets
        tk.Label(root, text="Enrollment").grid(row=0, column=0)
        tk.Label(root, text="Name").grid(row=1, column=0)
        tk.Label(root, text="Assignment").grid(row=2, column=0)
        tk.Label(root, text="Marks").grid(row=3, column=0)
        tk.Label(root, text="Status").grid(row=4, column=0)
        tk.Label(root, text="Remarks").grid(row=5, column=0)

        self.enrollment = tk.Entry(root)
        self.name = tk.Entry(root)
        self.assignment = tk.Entry(root)
        self.marks = tk.Entry(root)
        self.status = ttk.Combobox(root, values=["Pending", "Completed"])
        self.remarks = tk.Entry(root)

        self.enrollment.grid(row=0, column=1)
        self.name.grid(row=1, column=1)
        self.assignment.grid(row=2, column=1)
        self.marks.grid(row=3, column=1)
        self.status.grid(row=4, column=1)
        self.remarks.grid(row=5, column=1)

        tk.Button(root, text="Add Submission", command=self.add_submission).grid(row=6, column=0)
        tk.Button(root, text="Export CSV", command=lambda: export_csv(self.data)).grid(row=6, column=1)

        self.tree = ttk.Treeview(root, columns=("Enrollment", "Name", "Assignment", "Status", "Marks", "Remarks"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.grid(row=7, column=0, columnspan=2)

        self.refresh_tree()

    def add_submission(self):
        record = {
            "enrollment": self.enrollment.get(),
            "name": self.name.get(),
            "assignment": self.assignment.get(),
            "marks": self.marks.get(),
            "status": self.status.get(),
            "remarks": self.remarks.get()
        }

        if not record["enrollment"] or not record["name"]:
            messagebox.showerror("Error", "Enrollment and Name are required")
            return

        self.data.append(record)
        save_data(self.data)
        self.refresh_tree()
        messagebox.showinfo("Success", "Submission added successfully")

    def refresh_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for record in self.data:
            self.tree.insert("", "end", values=(record["enrollment"], record["name"], record["assignment"],
                                                record["status"], record["marks"], record["remarks"]))


# ---------------- SAMPLE USAGE ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = AssignmentTracker(root)
    root.mainloop()
