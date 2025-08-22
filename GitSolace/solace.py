import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
from tkinter import filedialog as fd
import customtkinter as ctk
import datetime, bcrypt, subprocess, sqlite3, platform, json, os
from datetime import datetime
import webbrowser


conn = sqlite3.connect('farm.db')
c = conn.cursor()

SESSION_FILE = "session.json"

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

__version__ = 1.0
my_url = 'https://github.com/soldiers-son/solace-your-farming-companion'

### Functions
def show_frame(frame):
    frame.tkraise()

def save_session(username):
    with open(SESSION_FILE, "w") as f:
        json.dump({"username": username}, f)

def load_session():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            data = json.load(f)
            return data.get("username")
    return None

def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

def validation_login():
    global current_user
    U = userl.get()
    P = passwordl.get()

    # check for empty fields first
    if len(U) == 0:
        messagebox.showerror("ERROR", "Please enter a Username.")
        return
    if len(P) == 0:
        messagebox.showerror("ERROR", "Please enter a Password.")
        return

    # query only for the username
    find_user = 'SELECT password_hash FROM users WHERE username = ?'
    c.execute(find_user, (U,))
    result = c.fetchone()

    if result:
        stored_hash = result[0]  # this should already be bytes
        if bcrypt.checkpw(P.encode(), stored_hash):
            current_user = U
            save_session(U)
            userl.delete(0, 'end')
            passwordl.delete(0, 'end')
            messagebox.showinfo("Welcome", f"Welcome back, {U}.")
            show_frame(main)
        else:
            messagebox.showerror("ERROR", "Invalid password.")
    else:
        messagebox.showerror("ERROR", "Username not found.")

    # clear input fields after any attempt
    userl.delete(0, 'end')
    passwordl.delete(0, 'end')

def logout():
    global current_user
    current_user = None
    clear_session()
    show_frame(login)
    
def create_user():
    find_user = 'SELECT * FROM users WHERE username = ?'
    find_password = 'SELECT * FROM users WHERE password_hash = ?'
    c.execute(find_user, [(userc.get())])
    c.execute(find_password, [(passwordc.get())])
    result=c.fetchall()
    if(len(userc.get()) == 0):
            messagebox.showerror(
                "ERROR", "Please enter a Username.")
    elif(len(passwordc.get()) == 0):
            messagebox.showerror(
                "ERROR", "Please enter a Password.")
    elif result:
         passwordc.delete(0, END)
         messagebox.showerror(
                "ERROR", "Password already exists.")
    else:
        N =userc.get()
        P =passwordc.get()
        hashed = bcrypt.hashpw(P.encode(), bcrypt.gensalt())
        c.execute("""
              INSERT INTO users(username, password_hash)
              VALUES(?,?)
              """, (N, hashed))
        conn.commit()
        userc.delete(0, END)
        passwordc.delete(0, END)
        show_frame(login)
        messagebox.showinfo('Congrats!', 'Account Created!')
### END


### Menu Bar Items
def open_weight_converter():

    if not current_user:
        messagebox.showerror('Error', 'Please login to use tools.')
        return

    def pounds_to_kilograms(Pounds):
        KG = Pounds * 0.453592
        return KG
    def kilograms_to_pounds(Kg_weight):
        pounds = Kg_weight / 0.453592
        return pounds

    def grams_to_kilograms(weight_in_grams):
        KG = weight_in_grams / 1000
        return KG

    def kilograms_to_grams(Kg_weight):
        grams = Kg_weight * 1000
        return grams

    def grams_to_pounds(grams):
        pounds = grams * 0.00220462
        return pounds
    
    def convert_weight():
        choice = choice_var.get()
        input_value = float(entry.get())

        if choice == 1:
            result = pounds_to_kilograms(input_value)
            result_label.configure(text=f"{input_value}lb = {result:.2f}kg.")
        elif choice == 2:
            result = kilograms_to_pounds(input_value)
            result_label.configure(text=f"{input_value}kg = {result:.2f}lb.")
        elif choice == 3:
            result = grams_to_kilograms(input_value)
            result_label.configure(text=f"{input_value}g = {result:.2f}kg.")
        elif choice == 4:
            result = kilograms_to_grams(input_value)
            result_label.configure(text=f"{input_value}kg = {result:.2f}g.") 
        elif choice == 5:
            result = grams_to_pounds(input_value)
            result_label.configure(text=f"{input_value}g = {result:.2f}lb.") 
        else:
            result_label.configure(text="Invalid choice. Please select valid choice.")


    converter_window = tk.Toplevel(root, bg='SteelBlue')
    converter_window.title('Weight Conversion')
    converter_window.geometry('300x425')
    choice_var = tk.IntVar()
    choice_var.set(1)
    label = ctk.CTkLabel(converter_window, font=("Default", 16, "bold"), text="Select Conversion:")
    label.grid(row=0, column=0, columnspan=2, pady=10)

    conversion_choices = [
    ("Pounds to Kilograms", 1),
    ("Kilograms to Pounds", 2),
    ("Grams to Kilograms", 3),
    ("Kilograms to Grams", 4),
    ("Grams to Pounds", 5)
    ]
    for i, (text, val) in enumerate(conversion_choices , 1):
        ctk.CTkRadioButton(converter_window, text=text, variable=choice_var, value=val).grid(row=i, column=0, columnspan=2, sticky=tk.W)

    entry_label = ctk.CTkLabel(converter_window, font=("Default", 16, "bold"), text="Enter weight:")
    entry_label.grid(row=len(conversion_choices ) + 1, column=0, pady=5)

    entry = ctk.CTkEntry(converter_window)
    entry.grid(row=len(conversion_choices ) + 1, column=1, pady=5)

    convert_button = ttk.Button(converter_window, text="Convert", command=convert_weight)
    convert_button.grid(row=len(conversion_choices ) + 2, column=0, columnspan=2, pady=5)

    result_label = ctk.CTkLabel(converter_window, text="")
    result_label.grid(row=len(conversion_choices ) + 3, column=0, columnspan=2, pady=5)

    for child in converter_window.winfo_children():
        child.grid_configure(padx=5, pady=10)

def show_about():
        info = ("Project: 🌿Solace - Your Farming Companion\n"
                f"Version: {__version__}\n"
                "Author: soldiers_son\n"
                "Github: https://github.com/soldiers-son\n\n")
        messagebox.showinfo("About", info)

def open_file():
    system = platform.system()
    txt_path = os.path.abspath("READ_ME.txt")

    if system == "Windows":
        if os.path.exists(txt_path):
            os.startfile(txt_path)
        else:
            messagebox.showerror('Error', 'File does not exist.')

    elif system == "Linux":
        if os.path.exists(txt_path):
            os.startfile(txt_path)
        else:
            messagebox.showerror('Error', 'File does not exist.')

    elif system == "Darwin":
        if os.path.exists(txt_path):
            os.startfile(txt_path)
        else:
            messagebox.showerror('Error', 'File does not exist.')
    else:
        raise RuntimeError(f"Unsupported OS: {system}")

def open_source():
    webbrowser.open_new(my_url)

def show_plant():
    if not current_user:
        messagebox.showerror('Error', 'Please login to view data.')
        return
    
    c.execute("SELECT * FROM plant")
    rows = c.fetchall()
    
    plant_window = tk.Toplevel(root)
    plant_window.title('Plant Logs')
    plant_window.geometry('350x425')
    plant_window.configure(bg='SteelBlue')
    
    ctk.CTkLabel(plant_window, font=("Default", 16, "bold"), text="View Data").pack(pady=10)
    
    # Create a frame to hold the Treeview and scrollbar
    tree_frame = tk.Frame(plant_window)
    tree_frame.pack(fill="both", expand=True)
    
    # Create the Treeview
    tree = ttk.Treeview(tree_frame, columns=("col1", "col2", "col3"), show="headings")
    tree.heading("col1", text="Type")
    tree.heading("col2", text="Amount")
    tree.heading("col3", text="Date/Time")
    tree.pack(side="left", fill="both", expand=True)
    
    # Create the vertical scrollbar
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    
    # Attach scrollbar to Treeview
    tree.configure(yscrollcommand=scrollbar.set)
    
    # Insert data
    for row in rows:
        tree.insert("", tk.END, values=row)

def show_harvest():
    if not current_user:
        messagebox.showerror('Error', 'Please login to view data.')
        return
    
    c.execute("SELECT * FROM harvest")
    rows = c.fetchall()
    
    harvest_window = tk.Toplevel(root)
    harvest_window.title('Harvest Logs')
    harvest_window.geometry('350x425')
    harvest_window.configure(bg='SteelBlue')
    
    ctk.CTkLabel(harvest_window, font=("Default", 16, "bold"), text="View Data").pack(pady=10)
    
    # Create a frame to hold the Treeview and scrollbar
    tree_frame = tk.Frame(harvest_window)
    tree_frame.pack(fill="both", expand=True)
    
    # Create the Treeview
    tree = ttk.Treeview(tree_frame, columns=("col1", "col2", "col3"), show="headings")
    tree.heading("col1", text="Type")
    tree.heading("col2", text="Amount")
    tree.heading("col3", text="Date/Time")
    tree.pack(side="left", fill="both", expand=True)
    
    # Create the vertical scrollbar
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    
    # Attach scrollbar to Treeview
    tree.configure(yscrollcommand=scrollbar.set)
    
    # Insert data
    for row in rows:
        tree.insert("", tk.END, values=row)
    
def show_task():
        if not current_user:
            messagebox.showerror('Error', 'Please login to view data.')
            return
        
        c.execute("SELECT * FROM task_tracker")
        rows = c.fetchall()

        task_window = tk.Toplevel(root)
        task_window.title('Task Logs')
        task_window.geometry('350x425')
        task_window.configure(bg='SteelBlue')
        
        ctk.CTkLabel(task_window, font=("Default", 16, "bold"), text="View Data").pack(pady=10)
        
        # Create a frame to hold the Treeview and scrollbar
        tree_frame = tk.Frame(task_window)
        tree_frame.pack(fill="both", expand=True)
        
        # Create the Treeview
        tree = ttk.Treeview(tree_frame, columns=("col1", "col2", "col3"), show="headings")
        tree.heading("col1", text="Name")
        tree.heading("col2", text="Date/Time")
        tree.heading("col3", text="Task")
        tree.pack(side="left", fill="both", expand=True)
        
        # Create the vertical scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        
        # Attach scrollbar to Treeview
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Insert data
        for row in rows:
            tree.insert("", tk.END, values=row)
### END


### Button Functions
def launch_ollama_gui():
    system = platform.system()
    exe_path = os.path.abspath("dist/ollama_gui.exe")
    script_path = os.path.abspath("ollama_gui.py")

    # Use logged-in user if available
    username = current_user if current_user else "Friend"

    if system == "Windows":
        if os.path.exists(exe_path):
            subprocess.Popen([exe_path, username], creationflags=subprocess.CREATE_NEW_CONSOLE)
        elif os.path.exists(script_path):
            subprocess.Popen(["python", script_path, username], creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            messagebox.showerror("Error", "Could not find ollama_gui.exe or ollama_gui.py")

    elif system == "Linux":
        if os.path.exists(exe_path):
            subprocess.Popen([exe_path, username])
        elif os.path.exists(script_path):
            subprocess.Popen(["python3", script_path, username])
        else:
            messagebox.showerror("Error", "Could not find ollama_gui executable or script")

    elif system == "Darwin":  # macOS
        if os.path.exists(exe_path):
            subprocess.Popen(["open", exe_path, "--args", username])
        elif os.path.exists(script_path):
            subprocess.Popen(["python3", script_path, username])
        else:
            messagebox.showerror("Error", "Could not find ollama_gui app or script")

    else:
        raise RuntimeError(f"Unsupported OS: {system}")

def button_function1():
    T =plant1.get()
    A = plant2.get()
    c.execute("""
    INSERT INTO plant(type, amount, date)
    VALUES(?,?,?)
    """, (T, A, timestamp))
    conn.commit()
    messagebox.showinfo('Congrats!', 'Data entry successful.')
    plant1.delete(0, END)
    plant2.delete(0, END)
    
def button_function2():
    T = h1.get()
    A = h2.get()
    c.execute("""
    INSERT INTO harvest(type, amount, date)
    VALUES(?,?,?)
    """, (T, A, timestamp))
    conn.commit()
    messagebox.showinfo('Congrats!', 'Data entry successful.')
    h1.delete(0, END)
    h2.delete(0, END)
    
def button_function3():
    T = task3.get("1.0",END)
    c.execute("""
    INSERT INTO task_tracker(name, date, task)
    VALUES(?,?,?)
    """, (current_user, timestamp, T))
    conn.commit()
    messagebox.showinfo('Congrats!', 'Data entry successful.')
    task3.delete("1.0",END)

def clear_plant():
    plant1.delete(0, END)
    plant2.delete(0, END)

def clear_harvest():
    h1.delete(0, END)
    h2.delete(0, END)
    
def clear_task():
    task3.delete("1.0",END)
### END    


root = tk.Tk()
root.title("Solace")
root.geometry('350x300')

container = tk.Frame(root)
container.pack(side="top", fill='both', expand=True)
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)
container.tk_setPalette('LightSteelBlue')

current_user = None


# LOGIN

login = tk.Frame(container)

tk.Label(login, padx=10, pady=10, text="Login", underline=-1).pack()

label_1 = tk.Label(master=login, text="Username")
label_1.pack(pady=5)

userl = ctk.CTkEntry(master=login)
userl.pack(pady=5)

label_1 = tk.Label(master=login, text="Password")
label_1.pack(pady=5)

passwordl = ctk.CTkEntry(master=login, show="*")
passwordl.pack(pady=5)

login_button = ctk.CTkButton(master=login, text_color="black", fg_color="white", hover_color="gray94", command=validation_login, text="Enter",)
login_button.pack(pady=5)

ctk.CTkButton(login, text="Create User",text_color="black", fg_color="white", hover_color="gray94", command=lambda: show_frame(create)).pack(pady=5)


# CREATE_USER

create = tk.Frame(container)

tk.Label(create, padx=10, pady=10, text="Create User").pack()

label_1 = tk.Label(master=create, text="Create Username")
label_1.pack(pady=5)

userc = ctk.CTkEntry(master=create)
userc.pack(pady=5)

label_1 = tk.Label(master=create, text="Create Password")
label_1.pack(pady=5)

passwordc = ctk.CTkEntry(master=create)
passwordc.pack(pady=5)

ctk.CTkButton(master=create, text_color="black", fg_color="white", hover_color="gray94", command=create_user, text="Submit",).pack(pady=5)

ctk.CTkButton(create, text="Back to Login", text_color="black", fg_color="white", hover_color="gray94", command=lambda: show_frame(login)).pack(pady=5)


# MAIN

main = tk.Frame(container)

tk.Label(main, padx=10, text="Main").pack(pady=(20, 10))

menubar = tk.Menu(main)
root.config(menu=menubar)

tool_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Tools", menu=tool_menu)
tool_menu.add_command(label="Weight Converter", command=open_weight_converter)

view_data = tk.Menu(menubar,tearoff=0)
menubar.add_cascade(label='View Data', menu=view_data)
view_data.add_command(label='Plant', command=show_plant)
view_data.add_command(label='Harvest', command=show_harvest)
view_data.add_command(label='Task Log', command=show_task)

help_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label='About', command=show_about)
help_menu.add_command(label='READ ME', command=open_file)
help_menu.add_command(label='Source Code',command=open_source)


ollama_gui_btn = ctk.CTkButton(main, text="Open Ollama GUI", text_color="black", fg_color="white", hover_color="gray94", command=launch_ollama_gui)
ollama_gui_btn.pack(padx=10, pady=10)


datalogging = ctk.CTkButton(main, text="Data Logging", text_color="black", fg_color="white", hover_color="gray94", command=lambda: show_frame(data_logging))
datalogging.pack(padx=10, pady=10)

ctk.CTkButton(main, text="Logout", text_color="black", fg_color="white", hover_color="gray94", command=logout).pack(padx=10, pady=10)

wake_label = tk.Label(main, text="🌿 Welcome, Solace awakens with you.", font=("Helvetica", 11, "italic"),fg="darkgreen", pady=5)
wake_label.pack(pady=10)


# Data Logging

data_logging = tk.Frame(container)

tk.Label(data_logging, padx=10, text="Data Logging").pack(pady=(20,10))

plant = ctk.CTkButton(data_logging, text="Plant Log", text_color="black", fg_color="white", hover_color="gray94", command=lambda: show_frame(plant))
plant.pack(padx=10, pady=10,)

harvest_log = ctk.CTkButton(data_logging, text="Harvest Log", text_color="black", fg_color="white", hover_color="gray94", command=lambda: show_frame(harvest))
harvest_log.pack(padx=10, pady=10,)

task_log  = ctk.CTkButton(data_logging, text="Task Log", text_color="black", fg_color="white", hover_color="gray94", command=lambda: show_frame(task))
task_log.pack(padx=10, pady=10,)

ctk.CTkButton(data_logging, text="Back To Main", text_color="black", fg_color="white", hover_color="gray94", command=lambda: show_frame(main)).pack(pady=10)


# Plant Log

plant = tk.Frame(container)

tk.Label(plant, text="Plant Log").pack()

label_1 = tk.Label(master=plant, text="Plant Type")
label_1.pack(pady=5)

plant1 = ctk.CTkEntry(master=plant)
plant1.pack(pady=5)

label_1 = tk.Label(master=plant, text="Amount")
label_1.pack(pady=5)

plant2 = ctk.CTkEntry(master=plant)
plant2.pack(pady=5)

submit_button = ctk.CTkButton(master=plant, text_color="black", fg_color="white", hover_color="gray94", command=button_function1, text="Submit",)
submit_button.pack(pady=5)

reset_button = ctk.CTkButton(master=plant, text_color="black", fg_color="white", hover_color="gray94", text='Clear Entries', command=clear_plant)
reset_button.pack(pady=5)

ctk.CTkButton(plant, text="Back", text_color="black", fg_color="white", hover_color="gray94", command=lambda: show_frame(data_logging)).pack()


# Harvest Log

harvest = tk.Frame(container)

tk.Label(harvest, text="Harvest Log").pack()

label_1 = tk.Label(master=harvest, text="Plant Type")
label_1.pack(pady=5)

h1 = ctk.CTkEntry(master=harvest)
h1.pack(pady=5)

label_1 = tk.Label(master=harvest, text="Amount")
label_1.pack(pady=5)

h2 = ctk.CTkEntry(master=harvest)
h2.pack(pady=5)

submit_button = ctk.CTkButton(master=harvest, text_color="black", fg_color="white", hover_color="gray94", command=button_function2, text="Submit",)
submit_button.pack(pady=5)

reset_button = ctk.CTkButton(master=harvest, text_color="black", fg_color="white", hover_color="gray94", text='Clear Entries', command=clear_harvest)
reset_button.pack(pady=5)

ctk.CTkButton(harvest, text="Back", text_color="black", fg_color="white", hover_color="gray94", command=lambda: show_frame(data_logging)).pack()




# Task Log
task = tk.Frame(container)

tk.Label(task, text="Task Log").pack()

label_1 = tk.Label(master=task, text="Task Complete")
label_1.pack(pady=5)

task3 = ctk.CTkTextbox(master=task, height=100)
task3.pack(pady=5)

submit_button = ctk.CTkButton(master=task, text_color="black", fg_color="white", hover_color="gray94", command=button_function3, text="Submit",)
submit_button.pack(pady=5)

reset_button = ctk.CTkButton(master=task, text='Clear Entries', text_color="black", fg_color="white", hover_color="gray94", command=clear_task)
reset_button.pack(pady=5)


ctk.CTkButton(task, text="Back", text_color="black", fg_color="white", hover_color="gray94", command=lambda: show_frame(data_logging)).pack()

for frame in (login, create, main, data_logging, plant, harvest, task):
    frame.grid(row=0, column=0, sticky="nsew")
    


current_user = load_session()

if current_user:
    # If a session exists, skip login and go straight to main frame
    show_frame(main)
else:
    # Otherwise, stay on login frame
    show_frame(login)


conn.commit()
root.mainloop()
conn.close()