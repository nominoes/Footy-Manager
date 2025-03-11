# main.py

import tkinter as tk
from tkinter import messagebox, ttk
from database import get_connection
import user_window
import admin_window

def login():
    uname = username.get()
    pwd = password.get()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (uname, pwd))
    result = cursor.fetchone()
    conn.close()

    if result:
        role = result[3]
        root.destroy()
        if role == 'admin':
            admin_window.show()
        else:
            user_window.show()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def register():
    uname = username.get()
    pwd = password.get()
    r = role.get()

    if not r:
        messagebox.showwarning("Missing Role", "Please select a role")
        return

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (uname, pwd, r))
        conn.commit()
        messagebox.showinfo("Success", f"Registered as {r.capitalize()}")
    except:
        messagebox.showerror("Error", "Registration Failed. Username may already exist.")
    conn.close()

root = tk.Tk()
root.title("Footy Login")
root.geometry("400x520")
root.configure(bg="#0f172a")

# Title
tk.Label(root, text="Footy Login", font=("Helvetica", 24, 'bold'), fg="#22c55e", bg="#0f172a").pack(pady=30)

# Username & Password
username = tk.StringVar()
password = tk.StringVar()
role = tk.StringVar()

style = {'font': ("Helvetica", 14), 'bg': "#1e293b", 'fg': "#e2e8f0", 'insertbackground': 'white'}

tk.Entry(root, textvariable=username, **style, width=25, relief='flat').pack(pady=10)
tk.Entry(root, textvariable=password, show="*", **style, width=25, relief='flat').pack(pady=10)

# Role Dropdown
role_label = tk.Label(root, text="Select Role:", bg="#0f172a", fg="#cbd5e1", font=("Helvetica", 12))
role_label.pack(pady=(10, 0))
role_dropdown = ttk.Combobox(root, textvariable=role, values=["user", "admin"], font=("Helvetica", 12), state="readonly")
role_dropdown.pack(pady=5)

# Buttons
btn_style = {'font': ("Helvetica", 12), 'width': 20, 'padx': 10, 'pady': 5}
tk.Button(root, text="Login", bg="#22c55e", fg="white", command=login, **btn_style).pack(pady=10)
tk.Button(root, text="Register", bg="#1e293b", fg="#22c55e", command=register, **btn_style).pack(pady=5)

root.mainloop()
