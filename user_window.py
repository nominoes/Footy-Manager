# user_window.py

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from database import get_connection
import csv

class UserWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Footy - User Panel")
        self.root.geometry("1200x700")
        self.root.configure(bg="#0f172a")
        self.current_theme = "dark"

        self.setup_ui()
        self.load_data()
        self.load_stats()

    def setup_ui(self):
        sidebar = tk.Frame(self.root, bg="#1e293b", width=200)
        sidebar.pack(side="left", fill="y")

        tk.Label(sidebar, text="FOOTY", font=("Helvetica", 20, "bold"), fg="#22c55e", bg="#1e293b").pack(pady=20)

        tk.Button(sidebar, text="Dashboard", font=("Helvetica", 12), bg="#22c55e", fg="white", command=self.load_data).pack(pady=10, fill="x")
        tk.Button(sidebar, text="Search", font=("Helvetica", 12), bg="#334155", fg="white", command=self.search_data).pack(pady=10, fill="x")
        tk.Button(sidebar, text="Sort", font=("Helvetica", 12), bg="#334155", fg="white", command=self.sort_data).pack(pady=10, fill="x")
        tk.Button(sidebar, text="Export CSV", font=("Helvetica", 12), bg="#334155", fg="white", command=self.export_csv).pack(pady=10, fill="x")
        tk.Button(sidebar, text="Toggle Theme", font=("Helvetica", 12), bg="#334155", fg="white", command=self.toggle_theme).pack(pady=10, fill="x")
        tk.Button(sidebar, text="Exit", font=("Helvetica", 12), bg="#334155", fg="white", command=self.root.destroy).pack(pady=30, fill="x")

        top_frame = tk.Frame(self.root, bg="#0f172a")
        top_frame.pack(fill="x", pady=(10, 0))

        tk.Label(top_frame, text="Welcome to the Footy Dashboard!", font=("Helvetica", 18, "bold"), bg="#0f172a", fg="#22c55e").pack(pady=10)

        self.stat_frame = tk.Frame(self.root, bg="#0f172a")
        self.stat_frame.pack(fill="x", padx=20, pady=(5, 10))

        self.card1 = self.create_stat_card(self.stat_frame, "Total Players", "0")
        self.card2 = self.create_stat_card(self.stat_frame, "Avg Goals", "0")
        self.card3 = self.create_stat_card(self.stat_frame, "Avg Assists", "0")

        self.card1.pack(side="left", padx=10)
        self.card2.pack(side="left", padx=10)
        self.card3.pack(side="left", padx=10)

        # Table frame
        main_frame = tk.Frame(self.root, bg="#0f172a")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#1e293b",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#1e293b",
                        font=("Helvetica", 11))
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background="#22c55e", foreground="black")

        self.tree = ttk.Treeview(main_frame, columns=("ID", "Name", "Position", "Age", "Club", "Nation", "Apps", "Goals", "Assists"), show="headings")
        self.tree.pack(fill="both", expand=True)

        for col in ("ID", "Name", "Position", "Age", "Club", "Nation", "Apps", "Goals", "Assists"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=100)

    def create_stat_card(self, parent, title, value):
        card = tk.Frame(parent, bg="#1e293b", width=200, height=100)
        card.pack_propagate(False)

        tk.Label(card, text=title, font=("Helvetica", 12), bg="#1e293b", fg="#94a3b8").pack(pady=(10, 0))
        label = tk.Label(card, text=value, font=("Helvetica", 20, "bold"), bg="#1e293b", fg="#22c55e")
        label.pack()

        return card

    def load_stats(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*), AVG(goals), AVG(assists) FROM player")
        total, avg_goals, avg_assists = cursor.fetchone()
        conn.close()

        self.card1.winfo_children()[1].config(text=str(total))
        self.card2.winfo_children()[1].config(text=f"{avg_goals:.2f}")
        self.card3.winfo_children()[1].config(text=f"{avg_assists:.2f}")

    def load_data(self):
        self.tree.delete(*self.tree.get_children())
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM player")
        rows = cursor.fetchall()
        for row in rows:
            self.tree.insert("", "end", values=row)
        conn.close()
        self.load_stats()

    def search_data(self):
        def perform_search():
            keyword = search_entry.get()
            self.tree.delete(*self.tree.get_children())
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM player WHERE name LIKE %s", ('%' + keyword + '%',))
            rows = cursor.fetchall()
            for row in rows:
                self.tree.insert("", "end", values=row)
            conn.close()
            top.destroy()

        top = tk.Toplevel(self.root)
        top.title("Search Player")
        top.geometry("300x100")
        tk.Label(top, text="Enter Name:").pack(pady=5)
        search_entry = tk.Entry(top)
        search_entry.pack(pady=5)
        tk.Button(top, text="Search", command=perform_search).pack(pady=5)

    def sort_data(self):
        def perform_sort():
            field = sort_var.get()
            self.tree.delete(*self.tree.get_children())
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM player ORDER BY {field} DESC")
            rows = cursor.fetchall()
            for row in rows:
                self.tree.insert("", "end", values=row)
            conn.close()
            top.destroy()

        top = tk.Toplevel(self.root)
        top.title("Sort Players")
        top.geometry("300x100")
        tk.Label(top, text="Sort by:").pack(pady=5)
        sort_var = tk.StringVar(value="goals")
        tk.OptionMenu(top, sort_var, "age", "goals", "assists").pack(pady=5)
        tk.Button(top, text="Sort", command=perform_sort).pack(pady=5)

    def export_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM player")
        rows = cursor.fetchall()
        conn.close()
        with open(file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Name", "Position", "Age", "Club", "Nation", "Apps", "Goals", "Assists"])
            writer.writerows(rows)
        messagebox.showinfo("Export Successful", "Data exported to CSV successfully!")

    def toggle_theme(self):
        if self.current_theme == "dark":
            self.root.configure(bg="white")
            self.stat_frame.configure(bg="white")
            self.current_theme = "light"
        else:
            self.root.configure(bg="#0f172a")
            self.stat_frame.configure(bg="#0f172a")
            self.current_theme = "dark"


def show():
    root = tk.Tk()
    app = UserWindow(root)
    root.mainloop()
