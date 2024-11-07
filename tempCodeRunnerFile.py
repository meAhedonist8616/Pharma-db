def manage_customers():
    customers_window = tk.Toplevel()
    customers_window.title("Manage Customers")
    customers_window.attributes('-fullscreen', True)  
    
    tree = ttk.Treeview(customers_window, columns=("ID", "Name", "Contact", "Address"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Contact", text="Contact")
    tree.heading("Address", text="Address")
    tree.pack(expand=True)

   
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

    tk.Button(customers_window, text="Add Customer", command=lambda: add_customer(refresh_treeview)).pack(expand=True)
    tk.Button(customers_window, text="Update Customer", command=lambda: update_customer(refresh_treeview)).pack(expand=True)
    tk.Button(customers_window, text="Delete Customer", command=lambda: delete_customer(refresh_treeview)).pack(expand=True)
    tk.Button(customers_window, text="Back", command=customers_window.destroy).pack(expand=True)

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
            cursor.execute("INSERT INTO Customers (name, phone, address) VALUES (%s, %s, %s)",
                           (name, contact, address))
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

    tk.Label(add_window, text="Name:", font=("Arial", 14)).pack(pady=10)
    name_entry = tk.Entry(add_window, font=("Arial", 14))
    name_entry.pack(pady=10)

    tk.Label(add_window, text="Contact:", font=("Arial", 14)).pack(pady=10)
    contact_entry = tk.Entry(add_window, font=("Arial", 14))
    contact_entry.pack(pady=10)

    tk.Label(add_window, text="Address:", font=("Arial", 14)).pack(pady=10)
    address_entry = tk.Entry(add_window, font=("Arial", 14))
    address_entry.pack(pady=10)

    tk.Button(add_window, text="Submit", command=submit, font=("Arial", 14)).pack(pady=20)
    tk.Button(add_window, text="Back", command=add_window.destroy, font=("Arial", 14)).pack(pady=20)
    
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
        cursor.execute("UPDATE Customers SET name = %s, phone = %s, address = %s WHERE customer_id = %s",
                       (name, contact, address, customer_id))
        conn.commit()
        conn.close()
        update_window.destroy()
        root.withdraw()
        refresh_function()
        messagebox.showinfo("Success", "Customer updated successfully!")
         

    update_window = tk.Toplevel()
    update_window.title("Update Customer")
    update_window.attributes('-fullscreen', True)  

    tk.Label(update_window, text="Customer ID:", font=("Arial", 14)).pack(pady=10)
    customer_id_entry = tk.Entry(update_window, font=("Arial", 14))
    customer_id_entry.pack(pady=10)

    tk.Button(update_window, text="Search", command=search_customer, font=("Arial", 14)).pack(pady=10)

    tk.Label(update_window, text="Name:", font=("Arial", 14)).pack(pady=10)
    name_entry = tk.Entry(update_window, font=("Arial", 14))
    name_entry.pack(pady=10)

    tk.Label(update_window, text="Contact:", font=("Arial", 14)).pack(pady=10)
    contact_entry = tk.Entry(update_window, font=("Arial", 14))
    contact_entry.pack(pady=10)

    tk.Label(update_window, text="Address:", font=("Arial", 14)).pack(pady=10)
    address_entry = tk.Entry(update_window, font=("Arial", 14))
    address_entry.pack(pady=10)

    tk.Button(update_window, text="Update", command=submit_update, font=("Arial", 14)).pack(pady=20)
    tk.Button(update_window, text="Back", command=update_window.destroy, font=("Arial", 14)).pack(pady=20)
    
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
    
    tk.Label(delete_window, text="Customer ID:", font=("Arial", 14)).pack(pady=10)
    customer_id_entry = tk.Entry(delete_window, font=("Arial", 14))
    customer_id_entry.pack(pady=10)

    tk.Button(delete_window, text="Delete", command=submit, font=("Arial", 14)).pack(pady=20)
    tk.Button(delete_window, text="Back", command=delete_window.destroy, font=("Arial", 14)).pack(pady=20)