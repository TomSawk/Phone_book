import os
import re

import customtkinter
from Contact import Contact, create_contact, search_contact, export_contacts_to_csv, import_contacts_from_csv, \
    search_contacts_by_keyword, search_contact_by_object, delete_contact
from DatabaseManager import DatabaseManager



# Create an instance of the DatabaseManager
db_manager = DatabaseManager()
# Create the contacts table
db_manager.create_table()

import_contacts_from_csv("file")

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class EditContactWindow(customtkinter.CTkToplevel):
    """
        A window for editing a contact.

        Attributes:
            contact: The contact object being edited.

        Methods:
            __init__: Initializes the EditContactWindow instance.
            edit_contact: Updates the contact with the entered information.
        """
    contact = None

    def __init__(self, *args, **kwargs):
        """
                Initializes the EditContactWindow instance.

                Args:
                    *args: Variable length argument list.
                    **kwargs: Arbitrary keyword arguments.
                """
        super().__init__(*args, **kwargs)
        self.geometry("250x600")

        self.label = customtkinter.CTkLabel(self, text="Edit Contact")
        self.label.pack(padx=20, pady=0)
        # Name filed and name label for errors display
        self.name_entry = customtkinter.CTkEntry(self, placeholder_text="Name: ")
        self.name_entry.pack(padx=20, pady=(20, 2))
        self.name_label = customtkinter.CTkLabel(self, text=f"{self.contact.name}")
        self.name_label.pack(padx=20, pady=0)
        # Surname filed and surname label for errors display
        self.surname_entry = customtkinter.CTkEntry(self, placeholder_text="Surname: ")
        self.surname_entry.pack(padx=20, pady=(13, 2))
        self.surname_label = customtkinter.CTkLabel(self, text=f"{self.contact.surname}")
        self.surname_label.pack(padx=20, pady=0)
        # Number filed and number label for errors display
        self.number_entry = customtkinter.CTkEntry(self, placeholder_text="Number: ")
        self.number_entry.pack(padx=20, pady=(13, 2))
        self.number_label = customtkinter.CTkLabel(self, text=f"{self.contact.number}")
        self.number_label.pack(padx=20, pady=0)
        #  Email filed and email label for errors display
        self.email_entry = customtkinter.CTkEntry(self, placeholder_text="Email: ")
        self.email_entry.pack(padx=20, pady=(13, 2))
        self.email_label = customtkinter.CTkLabel(self, text=f"{self.contact.email}")
        self.email_label.pack(padx=20, pady=0)
        # Error label to display errors to the user
        self.error_label = customtkinter.CTkLabel(self, text="")
        self.error_label.pack(padx=20, pady=20)
        self.error_label2 = customtkinter.CTkLabel(self, text="")
        self.error_label2.pack(padx=20, pady=20)
        # Add new to pc button
        self.add_new_to_pc = customtkinter.CTkButton(self, text="Edit contact",
                                                     command=self.edit_contact)
        self.add_new_to_pc.pack(padx=20, pady=20)
        # Add new to cloud button

    def edit_contact(self):
        """
               Updates the contact with the entered information.
               """
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        number = self.number_entry.get()
        email = self.email_entry.get()

        if not AddNewContactWindow.check_contact_input(self):
            self.error_label.configure(text="Wrong input", text_color="red")

        elif AddNewContactWindow.check_contact_input(self):
            found_contact = search_contact_by_object(self.contact)
            if found_contact is not None:
                found_contact.name = name
                found_contact.surname = surname
                found_contact.number = number
                found_contact.email = email
                self.error_label.configure(text="contact edited\non your PC", text_color="green")
            else:
                print("Contact not found in my pc.")

        try:
            db_manager.update_contact(self.contact.email, self.contact.number, name, surname, number, email)
            self.error_label2.configure(text="contact edited\non your Cloud", text_color="green")
        except Exception as e:
            exception_text = str(e)
            self.error_label.configure(text=f"{exception_text}", text_color="red")


class AddNewContactWindow(customtkinter.CTkToplevel):
    """
        A window for adding a new contact.

        Methods:
            check_contact_input: Validates the contact information entered by the user.
            __init__: Initializes the AddNewContactWindow instance.
            add_new_to_pc: Adds a new contact to the local PC.
            add_new_to_cloud: Adds a new contact to the cloud.
        """

    def check_contact_input(self):
        """
                Validates the contact information entered by the user.

                Returns:
                    bool: True if the contact information is valid, False otherwise.
                """
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        number = self.number_entry.get()
        email = self.email_entry.get()
        validName = False
        validSurname = False
        validNum = False
        validEmail = True
        # handle possible name input errors and display them to the user
        if not name:
            self.name_label.configure(text="Name cannot be empty", text_color="red")
        elif len(name) > Contact.MAX_NAME_LENGTH:
            self.name_label.configure(text=f"Name cannot exceed {Contact.MAX_NAME_LENGTH} characters", text_color="red")
        elif not all(char.isalpha() or char.isspace() for char in name):
            self.name_label.configure(text="Can only contain chars", text_color="red")
        elif name != "":
            self.name_label.configure(text="Valid name", text_color="green")
            validName = True

        # handle possible surname input errors and display them to the user
        if not surname:
            self.surname_label.configure(text="surname cannot be empty", text_color="red")
        elif len(surname) > Contact.MAX_SURNAME_LENGTH:
            self.surname_label.configure(text=f"surname cannot exceed {Contact.MAX_SURNAME_LENGTH} characters",
                                         text_color="red")
        elif not all(char.isalpha() or char.isspace() for char in surname):
            self.surname_label.configure(text="Can only contain chars", text_color="red")
        elif surname != "":
            self.surname_label.configure(text="Valid surname", text_color="green")
            validSurname = True

        # handle possible number input errors and display them to the user
        if not number:
            self.number_label.configure(text="Number cannot be empty", text_color="red")
        elif len(number) > Contact.MAX_NAME_LENGTH:
            self.number_label.configure(text=f"Number cannot exceed {Contact.MAX_NUMBER_LENGTH} integers",
                                        text_color="red")
        elif not number.isdigit():
            self.number_label.configure(text="Only digits", text_color="red")
        elif number != "":
            self.number_label.configure(text="Valid number", text_color="green")
            validNum = True
        # handle possible email input errors and display them to the user
        if len(email) > Contact.MAX_EMAIL_LENGTH:
            self.email_label.configure(text=f"Cannot exceed {Contact.MAX_EMAIL_LENGTH} chars", text_color="red")
            validEmail = False
        elif email and not re.match(r'^[\w.-]+@[a-zA-Z]+\.[a-zA-Z]{2,}$', email):
            self.email_label.configure(text="Invalid email format", text_color="red")
            validEmail = False
        elif email != "":
            self.email_label.configure(text="Valid email", text_color="green")
            validEmail = True

        print(f"name: {name} {surname}\nphone: {number}\nemail: {email}")
        return validName and validSurname and validNum and validEmail

    def __init__(self, *args, **kwargs):
        """
               Initializes the AddNewContactWindow instance.

               Args:
                   *args: Variable length argument list.
                   **kwargs: Arbitrary keyword arguments.
               """
        super().__init__(*args, **kwargs)
        self.geometry("250x600")

        self.label = customtkinter.CTkLabel(self, text="Add New Contact")
        self.label.pack(padx=20, pady=0)
        # Name filed and name label for errors display
        self.name_entry = customtkinter.CTkEntry(self, placeholder_text="Name: ")
        self.name_entry.pack(padx=20, pady=(20, 2))
        self.name_label = customtkinter.CTkLabel(self, text="")
        self.name_label.pack(padx=20, pady=0)
        # Surname filed and surname label for errors display
        self.surname_entry = customtkinter.CTkEntry(self, placeholder_text="Surname: ")
        self.surname_entry.pack(padx=20, pady=(13, 2))
        self.surname_label = customtkinter.CTkLabel(self, text="")
        self.surname_label.pack(padx=20, pady=0)
        # Number filed and number label for errors display
        self.number_entry = customtkinter.CTkEntry(self, placeholder_text="Number: ")
        self.number_entry.pack(padx=20, pady=(13, 2))
        self.number_label = customtkinter.CTkLabel(self, text="")
        self.number_label.pack(padx=20, pady=0)
        #  Email filed and email label for errors display
        self.email_entry = customtkinter.CTkEntry(self, placeholder_text="Email: ")
        self.email_entry.pack(padx=20, pady=(13, 2))
        self.email_label = customtkinter.CTkLabel(self, text="")
        self.email_label.pack(padx=20, pady=0)
        # Error label to display errors to the user
        self.error_label = customtkinter.CTkLabel(self, text="")
        self.error_label.pack(padx=20, pady=20)
        # Add new to pc button
        self.add_new_to_pc = customtkinter.CTkButton(self, text="Add new to PC",
                                                     command=self.add_new_to_pc)
        self.add_new_to_pc.pack(padx=20, pady=20)
        # Add new to cloud button
        self.add_new_to_could = customtkinter.CTkButton(self, text="Add new to Cloud",
                                                        command=self.add_new_to_cloud)
        self.add_new_to_could.pack(padx=20, pady=20)

    def add_new_to_pc(self):
        """
                Adds a new contact to the local PC.
                """
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        number = self.number_entry.get()
        email = self.email_entry.get()
        if not self.check_contact_input():
            self.error_label.configure(text="Wrong input", text_color="red")
        elif self.check_contact_input():
            try:
                create_contact(name, surname, number, email)
                self.error_label.configure(text="new contact added", text_color="green")
            except Exception as e:
                exception_text = str(e)
                self.error_label.configure(text=f"{exception_text}", text_color="red")

    def add_new_to_cloud(self):
        """
                Adds a new contact to the cloud.
                """
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        number = self.number_entry.get()
        email = self.email_entry.get()
        if not self.check_contact_input():
            self.error_label.configure(text="Wrong input", text_color="red")
        elif self.check_contact_input():
            try:
                db_manager.insert_contact(name, surname, number, email)
                self.error_label.configure(text="new contact added", text_color="green")
            except Exception as e:
                exception_text = str(e)
                self.error_label.configure(text=f"{exception_text}", text_color="red")


class ContactTextBox(customtkinter.CTk):
    """
        Custom tkinter textbox for contact details.
        """

    def __init__(self):
        super().__init__()
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        self.textbox = customtkinter.CTkTextbox(master=self, width=400, corner_radius=0)
        self.textbox.grid(row=0, column=0, sticky="nsew")
        self.textbox.insert("0.0", "Some example text!\n" * 50)


class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):
    """
        Custom tkinter frame for scrollable labels and buttons.
        """

    def __init__(self, master, command=None, **kwargs):
        """
                Initializes the ScrollableLabelButtonFrame class.

                Args:
                    master: The parent widget.
                    command: Optional command to be associated with the buttons.
                    kwargs: Additional keyword arguments for customization.
                Returns:
                    None
                """
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.command = command
        self.radiobutton_variable = customtkinter.StringVar()
        self.label_list = []
        self.button_list = []

    def add_item(self, item, image=None):
        """
                Add an item with a label and button to the frame.

                Args:
                    item: The item to be displayed.
                    image: Optional image to be displayed alongside the label.
                Returns:
                    None
                """
        contact = item
        label = customtkinter.CTkLabel(self, text=item, image=image, compound="left", padx=5, anchor="w")
        button = customtkinter.CTkButton(self, text="Details", width=100, height=24)
        if self.command is not None:
            button.configure(command=lambda: self.command(contact))
        label.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w")
        button.grid(row=len(self.button_list), column=1, pady=(0, 10), padx=5)
        self.label_list.append(label)
        self.button_list.append(button)

    def remove_item(self, item):
        """
               Remove an item from the frame.

               Args:
                   item: The item to be removed.
               Returns:
                   None
               """
        for label, button in zip(self.label_list, self.button_list):
            if item == label.cget("text"):
                label.destroy()
                button.destroy()
                self.label_list.remove(label)
                self.button_list.remove(button)

                return

    def clear_all(self):
        """
                Remove all items from the frame.

                Args:
                    None
                Returns:
                    None
                """
        while self.label_list and self.button_list != 0:
            for label, button in zip(self.label_list, self.button_list):
                label.destroy()
                button.destroy()
                self.label_list.remove(label)
                self.button_list.remove(button)


class GUI(customtkinter.CTk):
    """
        Graphical user interface for the PhoneBook application.
        """

    def __init__(self):
        super().__init__()

        """
        MAIN WINDOW
        """
        self.title("PhoneBook")
        self.geometry(f"{880}x{450}")
        self.resizable(False, False)
        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        # create sidebar frame with widgets
        """
        LEFT FRAME
        """
        self.left_frame = customtkinter.CTkFrame(self, width=220, corner_radius=0)
        self.left_frame.grid(row=0, column=0, padx=(0, 5), rowspan=5, sticky="nsew")
        self.left_frame.grid_rowconfigure(5, weight=1)
        self.left_frame_logo = customtkinter.CTkLabel(self.left_frame, text="Contacts",
                                                      font=customtkinter.CTkFont(size=20, weight="bold"))
        self.left_frame_logo.grid(row=0, column=0, padx=40, pady=(10, 20))

        # left side buttons
        # Button: All contacts on PC
        self.left_frame_button_all_on_pc = customtkinter.CTkButton(self.left_frame, text="All on PC",
                                                                   command=self.all_on_pc_button_event)
        self.left_frame_button_all_on_pc.grid(row=1, column=0, padx=20, pady=5)
        # Button: All contacts on Could
        self.left_frame_button_all_on_cloud = customtkinter.CTkButton(self.left_frame, text="All on Cloud",
                                                                      command=self.all_on_cloud_button_event)
        self.left_frame_button_all_on_cloud.grid(row=2, column=0, padx=20, pady=5)
        # Button: Back-UP
        self.left_frame_button_back_up = customtkinter.CTkButton(self.left_frame, text="Back-Up",
                                                                 command=self.back_up_button_event)
        self.left_frame_button_back_up.grid(row=3, column=0, padx=20, pady=5)
        # Button: Load from Cloud
        self.left_frame_button_load_from_cloud = customtkinter.CTkButton(self.left_frame, text="Load from Cloud",
                                                                         command=self.download_from_cloud_button_event)
        self.left_frame_button_load_from_cloud.grid(row=4, column=0, padx=20, pady=5)

        # status label use for statuses
        # backed up - success or failed
        # loaded - success or failed
        self.status_label = customtkinter.CTkLabel(self.left_frame, text="", anchor="w")
        self.status_label.grid(row=5, column=0, padx=20, pady=(0, 5))

        # csv
        self.csv_label = customtkinter.CTkLabel(self.left_frame, text="CSV:", anchor="w")
        self.csv_label.grid(row=6, column=0, padx=20, pady=(0, 0))
        # cvs button
        self.csv_button = customtkinter.CTkButton(self.left_frame, text="Import",
                                                  command=self.import_button_event)
        self.csv_button.grid(row=7, column=0, padx=20, pady=5)

        self.csv_button = customtkinter.CTkButton(self.left_frame, text="Export",
                                                  command=self.export_button_event)
        self.csv_button.grid(row=8, column=0, padx=20, pady=5)

        self.appearance_mode = customtkinter.CTkLabel(self.left_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode.grid(row=9, column=0, padx=20, pady=(20, 0))
        self.appearance_mode_option_menu = customtkinter.CTkOptionMenu(self.left_frame,
                                                                       values=["System", "Dark", "Light"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_option_menu.grid(row=10, column=0, padx=20, pady=(10, 20))

        """
        MIDDLE FRAME
        """
        self.middle_frame = customtkinter.CTkFrame(self, width=300, corner_radius=0)
        self.middle_frame.grid(row=0, column=1, rowspan=5, padx=(5, 5), pady=0, sticky="nsew")
        self.middle_frame.grid_rowconfigure(5, weight=1)

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self.middle_frame, placeholder_text="Contact")
        self.entry.grid(row=1, column=1, columnspan=1, padx=(20, 20), pady=(20, 5), sticky="nsew")
        self.search_button = customtkinter.CTkButton(master=self.middle_frame, text="Search", fg_color="transparent",
                                                     border_width=2, text_color=("gray10", "#DCE4EE"),
                                                     command=self.search_button_event)
        self.search_button.grid(row=2, column=1, padx=(20, 20), pady=(5, 5), sticky="nsew")
        self.scrollable_frame = ScrollableLabelButtonFrame(self.middle_frame, width=300, label_text="Names",
                                                           command=self.label_button_frame_event)
        self.scrollable_frame.grid(row=5, column=1, padx=(20, 20), pady=(5, 10), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        """
        RIGHT FRAME
        """
        self.right_frame = customtkinter.CTkFrame(self, width=430, corner_radius=0)
        self.right_frame.grid(row=0, column=3, columnspan=1, rowspan=5, padx=(5, 5), pady=0, sticky="nsew")
        self.right_frame.grid_rowconfigure(2, weight=1)
        self.right_frame.grid_columnconfigure(2, weight=1)
        self.right_frame_label = customtkinter.CTkLabel(self.right_frame, text="Selected contact details:",
                                                        font=customtkinter.CTkFont(size=18, weight="bold"))
        self.right_frame_label.grid(row=0, column=0, padx=(40, 40), pady=(10, 20))

        self.right_frame_details = customtkinter.CTkLabel(self.right_frame, text="No contact",
                                                          font=customtkinter.CTkFont(size=18, weight="bold"))
        self.right_frame_details.grid(row=1, column=0, padx=(0, 0), pady=(0, 0))

        self.right_frame_add_new_contact_button = customtkinter.CTkButton(self.right_frame, text="Add new contact",
                                                                          command=self.label_button_add_new_contact_event)
        self.right_frame_add_new_contact_button.grid(row=4, column=0, padx=(0, 0), pady=(10, 5))

        self.right_frame_add_edit = customtkinter.CTkButton(self.right_frame, text="Edit contact",
                                                            command=self.label_button_edit_event)
        self.right_frame_add_edit.grid(row=5, column=0, padx=(0, 0), pady=(5, 5))

        self.right_frame_add_new_contact_button = customtkinter.CTkButton(self.right_frame, text="Delete contact",
                                                                          command=self.delete_contact)
        self.right_frame_add_new_contact_button.grid(row=6, column=0, padx=(0, 0), pady=(5, 15))

        self.allSelected = "none"

        self.source_csv = ""

        self.add_new_contact_window = None
        self.edit_contact_window = None

    def change_appearance_mode_event(self, new_appearance_mode: str):
        """
                Handles the event of changing the appearance mode.

                Args:
                    new_appearance_mode (str): The new appearance mode to be set.
                Returns:
                    None
                """
        customtkinter.set_appearance_mode(new_appearance_mode)

    def all_on_pc_button_event(self):
        """
                Handles the event when the "All on PC" button is clicked.

                Args:
                    None
                Returns:
                    None
                """
        self.scrollable_frame.clear_all()
        self.allSelected = "pc"
        for contact in Contact.static_contacts:
            self.scrollable_frame.add_item(contact)

    def all_on_cloud_button_event(self):
        """
               Handles the event when the "All on Cloud" button is clicked.

               Args:
                   None
               Returns:
                   None
               """
        self.scrollable_frame.clear_all()
        self.allSelected = "cloud"
        cloud_contacts = db_manager.download_contacts()
        for contact in cloud_contacts:
            self.scrollable_frame.add_item(contact)

    def back_up_button_event(self):
        """
               Handles the event when the "Back Up" button is clicked.

               Args:
                   None
               Returns:
                   None
               """

        try:
            db_manager.backup(Contact.static_contacts)
            self.status_label.configure(text="Backed-Up", text_color="green")
        except Exception as e:
            self.status_label.configure(text="Failed", text_color="red")

    def download_from_cloud_button_event(self):
        """
               Handles the event when the "Download from Cloud" button is clicked.

               Args:
                   None
               Returns:
                   None
               """
        try:
            loaded_contacts = DatabaseManager.download_contacts(db_manager)
            Contact.static_contacts.update(loaded_contacts)
            self.status_label.configure(text="Loaded", text_color="green")
        except Exception as e:
            self.status_label.configure(text="Failed", text_color="red")

    def label_button_frame_event(self, item):
        """
                Handles the event when a label button in the frame is clicked.

                Args:
                    item: The item associated with the clicked label button.
                Returns:
                    None
                """
        if self.allSelected == "none":
            return
        if self.allSelected == "pc":
            contact = item
            EditContactWindow.contact = item
            print(f"contact: {contact.name} {contact.surname} {contact.number} {contact.email}")
            self.right_frame_details.configure(
                text=f"\nname: \n{contact.name} \n\nsurname: \n{contact.surname} \n\nnumber: \n{contact.number} \n"
                     f"\nemail: \n{contact.email}")
        if self.allSelected == "cloud":
            contact = item
            EditContactWindow.contact = item
            print(f"contact: {contact.name} {contact.surname} {contact.number} {contact.email}")
            self.right_frame_details.configure(
                text=f"\nname: \n{contact.name} \n\nsurname: \n{contact.surname} \n\nnumber: \n{contact.number} \n"
                     f"\nemail: \n{contact.email}")

    def label_button_edit_event(self):
        """
                Handles the event when the "Edit" label button is clicked.

                Args:
                    item: The item associated with the clicked label button.
                Returns:
                    None
                """
        if self.edit_contact_window is None or not self.edit_contact_window.winfo_exists():
            self.edit_contact_window = EditContactWindow(self)  # create window if its None or destroyed
            self.edit_contact_window.title("Edit Contact")
        else:
            self.edit_contact_window.focus()  # if window exists focus it
        print("label_button_edit_event")

    def label_button_add_new_contact_event(self):
        """
               Handles the event when the "Add New Contact" label button is clicked.

               Args:
                   None
               Returns:
                   None
               """
        if self.add_new_contact_window is None or not self.add_new_contact_window.winfo_exists():
            self.add_new_contact_window = AddNewContactWindow(self)  # create window if its None or destroyed
            self.add_new_contact_window.title("New Contact")
        else:
            self.add_new_contact_window.focus()  # if window exists focus it
        print(f"label_button_add_new_contact_event")

    def search_button_event(self):
        """
                Handles the event when the "Search" button is clicked.

                Args:
                    None
                Returns:
                    None
                """
        search_keyword = self.entry.get()
        if self.allSelected == "none":
            return
        if self.allSelected == "pc":
            contacts = search_contacts_by_keyword(search_keyword)
            self.scrollable_frame.clear_all()
            for contact in contacts:
                self.scrollable_frame.add_item(contact)
        if self.allSelected == "cloud":
            contacts = db_manager.search_contacts(search_keyword)
            self.scrollable_frame.clear_all()
            for contact in contacts:
                self.scrollable_frame.add_item(contact)

    def export_button_event(self):
        """
                Handles the event when the "Export" button is clicked.

                Args:
                    None
                Returns:
                    None
                """
        contacts_for_export = Contact.static_contacts
        try:
            export_contacts_to_csv("my_export", contacts_for_export)
            self.csv_label.configure(text="CVS: Exported", text_color="green")
        except Exception as e:
            self.csv_label.configure(text="Export failed", text_color="red")

    def import_button_event(self):
        """
                Handles the event when the "Import" button is clicked.

                Args:
                    None
                Returns:
                    None
                """

        dialog = customtkinter.CTkInputDialog(text="Type in file source:", title="Import CSV")
        self.source_csv = dialog.get_input()  # waits for input

        if not self.check_file_format(self.source_csv):
            self.csv_label.configure(text="wrong CVS src", text_color="red")
        if self.check_file_format(self.source_csv):
            try:
                import_contacts_from_csv(self.source_csv)
                self.csv_label.configure(text="CVS: Imported", text_color="green")
            except Exception as e:
                self.csv_label.configure(text="Import failed", text_color="red")

        print(f"import file: {self.source_csv}")

    def check_file_format(self, filename):
        """
        Checks if the file with the provided filename exists and determines its format (CSV or TXT). Returns a tuple
        (exists, format), where 'exists' is a boolean indicating if the file exists, and 'format' is a string
        indicating the file format ('csv', 'txt') if the file exists, or None if it doesn't exist.
        """
        if os.path.exists(filename):
            if filename.lower().endswith('.csv'):
                return True
            elif filename.lower().endswith('.txt'):
                return True
            else:
                return True
        else:
            return False

    def delete_contact(self):
        dialog = customtkinter.CTkInputDialog(text="Type \"CONFIRM DELETE\":", title="Delete confirmation")
        confirm_input = dialog.get_input()  # waits for input

        if confirm_input != "CONFIRM DELETE":
            self.status_label.configure(text="Failed to delete", text_color="red")
        if confirm_input == "CONFIRM DELETE":
            try:
                delete_contact(EditContactWindow.contact)
                self.status_label.configure(text="Contact was deleted\rfrom your PC", text_color="green")
            except Exception as e:
                self.status_label.configure(text="Failed to delete", text_color="red")


app = GUI()
app.mainloop()
