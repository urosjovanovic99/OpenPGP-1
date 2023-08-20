import json
import tkinter as tk
from tkinter import ttk
from tkinter.constants import TOP, RIGHT

from gui.dialogs.general.FilePicker import FilePicker
from gui.tables.key_rings.PrivateKeyRingTable import PrivateKeyRingTable
from gui.tables.user.UserDetailsTable import UserDetailsTable
from key_rings.base_key_ring.private_key_ring import PrivateKeyRing


class PrivateKeyRingDialog:
    def __init__(self, root, parent, email):
        self.root = root
        self.parent = parent
        self.email = email
        self.key_rings = (
            PrivateKeyRing.private_key_ring_by_user)[email] if email in PrivateKeyRing.private_key_ring_by_user else []
        self.dialog_private_key_table = tk.Toplevel(self.root)
        self.dialog_private_key_table.title("Private key ring for " + self.email)
        self.dialog_frame = ttk.Frame(self.dialog_private_key_table)
        self.dialog_frame.pack(fill="both", expand=True)

        self.create_dialog()

    def clear_window(self):
        for widget in self.dialog_frame.winfo_children():
            widget.destroy()

    def create_dialog(self):
        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 12))
        style.configure("TButton", font=("Helvetica", 12))

        user_information_fame = ttk.Frame(self.dialog_frame)
        user_information_fame.pack(side=TOP)
        UserDetailsTable(self.root, user_information_fame, self, self.email)

        receive_button = ttk.Button(user_information_fame, text="Receive message",
                                    command=lambda: self.receive_message())
        receive_button.pack(side=RIGHT)

        PrivateKeyRingTable(self.root, self.dialog_frame, self, self.email, self.key_rings)

        confirm_button = ttk.Button(user_information_fame, text="Close",
                                    command=lambda: self.dialog_private_key_table.destroy())
        confirm_button.pack(side=RIGHT)
        pass

    def render(self):
        self.clear_window()
        self.create_dialog()
        pass

    def receive_message(self):
        package = {}
        file_picker = FilePicker()
        received_file_path = file_picker.filename

        with open(received_file_path, mode='r') as received_file:
            unpacked_package = json.load(received_file)

        encrypted_session_key = unpacked_package["session_key_component"]["session_key"].encode()
        key_id_of_recipient_public_key = unpacked_package["session_key_component"]["key_id_of_recipient_public_key"]
        algorithm = unpacked_package["session_key_component"]["algorithm"]

        private_key_ring = PrivateKeyRing.find_private_key_ring_by_id(key_id_of_recipient_public_key, self.email)
        session_key = private_key_ring.decrypt_session_key(encrypted_session_key)
        print(session_key)
        pass
