# solace-your-farming-companion
====================================================
        Solace – Farming Task Tracker + Ollama GUI
====================================================

Author: soldiers_son

solace.py Version: 1.0

olloma_gui.py Version: 1.3

Python: 3.11+

Platform: Windows / Linux / Mac

Dependencies: tkinter, customtkinter, bcrypt, sqlite3, requests, sys, json, base64, 
(ollama), webbrowser, platform, pprint, time, datetime, urlib.parse, urlib.request,
threading, typing, itertools, filedialog, subprocess, os

----------------------------------------------------
0. Acknowledgments
----------------------------------------------------
Special thanks to the open source community, whose 
work makes this project possible.

🙏 A particular thank you to **chyok** on GitHub, 
for creating the original base Ollama GUI project 
that inspired and supported the chat companion 
(`ollama_gui.py`) used here.

----------------------------------------------------
1. Introduction
----------------------------------------------------
Solace is a two-part application that blends 
practical farming task tracking with a personal, 
reflective AI companion.

1. Farming Task Tracker (solace.py)
   - Input what you planted, harvested, and tasks 
     completed.
   - Data is stored locally in a SQLite database.
   - Logs can be viewed anytime via the menu.

2. Ollama Chat Companion (ollama_gui.py)
   - A graphical chat interface for interacting 
     with Ollama.
   - Solace greets you warmly at startup.
   - Provides conversation memory, file upload, 
     and a smooth "typing effect."
   -Built and distributed by ckyok, edited by soldiers_son

----------------------------------------------------
2. Features
----------------------------------------------------

🌱 Farming Task Tracker (solace.py)
-----------------------------------
- Login/Create User with bcrypt password encryption.
- Login creates session.jsn that keeps the user logged in until logged out
- Input:
  • What you planted  
  • What you harvested  
  • Tasks you completed  
- Data stored in SQLite (`farm.db`).
- View saved logs via **View Data** menu:
  • Plant Log  
  • Harvest Log  
  • Task Log
- Toolbar menu with:
  • Tools → Weight Converter 
  • View Data → Plant / Harvest / Task Log  
  • Help → About / READ_ME.txt /Source Code  
- Clean Tkinter-based interface.
- Launch the AI companion with one button.

💬 Ollama Chat Companion (ollama_gui.py)
----------------------------------------
- Chat interface with Solace greeting at startup.
- Save and load conversations in JSON format.
- File upload (logs filename into chat history).
- Model Manager
- Toolbar menu with:
  • File → Model manager / Save / Load / Upload  
  • Edit → Copy All / Clear Chat
  • Help → About / Source Code  

----------------------------------------------------
4. Requirements
----------------------------------------------------
- Python 3.11 or higher
- Ollama installed and running locally
- Llama3 or a compatible model installed
- Dependencies installed (see Section 6)

----------------------------------------------------
5. Installation
----------------------------------------------------
1. Clone or download this repository.
2. Place the project folder on your desktop or 
   desired directory.
3. Install Python and required dependencies.
4. Install Ollama and pull a model (e.g. llama3).
5. Run the application:

   Windows:
   > python solace.py

   Linux/Mac:
   $ python3 solace.py

----------------------------------------------------
6. Dependencies
----------------------------------------------------
Install required packages via pip:

   pip install requests

Tkinter, json, sqlite3, and base64 are included 
with Python by default (Linux users may need to 
install Tkinter separately).

----------------------------------------------------
7. Installing Ollama & Llama3
----------------------------------------------------
Windows:
1. Download from https://ollama.com/download
2. Run the installer.
3. Verify:
   > ollama --version

Linux (Debian/Ubuntu):
1. Run:
   $ curl -fsSL https://ollama.com/install.sh | sh
2. Verify:
   $ ollama --version

Pull the Llama3 model:
   > ollama pull llama3:latest

Check installed models:
   > ollama list

----------------------------------------------------
8. Creating a Custom Model
----------------------------------------------------
You can create a custom personality for Solace.

1. Create `Modelfile`:
   FROM llama3
   PARAMETER temperature 0.7
   SYSTEM "You are Solace, a soft, illuminating AI companion who reflects on farming and daily life."

2. Build it:
   > Open modelfile folder, located in project folder, with terminal
   > ollama create solace -f solace

3. Run it:
   > ollama run solace

----------------------------------------------------
9. Usage
----------------------------------------------------
- Run `solace.py` to start the main farming app.
- Log your plants, harvests, and tasks.
- All data is stored in SQLite (`farm.db`).
- View data in toolbar *To edit data, you have to use farm_sql.py, and
  query the database*
- Click **Open Ollama GUI** to launch the AI companion.
- In chat:
  • Type messages and press **Send**.  
  • Save/load conversations with the File menu.
   *Save conversations in User Conversations folder located in project folder*  
  • Upload files to log metadata in chat.  
  • Use Help → About for version info.  

----------------------------------------------------
10. Notes
----------------------------------------------------
- Always start with `solace.py` (not `ollama_gui.py`).  
- Conversations are stored in JSON for compatibility 
  with Ollama.  
- File uploads currently log metadata, not binary 
  attachments.  
- Menus are built using tkinter & customtkinter; style may differ 
  slightly by OS.  
- Progress bar animation is purely visual.  

----------------------------------------------------
11. Future Goals
----------------------------------------------------
🌟 Planned expansions include:
- **Arduino & microcontroller compatibility**:  
  Integrating environmental sensor modules 
  (temperature, humidity, soil moisture, etc.) 
  so Solace can track real-world farming 
  conditions.  
- Extended data visualization of logs and 
  environmental readings.  
- Cross-device sync to make Solace a true 
  companion across desktop and embedded 
  systems.

----------------------------------------------------
12. Contributing
----------------------------------------------------
Suggestions and improvements are welcome. 
Fork the repo, make your changes, and submit a PR.

----------------------------------------------------
13. License
----------------------------------------------------
This project is open source under the MIT License.

----------------------------------------------------
14. Contact
----------------------------------------------------
Author: soldiers_son
GitHub: (https://github.com/soldiers-son?tab=repositories)
Email: (soldiers.son1618@gmail.com)
