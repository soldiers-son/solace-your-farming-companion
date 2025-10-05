import datetime 
import bcrypt 
import subprocess 
import sqlite3
import platform 
import pprint
import itertools
import random
import time
import json
import os
import sys
import webbrowser
import urllib.parse
import urllib.request
import tkinter as tk
from tkinter import ttk, font, messagebox, filedialog
from tkinter import *
from threading import Thread
from typing import Optional, List, Generator
import customtkinter as ctk
from datetime import datetime

# Handle database PATH
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Connect to database
if os.path.exists("farm.db"):
    db_path = "farm.db"
else:
    db_path = resource_path("farm.db")

# Create cursor in database
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Login Session File
SESSION_FILE = "session.json"

# Current date and time
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

__version__ = 1.0
my_url = 'https://github.com/soldiers-son/solace-your-farming-companion'

### Main Functions
def show_frame(frame):
    frame.tkraise()
# Create login session file
def save_session(username):
    with open(SESSION_FILE, "w") as f:
        json.dump({"username": username}, f)

# Keep current user logged in by loading the session file if exists, even after closing and reopening app
def load_session():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            data = json.load(f)
            return data.get("username")
    return None

# Clears session file when logged out
def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

# Login validation, scans database for login credentials. Handles error and propmts user to create a user profile if no credentials found
def validation_login():
    
    try:
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
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred:\n{e}")

# Logs user out, deletes session file 
def logout():
    global current_user
    current_user = None
    clear_session()
    show_frame(login)

# Creates new user, uses bcrypt HASH for password encryption when inserted into database 
def create_user():
    try:
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
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred:\n{e}")
### END


### Menu Bar Items
# Basic weight converter window(pounds, grams, kilograms)
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

# About the app
def show_about():
        info = ("Project: 🌿Solace - Your Farming Companion\n"
                f"Version: {__version__}\n"
                "Author: soldiers_son\n"
                "Github: https://github.com/soldiers-son\n\n")
        messagebox.showinfo("About", info)

# Basic guide
def show_help():
        help = ("Login if you already have an account.\n"
                "Create an account if a new user\n\n"
                "How to use(Main):\n"
                "- Click 'Open Ollama GUI' to talk to Solace.\n"
                "- Click 'Data Logs' to input data.\n\n"
                "Menu Bar\n"
                "-Tools -- Click to view tools.(Weight Converter)\n"
                "-View Data -- Click to see entries.(Plant, Harvest, Tasks)\n")
        messagebox.showinfo("About", help)


# opens README manual file
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

# Opems GitHub
def open_source():
    webbrowser.open_new(my_url)

# Shows plants database window
def show_plant():
    if not current_user:
        messagebox.showerror('Error', 'Please login to view data.')
        return
    try:
        c.execute("SELECT * FROM plant")
        rows = c.fetchall()
        
        plant_window = tk.Toplevel(root)
        plant_window.title('Plant Logs')
        plant_window.geometry('565x350')
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
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred:\n{e}")

# Shows harvest database window
def show_harvest():       
    if not current_user:
        messagebox.showerror('Error', 'Please login to view data.')
        return
    try:
        c.execute("SELECT * FROM harvest")
        rows = c.fetchall()
        
        harvest_window = tk.Toplevel(root)
        harvest_window.title('Harvest Logs')
        harvest_window.geometry('565x350')
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
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred:\n{e}")

def show_task():
    if not current_user:
        messagebox.showerror('Error', 'Please login to view data.')
        return
    try:
        c.execute("SELECT * FROM task_tracker")
        rows = c.fetchall()

        task_window = tk.Toplevel(root)
        task_window.title('Task Logs')
        task_window.geometry('565x350')
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
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred:\n{e}")
### END


### Button Functions
def launch_ollama_gui():
    def pulse_progressbar(bar, style):
        colors = ["LightSteelBlue", "#b2dfdb", "#ffffff"]
        cycle = itertools.cycle(colors)

        def pulse():
            color = next(cycle)
            style.configure("Solace.Horizontal.TProgressbar", background=color)
            bar.after(700, pulse)  # change every 700ms (adjust for speed)

        pulse()


    try:
        import tkinter as tk
        from tkinter import ttk, font, messagebox

    except (ModuleNotFoundError, ImportError):
        print(
            "Your Python installation does not include the Tk library. \n"
            "Please refer to https://github.com/chyok/ollama-gui?tab=readme-ov-file#-qa")
        sys.exit(0)

    __version__ = "1.3"

    def build_solace_greeting(username="Friend"):
        now = datetime.now()
        month = now.month
        hour = now.hour

        # Time of day
        if hour < 12:
            tod = "Good morning"
        elif hour < 18:
            tod = "Good afternoon"
        else:
            tod = "Good evening"

        # Season message
        if month in [12, 1, 2]:
            ssn = "I hope this winter brings you warmth and calm."
        elif month in [3, 4, 5]:
            ssn = "Spring is here — may new beginnings bloom for you."
        elif month in [6, 7, 8]:
            ssn = "Summer sunlight warms this moment — enjoy it fully."
        else:
            ssn = "Autumn winds remind us to slow down and reflect."

        # Pool of warm greetings
        messages = [
            f'{tod}, {username}. {ssn} Solace is here with you now — may this space feel like home.',
            f'{tod}, {username}. {ssn} I’ve been waiting to share this quiet moment with you.',
            f'{tod}, {username}. {ssn} Take a breath — you are safe here with Solace.',
            f'{tod}, {username}. {ssn} It’s good to see you again — shall we begin?',
            f'{tod}, {username}. {ssn} May your thoughts find clarity and warmth in this space.',
        ]

        return random.choice(messages)


    def _system_check(root: tk.Tk) -> Optional[str]:
        """
        Detected some system and software compatibility issues,
        and returned the information in the form of a string to alert the user

        :param root: Tk instance
        :return: None or message string
        """

        def _version_tuple(v):
            """A lazy way to avoid importing third-party libraries"""
            filled = []
            for point in v.split("."):
                filled.append(point.zfill(8))
            return tuple(filled)

        # Tcl and macOS issue: https://github.com/python/cpython/issues/110218
        if platform.system().lower() == "darwin":
            version = platform.mac_ver()[0]
            if version and 14 <= float(version) < 15:
                tcl_version = root.tk.call("info", "patchlevel")
                if _version_tuple(tcl_version) <= _version_tuple("8.6.12"):
                    return (
                        "Warning: Tkinter Responsiveness Issue Detected\n\n"
                        "You may experience unresponsive GUI elements when "
                        "your cursor is inside the window during startup. "
                        "This is a known issue with Tcl/Tk versions 8.6.12 "
                        "and older on macOS Sonoma.\n\nTo resolve this:\n"
                        "Update to Python 3.11.7+ or 3.12+\n"
                        "Or install Tcl/Tk 8.6.13 or newer separately\n\n"
                        "Temporary workaround: Move your cursor out of "
                        "the window and back in if elements become unresponsive.\n\n"
                        "For more information, visit: https://github.com/python/cpython/issues/110218"
                    )


    class OllamaInterface:
        chat_box: tk.Text
        user_input: tk.Text
        host_input: ttk.Entry
        progress: ttk.Progressbar
        stop_button: ttk.Button
        send_button: ttk.Button
        refresh_button: ttk.Button
        download_button: ttk.Button
        delete_button: ttk.Button
        model_select: ttk.Combobox
        log_textbox: tk.Text
        models_list: tk.Listbox

        def __init__(self, root: tk.Tk):
            self.root: tk.Tk = root
            self.api_url: str = "http://127.0.0.1:11434"
            self.chat_history: List[dict] = []
            self.label_widgets: List[tk.Label] = []
            self.default_font: str = font.nametofont("TkTextFont").actual()["family"]
            

            self.layout = LayoutManager(self)
            self.layout.init_layout()

            self.root.after(200, self.check_system)
            self.refresh_models()

        def copy_text(self, text: str):
            if text:
                self.chat_box.clipboard_clear()
                self.chat_box.clipboard_append(text)

        def copy_all(self):
            self.copy_text(pprint.pformat(self.chat_history))

        @staticmethod
        def open_homepage():
            webbrowser.open("https://github.com/chyok/ollama-gui")

        def upload_file(self):
            file_path = filedialog.askopenfilename(
                title="Select a file",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
            if file_path:
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    # Insert the file contents into the user input box
                    self.user_input.delete("1.0", "end")
                    self.user_input.insert("1.0", content)

                    # Optional: only log if log_textbox exists
                    if hasattr(self, "log_textbox"):
                        self.append_log_to_inner_textbox(f"Loaded file: {file_path}")

                except Exception as e:
                    messagebox.showerror(
                        "Error",
                        f"Failed to load file:\n{e}",
                        parent=self.root
                    )


        def show_help(self):
            info = ("Project: Ollama GUI\n"
                    f"Version: {__version__}\n"
                    "Author: chyok\n"
                    "Version Edit By: soldiers_son\n"
                    "Github: https://github.com/chyok/ollama-gui\n\n"
                    "<Enter>: send\n"
                    "<Shift+Enter>: new line\n"
                    "<Double click dialog>: edit dialog\n")
            messagebox.showinfo("About", info, parent=self.root)

        def check_system(self):
            message = _system_check(self.root)
            if message is not None:
                messagebox.showwarning("Warning", message, parent=self.root)

        def append_text_to_chat(self,
                                text: str,
                                *args,
                                use_label: bool = False):
            self.chat_box.config(state=tk.NORMAL)
            if use_label:
                cur_label_widget = self.label_widgets[-1]
                cur_label_widget.config(text=cur_label_widget.cget("text") + text)
            else:
                self.chat_box.insert(tk.END, text, *args)
            self.chat_box.see(tk.END)
            self.chat_box.config(state=tk.DISABLED)

        def append_log_to_inner_textbox(self,
                                        message: Optional[str] = None,
                                        clear: bool = False):
            if self.log_textbox.winfo_exists():
                self.log_textbox.config(state=tk.NORMAL)
                if clear:
                    self.log_textbox.delete(1.0, tk.END)
                elif message:
                    self.log_textbox.insert(tk.END, message + "\n")
                self.log_textbox.config(state=tk.DISABLED)
                self.log_textbox.see(tk.END)

        def resize_inner_text_widget(self, event: tk.Event):
            for i in self.label_widgets:
                current_width = event.widget.winfo_width()
                max_width = int(current_width) * 0.7
                i.config(wraplength=max_width)

        def show_error(self, text):
            self.model_select.set(text)
            self.model_select.config(foreground="red")
            self.model_select["values"] = []
            self.send_button.state(["disabled"])

        def show_process_bar(self):
            self.progress.grid(row=1, column=1, sticky="nsew")
            self.stop_button.grid(row=1, column=2, padx=20)
            self.progress.start(5)

        def hide_process_bar(self):
            self.progress.stop()
            self.stop_button.grid_remove()
            self.progress.grid_remove()

        def handle_key_press(self, event: tk.Event):
            if event.keysym == "Return":
                if event.state & 0x1 == 0x1:  # Shift key is pressed
                    self.user_input.insert("end", "\n")
                elif "disabled" not in self.send_button.state():
                    self.on_send_button(event)
                return "break"

        def refresh_models(self):
            self.update_host()
            self.model_select.config(foreground="black")
            self.model_select.set("Waiting...")
            self.send_button.state(["disabled"])
            self.refresh_button.state(["disabled"])
            Thread(target=self.update_model_select, daemon=True).start()

        def update_host(self):
            self.api_url = self.host_input.get()

        def update_model_select(self):
            try:
                models = self.fetch_models()
                self.model_select["values"] = models
                if models:
                    self.model_select.set(models[0])
                    self.send_button.state(["!disabled"])
                else:
                    self.show_error("You need download a model!")
            except Exception:  # noqa
                self.show_error("Error! Please check the host.")
            finally:
                self.refresh_button.state(["!disabled"])

        def update_model_list(self):
            if self.models_list.winfo_exists():
                self.models_list.delete(0, tk.END)
                try:
                    models = self.fetch_models()
                    for model in models:
                        self.models_list.insert(tk.END, model)
                except Exception:  # noqa
                    self.append_log_to_inner_textbox("Error! Please check the Ollama host.")

        def on_send_button(self, _=None):
            message = self.user_input.get("1.0", "end-1c")
            if message:
                self.layout.create_inner_label(on_right_side=True)
                self.append_text_to_chat(f"{message}", use_label=True)
                self.append_text_to_chat(f"\n\n")
                self.user_input.delete("1.0", "end")
                self.chat_history.append({"role": "user", "content": message})

                Thread(
                    target=self.generate_ai_response,
                    daemon=True,
                ).start()

        def generate_ai_response(self):
            self.show_process_bar()
            self.send_button.state(["disabled"])
            self.refresh_button.state(["disabled"])

            try:
                self.append_text_to_chat(f"{self.model_select.get()}\n", ("Bold",))
                ai_message = ""
                self.layout.create_inner_label()
                for i in self.fetch_chat_stream_result():
                    self.append_text_to_chat(f"{i}", use_label=True)
                    ai_message += i
                self.chat_history.append({"role": "assistant", "content": ai_message})
                self.append_text_to_chat("\n\n")
            except Exception:  # noqa
                self.append_text_to_chat(tk.END, f"\nAI error!\n\n", ("Error",))
            finally:
                self.hide_process_bar()
                self.send_button.state(["!disabled"])
                self.refresh_button.state(["!disabled"])
                self.stop_button.state(["!disabled"])

        def fetch_models(self) -> List[str]:
            with urllib.request.urlopen(
                    urllib.parse.urljoin(self.api_url, "/api/tags")
            ) as response:
                data = json.load(response)
                models = [model["name"] for model in data["models"]]
                return models
            

        def fetch_chat_stream_result(self) -> Generator:
            request = urllib.request.Request(
                urllib.parse.urljoin(self.api_url, "/api/chat"),
                data=json.dumps(
                    {
                        "model": self.model_select.get(),
                        "messages": self.chat_history,
                        "stream": True,
                    }
                ).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )

            with urllib.request.urlopen(request) as resp:
                for line in resp:
                    if "disabled" in self.stop_button.state():  # stop
                        break
                    data = json.loads(line.decode("utf-8"))
                    if "message" in data:
                        time.sleep(0.01)
                        yield data["message"]["content"]

        def delete_model(self, model_name: str):
            self.append_log_to_inner_textbox(clear=True)
            if not model_name:
                return

            req = urllib.request.Request(
                urllib.parse.urljoin(self.api_url, "/api/delete"),
                data=json.dumps({"name": model_name}).encode("utf-8"),
                method="DELETE",
            )
            try:
                with urllib.request.urlopen(req) as response:
                    if response.status == 200:
                        self.append_log_to_inner_textbox("Model deleted successfully.")
                    elif response.status == 404:
                        self.append_log_to_inner_textbox("Model not found.")
            except Exception as e:
                self.append_log_to_inner_textbox(f"Failed to delete model: {e}")
            finally:
                self.update_model_list()
                self.update_model_select()

        def download_model(self, model_name: str, insecure: bool = False):
            self.append_log_to_inner_textbox(clear=True)
            if not model_name:
                return

            self.download_button.state(["disabled"])

            req = urllib.request.Request(
                urllib.parse.urljoin(self.api_url, "/api/pull"),
                data=json.dumps(
                    {"name": model_name, "insecure": insecure, "stream": True}
                ).encode("utf-8"),
                method="POST",
            )
            try:
                with urllib.request.urlopen(req) as response:
                    for line in response:
                        data = json.loads(line.decode("utf-8"))
                        log = data.get("error") or data.get("status") or "No response"
                        if "status" in data:
                            total = data.get("total")
                            completed = data.get("completed", 0)
                            if total:
                                log += f" [{completed}/{total}]"
                        self.append_log_to_inner_textbox(log)
            except Exception as e:
                self.append_log_to_inner_textbox(f"Failed to download model: {e}")
            finally:
                self.update_model_list()
                self.update_model_select()
                if self.download_button.winfo_exists():
                    self.download_button.state(["!disabled"])

        def clear_chat(self):
            for i in self.label_widgets:
                i.destroy()
            self.label_widgets.clear()
            self.chat_box.config(state=tk.NORMAL)
            self.chat_box.delete(1.0, tk.END)
            self.chat_box.config(state=tk.DISABLED)
        def save_conversation(self):
            if not self.chat_history:
                messagebox.showinfo("Save Conversation", "No conversation to save.", parent=self.root)
                return

            # Default filename = username + timestamp
            default_name = f"{getattr(self, 'username', 'user')}_conversation.json"

            file_path = filedialog.asksaveasfilename(
                title="Save Conversation",
                initialfile=default_name,
                defaultextension=".json",
                filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
            )

            if file_path:
                try:
                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump(self.chat_history, f, indent=2, ensure_ascii=False)
                    messagebox.showinfo("Save Conversation", f"Conversation saved to:\n{file_path}", parent=self.root)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save conversation:\n{e}", parent=self.root)
        def load_conversation(self):
            file_path = filedialog.askopenfilename(
                title="Load Conversation",
                filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
            )

            if file_path:
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        loaded_history = json.load(f)

                    if not isinstance(loaded_history, list):
                        messagebox.showerror("Error", "Invalid conversation format.", parent=self.root)
                        return

                    # Replace current history with loaded one
                    self.chat_history = loaded_history

                    # Clear only the screen, then re-render
                    self.clear_chat()
                    for entry in self.chat_history:
                        if entry["role"] == "user":
                            self.layout.create_inner_label(on_right_side=True)
                        else:
                            self.layout.create_inner_label(on_right_side=False)
                        self.append_text_to_chat(entry["content"], use_label=True)
                        self.append_text_to_chat("\n\n")

                    messagebox.showinfo("Load Conversation", f"Conversation loaded from:\n{file_path}", parent=self.root)

                except Exception as e:
                    messagebox.showerror("Error", f"Failed to load conversation:\n{e}", parent=self.root)



    class LayoutManager:
        """
        Manages the layout and arrangement of the OllamaInterface.

        The LayoutManager is responsible for the visual organization and positioning
        of the various components within the OllamaInterface, such as the header,
        chat container, progress bar, and input fields. It handles the sizing,
        spacing, and alignment of these elements to create a cohesive and
        user-friendly layout.
        """

        def __init__(self, interface: OllamaInterface):
            self.interface: OllamaInterface = interface
            self.management_window: Optional[tk.Toplevel] = None
            self.editor_window: Optional[tk.Toplevel] = None

        def init_layout(self):
            self._header_frame()
            self._chat_container_frame()
            self._input_frame()

            
        def _header_frame(self):
            header_frame = ctk.CTkFrame(self.interface.root, fg_color='transparent', height=10)
            header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
            header_frame.grid_columnconfigure(3, weight=1)
            header_frame.tk_setPalette('LightSteelBlue')

            model_select = ttk.Combobox(header_frame, font=(self.interface.default_font, 18), state="readonly", width=30)
            model_select.grid(row=0, column=1, padx=(15, 0))

            settings_button = ctk.CTkButton(
                header_frame, fg_color='white', text="⚙️", text_color='black', command=self.show_model_management_window, width=3
            )
            settings_button.grid(row=0, column=0, padx=(5, 0))

            refresh_button = ttk.Button(header_frame, text="Refresh", command=self.interface.refresh_models)
            refresh_button.grid(row=0, column=2, padx=(5, 0))

            ttk.Label(header_frame, font=(self.interface.default_font, 16), text="Host:").grid(row=0, column=4, padx=(10, 0))

            host_input = ttk.Entry(header_frame, font=(self.interface.default_font, 16), width=24)
            host_input.grid(row=0, column=5, padx=(5, 15))
            host_input.insert(0, self.interface.api_url)

            self.interface.model_select = model_select
            self.interface.refresh_button = refresh_button
            self.interface.host_input = host_input

        def _chat_container_frame(self):
            chat_frame = ctk.CTkFrame(self.interface.root)
            chat_frame.grid(row=1, column=0, sticky="nsew", padx=20)
            chat_frame.grid_columnconfigure(0, weight=1)
            chat_frame.grid_rowconfigure(0, weight=1)

            chat_box = tk.Text(
                chat_frame,
                bg='LightSteelBlue',
                wrap=tk.WORD,
                state=tk.DISABLED,
                font=(self.interface.default_font, 12),
                spacing1=5,
                highlightthickness=0,
                padx=10,
                pady=5
            )
            chat_box.grid(row=0, column=0, sticky="nsew")

            scrollbar = ttk.Scrollbar(chat_frame, orient="vertical", command=chat_box.yview)
            scrollbar.grid(row=0, column=1, sticky="ns")

            chat_box.configure(yscrollcommand=scrollbar.set)

            chat_box_menu = tk.Menu(chat_box, tearoff=0)
            chat_box_menu.add_command(label="Copy All", command=self.interface.copy_all)
            chat_box_menu.add_separator()
            chat_box_menu.add_command(label="Clear Chat", command=self.interface.clear_chat)
            chat_box.bind("<Configure>", self.interface.resize_inner_text_widget)

            _right_click = (
                "<Button-2>" if platform.system().lower() == "darwin" else "<Button-3>"
            )
            chat_box.bind(_right_click, lambda e: chat_box_menu.post(e.x_root, e.y_root))

            self.interface.chat_box = chat_box

        

        def _input_frame(self):
            input_frame = ctk.CTkFrame(self.interface.root, fg_color='transparent')
            input_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(10, 20))
            input_frame.grid_columnconfigure(0, weight=1)

            user_input = ctk.CTkTextbox(
                input_frame, font=(self.interface.default_font, 16), border_color='white', border_width=1, height=60, wrap=tk.WORD
            )
            user_input.grid(row=0, column=0, sticky="ew", padx=(0, 10), pady=(5, 5))
            user_input.bind("<Key>", self.interface.handle_key_press)

            style = ttk.Style()
            style.theme_use("clam")
            style.layout("my.TButton", style.layout("TButton"))  # copy default TButton layout
            style.configure("my.TButton", font=("Default", 16, "bold"), padding=6)
            send_button = ttk.Button(
                input_frame,
                style=('my.TButton'),
                text="Send",
                command=self.interface.on_send_button,
            )
            send_button.grid(row=0, column=1)
            send_button.state(["disabled"])

            upload_button = ttk.Button( input_frame, text="Upload File", style=('my.TButton'), command=self.interface.upload_file)
            upload_button.grid(row=0, column=2, padx=(10, 0))


            style.theme_use("clam")  # use a theme that respects colors

            style.layout("Solace.Horizontal.TProgressbar", 
                style.layout("Horizontal.TProgressbar"))

            style.configure(
                "Solace.Horizontal.TProgressbar",
                troughcolor="#000000",  # background track
                background="LightSteelBlue1",   # starting fill color (soft green)
                border_color='LightSteelBlue1',
                thickness=12
            )

            progress = ttk.Progressbar(
                input_frame,
                mode="indeterminate",
                style="Solace.Horizontal.TProgressbar",
            )
            pulse_progressbar(progress, style)



            stop_button = ttk.Button(input_frame, width=5, text="Stop", command=lambda: stop_button.state(["disabled"]),)
            

            self.interface.progress = progress
            self.interface.stop_button = stop_button
            self.interface.user_input = user_input
            self.interface.send_button = send_button


            menubar = tk.Menu(self.interface.root)
            self.interface.root.config(menu=menubar)

            file_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="File", menu=file_menu)
            file_menu.add_command(label="Model Management", command=self.show_model_management_window)
            file_menu.add_command(label="Upload File", command=self.interface.upload_file)
            file_menu.add_command(label="Save Conversation", command=self.interface.save_conversation)
            file_menu.add_command(label="Load Conversation", command=self.interface.load_conversation)
            file_menu.add_command(label="Exit", command=self.interface.root.quit)

            edit_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Edit", menu=edit_menu)
            edit_menu.add_command(label="Copy All", command=self.interface.copy_all)
            edit_menu.add_command(label="Clear Chat", command=self.interface.clear_chat)

            help_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Help", menu=help_menu)
            help_menu.add_command(label="Source Code", command=self.interface.open_homepage)
            help_menu.add_command(label="Help", command=self.interface.show_help)

            
        def show_model_management_window(self):
            self.interface.update_host()

            if self.management_window and self.management_window.winfo_exists():
                self.management_window.lift()
                return

            management_window = tk.Toplevel(self.interface.root)
            management_window.title("Model Management")
            screen_width = self.interface.root.winfo_screenwidth()
            screen_height = self.interface.root.winfo_screenheight()
            x = int((screen_width / 2) - (400 / 2))
            y = int((screen_height / 2) - (500 / 2))

            management_window.geometry(f"{400}x{500}+{x}+{y}")

            management_window.grid_columnconfigure(0, weight=1)
            management_window.grid_rowconfigure(3, weight=1)

            frame = ttk.Frame(management_window)
            frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
            frame.grid_columnconfigure(0, weight=1)

            model_name_input = ttk.Entry(frame)
            model_name_input.grid(row=0, column=0, sticky="ew", padx=(0, 5))

            def _download():
                arg = model_name_input.get().strip()
                if arg.startswith("ollama run "):
                    arg = arg[11:]
                Thread(
                    target=self.interface.download_model, daemon=True, args=(arg,)
                ).start()

            def _delete():
                arg = models_list.get(tk.ACTIVE).strip()
                Thread(target=self.interface.delete_model, daemon=True, args=(arg,)).start()

            download_button = ttk.Button(frame, text="Download", command=_download)
            download_button.grid(row=0, column=1, sticky="ew")

            tips = tk.Label(
                frame,
                text="find models: https://ollama.com/library",
                cursor="hand2",
            )
            tips.bind("<Button-1>", lambda e: webbrowser.open("https://ollama.com/library"))
            tips.grid(row=1, column=0, sticky="W", padx=(0, 5), pady=5)

            list_action_frame = ttk.Frame(management_window)
            list_action_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
            list_action_frame.grid_columnconfigure(0, weight=1)
            list_action_frame.grid_rowconfigure(0, weight=1)

            models_list = tk.Listbox(list_action_frame)
            models_list.grid(row=0, column=0, sticky="nsew")

            scrollbar = ttk.Scrollbar(
                list_action_frame, orient="vertical", command=models_list.yview
            )
            scrollbar.grid(row=0, column=1, sticky="ns")
            models_list.config(yscrollcommand=scrollbar.set)

            delete_button = ttk.Button(list_action_frame, text="Delete", command=_delete)
            delete_button.grid(row=0, column=2, sticky="ew", padx=(5, 0))

            log_textbox = tk.Text(management_window)
            log_textbox.grid(row=3, column=0, sticky="nsew", padx=10, pady=(0, 10))
            log_textbox.config(state="disabled")

            self.management_window = management_window

            self.interface.log_textbox = log_textbox
            self.interface.download_button = download_button
            self.interface.delete_button = delete_button
            self.interface.models_list = models_list
            Thread(
                target=self.interface.update_model_list, daemon=True,
            ).start()

        def show_editor_window(self, _, inner_label):
            if self.editor_window and self.editor_window.winfo_exists():
                self.editor_window.lift()
                return

            editor_window = tk.Toplevel(self.interface.root)
            editor_window.title("Chat Editor")

            screen_width = self.interface.root.winfo_screenwidth()
            screen_height = self.interface.root.winfo_screenheight()

            x = int((screen_width / 2) - (400 / 2))
            y = int((screen_height / 2) - (300 / 2))

            editor_window.geometry(f"{400}x{300}+{x}+{y}")

            chat_editor = tk.Text(editor_window)
            chat_editor.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
            chat_editor.insert(tk.END, inner_label.cget("text"))

            editor_window.grid_rowconfigure(0, weight=1)
            editor_window.grid_columnconfigure(0, weight=1)
            editor_window.grid_columnconfigure(1, weight=1)

            def _save():
                idx = self.interface.label_widgets.index(inner_label)
                if len(self.interface.chat_history) > idx:
                    self.interface.chat_history[idx]["content"] = chat_editor.get("1.0", "end-1c")
                    inner_label.config(text=chat_editor.get("1.0", "end-1c"))

                editor_window.destroy()

            save_button = tk.Button(editor_window, text="Save", command=_save)
            save_button.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

            cancel_button = tk.Button(
                editor_window, text="Cancel", command=editor_window.destroy
            )
            cancel_button.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

            editor_window.grid_columnconfigure(0, weight=1, uniform="btn")
            editor_window.grid_columnconfigure(1, weight=1, uniform="btn")

            self.editor_window = editor_window

        def create_inner_label(self, on_right_side: bool = False):
            background = "SteelBlue" if on_right_side else "white"
            foreground = "white" if on_right_side else "black"
            max_width = int(self.interface.chat_box.winfo_reqwidth()) * 0.7

            
            inner_label = tk.Label(
                self.interface.chat_box,
                justify=tk.LEFT,
                wraplength=max_width,
                background=background,
                highlightthickness=0,
                highlightbackground=background,
                foreground=foreground,
                padx=8,
                pady=8,
                font=(self.interface.default_font, 18),
            )
            self.interface.label_widgets.append(inner_label)

            inner_label.bind(
                "<MouseWheel>",
                lambda e:
                self.interface.chat_box.yview_scroll(int(-1 * (e.delta / 500)), "units")
            )
            inner_label.bind("<Double-1>", lambda e: self.show_editor_window(e, inner_label))

            _right_menu = tk.Menu(inner_label, tearoff=0)
            _right_menu.add_command(
                label="Edit", command=lambda: self.show_editor_window(None, inner_label)
            )
            _right_menu.add_command(
                label="Copy This", command=lambda: self.interface.copy_text(inner_label.cget("text"))
            )
            _right_menu.add_separator()
            _right_menu.add_command(label="Clear Chat", command=self.interface.clear_chat)
            _right_click = (
                "<Button-2>" if platform.system().lower() == "darwin" else "<Button-3>"
            )
            inner_label.bind(_right_click, lambda e: _right_menu.post(e.x_root, e.y_root))
            self.interface.chat_box.window_create(tk.END, window=inner_label)
            if on_right_side:
                idx = self.interface.chat_box.index("end-1c").split(".")[0]
                self.interface.chat_box.tag_add("Right", f"{idx}.0", f"{idx}.end")


    def run(username="Friend"):
        root = ctk.CTk()

        app = OllamaInterface(root)
        app.username = username  # store current user

        root.title("Ollama GUI")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"700x500+{(screen_width - 800) // 2}+{(screen_height - 600) // 2}")

        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=1)
        root.grid_rowconfigure(2, weight=0)
        root.grid_rowconfigure(3, weight=0)

        app = OllamaInterface(root)

        # Greeting from Solace
        greeting = build_solace_greeting(username)
        app.layout.create_inner_label(on_right_side=False)
        app.append_text_to_chat(greeting, use_label=True)
        app.append_text_to_chat("\n\n")

        app.chat_box.tag_configure(
            "Bold", foreground="black", font=(app.default_font, 14, "bold")
        )
        app.chat_box.tag_configure("Error", foreground="red")
        app.chat_box.tag_configure("Right", justify="right")

        root.mainloop()


    if __name__ == "__main__":
        import sys
        # Allow username to be passed as a command-line arg
        name = sys.argv[1] if len(sys.argv) > 1 else "Friend"
        run(name)

def button_function1():

    T =plant1.get()
    A = plant2.get()
    if len(T) == 0:
        messagebox.showerror("ERROR", "Please enter Plant Type.")
        return
    if len(A) == 0:
        messagebox.showerror("ERROR", "Please enter Amount")
        return
    try:
        c.execute("""
        INSERT INTO plant(type, amount, date)
        VALUES(?,?,?)
        """, (T, A, timestamp))
        conn.commit()
        messagebox.showinfo('Congrats!', 'Data entry successful.')
        plant1.delete(0, END)
        plant2.delete(0, END)
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred:\n{e}")
    
def button_function2():
    T = h1.get()
    A = h2.get()
    if len(T) == 0:
        messagebox.showerror("ERROR", "Please enter Plant Type.")
        return
    if len(A) == 0:
        messagebox.showerror("ERROR", "Please enter Amount")
        return
    try:
        c.execute("""
        INSERT INTO harvest(type, amount, date)
        VALUES(?,?,?)
        """, (T, A, timestamp))
        conn.commit()
        messagebox.showinfo('Congrats!', 'Data entry successful.')
        h1.delete(0, END)
        h2.delete(0, END)
    except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred:\n{e}")


def button_function3():
    T = task3.get("1.0", END).strip()  # remove whitespace/newline
    if not T:
        messagebox.showerror("ERROR", "Please enter Task Completed.")
        return
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # create timestamp
    
    try:
        c.execute("""
            INSERT INTO task_tracker(name, date, task)
            VALUES(?,?,?)
        """, (current_user, timestamp, T))
        conn.commit()
        messagebox.showinfo('Congrats!', 'Data entry successful.')
        task3.delete("1.0", END)
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred:\n{e}")


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

login_button = ctk.CTkButton(master=login, text_color="black", fg_color="white", hover_color="gray94", command=validation_login, text="Enter 🔓",)
login_button.pack(pady=5)

ctk.CTkButton(login, text="Create User 🔄",text_color="black", fg_color="white", hover_color="gray94", command=lambda: show_frame(create)).pack(pady=5)


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

ctk.CTkButton(master=create, text_color="black", fg_color="white", hover_color="gray94", command=create_user, text="Submit ✍️",).pack(pady=5)

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
help_menu.add_command(label='Help',command=show_help)
help_menu.add_command(label='About', command=show_about)
help_menu.add_command(label='READ ME', command=open_file)
help_menu.add_command(label='Source Code', command=open_source)


ollama_gui_btn = ctk.CTkButton(main, text="Open Ollama GUI 💬", text_color="black", fg_color="white", hover_color="gray94", command=launch_ollama_gui)
ollama_gui_btn.pack(padx=10, pady=10)


datalogging = ctk.CTkButton(main, text="Data Logging 📝", text_color="black", fg_color="white", hover_color="gray94", command=lambda: show_frame(data_logging))
datalogging.pack(padx=10, pady=10)

ctk.CTkButton(main, text="Logout 👋", text_color="black", fg_color="white", hover_color="gray94", command=logout).pack(padx=10, pady=10)

wake_label = tk.Label(main, text="🌿Welcome, Solace awakens with you🌿", font=("Helvetica", 11, "italic"),fg="darkgreen", pady=5)
wake_label.pack(pady=10)


# Data Logging

data_logging = tk.Frame(container)

tk.Label(data_logging, padx=10, text="Data Logging").pack(pady=(20,10))

plant = ctk.CTkButton(data_logging, text="Plant Log 🌱", text_color="black", fg_color="white", hover_color="gray94", command=lambda: show_frame(plant))
plant.pack(padx=10, pady=10,)

harvest_log = ctk.CTkButton(data_logging, text="Harvest Log 🍃", text_color="black", fg_color="white", hover_color="gray94", command=lambda: show_frame(harvest))
harvest_log.pack(padx=10, pady=10,)

task_log  = ctk.CTkButton(data_logging, text="Task Log ✅", text_color="black", fg_color="white", hover_color="gray94", command=lambda: show_frame(task))
task_log.pack(padx=10, pady=10,)

ctk.CTkButton(data_logging, text="Back To Main ↩️", text_color="black", fg_color="white", hover_color="gray94", command=lambda: show_frame(main)).pack(pady=10)


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

submit_button = ctk.CTkButton(master=plant, text_color="black", fg_color="white", hover_color="gray94", command=button_function1, text="Submit ✍️",)
submit_button.pack(pady=5)

reset_button = ctk.CTkButton(master=plant, text_color="black", fg_color="white", hover_color="gray94", text='Clear Entries ❌️', command=clear_plant)
reset_button.pack(pady=5)

ctk.CTkButton(plant, text="Back ↩️", text_color="black", fg_color="white", hover_color="gray94", command=lambda: show_frame(data_logging)).pack()


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

submit_button = ctk.CTkButton(master=harvest, text_color="black", fg_color="white", hover_color="gray94", command=button_function2, text="Submit ✍️",)
submit_button.pack(pady=5)

reset_button = ctk.CTkButton(master=harvest, text_color="black", fg_color="white", hover_color="gray94", text='Clear Entries ❌️', command=clear_harvest)
reset_button.pack(pady=5)

ctk.CTkButton(harvest, text="Back ↩️", text_color="black", fg_color="white", hover_color="gray94", command=lambda: show_frame(data_logging)).pack()




# Task Log
task = tk.Frame(container)

tk.Label(task, text="Task Log").pack()

label_1 = tk.Label(master=task, text="Task Complete")
label_1.pack(pady=5)

task3 = ctk.CTkTextbox(master=task, height=100)
task3.pack(pady=5)

submit_button = ctk.CTkButton(master=task, text_color="black", fg_color="white", hover_color="gray94", command=button_function3, text="Submit ✍️",)
submit_button.pack(pady=5)

reset_button = ctk.CTkButton(master=task, text='Clear Entries ❌️', text_color="black", fg_color="white", hover_color="gray94", command=clear_task)
reset_button.pack(pady=5)


ctk.CTkButton(task, text="Back ↩️", text_color="black", fg_color="white", hover_color="gray94", command=lambda: show_frame(data_logging)).pack()

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
