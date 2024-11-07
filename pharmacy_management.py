import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="SreyasGiri",
        password="Sre247yas@04",
        database="pharmacy_management"
    )

def open_admin_dashboard():
    admin_window = tk.Toplevel()
    admin_window.title("Admin Dashboard")
    admin_window.attributes('-fullscreen', True)
    admin_window.configure(bg="#f0f0f0")
    frame = tk.Frame(admin_window, bg="#ffffff", padx=40, pady=40)
    frame.pack(expand=True)
    tk.Label(frame, text="Welcome to the Admin Dashboard!", font=("Arial", 36, "bold"), bg="#ffffff").pack(pady=20)

    def create_button(text, command):
        return tk.Button(frame, text=text, command=command, font=("Arial", 18), bg="#007bff", fg="#ffffff", relief="flat", padx=10, pady=15)

    create_button("Manage Medicines", manage_medicines).pack(pady=10, fill=tk.X)
    create_button("Manage Customers", manage_customers).pack(pady=10, fill=tk.X)
    create_button("Manage Sales", manage_sales).pack(pady=10, fill=tk.X)
    create_button("Manage Suppliers", manage_suppliers).pack(pady=10, fill=tk.X)
    create_button("Manage Employees", manage_employees).pack(pady=10, fill=tk.X)
    tk.Button(frame, text="Logout", command=admin_window.destroy, font=("Arial", 18), bg="#dc3545", fg="#ffffff", relief="flat", padx=10, pady=15).pack(pady=20, fill=tk.X)

def open_employee_dashboard():
    employee_window = tk.Toplevel()
    employee_window.title("Employee Dashboard")
    employee_window.attributes('-fullscreen', True)
    employee_window.configure(bg="#f0f0f0")
    frame = tk.Frame(employee_window, bg="#ffffff", padx=40, pady=40)
    frame.pack(expand=True)
    tk.Label(frame, text="Welcome to the Employee Dashboard!", font=("Arial", 36, "bold"), bg="#ffffff").pack(pady=20)

    def create_button(text, command):
        return tk.Button(frame, text=text, command=command, font=("Arial", 18), bg="#007bff", fg="#ffffff", relief="flat", padx=10, pady=15)

    create_button("Manage Medicines", manage_medicines).pack(pady=10, fill=tk.X)
    create_button("Manage Customers", manage_customers).pack(pady=10, fill=tk.X)
    create_button("Manage Sales", manage_sales).pack(pady=10, fill=tk.X)
    create_button("Manage Suppliers", manage_suppliers).pack(pady=10, fill=tk.X)
    tk.Button(frame, text="Logout", command=employee_window.destroy, font=("Arial", 18), bg="#dc3545", fg="#ffffff", relief="flat", padx=10, pady=15).pack(pady=20, fill=tk.X)

def login_user(role, password):
    conn = create_connection()
    cursor = conn.cursor()
    if role == "Admin":
        cursor.execute("SELECT * FROM Employees WHERE password = %s AND role = 'Admin'", (password,))
        admin = cursor.fetchone()
        return "Admin" if admin else "Invalid"
    elif role == "Employee":
        cursor.execute("SELECT * FROM Employees WHERE password = %s", (password,))
        employee = cursor.fetchone()
        return "Employee" if employee else "Invalid"

def prompt_password(role):
    def submit():
        password = password_entry.get()
        role_result = login_user(role, password)
        if role_result == "Admin":
            messagebox.showinfo("Login Successful", "Welcome Admin!")
            open_admin_dashboard()
        elif role_result == "Employee":
            messagebox.showinfo("Login Successful", "Welcome Employee!")
            open_employee_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid password.")
            password_window.destroy()

    password_window = tk.Toplevel()
    password_window.title(f"{role} Login")
    password_window.attributes('-fullscreen', True)
    password_window.configure(bg="#f0f0f0")
    frame = tk.Frame(password_window, bg="#ffffff", padx=40, pady=40)
    frame.pack(expand=True)
    tk.Label(frame, text=f"{role} Password:", font=("Arial", 24, "bold"), bg="#ffffff").pack(pady=20)
    password_entry = tk.Entry(frame, show="*", font=("Arial", 18), width=30)
    password_entry.pack(pady=10)
    tk.Button(frame, text="Submit", command=submit, font=("Arial", 18), bg="#007bff", fg="#ffffff", relief="flat", padx=10, pady=10).pack(pady=20)
    tk.Button(frame, text="Back", command=password_window.destroy, font=("Arial", 18), bg="#dc3545", fg="#ffffff", relief="flat", padx=10, pady=10).pack(pady=10)

import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="SreyasGiri",
        password="Sre247yas@04",
        database="pharmacy_management"
    )

def manage_medicines():
    medicines_window = tk.Toplevel()
    medicines_window.title("Manage Medicines")
    medicines_window.attributes('-fullscreen', True)
    medicines_window.configure(bg="#f0f0f0")
    frame = tk.Frame(medicines_window, bg="#ffffff", padx=40, pady=40)
    frame.pack(expand=True, fill=tk.BOTH)
    global tree  
    tree = ttk.Treeview(frame, columns=("ID", "Name", "Price", "Quantity", "Expiry Date"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Price", text="Price")
    tree.heading("Quantity", text="Quantity")
    tree.heading("Expiry Date", text="Expiry Date")
    tree.pack(expand=True, fill=tk.BOTH)

    def refresh_treeview():
        for row in tree.get_children():
            tree.delete(row)
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Medicines")
        medicines = cursor.fetchall()
        conn.close()
        for medicine in medicines:
            tree.insert("", tk.END, values=medicine)

    refresh_treeview()

    def create_button(text, command):
        return tk.Button(frame, text=text, command=command, font=("Arial", 14), bg="#007bff", fg="#ffffff", relief="flat", padx=10, pady=10)

    create_button("Add Medicine", lambda: add_medicine(refresh_treeview)).pack(pady=10, fill=tk.X)
    create_button("Update Medicine", lambda: update_medicine(refresh_treeview)).pack(pady=10, fill=tk.X)
    create_button("Delete Medicine", lambda: delete_medicine(refresh_treeview)).pack(pady=10, fill=tk.X)
    create_button("Back", command=medicines_window.destroy).pack(pady=10, fill=tk.X)

def add_medicine(refresh_function):
    def submit():
        name = name_entry.get()
        price = price_entry.get()
        quantity = quantity_entry.get()
        expiry_date = expiry_entry.get()
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Medicines (name, price, quantity, expiry_date) VALUES (%s, %s, %s, %s)",
                       (name, price, quantity, expiry_date))
        conn.commit()
        conn.close()
        add_window.destroy()
        root.withdraw()
        refresh_function()
        messagebox.showinfo("Success", "Medicine added successfully!")

    add_window = tk.Toplevel()
    add_window.title("Add Medicine")
    add_window.attributes('-fullscreen', True)
    add_window.configure(bg="#f0f0f0")
    tk.Label(add_window, text="Add Medicine", font=("Arial", 24, "bold"), bg="#f0f0f0").pack(pady=20)
    tk.Label(add_window, text="Name:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    name_entry = tk.Entry(add_window, font=("Arial", 14))
    name_entry.pack(pady=10)
    tk.Label(add_window, text="Price:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    price_entry = tk.Entry(add_window, font=("Arial", 14))
    price_entry.pack(pady=10)
    tk.Label(add_window, text="Quantity:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    quantity_entry = tk.Entry(add_window, font=("Arial", 14))
    quantity_entry.pack(pady=10)
    tk.Label(add_window, text="Expiry Date (YYYY-MM-DD):", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    expiry_entry = tk.Entry(add_window, font=("Arial", 14))
    expiry_entry.pack(pady=10)
    tk.Button(add_window, text="Submit", command=submit, font=("Arial", 14), bg="#28a745", fg="#ffffff").pack(pady=20)
    tk.Button(add_window, text="Back", command=add_window.destroy, font=("Arial", 14), bg="#dc3545", fg="#ffffff").pack(pady=20)

def update_medicine(refresh_function):
    def search_medicine():
        medicine_id = medicine_id_entry.get()
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Medicines WHERE medicine_id = %s", (medicine_id,))
        medicine = cursor.fetchone()
        conn.close()
        if medicine:
            name_entry.delete(0, tk.END)
            name_entry.insert(0, medicine[1])
            price_entry.delete(0, tk.END)
            price_entry.insert(0, medicine[2])
            quantity_entry.delete(0, tk.END)
            quantity_entry.insert(0, medicine[3])
            expiry_entry.delete(0, tk.END)
            expiry_entry.insert(0, medicine[4])
        else:
            messagebox.showerror("Error", "Medicine ID not found!")

    def submit_update():
        medicine_id = medicine_id_entry.get()
        name = name_entry.get()
        price = price_entry.get()
        quantity = quantity_entry.get()
        expiry_date = expiry_entry.get()
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Medicines SET name = %s, price = %s, quantity = %s, expiry_date = %s WHERE medicine_id = %s",
                       (name, price, quantity, expiry_date, medicine_id))
        conn.commit()
        conn.close()
        update_window.destroy()
        root.withdraw()
        refresh_function()
        messagebox.showinfo("Success", "Medicine updated successfully!")

    update_window = tk.Toplevel()
    update_window.title("Update Medicine")
    update_window.attributes('-fullscreen', True)
    update_window.configure(bg="#f0f0f0")
    tk.Label(update_window, text="Update Medicine", font=("Arial", 24, "bold"), bg="#f0f0f0").pack(pady=20)
    tk.Label(update_window, text="Medicine ID:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    medicine_id_entry = tk.Entry(update_window, font=("Arial", 14))
    medicine_id_entry.pack(pady=10)
    tk.Button(update_window, text="Search", command=search_medicine, font=("Arial", 14), bg="#007bff", fg="#ffffff").pack(pady=10)
    tk.Label(update_window, text="Name:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    name_entry = tk.Entry(update_window, font=("Arial", 14))
    name_entry.pack(pady=10)
    tk.Label(update_window, text="Price:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    price_entry = tk.Entry(update_window, font=("Arial", 14))
    price_entry.pack(pady=10)
    tk.Label(update_window, text="Quantity:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    quantity_entry = tk.Entry(update_window, font=("Arial", 14))
    quantity_entry.pack(pady=10)
    tk.Label(update_window, text="Expiry Date (YYYY-MM-DD):", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    expiry_entry = tk.Entry(update_window, font=("Arial", 14))
    expiry_entry.pack(pady=10)
    tk.Button(update_window, text="Update", command=submit_update, font=("Arial", 14), bg="#28a745", fg="#ffffff").pack(pady=20)
    tk.Button(update_window, text="Back", command=update_window.destroy, font=("Arial", 14), bg="#dc3545", fg="#ffffff").pack(pady=20)

def delete_medicine(refresh_function):
    def submit():
        medicine_id = medicine_id_entry.get()
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Medicines WHERE medicine_id = %s", (medicine_id,))
        conn.commit()
        conn.close()
        delete_window.destroy()
        root.withdraw()
        refresh_function()
        messagebox.showinfo("Success", "Medicine deleted successfully!")

    delete_window = tk.Toplevel()
    delete_window.title("Delete Medicine")
    delete_window.attributes('-fullscreen', True)
    delete_window.configure(bg="#f0f0f0")
    tk.Label(delete_window, text="Delete Medicine", font=("Arial", 24, "bold"), bg="#f0f0f0").pack(pady=20)
    tk.Label(delete_window, text="Medicine ID:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    medicine_id_entry = tk.Entry(delete_window, font=("Arial", 14))
    medicine_id_entry.pack(pady=10)
    tk.Button(delete_window, text="Delete", command=submit, font=("Arial", 14), bg="#28a745", fg="#ffffff").pack(pady=20)
    tk.Button(delete_window, text="Back", command=delete_window.destroy, font=("Arial", 14), bg="#dc3545", fg="#ffffff").pack(pady=20)


def manage_customers():
    customers_window = tk.Toplevel()
    customers_window.title("Manage Customers")
    customers_window.attributes('-fullscreen', True)
    customers_window.configure(bg="#f0f0f0")

    frame = tk.Frame(customers_window, bg="#ffffff", padx=40, pady=40)
    frame.pack(expand=True, fill=tk.BOTH)

    global tree
    tree = ttk.Treeview(frame, columns=("ID", "Name", "Contact", "Address"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Contact", text="Contact")
    tree.heading("Address", text="Address")
    tree.pack(expand=True, fill=tk.BOTH)

    def refresh_treeview():
        for row in tree.get_children():
            tree.delete(row)
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Customers")
        customers = cursor.fetchall()
        conn.close()
        for customer in customers:
            tree.insert("", tk.END, values=customer)
    refresh_treeview()

    def create_button(text, command):
        return tk.Button(frame, text=text, command=command, font=("Arial", 14), bg="#007bff", fg="#ffffff", relief="flat", padx=10, pady=10)

    create_button("Add Customer", lambda: add_customer(refresh_treeview)).pack(pady=10, fill=tk.X)
    create_button("Update Customer", lambda: update_customer(refresh_treeview)).pack(pady=10, fill=tk.X)
    create_button("Delete Customer", lambda: delete_customer(refresh_treeview)).pack(pady=10, fill=tk.X)
    create_button("Back", command=customers_window.destroy).pack(pady=10, fill=tk.X)

def add_customer(refresh_function):
    def submit():
        name = name_entry.get()
        contact = contact_entry.get()
        address = address_entry.get()
        if not name or not contact or not address:
            messagebox.showwarning("Input Error", "All fields must be filled out.")
            return
        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Customers (name, phone, address) VALUES (%s, %s, %s)", (name, contact, address))
            conn.commit()
            messagebox.showinfo("Success", "Customer added successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
            add_window.destroy()
            root.withdraw()
            refresh_function()

    add_window = tk.Toplevel()
    add_window.title("Add Customer")
    add_window.attributes('-fullscreen', True)
    add_window.configure(bg="#f0f0f0")
    tk.Label(add_window, text="Add Customer", font=("Arial", 24, "bold"), bg="#f0f0f0").pack(pady=20)
    tk.Label(add_window, text="Name:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    name_entry = tk.Entry(add_window, font=("Arial", 14))
    name_entry.pack(pady=10)
    tk.Label(add_window, text="Contact:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    contact_entry = tk.Entry(add_window, font=("Arial", 14))
    contact_entry.pack(pady=10)
    tk.Label(add_window, text="Address:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    address_entry = tk.Entry(add_window, font=("Arial", 14))
    address_entry.pack(pady=10)
    tk.Button(add_window, text="Submit", command=submit, font=("Arial", 14), bg="#28a745", fg="#ffffff").pack(pady=20)
    tk.Button(add_window, text="Back", command=add_window.destroy, font=("Arial", 14), bg="#dc3545", fg="#ffffff").pack(pady=20)

def update_customer(refresh_function):
    def search_customer():
        customer_id = customer_id_entry.get()
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Customers WHERE customer_id = %s", (customer_id,))
        customer = cursor.fetchone()
        conn.close()
        if customer:
            name_entry.delete(0, tk.END)
            name_entry.insert(0, customer[1])
            contact_entry.delete(0, tk.END)
            contact_entry.insert(0, customer[2])
            address_entry.delete(0, tk.END)
            address_entry.insert(0, customer[3])
        else:
            messagebox.showerror("Error", "Customer ID not found!")

    def submit_update():
        customer_id = customer_id_entry.get()
        name = name_entry.get()
        contact = contact_entry.get()
        address = address_entry.get()
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Customers SET name = %s, phone = %s, address = %s WHERE customer_id = %s", (name, contact, address, customer_id))
        conn.commit()
        conn.close()
        update_window.destroy()
        root.withdraw()
        refresh_function()
        messagebox.showinfo("Success", "Customer updated successfully!")

    update_window = tk.Toplevel()
    update_window.title("Update Customer")
    update_window.attributes('-fullscreen', True)
    update_window.configure(bg="#f0f0f0")
    tk.Label(update_window, text="Update Customer", font=("Arial", 24, "bold"), bg="#f0f0f0").pack(pady=20)
    tk.Label(update_window, text="Customer ID:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    customer_id_entry = tk.Entry(update_window, font=("Arial", 14))
    customer_id_entry.pack(pady=10)
    tk.Button(update_window, text="Search", command=search_customer, font=("Arial", 14), bg="#007bff", fg="#ffffff").pack(pady=10)
    tk.Label(update_window, text="Name:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    name_entry = tk.Entry(update_window, font=("Arial", 14))
    name_entry.pack(pady=10)
    tk.Label(update_window, text="Contact:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    contact_entry = tk.Entry(update_window, font=("Arial", 14))
    contact_entry.pack(pady=10)
    tk.Label(update_window, text="Address:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    address_entry = tk.Entry(update_window, font=("Arial", 14))
    address_entry.pack(pady=10)
    tk.Button(update_window, text="Update", command=submit_update, font=("Arial", 14), bg="#28a745", fg="#ffffff").pack(pady=20)
    tk.Button(update_window, text="Back", command=update_window.destroy, font=("Arial", 14), bg="#dc3545", fg="#ffffff").pack(pady=20)

def delete_customer(refresh_function):
    def submit():
        customer_id = customer_id_entry.get()
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Customers WHERE customer_id = %s", (customer_id,))
        conn.commit()
        conn.close()
        delete_window.destroy()
        root.withdraw()
        refresh_function()
        messagebox.showinfo("Success", "Customer deleted successfully!")

    delete_window = tk.Toplevel()
    delete_window.title("Delete Customer")
    delete_window.attributes('-fullscreen', True)
    delete_window.configure(bg="#f0f0f0")
    tk.Label(delete_window, text="Delete Customer", font=("Arial", 24, "bold"), bg="#f0f0f0").pack(pady=20)
    tk.Label(delete_window, text="Customer ID:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    customer_id_entry = tk.Entry(delete_window, font=("Arial", 14))
    customer_id_entry.pack(pady=10)
    tk.Button(delete_window, text="Delete", command=submit, font=("Arial", 14), bg="#28a745", fg="#ffffff").pack(pady=20)
    tk.Button(delete_window, text="Back", command=delete_window.destroy, font=("Arial", 14), bg="#dc3545", fg="#ffffff").pack(pady=20)

def manage_sales():
    sales_window = tk.Toplevel()
    sales_window.title("Manage Sales")
    sales_window.attributes('-fullscreen', True)
    sales_window.configure(bg="#f0f0f0")

    frame = tk.Frame(sales_window, bg="#ffffff", padx=40, pady=40)
    frame.pack(expand=True, fill=tk.BOTH)

    tree = ttk.Treeview(frame, columns=("ID", "Medicine ID", "Customer ID", "Date", "Quantity Sold"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Medicine ID", text="Medicine ID")
    tree.heading("Customer ID", text="Customer ID")
    tree.heading("Date", text="Date")
    tree.heading("Quantity Sold", text="Quantity Sold")
    tree.pack(expand=True, fill=tk.BOTH)

    def refresh_treeview():
        for row in tree.get_children():
            tree.delete(row)
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Sales")
        sales = cursor.fetchall()
        conn.close()
        for sale in sales:
            tree.insert("", tk.END, values=sale)
    refresh_treeview()

    def create_button(text, command):
        return tk.Button(frame, text=text, command=command, font=("Arial", 14),
                         bg="#007bff", fg="#ffffff", relief="flat", padx=10, pady=10)

    create_button("Add Sale", lambda: add_sale(refresh_treeview)).pack(pady=10, fill=tk.X)
    create_button("Update Sale", lambda: update_sale(refresh_treeview)).pack(pady=10, fill=tk.X)
    create_button("Delete Sale", lambda: delete_sale(refresh_treeview)).pack(pady=10, fill=tk.X)
    create_button("Back", command=sales_window.destroy).pack(pady=10, fill=tk.X)

def add_sale(refresh_function):
    def submit():
        medicine_id = medicine_id_entry.get()
        customer_id = customer_id_entry.get()
        date = date_entry.get()
        quantity = quantity_entry.get()
        if not medicine_id or not customer_id or not date or not quantity:
            messagebox.showwarning("Input Error", "All fields must be filled out.")
            return
        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Sales (medicine_id, customer_id, date, quantity_sold) VALUES (%s, %s, %s, %s)",
                           (medicine_id, customer_id, date, quantity))
            conn.commit()
            messagebox.showinfo("Success", "Sale added successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
            add_window.destroy()
            root.withdraw()
            refresh_function()

    add_window = tk.Toplevel()
    add_window.title("Add Sale")
    add_window.attributes('-fullscreen', True)
    add_window.configure(bg="#f0f0f0")

    tk.Label(add_window, text="Add Sale", font=("Arial", 24, "bold"), bg="#f0f0f0").pack(pady=20)
    tk.Label(add_window, text="Customer ID:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    customer_id_entry = tk.Entry(add_window, font=("Arial", 14))
    customer_id_entry.pack(pady=10)
    tk.Label(add_window, text="Medicine ID:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    medicine_id_entry = tk.Entry(add_window, font=("Arial", 14))
    medicine_id_entry.pack(pady=10)
    tk.Label(add_window, text="Quantity:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    quantity_entry = tk.Entry(add_window, font=("Arial", 14))
    quantity_entry.pack(pady=10)
    tk.Label(add_window, text="Date (YYYY-MM-DD):", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    date_entry = tk.Entry(add_window, font=("Arial", 14))
    date_entry.pack(pady=10)
    tk.Button(add_window, text="Submit", command=submit, font=("Arial", 14), bg="#28a745", fg="#ffffff").pack(pady=20)
    tk.Button(add_window, text="Back", command=add_window.destroy, font=("Arial", 14), bg="#dc3545", fg="#ffffff").pack(pady=20)

def update_sale(refresh_function):
    def search_sale():
        sale_id = sale_id_entry.get()
        if not sale_id:
            messagebox.showwarning("Input Error", "Sale ID must be provided.")
            return

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Sales WHERE sale_id = %s", (sale_id,))
        sale = cursor.fetchone()
        conn.close()

        if sale:
            
            medicine_id_entry.delete(0, tk.END)
            medicine_id_entry.insert(0, sale[1])
            customer_id_entry.delete(0, tk.END)
            customer_id_entry.insert(0, sale[2])
            date_entry.delete(0, tk.END)
            date_entry.insert(0, sale[3])
            quantity_entry.delete(0, tk.END)
            quantity_entry.insert(0, sale[4])
        else:
            messagebox.showerror("Error", "Sale ID not found!")

    def submit_update():
        sale_id = sale_id_entry.get()
        medicine_id = medicine_id_entry.get()
        customer_id = customer_id_entry.get()
        date = date_entry.get()
        quantity = quantity_entry.get()

        if not (sale_id and medicine_id and customer_id and date and quantity):
            messagebox.showwarning("Input Error", "All fields must be filled out.")
            return

        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Sales 
                SET medicine_id = %s, customer_id = %s, date = %s, quantity_sold = %s 
                WHERE sale_id = %s
            """, (medicine_id, customer_id, date, quantity, sale_id))
            conn.commit()
            messagebox.showinfo("Success", "Sale updated successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
            update_window.destroy()
            root.withdraw()
            refresh_function()

    update_window = tk.Toplevel()
    update_window.title("Update Sale")
    update_window.attributes('-fullscreen', True)
    update_window.configure(bg="#f0f0f0")

    tk.Label(update_window, text="Update Sale", font=("Arial", 24, "bold"), bg="#f0f0f0").pack(pady=20)
    tk.Label(update_window, text="Sale ID:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    sale_id_entry = tk.Entry(update_window, font=("Arial", 14))
    sale_id_entry.pack(pady=10)
    tk.Button(update_window, text="Search", command=search_sale, font=("Arial", 14), bg="#007bff", fg="#ffffff").pack(pady=10)
    tk.Label(update_window, text="Medicine ID:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    medicine_id_entry = tk.Entry(update_window, font=("Arial", 14))
    medicine_id_entry.pack(pady=10)
    tk.Label(update_window, text="Customer ID:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    customer_id_entry = tk.Entry(update_window, font=("Arial", 14))
    customer_id_entry.pack(pady=10)
    tk.Label(update_window, text="Date (YYYY-MM-DD):", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    date_entry = tk.Entry(update_window, font=("Arial", 14))
    date_entry.pack(pady=10)
    tk.Label(update_window, text="Quantity:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    quantity_entry = tk.Entry(update_window, font=("Arial", 14))
    quantity_entry.pack(pady=10)
    tk.Button(update_window, text="Update", command=submit_update, font=("Arial", 14), bg="#28a745", fg="#ffffff").pack(pady=20)
    tk.Button(update_window, text="Back", command=update_window.destroy, font=("Arial", 14), bg="#dc3545", fg="#ffffff").pack(pady=20)


def delete_sale(refresh_function):
    def submit():
        sale_id = sale_id_entry.get()
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Sales WHERE sale_id = %s", (sale_id,))
        conn.commit()
        conn.close()
        delete_window.destroy()
        root.withdraw()
        refresh_function()
        messagebox.showinfo("Success", "Sale deleted successfully!")

    delete_window = tk.Toplevel()
    delete_window.title("Delete Sale")
    delete_window.attributes('-fullscreen', True)
    delete_window.configure(bg="#f0f0f0")

    tk.Label(delete_window, text="Delete Sale", font=("Arial", 24, "bold"), bg="#f0f0f0").pack(pady=20)
    tk.Label(delete_window, text="Sale ID:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    sale_id_entry = tk.Entry(delete_window, font=("Arial", 14))
    sale_id_entry.pack(pady=10)
    tk.Button(delete_window, text="Delete", command=submit, font=("Arial", 14), bg="#dc3545", fg="#ffffff").pack(pady=20)
    tk.Button(delete_window, text="Back", command=delete_window.destroy, font=("Arial", 14), bg="#dc3545", fg="#ffffff").pack(pady=20)



def manage_suppliers():
    suppliers_window = tk.Toplevel()
    suppliers_window.title("Manage Suppliers")
    suppliers_window.attributes('-fullscreen', True)
    suppliers_window.configure(bg="#f0f0f0")

    frame = tk.Frame(suppliers_window, bg="#ffffff", padx=40, pady=40)
    frame.pack(expand=True, fill=tk.BOTH)

    global tree 
    tree = ttk.Treeview(frame, columns=("ID", "Name", "Contact", "Address"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Contact", text="Contact")
    tree.heading("Address", text="Address")
    tree.pack(expand=True, fill=tk.BOTH)

    load_suppliers()

    def create_button(text, command):
        return tk.Button(frame, text=text, command=command, font=("Arial", 14),
                         bg="#007bff", fg="#ffffff", relief="flat", padx=10, pady=10)

    create_button("Add Supplier", add_supplier).pack(pady=10, fill=tk.X)
    create_button("Update Supplier", update_supplier).pack(pady=10, fill=tk.X)
    create_button("Delete Supplier", delete_supplier).pack(pady=10, fill=tk.X)
    create_button("Back", suppliers_window.destroy).pack(pady=10, fill=tk.X)

def load_suppliers():
    for item in tree.get_children():
        tree.delete(item)

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Suppliers")
    suppliers = cursor.fetchall()
    conn.close()

    for supplier in suppliers:
        tree.insert("", tk.END, values=supplier)

def add_supplier():
    def submit():
        name = name_entry.get()
        contact = contact_entry.get()
        address = address_entry.get()

        if not name or not contact or not address:
            messagebox.showwarning("Input Error", "All fields must be filled out.")
            return

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Suppliers (name, contact, address) VALUES (%s, %s, %s)",
                       (name, contact, address))
        conn.commit()
        conn.close()
        add_window.destroy()
        root.withdraw()
        load_suppliers() 
        messagebox.showinfo("Success", "Supplier added successfully!")

    add_window = tk.Toplevel()
    add_window.title("Add Supplier")
    add_window.attributes('-fullscreen', True)
    add_window.configure(bg="#f0f0f0")

    tk.Label(add_window, text="Add Supplier", font=("Arial", 24, "bold"), bg="#f0f0f0").pack(pady=20)

    tk.Label(add_window, text="Name:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    name_entry = tk.Entry(add_window, font=("Arial", 14))
    name_entry.pack(pady=10)

    tk.Label(add_window, text="Contact:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    contact_entry = tk.Entry(add_window, font=("Arial", 14))
    contact_entry.pack(pady=10)

    tk.Label(add_window, text="Address:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    address_entry = tk.Entry(add_window, font=("Arial", 14))
    address_entry.pack(pady=10)

    tk.Button(add_window, text="Submit", command=submit, font=("Arial", 14), bg="#28a745", fg="#ffffff").pack(pady=20)
    tk.Button(add_window, text="Back", command=add_window.destroy, font=("Arial", 14), bg="#dc3545", fg="#ffffff").pack(pady=20)

def update_supplier():
    def search_supplier():
        supplier_id = supplier_id_entry.get()

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Suppliers WHERE supplier_id = %s", (supplier_id,))
        supplier = cursor.fetchone()
        conn.close()

        if supplier:
            name_entry.delete(0, tk.END)
            name_entry.insert(0, supplier[1])  
            contact_entry.delete(0, tk.END)
            contact_entry.insert(0, supplier[2])  
            address_entry.delete(0, tk.END)
            address_entry.insert(0, supplier[3])  
        else:
            messagebox.showerror("Error", "Supplier ID not found!")

    def submit_update():
        supplier_id = supplier_id_entry.get()
        name = name_entry.get()
        contact = contact_entry.get()
        address = address_entry.get()

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Suppliers SET name = %s, contact = %s, address = %s WHERE supplier_id = %s",
                       (name, contact, address, supplier_id))
        conn.commit()
        conn.close()
        update_window.destroy()
        root.withdraw()
        load_suppliers()  
        messagebox.showinfo("Success", "Supplier updated successfully!")

    update_window = tk.Toplevel()
    update_window.title("Update Supplier")
    update_window.attributes('-fullscreen', True)
    update_window.configure(bg="#f0f0f0")

    tk.Label(update_window, text="Update Supplier", font=("Arial", 24, "bold"), bg="#f0f0f0").pack(pady=20)

    tk.Label(update_window, text="Supplier ID:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    supplier_id_entry = tk.Entry(update_window, font=("Arial", 14))
    supplier_id_entry.pack(pady=10)

    tk.Button(update_window, text="Search", command=search_supplier, font=("Arial", 14), bg="#007bff", fg="#ffffff").pack(pady=10)

    tk.Label(update_window, text="Name:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    name_entry = tk.Entry(update_window, font=("Arial", 14))
    name_entry.pack(pady=10)

    tk.Label(update_window, text="Contact:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    contact_entry = tk.Entry(update_window, font=("Arial", 14))
    contact_entry.pack(pady=10)

    tk.Label(update_window, text="Address:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    address_entry = tk.Entry(update_window, font=("Arial", 14))
    address_entry.pack(pady=10)

    tk.Button(update_window, text="Update", command=submit_update, font=("Arial", 14), bg="#28a745", fg="#ffffff").pack(pady=20)
    tk.Button(update_window, text="Back", command=update_window.destroy, font=("Arial", 14), bg="#dc3545", fg="#ffffff").pack(pady=20)

def delete_supplier():
    def submit():
        supplier_id = supplier_id_entry.get()

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Suppliers WHERE supplier_id = %s", (supplier_id,))
        conn.commit()
        conn.close()
        delete_window.destroy()
        root.withdraw()
        load_suppliers()  
        messagebox.showinfo("Success", "Supplier deleted successfully!")

    delete_window = tk.Toplevel()
    delete_window.title("Delete Supplier")
    delete_window.attributes('-fullscreen', True)
    delete_window.configure(bg="#f0f0f0")

    tk.Label(delete_window, text="Delete Supplier", font=("Arial", 24, "bold"), bg="#f0f0f0").pack(pady=20)

    tk.Label(delete_window, text="Supplier ID:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    supplier_id_entry = tk.Entry(delete_window, font=("Arial", 14))
    supplier_id_entry.pack(pady=10)

    tk.Button(delete_window, text="Delete", command=submit, font=("Arial", 14), bg="#28a745", fg="#ffffff").pack(pady=20)
    tk.Button(delete_window, text="Back", command=delete_window.destroy, font=("Arial", 14), bg="#dc3545", fg="#ffffff").pack(pady=20)


def manage_employees():
    employees_window = tk.Toplevel()
    employees_window.title("Manage Employees")
    employees_window.attributes('-fullscreen', True)
    employees_window.configure(bg="#f0f0f0")
    frame = tk.Frame(employees_window, bg="#ffffff", padx=40, pady=40)
    frame.pack(expand=True, fill=tk.BOTH)
    global tree
    tree = ttk.Treeview(frame, columns=("ID", "Name", "Role", "Password", "Salary"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Role", text="Role")
    tree.heading("Password", text="Password")
    tree.heading("Salary", text="Salary")
    tree.pack(expand=True, fill=tk.BOTH)
    load_employees()

    def create_button(text, command):
        return tk.Button(frame, text=text, command=command, font=("Arial", 14),
                         bg="#007bff", fg="#ffffff", relief="flat", padx=10, pady=10)

    create_button("Add Employee", add_employee).pack(pady=10, fill=tk.X)
    create_button("Update Employee", update_employee).pack(pady=10, fill=tk.X)
    create_button("Delete Employee", delete_employee).pack(pady=10, fill=tk.X)
    create_button("Back", employees_window.destroy).pack(pady=10, fill=tk.X)

def load_employees():
    for item in tree.get_children():
        tree.delete(item)
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Employees")
    employees = cursor.fetchall()
    conn.close()
    for employee in employees:
        tree.insert("", tk.END, values=employee)

def add_employee():
    def submit():
        name = name_entry.get()
        role = role_entry.get()
        password = password_entry.get()
        salary = salary_entry.get()
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Employees (name, role, password, salary) VALUES (%s, %s, %s, %s)",
                       (name, role, password, salary))
        conn.commit()
        conn.close()
        add_window.destroy()
        root.withdraw()
        load_employees()
        messagebox.showinfo("Success", "Employee added successfully!")
    add_window = tk.Toplevel()
    add_window.title("Add Employee")
    add_window.attributes('-fullscreen', True)
    add_window.configure(bg="#f0f0f0")
    tk.Label(add_window, text="Name:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    name_entry = tk.Entry(add_window, font=("Arial", 14))
    name_entry.pack(pady=10)
    tk.Label(add_window, text="Role:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    role_entry = tk.Entry(add_window, font=("Arial", 14))
    role_entry.pack(pady=10)
    tk.Label(add_window, text="Password:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    password_entry = tk.Entry(add_window, show="*", font=("Arial", 14))
    password_entry.pack(pady=10)
    tk.Label(add_window, text="Salary:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    salary_entry = tk.Entry(add_window, font=("Arial", 14))
    salary_entry.pack(pady=10)
    tk.Button(add_window, text="Submit", command=submit, font=("Arial", 14), bg="#28a745", fg="#ffffff").pack(pady=20)
    tk.Button(add_window, text="Back", command=add_window.destroy, font=("Arial", 14), bg="#dc3545", fg="#ffffff").pack(pady=20)

def update_employee():
    def search_employee():
        employee_id = employee_id_entry.get()
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Employees WHERE employee_id = %s", (employee_id,))
        employee = cursor.fetchone()
        conn.close()
        if employee:
            name_entry.delete(0, tk.END)
            name_entry.insert(0, employee[1])
            role_entry.delete(0, tk.END)
            role_entry.insert(0, employee[2])
            password_entry.delete(0, tk.END)
            password_entry.insert(0, employee[3])
            salary_entry.delete(0, tk.END)
            salary_entry.insert(0, employee[4])
        else:
            messagebox.showerror("Error", "Employee ID not found!")

    def submit_update():
        employee_id = employee_id_entry.get()
        name = name_entry.get()
        role = role_entry.get()
        password = password_entry.get()
        salary = salary_entry.get()
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Employees SET name = %s, role = %s, password = %s, salary = %s WHERE employee_id = %s",
                       (name, role, password, salary, employee_id))
        conn.commit()
        conn.close()
        update_window.destroy()
        root.withdraw()
        load_employees()
        messagebox.showinfo("Success", "Employee updated successfully!")
    update_window = tk.Toplevel()
    update_window.title("Update Employee")
    update_window.attributes('-fullscreen', True)
    update_window.configure(bg="#f0f0f0")
    tk.Label(update_window, text="Employee ID:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    employee_id_entry = tk.Entry(update_window, font=("Arial", 14))
    employee_id_entry.pack(pady=10)
    tk.Button(update_window, text="Search", command=search_employee, font=("Arial", 14), bg="#007bff", fg="#ffffff").pack(pady=10)
    tk.Label(update_window, text="Name:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    name_entry = tk.Entry(update_window, font=("Arial", 14))
    name_entry.pack(pady=10)
    tk.Label(update_window, text="Role:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    role_entry = tk.Entry(update_window, font=("Arial", 14))
    role_entry.pack(pady=10)
    tk.Label(update_window, text="Password:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    password_entry = tk.Entry(update_window, show="*", font=("Arial", 14))
    password_entry.pack(pady=10)
    tk.Label(update_window, text="Salary:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    salary_entry = tk.Entry(update_window, font=("Arial", 14))
    salary_entry.pack(pady=10)
    tk.Button(update_window, text="Update", command=submit_update, font=("Arial", 14), bg="#28a745", fg="#ffffff").pack(pady=20)
    tk.Button(update_window, text="Back", command=update_window.destroy, font=("Arial", 14), bg="#dc3545", fg="#ffffff").pack(pady=20)

def delete_employee():
    def submit():
        employee_id = employee_id_entry.get()
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Employees WHERE employee_id = %s", (employee_id,))
        conn.commit()
        conn.close()
        delete_window.destroy()
        root.withdraw()
        load_employees()
        messagebox.showinfo("Success", "Employee deleted successfully!")
    delete_window = tk.Toplevel()
    delete_window.title("Delete Employee")
    delete_window.attributes('-fullscreen', True)
    delete_window.configure(bg="#f0f0f0")
    tk.Label(delete_window, text="Employee ID:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
    employee_id_entry = tk.Entry(delete_window, font=("Arial", 14))
    employee_id_entry.pack(pady=10)
    tk.Button(delete_window, text="Delete", command=submit, font=("Arial", 14), bg="#28a745", fg="#ffffff").pack(pady=20)
    tk.Button(delete_window, text="Back", command=delete_window.destroy, font=("Arial", 14), bg="#dc3545", fg="#ffffff").pack(pady=20)

root = tk.Tk()
root.title("Pharmacy Management Login")
root.state('zoomed')
root.configure(bg="#f0f0f0")
frame = tk.Frame(root, bg="#ffffff", padx=40, pady=40)
frame.pack(expand=True)
title_label = tk.Label(frame, text="PHARMACY MANAGEMENT SYSTEM", font=("Arial", 40, "bold"), bg="#ffffff")
title_label.pack(pady=20)
admin_button = tk.Button(frame, text="Admin", command=lambda: prompt_password("Admin"), font=("Arial", 25),
                         bg="#007bff", fg="#ffffff", relief="flat", padx=10, pady=10)
admin_button.pack(pady=20)
employee_button = tk.Button(frame, text="Employee", command=lambda: prompt_password("Employee"), font=("Arial", 25),
                            bg="#28a745", fg="#ffffff", relief="flat", padx=10, pady=10)
employee_button.pack(pady=20)
footer_label = tk.Label(frame, text="Please select your role to continue.", font=("Arial", 16), bg="#ffffff")
footer_label.pack(pady=10)
root.mainloop()
