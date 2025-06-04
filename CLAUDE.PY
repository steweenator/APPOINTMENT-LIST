import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
import re
import json
from datetime import datetime, date
import os

class ModernPatientAppointmentSystem:
    def __init__(self):
        self.appointments = []
        self.setup_gui()
        self.load_data()

    def setup_gui(self):
        # Main window setup
        self.root = tk.Tk()
        self.root.title("Patient Appointment Management System")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Custom colors
        self.colors = {
            'primary': '#2563eb',
            'secondary': '#64748b',
            'success': '#16a34a',
            'danger': '#dc2626',
            'background': '#ffffff',
            'light_gray': '#f8fafc'
        }
        
        self.create_header()
        self.create_notebook()
        self.create_footer()
        
    def create_header(self):
        # Header frame
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header_frame.pack(fill='x', pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            header_frame, 
            text="🏥 Patient Appointment System",
            font=('Arial', 24, 'bold'),
            fg='white',
            bg=self.colors['primary']
        )
        title_label.pack(expand=True)
        
    def create_notebook(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Create tabs
        self.create_add_appointment_tab()
        self.create_view_appointments_tab()
        self.create_search_tab()
        
    def create_add_appointment_tab(self):
        # Add Appointment Tab
        add_frame = ttk.Frame(self.notebook)
        self.notebook.add(add_frame, text="➕ Add Appointment")
        
        # Main container with padding
        container = tk.Frame(add_frame, bg='white', relief='raised', bd=1)
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title = tk.Label(
            container, 
            text="New Patient Appointment",
            font=('Arial', 18, 'bold'),
            bg='white',
            fg=self.colors['primary']
        )
        title.pack(pady=(20, 30))
        
        # Form frame
        form_frame = tk.Frame(container, bg='white')
        form_frame.pack(expand=True, fill='both', padx=40)
        
        # Form fields
        self.create_form_field(form_frame, "Patient Name:", "name_var", 0)
        self.create_procedure_field(form_frame, "Procedure:", "procedure_var", 1)
        self.create_form_field(form_frame, "Phone Number:", "phone_var", 2)
        self.create_form_field(form_frame, "Clinic/Hospital:", "clinic_var", 3)
        
        # Date field with calendar
        tk.Label(
            form_frame, 
            text="Appointment Date:",
            font=('Arial', 12, 'bold'),
            bg='white',
            anchor='w'
        ).grid(row=4, column=0, sticky='w', pady=(15, 5))
        
        self.date_entry = DateEntry(
            form_frame,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            font=('Arial', 11),
            mindate=date.today()
        )
        self.date_entry.grid(row=4, column=1, sticky='ew', pady=(15, 5))
        
        # Configure grid weights
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Buttons frame
        button_frame = tk.Frame(container, bg='white')
        button_frame.pack(pady=30)
        
        # Add appointment button
        add_btn = tk.Button(
            button_frame,
            text="💾 Save Appointment",
            command=self.add_appointment,
            bg=self.colors['success'],
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=30,
            pady=10,
            relief='flat',
            cursor='hand2'
        )
        add_btn.pack(side='left', padx=10)
        
        # Clear form button
        clear_btn = tk.Button(
            button_frame,
            text="🗑️ Clear Form",
            command=self.clear_form,
            bg=self.colors['secondary'],
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=30,
            pady=10,
            relief='flat',
            cursor='hand2'
        )
        clear_btn.pack(side='left', padx=10)
        
    def create_form_field(self, parent, label_text, var_name, row):
        # Label
        tk.Label(
            parent, 
            text=label_text,
            font=('Arial', 12, 'bold'),
            bg='white',
            anchor='w'
        ).grid(row=row, column=0, sticky='w', pady=(15, 5))
        
        # Entry
        var = tk.StringVar()
        setattr(self, var_name, var)
        
        entry = tk.Entry(
            parent,
            textvariable=var,
            font=('Arial', 11),
            relief='solid',
            bd=1,
            bg='#f8fafc'
        )
    def create_procedure_field(self, parent, label_text, var_name, row):
        # Label
        tk.Label(
            parent, 
            text=label_text,
            font=('Arial', 12, 'bold'),
            bg='white',
            anchor='w'
        ).grid(row=row, column=0, sticky='w', pady=(15, 5))
        
        # Dropdown for procedures
        var = tk.StringVar()
        setattr(self, var_name, var)
        
        procedures = [
            "Computed Tomography (CT)",
            "X-ray (DX)", 
            "Ultrasound (US)",
            "Mammogram (MG)"
        ]
        
        dropdown = ttk.Combobox(
            parent,
            textvariable=var,
            values=procedures,
            state="readonly",
            font=('Arial', 11),
            width=25
        )
        dropdown.grid(row=row, column=1, sticky='ew', pady=(15, 5), ipady=8)
        dropdown.set("Select Procedure")  # Default text
        
    def create_view_appointments_tab(self):
        # View Appointments Tab
        view_frame = ttk.Frame(self.notebook)
        self.notebook.add(view_frame, text="📋 View Appointments")
        
        # Container
        container = tk.Frame(view_frame, bg='white', relief='raised', bd=1)
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title and controls frame
        title_frame = tk.Frame(container, bg='white')
        title_frame.pack(fill='x', padx=20, pady=(20, 10))
        
        tk.Label(
            title_frame,
            text="All Appointments",
            font=('Arial', 18, 'bold'),
            bg='white',
            fg=self.colors['primary']
        ).pack(side='left')
        
        # Refresh button
        refresh_btn = tk.Button(
            title_frame,
            text="🔄 Refresh",
            command=self.refresh_appointments,
            bg=self.colors['primary'],
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=5,
            relief='flat',
            cursor='hand2'
        )
        refresh_btn.pack(side='right')
        
        # Treeview for appointments
        tree_frame = tk.Frame(container, bg='white')
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side='right', fill='y')
        
        # Treeview
        self.appointments_tree = ttk.Treeview(
            tree_frame,
            columns=('ID', 'Name', 'Procedure', 'Phone', 'Clinic', 'Date'),
            show='headings',
            yscrollcommand=scrollbar.set
        )
        
        # Configure scrollbar
        scrollbar.config(command=self.appointments_tree.yview)
        
        # Define columns
        columns = [
            ('ID', 50),
            ('Name', 150),
            ('Procedure', 150),
            ('Phone', 120),
            ('Clinic', 150),
            ('Date', 100)
        ]
        
        for col, width in columns:
            self.appointments_tree.heading(col, text=col)
            self.appointments_tree.column(col, width=width, anchor='center')
        
        self.appointments_tree.pack(fill='both', expand=True)
        
        # Delete button
        delete_btn = tk.Button(
            container,
            text="🗑️ Delete Selected",
            command=self.delete_appointment,
            bg=self.colors['danger'],
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=20,
            pady=8,
            relief='flat',
            cursor='hand2'
        )
        delete_btn.pack(pady=20)
        
    def create_search_tab(self):
        # Search Tab
        search_frame = ttk.Frame(self.notebook)
        self.notebook.add(search_frame, text="🔍 Search")
        
        # Container
        container = tk.Frame(search_frame, bg='white', relief='raised', bd=1)
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title = tk.Label(
            container,
            text="Search Appointments",
            font=('Arial', 18, 'bold'),
            bg='white',
            fg=self.colors['primary']
        )
        title.pack(pady=(20, 30))
        
        # Search frame
        search_input_frame = tk.Frame(container, bg='white')
        search_input_frame.pack(pady=10)
        
        tk.Label(
            search_input_frame,
            text="Search by Name or Phone:",
            font=('Arial', 12, 'bold'),
            bg='white'
        ).pack(side='left', padx=(0, 10))
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_input_frame,
            textvariable=self.search_var,
            font=('Arial', 11),
            width=30,
            relief='solid',
            bd=1
        )
        search_entry.pack(side='left', padx=(0, 10), ipady=5)
        
        search_btn = tk.Button(
            search_input_frame,
            text="🔍 Search",
            command=self.search_appointments,
            bg=self.colors['primary'],
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=5,
            relief='flat',
            cursor='hand2'
        )
        search_btn.pack(side='left')
        
        # Search results
        results_frame = tk.Frame(container, bg='white')
        results_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Results treeview
        results_scrollbar = ttk.Scrollbar(results_frame)
        results_scrollbar.pack(side='right', fill='y')
        
        self.search_tree = ttk.Treeview(
            results_frame,
            columns=('ID', 'Name', 'Procedure', 'Phone', 'Clinic', 'Date'),
            show='headings',
            yscrollcommand=results_scrollbar.set
        )
        
        results_scrollbar.config(command=self.search_tree.yview)
        
        for col, width in columns:
            self.search_tree.heading(col, text=col)
            self.search_tree.column(col, width=width, anchor='center')
        
        self.search_tree.pack(fill='both', expand=True)
        
    def create_footer(self):
        # Footer
        footer_frame = tk.Frame(self.root, bg=self.colors['light_gray'], height=50)
        footer_frame.pack(fill='x', side='bottom')
        footer_frame.pack_propagate(False)
        
        # Export/Import buttons
        button_frame = tk.Frame(footer_frame, bg=self.colors['light_gray'])
        button_frame.pack(expand=True)
        
        export_btn = tk.Button(
            button_frame,
            text="📤 Export Data",
            command=self.export_data,
            bg=self.colors['secondary'],
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=15,
            pady=5,
            relief='flat',
            cursor='hand2'
        )
        export_btn.pack(side='left', padx=10)
        
        import_btn = tk.Button(
            button_frame,
            text="📥 Import Data",
            command=self.import_data,
            bg=self.colors['secondary'],
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=15,
            pady=5,
            relief='flat',
            cursor='hand2'
        )
        import_btn.pack(side='left', padx=10)
        
    def validate_phone(self, phone):
        phone = re.sub(r'[\s\-\(\)]', '', phone)
        return re.match(r'^\+?\d{10,15}$', phone) is not None
        
    def add_appointment(self):
        # Validate inputs
        name = self.name_var.get().strip()
        procedure = self.procedure_var.get().strip()
        phone = self.phone_var.get().strip()
        clinic = self.clinic_var.get().strip()
        appointment_date = self.date_entry.get_date()
        
        if not all([name, procedure, phone, clinic]) or procedure == "Select Procedure":
            messagebox.showerror("Error", "Please fill in all fields and select a procedure!")
            return
            
        if not self.validate_phone(phone):
            messagebox.showerror("Error", "Please enter a valid phone number!")
            return
            
        # Create appointment
        appointment = {
            'id': len(self.appointments) + 1,
            'patient_name': name,
            'procedure': procedure,
            'phone_number': phone,
            'clinic': clinic,
            'appointment_date': appointment_date.strftime('%Y-%m-%d'),
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        self.appointments.append(appointment)
        self.save_data()
        self.refresh_appointments()
        self.clear_form()
        
        messagebox.showinfo("Success", f"Appointment saved successfully!\nID: {appointment['id']}")
        
    def clear_form(self):
        self.name_var.set("")
        self.procedure_var.set("Select Procedure")
        self.phone_var.set("")
        self.clinic_var.set("")
        self.date_entry.set_date(date.today())
        
    def refresh_appointments(self):
        # Clear existing items
        for item in self.appointments_tree.get_children():
            self.appointments_tree.delete(item)
            
        # Add appointments
        for apt in self.appointments:
            self.appointments_tree.insert('', 'end', values=(
                apt['id'],
                apt['patient_name'],
                apt['procedure'],
                apt['phone_number'],
                apt['clinic'],
                apt['appointment_date']
            ))
            
    def delete_appointment(self):
        selected = self.appointments_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an appointment to delete!")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this appointment?"):
            item = self.appointments_tree.item(selected[0])
            apt_id = int(item['values'][0])
            
            self.appointments = [apt for apt in self.appointments if apt['id'] != apt_id]
            self.save_data()
            self.refresh_appointments()
            messagebox.showinfo("Success", "Appointment deleted successfully!")
            
    def search_appointments(self):
        search_term = self.search_var.get().strip().lower()
        if not search_term:
            messagebox.showwarning("Warning", "Please enter a search term!")
            return
            
        # Clear existing search results
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)
            
        # Search and display results
        results = []
        for apt in self.appointments:
            if (search_term in apt['patient_name'].lower() or 
                search_term in apt['phone_number']):
                results.append(apt)
                
        if results:
            for apt in results:
                self.search_tree.insert('', 'end', values=(
                    apt['id'],
                    apt['patient_name'],
                    apt['procedure'],
                    apt['phone_number'],
                    apt['clinic'],
                    apt['appointment_date']
                ))
            messagebox.showinfo("Search Results", f"Found {len(results)} matching appointment(s)!")
        else:
            messagebox.showinfo("Search Results", "No matching appointments found!")
            
    def save_data(self):
        try:
            with open('appointments.json', 'w') as f:
                json.dump(self.appointments, f, indent=2, default=str)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")
            
    def load_data(self):
        try:
            if os.path.exists('appointments.json'):
                with open('appointments.json', 'r') as f:
                    self.appointments = json.load(f)
                self.refresh_appointments()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
            
    def export_data(self):
        if not self.appointments:
            messagebox.showwarning("Warning", "No appointments to export!")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(self.appointments, f, indent=2, default=str)
                messagebox.showinfo("Success", f"Data exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export data: {str(e)}")
                
    def import_data(self):
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    imported_data = json.load(f)
                    
                if messagebox.askyesno("Confirm", "This will replace all current data. Continue?"):
                    self.appointments = imported_data
                    self.save_data()
                    self.refresh_appointments()
                    messagebox.showinfo("Success", "Data imported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import data: {str(e)}")
                
    def run(self):
        self.root.mainloop()

# Run the application
if __name__ == "__main__":
    # Note: You'll need to install tkcalendar for the date picker
    # pip install tkcalendar
    
    app = ModernPatientAppointmentSystem()
    app.run()
