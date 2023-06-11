import sqlite3

from Contact import Contact


class DatabaseManager:
    """
        Initializes the DatabaseManager object and establishes a connection to the SQLite database.
        If no database name is provided, 'contacts_database.db' is used as the default.
        """

    def __init__(self, db_name='contacts_database.db'):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    """
        Creates the 'contacts' table in the database if it does not already exist.
        The table has columns for id, name, surname, number, and email.
        """

    def create_table(self):
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY,
                name TEXT,
                surname TEXT,
                number TEXT,
                email TEXT
            )
        '''
        self.cursor.execute(create_table_query)

    def insert_contact(self, name, surname, number, email):
        """
           Inserts a new contact into the 'contacts' table with the provided name, surname, number, and email.
           Raises a ValueError if a contact with the same email or number already exists in the table.
           Returns the ID of the newly inserted contact.
           """
        self.cursor.execute("SELECT COUNT(*) FROM contacts WHERE email = ?", (email,))
        result = self.cursor.fetchone()
        if result[0] > 0:
            raise ValueError("Contact with the same \nemail already exists")

        # Check if contact with the same number exists
        self.cursor.execute("SELECT COUNT(*) FROM contacts WHERE number = ?", (number,))
        result = self.cursor.fetchone()
        if result[0] > 0:
            raise ValueError("Contact with the same \nnumber already exists")

        # Insert the new contact
        self.cursor.execute("INSERT INTO contacts (name, surname, number, email) VALUES (?, ?, ?, ?)",
                            (name, surname, number, email))
        self.connection.commit()
        contact_id = self.cursor.lastrowid

        return contact_id

    def download_contacts(self):
        """
            Fetches all contacts from the 'contacts' table and returns them as a list of Contact objects.
            Prints status messages for each contact that is successfully inserted, and prints error messages
            for contacts that fail to insert due to validation errors.
            """
        self.cursor.execute("SELECT name, surname, number, email FROM contacts")
        rows = self.cursor.fetchall()

        contacts2 = []
        for row in rows:
            name, surname, number, email = row
            try:
                contact = Contact(name, surname, number, email)
                print(f"Inserted contact: {name} {surname}")
                contacts2.append(contact)
            except ValueError as e:
                print(f"Failed to insert contact: {name} {surname}. Reason: {str(e)}")

        return contacts2

    def search_contact(self, full_name):
        """
            Searches for a contact with the provided full name in the 'contacts' table.
            Returns the matching Contact object if found, None otherwise.
        """
        name, surname = full_name.split()
        query = '''
            SELECT name, surname, number, email
            FROM contacts
            WHERE name = ? AND surname = ?
        '''
        self.cursor.execute(query, (name, surname))
        row = self.cursor.fetchone()

        if row:
            name, surname, number, email = row
            contact = Contact(name, surname, number, email)
            return contact

        return None

    def search_contacts(self, keyword):
        """
            Searches for contacts in the 'contacts' table based on the provided keyword.
            Returns a list of Contact objects that match the keyword in name, surname, number, or email.
            """
        query = '''
            SELECT name, surname, number, email
            FROM contacts
            WHERE name LIKE ? OR surname LIKE ? OR number LIKE ? OR email LIKE ?
        '''
        pattern = f"%{keyword}%"
        self.cursor.execute(query, (pattern, pattern, pattern, pattern))
        rows = self.cursor.fetchall()

        contacts = []
        for row in rows:
            name, surname, number, email = row
            contact = Contact(name, surname, number, email)
            contacts.append(contact)

        return contacts

    def update_contact(self, email, number, new_name, new_surname, new_number, new_email):
        """
        Updates the contact with the provided email and number in the 'contacts' table
        with the new name, surname, number, and email.
        Returns True if the contact was successfully updated, False otherwise.
        """
        # Check if the new email is already taken
        self.cursor.execute("SELECT COUNT(*) FROM contacts WHERE email = ? AND (number != ? OR email != ?)",
                            (new_email, number, email))
        result = self.cursor.fetchone()
        if result[0] > 0:
            raise ValueError("Contact with the same email already exists")

        # Check if the new number is already taken
        self.cursor.execute("SELECT COUNT(*) FROM contacts WHERE number = ? AND (email != ? OR number != ?)",
                            (new_number, email, number))
        result = self.cursor.fetchone()
        if result[0] > 0:
            raise ValueError("Contact with the same number already exists")

        # Update the contact
        query = '''
            UPDATE contacts
            SET name = ?, surname = ?, number = ?, email = ?
            WHERE email = ? AND number = ?
        '''
        params = (new_name, new_surname, new_number, new_email, email, number)
        self.cursor.execute(query, params)
        self.connection.commit()

        if self.cursor.rowcount > 0:
            return True
        else:
            return False

    def backup(self, contacts):
        """
           Creates a backup of the provided list of Contact objects by inserting them into the 'contacts' table.
           Prints status messages for each contact that is successfully backed up, and prints error messages
           for contacts that fail to back up due to validation errors.
           Returns a list of Contact objects that were successfully backed up.
           """
        backup_contacts = []
        for contact in contacts:
            try:
                self.insert_contact(contact.name, contact.surname, contact.number, contact.email)
                backup_contacts.append(contact)
            except ValueError as e:
                print(f"Failed to backup contact: {contact}. Reason: {str(e)}")

        return backup_contacts

    def close_connection(self):
        """
            Closes the connection to the SQLite database.
            """
        self.connection.close()
