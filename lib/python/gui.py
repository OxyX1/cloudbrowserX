import customtkinter as ctk
from lib.python.lib import PathAPI # Assuming PathAPI is defined in path.py

# Create the main window
root = ctk.CTk()
root.title('Injection Menu')
root.geometry('400x250')

def internal_ui_injection():
    path_string = process_entry.get()  # Get process name from user input
    dll_string = dll_entry.get()       # Get DLL path from user input
    try:
        injector = PathAPI(path_string, dll_string)
        injector.inject()
        status_label.configure(text=f"✅ Injection successful!", text_color="green")
    except Exception as e:
        status_label.configure(text=f"❌ Injection failed: {e}", text_color="red")


ctk.CTkLabel(root, text="Process Name (e.g., game.exe):").pack(pady=(10, 0))
process_entry = ctk.CTkEntry(root, width=300)
process_entry.pack(pady=(0, 10))

ctk.CTkLabel(root, text="DLL Path (e.g., C:\\path\\to\\your.dll):").pack(pady=(10, 0))
dll_entry = ctk.CTkEntry(root, width=300)
dll_entry.pack(pady=(0, 10))

internal_ui_injection_button = ctk.CTkButton(
    master=root,
    width=120,
    height=35,
    text="Inject DLL",
    command=internal_ui_injection
)
internal_ui_injection_button.pack(pady=10)

status_label = ctk.CTkLabel(root, text="", text_color="white")
status_label.pack(pady=10)

root.mainloop()



"""

this gui.py injects the main gui; "gui.cpp".
the gui.cpp will be turned into a dll once ran.
then it will inject the gui into the software.


"""