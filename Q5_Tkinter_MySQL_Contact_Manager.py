"""Q5: Tkinter contact manager backed by MySQL.
Install: pip install mysql-connector-python
"""
import re
import tkinter as tk
from tkinter import ttk, messagebox
import getpass

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

class ContactManager:
    def __init__(self, root, connection):
        self.root, self.connection = root, connection
        self.root.title("Contact Manager")
        self.fields = {}
        self.build()
        self.refresh()

    def build(self):
        form = ttk.LabelFrame(self.root, text="Contact details", padding=8)
        form.pack(fill="x", padx=8, pady=8)
        for i, name in enumerate(("id", "name", "email", "phone", "category", "notes")):
            ttk.Label(form, text=name.title()).grid(row=i//3*2, column=i%3, sticky="w")
            var = tk.StringVar()
            self.fields[name] = var
            if name == "category":
                widget = ttk.Combobox(form, textvariable=var,
                    values=("Personal", "Faculty", "Student", "Work"), state="readonly")
            else:
                widget = ttk.Entry(form, textvariable=var, width=28)
            widget.grid(row=i//3*2+1, column=i%3, padx=4, pady=3, sticky="ew")
        buttons = ttk.Frame(self.root); buttons.pack(fill="x", padx=8)
        for label, command in (("Add", self.add), ("Update", self.update),
                               ("Delete", self.delete), ("Search", self.search),
                               ("Show All", self.refresh)):
            ttk.Button(buttons, text=label, command=command).pack(side="left", padx=3)
        self.query = tk.StringVar()
        ttk.Entry(buttons, textvariable=self.query, width=20).pack(side="left", padx=5)
        self.tree = ttk.Treeview(self.root, columns=("id","name","email","phone","category","notes"),
                                 show="headings", height=14)
        for c in self.tree["columns"]:
            self.tree.heading(c, text=c.title()); self.tree.column(c, width=125)
        self.tree.pack(fill="both", expand=True, padx=8, pady=8)
        self.tree.bind("<<TreeviewSelect>>", self.select)

    def values(self):
        return {key: value.get().strip() for key, value in self.fields.items()}

    def validate(self):
        d = self.values()
        if not d["name"] or not d["email"]: raise ValueError("Name and email are required")
        if not EMAIL_RE.fullmatch(d["email"]): raise ValueError("Invalid email address")
        return d

    def run(self, sql, params=()):
        cur = self.connection.cursor()
        cur.execute(sql, params)
        result = cur.fetchall() if sql.lstrip().upper().startswith("SELECT") else None
        self.connection.commit(); cur.close()
        return result

    def add(self):
        try:
            d = self.validate()
            self.run("INSERT INTO Contact(name,email,phone,category,notes) VALUES(%s,%s,%s,%s,%s)",
                     (d["name"], d["email"], d["phone"], d["category"], d["notes"]))
            self.refresh(); messagebox.showinfo("Saved", "Contact added")
        except Exception as e: messagebox.showerror("Cannot add contact", str(e))

    def update(self):
        try:
            d = self.validate()
            if not d["id"].isdigit(): raise ValueError("Select a contact or enter its numeric ID")
            self.run("UPDATE Contact SET name=%s,email=%s,phone=%s,category=%s,notes=%s WHERE id=%s",
                     (d["name"], d["email"], d["phone"], d["category"], d["notes"], int(d["id"])))
            self.refresh()
        except Exception as e: messagebox.showerror("Cannot update contact", str(e))

    def delete(self):
        try:
            ident = self.fields["id"].get().strip()
            if not ident.isdigit(): raise ValueError("Select a contact first")
            self.run("DELETE FROM Contact WHERE id=%s", (int(ident),)); self.refresh()
        except Exception as e: messagebox.showerror("Cannot delete contact", str(e))

    def search(self):
        term = "%" + self.query.get().strip() + "%"
        try:
            rows = self.run("SELECT id,name,email,phone,category,notes FROM Contact "
                            "WHERE name LIKE %s OR email LIKE %s OR phone LIKE %s ORDER BY name",
                            (term, term, term))
            self.show_rows(rows)
        except Exception as e: messagebox.showerror("Search error", str(e))

    def refresh(self):
        try: self.show_rows(self.run("SELECT id,name,email,phone,category,notes FROM Contact ORDER BY name"))
        except Exception as e: messagebox.showerror("Database error", str(e))

    def show_rows(self, rows):
        self.tree.delete(*self.tree.get_children())
        for row in rows: self.tree.insert("", "end", values=row)

    def select(self, _event=None):
        selected = self.tree.selection()
        if selected:
            for key, value in zip(self.fields, self.tree.item(selected[0], "values")):
                self.fields[key].set(value)

def main():
    try:
        import mysql.connector
        host = input("MySQL host [localhost]: ").strip() or "localhost"
        user = input("MySQL user: ").strip()
        password = getpass.getpass("MySQL password: ")
        database = input("Database: ").strip()
        conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS Contact(
            id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(200) NOT NULL,
            email VARCHAR(254) NOT NULL UNIQUE, phone VARCHAR(40),
            category VARCHAR(40), notes TEXT, INDEX(name), INDEX(phone))""")
        conn.commit(); cur.close()
        root = tk.Tk(); ContactManager(root, conn); root.mainloop()
        conn.close()
    except Exception as exc:
        print(f"Startup error: {exc}")

if __name__ == "__main__":
    main()
