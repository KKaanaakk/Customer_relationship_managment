import re
import sqlite3
import hashlib

def create_user_table():
    connection = sqlite3.connect('crm.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        );
    ''')
    connection.commit()
    connection.close()

def register_user():
    username, password = input("Enter username: "), input("Enter password: ")

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    connection = sqlite3.connect('crm.db')
    cursor = connection.cursor()

    cursor.execute('''
        INSERT INTO users (username, password)
        VALUES (?, ?);
    ''', (username, hashed_password))

    connection.commit()
    connection.close()

    print("User registered successfully!")

def login():
    username, password = input("Enter username: "), input("Enter password: ")

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    connection = sqlite3.connect('crm.db')
    cursor = connection.cursor()

    cursor.execute('''
        SELECT * FROM users
        WHERE username = ? AND password = ?;
    ''', (username, hashed_password))

    user = cursor.fetchone()

    connection.close()

    if user:
        print("Login successful!")
    else:
        print("Invalid username or password.")

def create_contact_table():
    connection = sqlite3.connect('crm.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            email TEXT,
            phone TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    ''')
    connection.commit()
    connection.close()

def is_valid_phone(phone):
    pattern = re.compile(r'^[7-9][0-9]{9}$')
    return bool(re.match(pattern, phone))

def is_valid_email(email):
    pattern = re.compile(r'^\S+@\S+\.\S+$')
    return bool(re.match(pattern, email))

def add_contact():

    """
    Here we have used exception handling as adding data into data is a crucel part
    so we handle the complexity here so it wont affect any data and also fuctionality.
    """

    try:
        user_id, name = int(input("Enter user ID: ")), input("Enter contact name: ")

        email = input("Enter contact email: ")
        while not is_valid_email(email):
            print("Invalid email format. Please enter a valid email address.")
            email = input("Enter contact email: ")

        phone = input("Enter contact phone (format: xxx-xxx-xxxx): ")
        while not is_valid_phone(phone):
            print("Invalid phone number format. Please enter in the format xxx-xxx-xxxx.")
            phone = input("Enter contact phone (format: xxx-xxx-xxxx): ")

        connection = sqlite3.connect('crm.db')
        cursor = connection.cursor()

        cursor.execute('''
            INSERT INTO contacts (user_id, name, email, phone)
            VALUES (?, ?, ?, ?);
        ''', (user_id, name, email, phone))

        connection.commit()
        connection.close()

        print("Contact added successfully!")
    
    except Exception as e:
        print(f"It occured due to: {e}")

def view_contacts():
    user_id = int(input("Enter user ID: "))

    connection = sqlite3.connect('crm.db')
    cursor = connection.cursor()

    cursor.execute('''
        SELECT * FROM contacts
        WHERE user_id = ?;
    ''', (user_id,))

    contacts = cursor.fetchall()

    """
    Here we have used a List comp. concept while using dict(JSON)
    So it would be easier to figuring out data and also while fetching the data
    we were getting the tuple in  'contact' hence we have given the indexes to the 
    tuple to arrange the data in proper form.

    """
    contact_data = [{ 
        "User_ID": contact[1],
        "Name": contact[2],
        "Email": contact[3],
        "Phone No.": contact[4]        
    }
    for contact in contacts    
    ]
    print(contact_data)
    connection.close()

def update_contact():
    contact_id = int(input("Enter contact ID to update: "))
    name = input("Enter updated contact name: ")

    email = input("Enter updated contact email: ")
    while not is_valid_email(email):
        print("Invalid email format. Please enter a valid email address.")
        email = input("Enter updated contact email: ")

    phone = input("Enter updated contact phone (format: xxx-xxx-xxxx): ")
    while not is_valid_phone(phone):
        print("Invalid phone number format. Please enter in the format xxx-xxx-xxxx.")
        phone = input("Enter updated contact phone (format: xxx-xxx-xxxx): ")

    connection = sqlite3.connect('crm.db')
    cursor = connection.cursor()

    cursor.execute('''
        UPDATE contacts
        SET name = ?, email = ?, phone = ?
        WHERE id = ?;
    ''', (name, email, phone, contact_id))

    connection.commit()
    connection.close()

    print("Contact updated successfully!")

def delete_contact():
    contact_id = int(input("Enter contact ID to delete: "))

    connection = sqlite3.connect('crm.db')
    cursor = connection.cursor()

    cursor.execute('''
        DELETE FROM contacts
        WHERE id = ?;
    ''', (contact_id,))

    connection.commit()
    connection.close()

    print("Contact deleted successfully!")

while True:
    print("\nCRM System Menu:")
    print("1. Register User")
    print("2. Login")
    print("3. Add Contact")
    print("4. View Contacts")
    print("5. Update Contact")
    print("6. Delete Contact")
    print("7. Exit")

    choice = input("Enter your choice (1-7): ")

    if choice == '1':
        create_user_table()
        register_user()
    elif choice == '2':
        create_user_table()
        login()
    elif choice == '3':
        create_contact_table()
        add_contact()
    elif choice == '4':
        create_contact_table()
        view_contacts()
    elif choice == '5':
        create_contact_table()
        update_contact()
    elif choice == '6':
        create_contact_table()
        delete_contact()
    elif choice == '7':
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 7.")