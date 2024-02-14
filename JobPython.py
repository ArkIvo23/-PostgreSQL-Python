import sqlite3

class Client:
    def __init__(self, name, surname, email, phones=None):
        self.name = name
        self.surname = surname
        self.email = email
        self.phones = phones or []

    def add_phone(self, phone):
        self.phones.append(phone)

    def remove_phone(self, phone):
        self.phones.remove(phone)

    def update(self, name, surname, email, phones=None):
        self.name = name
        self.surname = surname
        self.email = email
        self.phones = phones or []

    def __repr__(self):
        return f"Client('{self.name}', '{self.surname}', '{self.email}', {self.phones})"

def create_table():
    conn = sqlite3.connect("clients.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS clients (id INTEGER PRIMARY KEY, name TEXT, surname TEXT, email TEXT, phones TEXT)")
    conn.commit()
    conn.close()

def add_client(name, surname, email, phones=None):
    conn = sqlite3.connect("clients.db")
    c = conn.cursor()
    c.execute("INSERT INTO clients (name, surname, email, phones) VALUES (?, ?, ?, ?)", (name, surname, email, phones))
    conn.commit()
    conn.close()

def get_client_by_id(id):
    conn = sqlite3.connect("clients.db")
    c = conn.cursor()
    c.execute("SELECT * FROM clients WHERE id = ?", (id,))
    result = c.fetchone()
    conn.close()
    return result

def get_clients_by_field(field, value):
    conn = sqlite3.connect("clients.db")
    c = conn.cursor()
    c.execute("SELECT * FROM clients WHERE ? = ?", (field, value))
    result = c.fetchall()
    conn.close()
    return result

def update_client(id, name=None, surname=None, email=None, phones=None):
    conn = sqlite3.connect("clients.db")
    c = conn.cursor()
    c.execute("UPDATE clients SET name = ?, surname = ?, email = ?, phones = ? WHERE id = ?", (name, surname, email, phones, id))
    conn.commit()
    conn.close()

def remove_client(id):
    conn = sqlite3.connect("clients.db")
    c = conn.cursor()
    c.execute("DELETE FROM clients WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def remove_phone(id, phone):
    conn = sqlite3.connect("clients.db")
    c = conn.cursor()
    c.execute("UPDATE clients SET phones = phones - ? WHERE id = ?", (phone, id))
    conn.commit()
    conn.close()
    
def search_client(name=None, surname=None, email=None, phones=None):
    conn = sqlite3.connect("clients.db")
    c = conn.cursor()
    query = "SELECT * FROM clients"
    if name:
        query += " WHERE name = ?"
        assert isinstance(surname, object)
    if surname:
        query += " AND surname = ?"
    if email:
        query += " AND email = ?"
    if phones:
        query += " AND phones = ?"
    c.execute(query, (name, surname, email, phones))
    result = c.fetchall()
    conn.close()
    return result


if __name__ == "__main__":
    create_table()

    client1 = Client("John", "Doe", "johndoe@example.com", ["1234567890", "9876543210"])
    client2 = Client("Jane", "Smith", "janesmith@example.com", ["0123456789", "1111111111"])

    #add_client(client1)
    #add_client(client2)

    print(get_client_by_id(1))
    print(get_clients_by_field("email", "janesmith@example.com"))

    client1.update("Johan", "Doe", "johan@example.com")
    client2.update("Jane", "Smith", "janesmith@example.com")

    print(get_client_by_id(1))
    print(get_clients_by_field("email", "johan@example.com"))

    remove_client(2)
    remove_phone(1, "9876543210")

    print(get_client_by_id(1))
    print(get_clients_by_field("email", "johan@example.com"))
