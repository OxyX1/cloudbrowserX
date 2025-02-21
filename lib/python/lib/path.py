import pymem
import pymem.process
import ctypes


class PathAPI:
    def __init__(self, process_name, dll_path):
        self.process_name = process_name
        self.dll_path = dll_path
        self.pm = None
        self.kernel32 = ctypes.windll.kernel32
        self.load_library = None
        self.arg_address = None

    def processor(self):
        """Attach to the target process."""
        try:
            self.pm = pymem.Pymem(self.process_name)
            print(f"[+] Attached to process: {self.process_name}")
        except Exception as e:
            print(f"[!] Failed to attach to process: {e}")

    def allocate_memory(self):
        """Allocate memory in the target process and write the DLL path."""
        try:
            self.arg_address = pymem.process.allocate_memory(self.pm.process_handle, len(self.dll_path) + 1)
            pymem.memory.write_string(self.pm.process_handle, self.arg_address, self.dll_path)
            print(f"[+] Allocated memory at {hex(self.arg_address)} for DLL path.")
        except Exception as e:
            print(f"[!] Memory allocation failed: {e}")

    def get_load_library_address(self):
        """Get the address of LoadLibraryA from kernel32.dll."""
        try:
            handle = self.kernel32.GetModuleHandleW("kernel32.dll")
            self.load_library = self.kernel32.GetProcAddress(handle, b"LoadLibraryA")
            print(f"[+] LoadLibraryA address: {hex(self.load_library)}")
        except Exception as e:
            print(f"[!] Failed to get LoadLibraryA address: {e}")

    def inject_dll(self):
        """Create a remote thread in the target process to load the DLL."""
        try:
            thread_id = ctypes.c_ulong(0)
            if not self.kernel32.CreateRemoteThread(
                self.pm.process_handle,
                None,
                0,
                self.load_library,
                self.arg_address,
                0,
                ctypes.byref(thread_id)
            ):
                raise ctypes.WinError()
            print(f"[+] DLL injected successfully with thread ID: {thread_id.value}")
        except Exception as e:
            print(f"[!] DLL injection failed: {e}")

    def inject(self):
        """Run the full injection process."""
        self.processor()
        self.allocate_memory()
        self.get_load_library_address()
        self.inject_dll()


"""

PathAPI is a wrapper / api

PathAPI is used for injecting dlls into files example: game.exe

"""