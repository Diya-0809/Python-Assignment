"""
Q10 - Tkinter Assignment Tracker with File Persistence
Python 3.10+
"""
import csv
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

DATA_FILE = Path("assignment_tracker.json")

class AssignmentTracker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Assignment Tracker")
        self.geometry("900x600")
        self.records = []
        self.load_data()
        self.build_ui()
        self.refresh()

    def load_data(self):
        if DATA_FILE.exists():
            try:
                with DATA_FILE.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, list):
                    self.records = data
            except (OSError, json.JSONDecodeError):
                self.records = []

    def save_data(self):
        with DATA_FILE.open("w", encoding="utf-8") as f:
            json.dump(self.records, f, indent=2)

    def build_ui(self):
        form = ttk.LabelFrame(self, text="Record")
        form.pack(fill="x", padx=10, pady=10)

        labels = [
            ("Enrollment", "enrollment"),
            ("Name", "name"),
            ("Assignment", "assignment"),
            ("Marks", "marks"),
            ("Remarks", "remarks"),
        ]
        self.entries = {}

        for col, (label, key) in enumerate(labels):
            ttk.Label(form, text=label).grid(row=0, column=col, padx=5, pady=5)
            entry = ttk.Entry(form, width=18)
            entry.grid(row=1, column=col, padx=5, pady=5)
            self.entries[key] = entry

        ttk.Label(form, text="Status").grid(row=0, column=5)
        self.status_var = tk.StringVar(value="Pending")
        status = ttk.Combobox(
            form, textvariable=self.status_var,
            values=["Pending", "Completed"], state="readonly", width=14
        )
        status.grid(row=1, column=5, padx=5)

        buttons = ttk.Frame(self)
        buttons.pack(fill="x", padx=10)

        ttk.Button(buttons, text="Add Student", command=self.add_student).pack(side="left", padx=4)
        ttk.Button(buttons, text="Add Submission", command=self.add_submission).pack(side="left", padx=4)
        ttk.Button(buttons, text="Update Marks", command=self.update_marks).pack(side="left", padx=4)
        ttk.Button(buttons, text="Export CSV", command=self.export_csv).pack(side="left", padx=4)

        ttk.Label(buttons, text="Filter:").pack(side="left", padx=(20, 4))
        self.filter_var = tk.StringVar(value="All")
        filter_box = ttk.Combobox(
            buttons, textvariable=self.filter_var,
            values=["All", "Pending", "Completed"], state="readonly", width=12
        )
        filter_box.pack(side="left")
        filter_box.bind("<<ComboboxSelected>>", lambda _: self.refresh())

        columns = ("enrollment", "name", "assignment", "status", "marks", "remarks")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        headings = {
            "enrollment": "Enrollment", "name": "Name",
            "assignment": "Assignment", "status": "Status",
            "marks": "Marks", "remarks": "Remarks"
        }
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=130)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def get_fields(self, require_assignment=True):
        e = {key: box.get().strip() for key, box in self.entries.items()}
        if not e["enrollment"] or not e["name"]:
            raise ValueError("Enrollment and name are required.")
        if require_assignment and not e["assignment"]:
            raise ValueError("Assignment is required.")
        return e

    def add_student(self):
        try:
            e = self.get_fields(require_assignment=False)
            # Student creation is represented by ensuring a student record exists.
            if not any(r["enrollment"] == e["enrollment"] for r in self.records):
                self.records.append({
                    "enrollment": e["enrollment"], "name": e["name"],
                    "assignment": "", "status": "Pending",
                    "marks": "", "remarks": ""
                })
                self.save_data()
                self.refresh()
            else:
                messagebox.showinfo("Info", "Student already exists.")
        except ValueError as exc:
            messagebox.showerror("Validation Error", str(exc))

    def add_submission(self):
        try:
            e = self.get_fields(require_assignment=True)
            marks = e["marks"]
            if marks:
                value = float(marks)
                if value < 0:
                    raise ValueError("Marks cannot be negative.")
                if value > 100:
                    raise ValueError("Marks cannot exceed 100.")
                marks = str(int(value)) if value.is_integer() else str(value)

            self.records.append({
                "enrollment": e["enrollment"],
                "name": e["name"],
                "assignment": e["assignment"],
                "status": self.status_var.get(),
                "marks": marks,
                "remarks": e["remarks"],
            })
            self.save_data()
            self.refresh()
        except ValueError as exc:
            messagebox.showerror("Validation Error", str(exc))

    def update_marks(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a record first.")
            return
        marks = self.entries["marks"].get().strip()
        try:
            value = float(marks)
            if not 0 <= value <= 100:
                raise ValueError("Marks must be between 0 and 100.")
        except ValueError:
            messagebox.showerror("Validation Error", "Enter marks between 0 and 100.")
            return

        item = self.tree.item(selected[0])
        enrollment = item["values"][0]
        assignment = item["values"][2]

        for record in self.records:
            if record["enrollment"] == enrollment and record["assignment"] == assignment:
                record["marks"] = str(int(value)) if value.is_integer() else str(value)
                record["status"] = "Completed"
                break

        self.save_data()
        self.refresh()

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        selected_filter = self.filter_var.get()
        for r in self.records:
            if selected_filter != "All" and r.get("status") != selected_filter:
                continue
            self.tree.insert("", "end", values=(
                r.get("enrollment", ""), r.get("name", ""),
                r.get("assignment", ""), r.get("status", ""),
                r.get("marks", ""), r.get("remarks", "")
            ))

    def export_csv(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if not path:
            return

        fields = ["enrollment", "name", "assignment", "status", "marks", "remarks"]
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writeheader()
                writer.writerows(self.records)
            messagebox.showinfo("Export", "CSV report exported successfully.")
        except OSError as exc:
            messagebox.showerror("Export Error", str(exc))

if __name__ == "__main__":
    app = AssignmentTracker()
    app.mainloop()
