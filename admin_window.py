# admin_window.py

import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection

root = None
tree = None

# ---------------------------- Load Players -----------------------------
def load_players():
    for row in tree.get_children():
        tree.delete(row)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, position, age, club, nation, appearances, goals, assists FROM player")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    conn.close()

# ---------------------------- Add Player ------------------------------
def add_player():
    data = [e.get() for e in entries]
    if "" in data:
        messagebox.showerror("Error", "All fields are required")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO player (name, position, age, club, nation, appearances, goals, assists) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", data)
        conn.commit()
        conn.close()
        load_players()
        clear_entries()
        messagebox.showinfo("Success", "Player added successfully")
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# ---------------------------- Update Player ------------------------------
def update_player():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Select Player", "Select a player to update")
        return

    player_id = tree.item(selected)['values'][0]
    data = [e.get() for e in entries]

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE player SET name=%s, position=%s, age=%s, club=%s, nation=%s, appearances=%s, goals=%s, assists=%s WHERE id=%s", data + [player_id])
        conn.commit()
        conn.close()
        load_players()
        clear_entries()
        messagebox.showinfo("Updated", "Player details updated")
    except Exception as e:
        messagebox.showerror("Update Error", str(e))

# ---------------------------- Delete Player ------------------------------
def delete_player():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Select Player", "Select a player to delete")
        return

    player_id = tree.item(selected)['values'][0]

    confirm = messagebox.askyesno("Confirm", "Delete selected player?")
    if confirm:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM player WHERE id=%s", (player_id,))
            conn.commit()
            conn.close()
            load_players()
            clear_entries()
            messagebox.showinfo("Deleted", "Player deleted successfully")
        except Exception as e:
            messagebox.showerror("Delete Error", str(e))

# ---------------------------- Fill Fields from Tree ------------------------------
def fill_entries(event):
    selected = tree.focus()
    if not selected:
        return

    values = tree.item(selected)['values'][1:]  # Skip ID
    for entry, val in zip(entries, values):
        entry.delete(0, tk.END)
        entry.insert(0, val)

# ---------------------------- Clear Fields ------------------------------
def clear_entries():
    for e in entries:
        e.delete(0, tk.END)

# ---------------------------- Show Admin Window ------------------------------
def show():
    global root, tree, entries
    root = tk.Tk()
    root.title("Admin Panel - Footy")
    root.geometry("1100x600")
    root.configure(bg="#0f172a")

    # Sidebar
    sidebar = tk.Frame(root, bg="#1e293b", width=200)
    sidebar.pack(side="left", fill="y")
    tk.Label(sidebar, text="FOOTY Admin", font=("Helvetica", 16, "bold"), bg="#1e293b", fg="#22c55e").pack(pady=20)

    tk.Button(sidebar, text="Add Player", command=add_player, font=("Helvetica", 12), bg="#22c55e", fg="white").pack(pady=10, fill="x", padx=10)
    tk.Button(sidebar, text="Update Player", command=update_player, font=("Helvetica", 12), bg="#22c55e", fg="white").pack(pady=10, fill="x", padx=10)
    tk.Button(sidebar, text="Delete Player", command=delete_player, font=("Helvetica", 12), bg="#ef4444", fg="white").pack(pady=10, fill="x", padx=10)
    tk.Button(sidebar, text="Clear Fields", command=clear_entries, font=("Helvetica", 12), bg="#1e293b", fg="#22c55e").pack(pady=10, fill="x", padx=10)

    # Form Panel
    form_frame = tk.Frame(root, bg="#0f172a")
    form_frame.pack(side="top", fill="x", padx=20, pady=10)

    fields = ["Name", "Position", "Age", "Club", "Nation", "Apps", "Goals", "Assists"]
    entries = []
    for idx, label in enumerate(fields):
        tk.Label(form_frame, text=label, font=("Helvetica", 10), bg="#0f172a", fg="white").grid(row=0, column=idx, padx=8)
        e = tk.Entry(form_frame, width=12)
        e.grid(row=1, column=idx, padx=8)
        entries.append(e)

    # Data Table
    table_frame = tk.Frame(root)
    table_frame.pack(fill="both", expand=True, padx=20, pady=20)

    cols = ["ID"] + fields
    tree = ttk.Treeview(table_frame, columns=cols, show="headings")
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    tree.pack(fill="both", expand=True)
    tree.bind("<ButtonRelease-1>", fill_entries)

    load_players()
    root.mainloop()
