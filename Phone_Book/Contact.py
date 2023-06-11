import re
import csv


# Import contacts from a CSV file
def import_contacts_from_csv(filename):
    """
        Imports contacts from a CSV file with the provided filename.
        Returns a list of Contact objects created from the CSV data.
        """
    contacts = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['Name']
            surname = row['Surname']
            number = row['Number']
            email = row['Email']

            try:
                contact = create_contact(name, surname, number, email)
                print(f"Imported contact: {name} {surname}")
                contacts.append(contact)
            except ValueError as e:
                print(f"Failed to insert contact: {name} {surname}. Reason: {str(e)}")

    return contacts


# Export contacts to a CSV file
def export_contacts_to_csv(filename, contacts):
    """
        Exports the provided list of Contact objects to a CSV file with the provided filename.
        The CSV file is structured with columns for Name, Surname, Number, and Email.
        """
    fieldnames = ['Name', 'Surname', 'Number', 'Email']
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for contact in contacts:
            writer.writerow({
                'Name': contact.name,
                'Surname': contact.surname,
                'Number': contact.number,
                'Email': contact.email
            })


# Create a new contact
def create_contact(name, surname, number, email):
    """
        Creates a new Contact object with the provided name, surname, number, and email.
        Raises a ValueError if a contact with the same number or email already exists.
        Returns the created Contact object.
        """
    if Contact.number_exists(number):
        raise ValueError(f"\n{number}\nnumber already added ")
    if Contact.email_exists(email):
        raise ValueError(f"{email}\nmail already added")
    contact = Contact(name, surname, number, email)
    Contact.static_contacts.add(contact)
    return contact


# Delete a contact
def delete_contact(contact):
    """
        Deletes the provided Contact object from the list of contacts.
        """
    Contact.static_contacts.remove(contact)


def search_contact_by_object(contact_object):
    """
    Searches for a contact by the provided contact object in the given set of contacts.
    Returns the matching contact object if found, None otherwise.
    """
    for contact in Contact.static_contacts:
        if contact == contact_object:
            return contact
    return None


# Search for a contact by full name
def search_contact(full_name):
    """
        Searches for a contact with the provided full name in the list of contacts.
        Returns the matching Contact object if found, None otherwise.
        """
    name, surname = full_name.split()
    for contact in Contact.static_contacts:
        if name in contact.name and surname in contact.surname:
            return contact


def search_contacts_by_keyword(keyword):
    """
        Searches for contacts that match the provided keyword in either name or surname.
        Returns a list of matching Contact objects.
        """
    matches = []
    keyword = keyword.lower()
    for contact in Contact.static_contacts:
        if keyword in contact.name.lower() or keyword in contact.surname.lower():
            matches.append(contact)
    return matches


# Class representing a contact
class Contact:
    MAX_NAME_LENGTH, MAX_SURNAME_LENGTH = (50, 50)
    MAX_NUMBER_LENGTH = 15
    MAX_EMAIL_LENGTH = 63

    # static set for contacts to insure uniqueness
    static_contacts = set()

    def __init__(self, name, surname, number, email):
        # Handle exceptions for name input
        if not name:
            raise ValueError("Name cannot be empty")
        if len(name) > Contact.MAX_NAME_LENGTH:
            raise ValueError(f"Name cannot exceed {Contact.MAX_NAME_LENGTH} characters")
        if not all(char.isalpha() or char.isspace() for char in name):
            raise ValueError("Name can only contain alphabetic characters and spaces")

        # Handle exceptions for surname input
        if not surname:
            raise ValueError("Surname cannot be empty")
        if len(surname) > Contact.MAX_SURNAME_LENGTH:
            raise ValueError(f"Surname cannot exceed {Contact.MAX_NAME_LENGTH} characters")
        if not all(char.isalpha() or char.isspace() for char in surname):
            raise ValueError("Surname can only contain alphabetic characters and spaces")

        # Handle exceptions for number input
        if not number:
            raise ValueError("Number cannot be empty")
        if len(number) > Contact.MAX_NAME_LENGTH:
            raise ValueError(f"Number cannot exceed {Contact.MAX_NUMBER_LENGTH} integers")
        if not number.isdigit():
            raise ValueError("Number can only contain digits")

        # Handle exceptions for email input
        # A person can have no email
        if len(email) > Contact.MAX_EMAIL_LENGTH:
            raise ValueError(f"Email cannot exceed {Contact.MAX_EMAIL_LENGTH} characters")
        if email and not re.match(r'^[\w.-]+@[a-zA-Z]+\.[a-zA-Z]{2,}$', email):
            raise ValueError("Invalid email format")

        self._name = name
        self._surname = surname
        self._number = number
        self._email = email

    # Getter for the name property
    @property
    def name(self):
        return self._name

    # edit name
    @name.setter
    def name(self, name):
        if not name:
            raise ValueError("Name cannot be empty")
        if len(name) > Contact.MAX_NAME_LENGTH:
            raise ValueError(f"Name cannot exceed {Contact.MAX_NAME_LENGTH} characters")
        if not all(char.isalpha() or char.isspace() for char in name):
            raise ValueError("Name can only contain alphabetic characters and spaces")
        self._name = name

    # Getter for the surname property
    @property
    def surname(self):
        return self._surname

    # edit surname
    @surname.setter
    def surname(self, surname):
        if not surname:
            raise ValueError("Surname cannot be empty")
        if len(surname) > Contact.MAX_SURNAME_LENGTH:
            raise ValueError(f"Surname cannot exceed {Contact.MAX_NAME_LENGTH} characters")
        if not all(char.isalpha() or char.isspace() for char in surname):
            raise ValueError("Surname can only contain alphabetic characters and spaces")
        self._surname = surname

    # Getter for the number property
    @property
    def number(self):
        return self._number

    # edit number
    @number.setter
    def number(self, number):
        if not number:
            raise ValueError("Number cannot be empty")
        if len(number) > Contact.MAX_NAME_LENGTH:
            raise ValueError(f"Number cannot exceed {Contact.MAX_NUMBER_LENGTH} integers")
        if not number.isdigit():
            raise ValueError("Name can only contain alphabetic characters")
        self._number = number

    # Getter for the number property
    @property
    def email(self):
        return self._email

    # edit email
    @email.setter
    def email(self, email):
        if len(email) > Contact.MAX_EMAIL_LENGTH:
            raise ValueError(f"Email cannot exceed {Contact.MAX_EMAIL_LENGTH} characters")
        if email and not re.match(r'^[\w.-]+@[a-zA-Z]+\.[a-zA-Z]{2,}$', email):
            raise ValueError("Invalid email format")
        self._email = email

    # Check if an email already exists in the contacts
    @classmethod
    def email_exists(cls, email):
        """
                Checks if a contact with the provided email already exists in the list of contacts.
                Returns True if a match is found, False otherwise.
                """
        for contact in cls.static_contacts:
            if contact.email == email:
                return True
        return False

    # Check if a number already exists in the contacts
    @classmethod
    def number_exists(cls, number):
        """
                Checks if a contact with the provided number already exists in the list of contacts.
                Returns True if a match is found, False otherwise.
                """
        for contact in cls.static_contacts:
            if contact.number == number:
                return True
        return False

    def __str__(self):
        return f"{self._name} {self._surname}"
